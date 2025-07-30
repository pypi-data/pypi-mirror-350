"""
Dataset implementations for vascular simulation data.

This module provides PyTorch Dataset implementations for loading and processing
vascular simulation data, with support for streaming from remote sources.
"""

import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import torch
from torch.utils.data import Dataset
from torch_geometric.data import Data

from ..io.streaming import HuggingFaceStreamer, LocalStreamer, NASStreamer
from ..processing.domain import DomainManager, decompose_vtu_file, process_subdomains
from .conversion import vtu_to_pyg

logger = logging.getLogger(__name__)

_PREFETCH_REGISTRY = {}


class VascuDataset(Dataset):
    """
    Dataset for vascular simulation data.

    This class provides a PyTorch Dataset implementation for loading and
    processing vascular simulation data from VTU/VTP files.

    Attributes:
        source_url (str): URL or path to the data source.
        source_dir (Path): Directory to store raw data on NAS / local side.
        raw_dir (Path): Directory to store raw data.
        processed_dir (Path): Directory to store processed data.
        streaming_type (str): Type of streaming to use ("auto", "hf", "nas").
        use_pyg (bool): Whether to use PyG files instead of VTU when available.
        convert_if_missing (bool): Whether to convert VTU to PyG when PyG is missing.
        use_domain_decomposition (bool): Whether to use domain decomposition.
        num_partitions (int): Number of partitions for domain decomposition.
        domain_boundary_mode (str): Boundary handling mode for domain decomposition.
        domain_cache_dir (Path): Directory to store domain decomposition cache.
        super_resolution (bool): Whether to use super-resolution data.
        max_cache_size (int): Maximum cache size in bytes.
        include_attributes (List[str]): List of specific attributes to include.
        cache_dir (Path): Directory to store cached files.
        file_list (List[str]): List of files to load.
        transform (Optional[Callable]): Transform to apply to the data.
        pre_transform (Optional[Callable]): Transform to apply during loading.
        filter_fn (Optional[Callable]): Function to filter files by metadata.
        streamer (DataStreamer): Data streamer for retrieving files.
    """

    def __init__(
        self,
        source_url: Optional[str] = None,
        source_dir: Optional[str] = None,
        cache_dir: Optional[str] = None,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
        filter_fn: Optional[Callable[[Dict], bool]] = None,
        max_cache_size: Optional[int] = None,
        include_attributes: Optional[List[str]] = None,
        normalize: bool = False,
        streaming_type: str = "auto",
        use_pyg: bool = True,
        convert_if_missing: bool = True,
        # New parameters for domain decomposition
        use_domain_decomposition: bool = False,
        num_partitions: int = 0,  # 0 means automatic based on system
        domain_boundary_mode: str = "assign_to_one_region",
        domain_cache_dir: Optional[str] = None,
        super_resolution: bool = False,
        **kwargs,  # Additional params required by the streamer
    ):
        """
        Initialize the dataset.

        Args:
            source_url: URL or path to the data source.
            source_dir: Directory to store raw data on NAS / local side.
            cache_dir: Directory to store cached files.
            transform: Transform to apply to the data.
            pre_transform: Transform to apply during loading.
            filter_fn: Function to filter files by metadata.
            max_cache_size: Maximum cache size in bytes.
            include_attributes: List of specific attributes to include.
            normalize: Whether to normalize node positions.
            streaming_type: Type of streaming to use ("auto", "hf", "nas").
            use_pyg: Whether to use PyG files instead of VTU when available.
            convert_if_missing: Whether to convert VTU to PyG when PyG is missing.
            use_domain_decomposition: Whether to use domain decomposition.
            num_partitions: Number of partitions for domain decomposition.
            domain_boundary_mode: Boundary handling mode for domain decomposition.
            domain_cache_dir: Directory to store domain decomposition cache.
            super_resolution: Whether to use super-resolution data.
            **kwargs: Additional parameters for the streamer. (username, password, etc.)
        """
        self.source_url = source_url

        # Set up cache directory
        if cache_dir is None:
            home_dir = os.path.expanduser("~")
            cache_dir = os.path.join(home_dir, ".vascusim", "cache")

        if source_dir is None:
            home_dir = os.path.expanduser("~")
            source_dir = os.path.join(home_dir, ".vascusim", "raw")
        self.source_dir = Path(source_dir)
        self.raw_dir = self.source_dir / "raw"
        self.processed_dir = self.source_dir / "processed"

        self.cache_dir = Path(cache_dir)
        self.transform = transform
        self.pre_transform = pre_transform
        self.filter_fn = filter_fn
        self.include_attributes = include_attributes
        self.normalize = normalize

        self.use_pyg = use_pyg
        self.convert_if_missing = convert_if_missing

        # Create streamer based on source URL
        if streaming_type == "auto":
            if "huggingface.co" in source_url or "hf.co" in source_url:
                streaming_type = "hf"
            else:
                streaming_type = "nas"

        if streaming_type == "hf":
            self.streamer = HuggingFaceStreamer(
                repo_id=source_url, cache_dir=str(self.cache_dir), max_cache_size=max_cache_size
            )
        elif streaming_type == "nas":
            # check if kwargs are provided
            if not all(k in kwargs for k in ["username", "password"]):
                raise ValueError("For NAS streaming, 'username', 'password' must be provided.")

            if "access_mode" not in kwargs:
                kwargs["access_mode"] = "api"

            self.streamer = NASStreamer(
                source_url=source_url,
                source_dir=source_dir,
                cache_dir=str(self.cache_dir),
                max_cache_size=max_cache_size,
                username=kwargs.get("username"),
                password=kwargs.get("password"),
                access_mode=kwargs.get("access_mode"),
            )
        elif streaming_type == "local":
            self.streamer = LocalStreamer(source_dir=source_dir)
        else:
            raise ValueError(f"Unsupported streaming type: {streaming_type}")

        # Get metadata from the streamer
        metadata_path = self.streamer.get_file(
            file_path=self.source_dir / "vascuSim_metadata_index.json", download_if_missing=True
        )
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.metadata = metadata

        # Store domain decomposition settings
        self.use_domain_decomposition = use_domain_decomposition
        self.num_partitions = num_partitions
        self.domain_boundary_mode = domain_boundary_mode

        # Set up domain cache directory
        if domain_cache_dir is None and use_domain_decomposition:
            domain_cache_dir = self.processed_dir
        self.domain_cache_dir = Path(domain_cache_dir) if domain_cache_dir else None

        # Create cache directory if needed
        if self.use_domain_decomposition and self.domain_cache_dir:
            self.domain_cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize domain manager if needed
        self.domain_manager = None
        if self.use_domain_decomposition:
            self.domain_manager = DomainManager(
                num_partitions=self.num_partitions,
                cache_dir=str(self.domain_cache_dir),
                boundary_mode=self.domain_boundary_mode,
                transform=transform,
                pre_transform=pre_transform,
            )

        # Set up super-resolution if needed
        self.super_resolution = super_resolution

        # Check dataset process status from metadata
        if "processed" in metadata and metadata["processed"]:
            # check processed function matches current configuration (super_resolution, use_domain_decomposition, use_pyg)
            if (
                metadata.get("super_resolution", False) != self.super_resolution
                or metadata.get("use_domain_decomposition", False) != self.use_domain_decomposition
                or metadata.get("use_pyg", False) != self.use_pyg
            ):
                logger.warning(
                    "Metadata indicates processed data, but configuration does not match. "
                    "Reprocessing may be required."
                )
                self.processed = False
            else:
                logger.info("Metadata indicates processed data. Using existing processed files.")
                self.processed = True
        else:
            logger.info("Metadata indicates unprocessed data. Processing required.")
            self.processed = False

        # Initialize file list
        self.file_list = self._initialize_file_list()

    def _initialize_file_list(self) -> List[str]:
        """
        Initialize the list of files to load.

        Returns:
            List of file paths.
        """
        try:
            # If available, use the streamer's list_files method
            if hasattr(self.streamer, "list_directory"):
                raw_dir = self.raw_dir
                processed_dir = self.processed_dir
                if self.processed:
                    # If processed, use the processed directory
                    all_files = self.streamer.list_directory(processed_dir)
                else:
                    # If not processed, use the raw directory
                    all_files = self.streamer.list_directory(raw_dir)
            else:
                # Otherwise, try to find an index file
                index_path = self.streamer.get_file(
                    "vascuSim_metadata_index.json", download_if_missing=True
                )
                with open(index_path, "r") as f:
                    index_data = json.load(f)
                all_files = index_data.get("files", [])

            # Filter files by type
            vtu_files = [f for f in all_files if f.endswith(".vtu")]
            h5_files = [f for f in all_files if f.endswith(".h5")]

            # Combine and sort
            # file_list = sorted(vtu_files)
            file_list = sorted(vtu_files + h5_files)

            # Apply metadata filter if provided
            if self.filter_fn is not None:
                filtered_files = []
                for file_path in file_list:
                    try:
                        # Get metadata for the file
                        metadata_id = file_path.rsplit(".", 1)[0] + ".json"
                        metadata = self.streamer.get_metadata(metadata_id)

                        # Apply filter
                        if self.filter_fn(metadata):
                            filtered_files.append(file_path)
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        logger.warning(f"Error loading metadata for {file_path}: {e}")

                file_list = filtered_files

            return file_list

        except Exception as e:
            logger.error(f"Failed to initialize file list: {e}")
            return []

    def extract_data_by_criteria(
        self, geometry_id=None, timestep=None, resolution=None, geometry_type=None
    ):
        """
        Extract file references based on specific criteria.

        Args:
            geometry_id: Optional ID of the geometry to filter by
            timestep: Optional timestep to filter by
            resolution: Optional resolution to filter by
            geometry_type: Optional geometry type to filter by

        Returns:
            List of file references matching the criteria
        """
        results = []

        def match_filters(path, g=None, t=None, r=None, gt=None):
            if geometry_id is not None and g is not None and str(g) != str(geometry_id):
                return False
            if timestep is not None and t is not None and str(t) != str(timestep):
                return False
            if resolution is not None and r is not None and r != resolution:
                return False
            if geometry_type is not None and gt is not None and gt != geometry_type:
                return False
            return True

        # Decide which index to use
        if geometry_id is not None and str(geometry_id) in self.metadata["geometry_index"]:
            entry = self.metadata["geometry_index"][str(geometry_id)]
            for t, t_data in entry["timesteps"].items():
                for r, r_data in t_data["resolutions"].items():
                    for gt, gt_data in r_data["geometry_type"].items():
                        if match_filters(path="geometry", g=geometry_id, t=t, r=r, gt=gt):
                            results.extend(f["vtu"] for f in gt_data["files"])

        elif timestep is not None and str(timestep) in self.metadata["timestep_index"]:
            entry = self.metadata["timestep_index"][str(timestep)]
            for g, g_data in entry["geometries"].items():
                for r, r_data in g_data["resolutions"].items():
                    for gt, gt_data in r_data["geometry_type"].items():
                        if match_filters(path="timestep", g=g, t=timestep, r=r, gt=gt):
                            results.extend(f["vtu"] for f in gt_data["files"])

        elif resolution is not None and resolution in self.metadata["resolution_index"]:
            entry = self.metadata["resolution_index"][resolution]
            for g, g_data in entry["geometries"].items():
                for t, t_data in g_data["timesteps"].items():
                    for gt, gt_data in t_data["geometry_type"].items():
                        if match_filters(path="resolution", g=g, t=t, r=resolution, gt=gt):
                            results.extend(f["vtu"] for f in gt_data["files"])

        elif geometry_type is not None and geometry_type in self.metadata["geometry_type_index"]:
            entry = self.metadata["geometry_type_index"][geometry_type]
            for g, g_data in entry["geometries"].items():
                for t, t_data in g_data["timesteps"].items():
                    for r, r_data in t_data["resolution"].items():
                        if match_filters(path="gtype", g=g, t=t, r=r, gt=geometry_type):
                            results.extend(f["vtu"] for f in r_data["files"])

        return list(set(results))  # Remove duplicates

    def __len__(self) -> int:
        """
        Get the number of samples in the dataset.

        Returns:
            Number of samples.
        """
        return len(self.file_list)

    def __getitem__(self, idx: int) -> Union[Data, List[Data]]:
        """
        Get a sample from the dataset.

        Args:
            idx: Index of the sample to get.

        Returns:
            PyTorch Geometric Data object or list of subdomains.

        Raises:
            IndexError: If the index is out of range.
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file is invalid.
        """
        if idx >= len(self.file_list) or idx < 0:
            raise IndexError(
                f"Index {idx} out of range for dataset with {len(self.file_list)} samples"
            )

        file_path = self.file_list[idx]

        # Handle domain decomposition if enabled
        if self.use_domain_decomposition:
            try:
                # Try to load domains from HDF5 file
                domains_file = self._get_domains_file_path(file_path)

                if self.processed:
                    domains_file = self.streamer.get_file(
                        self.processed_dir / file_path,
                        local_file_path=domains_file,
                        download_if_missing=True,
                    )
                    self.domain_manager, subdomains = DomainManager.load_from_hdf5(domains_file)
                else:
                    # If domains file doesn't exist, decompose the VTU file
                    local_path = self.streamer.get_file(
                        self.raw_dir / file_path, download_if_missing=True
                    )
                    subdomains = self._decompose_vtu_file(file_path)

                # Apply transformations to each subdomain if needed
                if self.pre_transform is not None:
                    subdomains = [self.pre_transform(subdomain) for subdomain in subdomains]

                if self.transform is not None:
                    subdomains = [self.transform(subdomain) for subdomain in subdomains]

                return subdomains

            except Exception as e:
                logger.error(f"Error loading subdomains for {file_path}: {e}")
                logger.info("Falling back to single domain loading")
                # Fall back to regular loading

        # Regular loading logic
        # Try to get PyG file if enabled
        if self.use_pyg:
            try:
                # Use the get_pyg_file method from the streamer
                local_path = self.streamer.get_pyg_file(
                    file_path, download_if_missing=True, convert_if_missing=self.convert_if_missing
                )

                # Load PyG data directly
                data = torch.load(local_path)

            except (FileNotFoundError, ImportError, AttributeError) as e:
                # Fall back to VTU if PyG loading fails
                # Download VTU file
                local_path = self.streamer.get_file(file_path, download_if_missing=True)

                # Load VTU data
                if file_path.endswith(".vtu"):
                    data = vtu_to_pyg(
                        str(local_path),
                        attributes=self.include_attributes,
                        normalize=self.normalize,
                    )
                else:
                    raise ValueError(f"Unsupported file type: {file_path}")
        else:
            # Original VTU loading logic
            local_path = self.streamer.get_file(file_path, download_if_missing=True)

            # Load data based on file type
            if file_path.endswith(".vtu"):
                data = vtu_to_pyg(
                    str(local_path), attributes=self.include_attributes, normalize=self.normalize
                )
            else:
                raise ValueError(f"Unsupported file type: {file_path}")

        # Apply pre-transform if provided
        if self.pre_transform is not None:
            data = self.pre_transform(data)

        # Apply transform if provided
        if self.transform is not None:
            data = self.transform(data)

        return data

    def _decompose_vtu_file(self, file_path: str) -> List[Data]:
        """
        Decompose a VTU file into subdomains.

        Args:
            file_path: Path to the VTU file

        Returns:
            List of PyG subdomains
        """
        # Get local path to VTU file
        local_path = self.streamer.get_file(file_path, download_if_missing=True)

        # Decompose VTU file
        self.domain_manager.decompose_vtu(local_path)

        # Extract PyG subdomains
        subdomains = self.domain_manager.extract_pyg_subdomains()

        # Save subdomains to HDF5 file
        domains_file = self._get_domains_file_path(file_path)
        self.domain_manager.save_subdomains_to_hdf5(domains_file)

        return subdomains

    def _get_domains_file_path(self, file_path: str) -> Path:
        """
        Get the path to the domains file for a VTU file.

        Args:
            file_path: Path to the VTU file

        Returns:
            Path to the domains file
        """
        # Use the same file name but with .domains.h5 extension in the domain cache directory
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]
        # JUST FOR TESTING
        base_name = os.path.splitext(base_name)[0]

        domains_file = self.domain_cache_dir / f"{base_name}.vtu.h5"
        return domains_file

    def _load_domains(self, file_path: str) -> List[Data]:
        """
        Load domains for a VTU file.

        Args:
            file_path: Path to the VTU file

        Returns:
            List of PyG subdomains
        """
        # Get the domains file path
        domains_file = self._get_domains_file_path(file_path)

        # Check if domains file exists
        if not domains_file.exists():
            return self._decompose_vtu_file(file_path)

        # Load domains
        domain_manager, subdomains = DomainManager.load_from_hdf5(domains_file)
        self.domain_manager = domain_manager

        return subdomains

    def process(self) -> List[Data]:
        """
        Process VTU files in the dataset and save PyG object to source_dir/processed according to decomposition flag.
        Can be called prior to training for more efficient data loading.
        """
        # Create processed directory if it doesn't exist
        try:
            self.streamer.create_directory(folder_path=self.source_dir, name="processed")
        except Exception as e:
            logger.warning(f"Failed to create processed directory: {e}")
            self.processed_dir.mkdir(parents=True, exist_ok=True)

        # Process the dataset based on the type of data
        if self.super_resolution:
            self.process_super_resolution()
        else:
            self.process_regular_list()
        return self.file_list

    def process_regular_list(self):
        """
        Process the dataset for regular list of files.

        This method processes each file in the dataset, converting it to a PyG
        object and saving it to the processed directory. If domain decomposition
        is enabled, it decomposes the VTU file into subdomains and saves them
        to HDF5 files.
        """
        # Process each file in the dataset
        for idx in range(len(self.file_list)):
            file_path = self.raw_dir / self.file_list[idx]
            if self.use_domain_decomposition:
                _ = self.domain_manager.decompose_vtu(file_path)
                _ = self.domain_manager.extract_pyg_subdomains()
                save_path = self.processed_dir / f"{os.path.basename(file_path)}.h5"
                self.domain_manager.save_subdomains_to_hdf5(save_path)
                logger.info(f"Decomposed {file_path} and saved to {save_path}")
            else:
                # Load VTU file and convert to PyG
                local_path = self.streamer.get_file(file_path, download_if_missing=True)
                data = vtu_to_pyg(
                    str(local_path),
                    attributes=self.include_attributes,
                    normalize=self.normalize,
                )

                # Save PyG object to processed directory
                save_path = self.processed_dir / f"{os.path.basename(file_path)}.pt"
                torch.save(data, save_path)
                logger.info(f"Processed {file_path} and saved to {save_path}")
        # Update file list with processed files
        if self.use_domain_decomposition:
            self.file_list = sorted(self.processed_dir.glob("*.h5"))
        else:
            self.file_list = sorted(self.processed_dir.glob("*.pt"))
        # Update metadata
        self.metadata["processed"] = True
        self.metadata["super_resolution"] = self.super_resolution
        self.metadata["use_domain_decomposition"] = self.use_domain_decomposition
        self.metadata["use_pyg"] = self.use_pyg

        # Save metadata
        metadata_path = self.source_dir / "vascuSim_metadata_index.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=4)
        logger.info(f"Processed metadata saved to {metadata_path}")

        return self.file_list

    def process_super_resolution(self):
        """
        Process the dataset for super-resolution.

        This method processes high-resolution files in the dataset, converting
        them to PyG objects and saving them to the processed directory. If
        domain decomposition is enabled, it decomposes the VTU file into
        subdomains and saves them to HDF5 files.
        """
        high_res_file_list = self.extract_data_by_criteria(resolution="high")

        if self.use_domain_decomposition:
            # Decompose high-resolution files
            for file_path in high_res_file_list:
                file_path_abs = self.raw_dir / file_path
                local_path = self.streamer.get_file(file_path_abs, download_if_missing=True)
                self.domain_manager.decompose_vtu(local_path)
                subdomains = self.domain_manager.extract_pyg_subdomains()
                save_path = self.processed_dir / f"{os.path.basename(file_path)}.h5"
                self.domain_manager.save_subdomains_to_hdf5(save_path, streamer=self.streamer)
                logger.info(f"Decomposed {file_path} and saved to {save_path}")
        else:
            # Process high-resolution files
            for file_path in high_res_file_list:
                file_path_abs = self.raw_dir / file_path
                local_path = self.streamer.get_file(file_path_abs, download_if_missing=True)
                data = vtu_to_pyg(
                    str(local_path),
                    attributes=self.include_attributes,
                    normalize=self.normalize,
                )

                # Save processed data to the processed directory
                save_path = self.processed_dir / f"{os.path.basename(file_path)}.pt"
                torch.save(data, save_path)
                logger.info(f"Processed {file_path} and saved to {save_path}")
        # Update file list with processed files
        if self.use_domain_decomposition:
            self.file_list = sorted(self.processed_dir.glob("*.h5"))
        else:
            self.file_list = sorted(self.processed_dir.glob("*.pt"))

        # Update metadata
        self.metadata["processed"] = True
        self.metadata["super_resolution"] = self.super_resolution
        self.metadata["use_domain_decomposition"] = self.use_domain_decomposition
        self.metadata["use_pyg"] = self.use_pyg
        # Save metadata
        metadata_path = self.source_dir / "vascuSim_metadata_index.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=4)
        logger.info(f"Processed metadata saved to {metadata_path}")

        return self.file_list


class StreamingVascuDataset(VascuDataset):
    """
    Streaming dataset for vascular simulation data.

    This class extends VascuDataset with additional streaming functionality,
    including background downloading and dynamic cache management.

    Attributes:
        prefetch (bool): Whether to prefetch data in the background.
        prefetch_size (int): Number of samples to prefetch.
        delete_after_use (bool): Whether to delete files after use.
    """

    def __init__(
        self,
        source_url: Optional[str] = None,
        source_dir: Optional[str] = None,
        cache_dir: Optional[str] = None,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
        filter_fn: Optional[Callable[[Dict], bool]] = None,
        max_cache_size: Optional[int] = None,
        include_attributes: Optional[List[str]] = None,
        normalize: bool = False,
        streaming_type: str = "auto",
        use_pyg: bool = True,
        convert_if_missing: bool = True,
        prefetch: bool = True,
        prefetch_size: int = 5,
        prefetch_stop_idx: Optional[int] = None,
        delete_after_use: bool = False,
        # Domain decomposition parameters
        use_domain_decomposition: bool = False,
        num_partitions: int = 0,
        domain_boundary_mode: str = "assign_to_one_region",
        domain_cache_dir: Optional[str] = None,
        super_resolution: bool = False,
        **kwargs,  # Additional params required by the streamer
    ):
        """
        Initialize the streaming dataset.

        Args:
            source_url: URL or path to the data source.
            cache_dir: Directory to store cached files.
            transform: Transform to apply to the data.
            pre_transform: Transform to apply during loading.
            filter_fn: Function to filter files by metadata.
            load_vtu: Whether to load VTU files.
            load_vtp: Whether to load VTP files.
            max_cache_size: Maximum cache size in bytes.
            include_attributes: List of specific attributes to include.
            normalize: Whether to normalize node positions.
            streaming_type: Type of streaming to use ("auto", "hf", "nas").
            prefetch: Whether to prefetch data in the background.
            prefetch_size: Number of samples to prefetch.
            delete_after_use: Whether to delete files after use.
            use_domain_decomposition: Whether to use domain decomposition.
            num_partitions: Number of partitions for domain decomposition.
            domain_boundary_mode: Boundary handling mode for domain decomposition.
            domain_cache_dir: Directory to store domain decomposition cache.
        """
        super().__init__(
            source_url=source_url,
            source_dir=source_dir,
            cache_dir=cache_dir,
            transform=transform,
            pre_transform=pre_transform,
            filter_fn=filter_fn,
            max_cache_size=max_cache_size,
            include_attributes=include_attributes,
            normalize=normalize,
            streaming_type=streaming_type,
            use_pyg=use_pyg,
            convert_if_missing=convert_if_missing,
            use_domain_decomposition=use_domain_decomposition,
            num_partitions=num_partitions,
            domain_boundary_mode=domain_boundary_mode,
            domain_cache_dir=domain_cache_dir,
            super_resolution=super_resolution,
            **kwargs,
        )

        self.prefetch = prefetch
        self.prefetch_size = prefetch_size
        self.delete_after_use = delete_after_use
        self._last_index = None
        if prefetch_stop_idx is not None:
            self.stop_index = prefetch_stop_idx
        else:
            self.stop_index = len(self.file_list) - 1

        # Start prefetching if enabled
        self.prefetch_initialized = False

    def __getstate__(self):
        """
        Custom method to control what gets pickled.
        Remove any unpicklable attributes before pickling.
        """
        state = self.__dict__.copy()
        # Don't try to pickle thread-related objects
        return state

    def _ensure_process_registry(self):
        """
        Ensure this process has an entry in the registry.
        Must be called in every method that needs access to process-specific data.
        """
        global _PREFETCH_REGISTRY
        self.process_id = os.getpid()  # Get current process ID

        if self.process_id not in _PREFETCH_REGISTRY:
            _PREFETCH_REGISTRY[self.process_id] = {"memory_table": {}, "active_indices": set()}
            logging.info(f"Initialized registry for process {self.process_id}")

    def _initialize_prefetch(self):
        """
        Initialize prefetching after the dataset has been pickled and sent to worker processes.
        """
        if self.prefetch and not self.prefetch_initialized:
            self._prefetch(0)
            self.prefetch_initialized = True

    def _get_memory_table(self):
        """
        Get the process-specific memory table.
        """
        self._ensure_process_registry()  # Ensure registry is initialized
        global _PREFETCH_REGISTRY
        return _PREFETCH_REGISTRY[self.process_id]["memory_table"]

    def _get_active_indices(self):
        """
        Get the set of indices currently being prefetched.
        """
        self._ensure_process_registry()  # Ensure registry is initialized
        global _PREFETCH_REGISTRY
        return _PREFETCH_REGISTRY[self.process_id]["active_indices"]

    def prefetch_worker(self, idx):
        """
        Worker function to prefetch data at the given index.
        Designed to be pickle-safe.

        Args:
            idx: Index to prefetch data for.
        """
        self._ensure_process_registry()  # Ensure registry is initialized
        memory_table = self._get_memory_table()
        active_indices = self._get_active_indices()

        try:
            # Mark this index as being processed
            active_indices.add(idx)

            if idx in memory_table:
                # Skip if already in memory
                return
            else:
                # Initialize memory table entry
                memory_table[idx] = None

            if idx >= len(self.file_list):
                return

            file_path = self.file_list[idx]

            # Prefetch differently based on domain decomposition
            if self.use_domain_decomposition:
                # Check if domains file exists
                domains_file = self._get_domains_file_path(file_path)
                if self.processed:
                    domains_file = self.streamer.get_file(
                        self.processed_dir / file_path,
                        local_file_path=domains_file,
                        download_if_missing=True,
                    )
                    domain_manager, subdomains = DomainManager.load_from_hdf5(domains_file)
                    # Store the pre-fetched data
                    memory_table[idx] = subdomains
            else:
                # Regular prefetch - just ensure files are downloaded
                if self.use_pyg:
                    self.streamer.get_pyg_file(
                        file_path,
                        download_if_missing=True,
                        convert_if_missing=self.convert_if_missing,
                    )
                else:
                    # Just download the file
                    self.streamer.get_file(file_path, download_if_missing=True)

                # Also prefetch metadata
                metadata_id = file_path.rsplit(".", 1)[0] + ".json"
                self.streamer.get_file(metadata_id, download_if_missing=True)

                # For non-domain decomposition, we don't store data in memory
                # Just mark that prefetching is complete
                memory_table[idx] = True

        except Exception as e:
            logger.warning(f"Process {self.process_id}: Error prefetching file at index {idx}: {e}")
        finally:
            # Remove this index from active set when done
            active_indices.discard(idx)

    def _prefetch(self, start_idx: int) -> None:
        """
        Prefetch data starting from the given index.
        Process-safe implementation that doesn't store thread objects.

        Args:
            start_idx: Index to start prefetching from.
        """
        if not self.prefetch or start_idx >= len(self.file_list):
            return
        # Create prefetch indices
        prefetch_indices = list(
            range(start_idx, min(start_idx + self.prefetch_size, len(self.file_list)))
        )
        active_indices = self._get_active_indices()

        # Only start new threads for indices not already being processed
        for idx in prefetch_indices:
            if idx not in active_indices:
                # Use daemon threads that won't prevent process exit
                thread = threading.Thread(
                    target=self.prefetch_worker,
                    args=(idx,),
                    daemon=True,  # Daemon threads don't block process exit
                )
                thread.start()

    def terminate_prefetch(self):
        """
        External call to terminate prefetching.
        Process-safe implementation.
        """
        self._ensure_process_registry()  # Ensure registry is initialized

        global _PREFETCH_REGISTRY
        if self.process_id in _PREFETCH_REGISTRY:
            _PREFETCH_REGISTRY[self.process_id] = {"memory_table": {}, "active_indices": set()}
        self._last_index = None
        self.stop_index = len(self.file_list) - 1
        self.prefetch_initialized = False
        print(f"Process {self.process_id}: Prefetching terminated.")

    def __getitem__(self, idx: int) -> Union[Data, List[Data]]:
        """
        Get a sample from the dataset with streaming functionality.
        Initialize prefetching if needed.

        Args:
            idx: Index of the sample to get.

        Returns:
            PyTorch Geometric Data object or list of subdomains.
        """
        # Initialize prefetching on first access
        if self.prefetch and not self.prefetch_initialized:
            self._initialize_prefetch()

        self._ensure_process_registry()  # Ensure registry is initialized
        memory_table = self._get_memory_table()

        # Handle domain decomposition if enabled
        if self.use_domain_decomposition:
            # Check if the index is in the prefetch memory table
            if idx in memory_table and memory_table[idx] is not None:
                # Get the pre-fetched subdomain from memory
                domains = memory_table.pop(idx)

            elif idx in memory_table and memory_table[idx] is None:
                timer = 0
                # If the prefetch memory table is empty, wait for the prefetch to finish
                while memory_table[idx] is None:
                    time.sleep(0.1)
                    timer += 0.1
                    if timer > 120:
                        logger.warning(
                            f"Process {self.process_id}: Timeout waiting for prefetch at index {idx}"
                        )
                        return None
                # Get the pre-fetched subdomain from memory
                domains = memory_table.pop(idx)

            else:
                # Get domains from parent class
                domains = super().__getitem__(idx)

            # Start prefetching next batch if needed
            if (
                self.prefetch
                and (self._last_index is None or idx + self.prefetch_size > self._last_index)
                and idx + self.prefetch_size < self.stop_index
            ):
                self._prefetch(idx + 1)
                self._last_index = idx + self.prefetch_size

            if self.delete_after_use:
                try:
                    file_path = self.file_list[idx]
                    local_path = self._get_domains_file_path(file_path)

                    if local_path.exists():
                        os.remove(local_path)
                except Exception as e:
                    logger.warning(
                        f"Process {self.process_id}: Error deleting file at index {idx}: {e}"
                    )

            return domains

        else:
            # Original implementation for single data object
            # Get data from parent class
            data = super().__getitem__(idx)

            # Start prefetching next batch if needed
            if self.prefetch and (
                self._last_index is None or idx + self.prefetch_size > self._last_index
            ):
                self._prefetch(idx + 1)
                self._last_index = idx + self.prefetch_size

            # Delete file after use if requested
            if self.delete_after_use:
                try:
                    file_path = self.file_list[idx]
                    local_path = self.streamer.get_file(file_path, download_if_missing=False)

                    if local_path.exists():
                        os.remove(local_path)

                    # Also remove metadata
                    metadata_id = file_path.rsplit(".", 1)[0] + ".json"
                    metadata_path = self.streamer.get_file(metadata_id, download_if_missing=False)

                    if metadata_path.exists():
                        os.remove(metadata_path)
                except Exception as e:
                    logger.warning(
                        f"Process {self.process_id}: Error deleting file at index {idx}: {e}"
                    )

            return data


class SubDataset(Dataset):
    """
    Subset of a dataset for specific indices.

    This class provides a PyTorch Dataset implementation for creating a
    subset of a dataset based on specific data.
    """

    def __init__(self, data: List[Data]):
        """
        Initialize the subset dataset.

        Args:
            dataset: The original dataset to create a subset from.
            indices: List of indices to include in the subset.
        """
        self.dataset = data

    def __len__(self) -> int:
        """
        Get the number of samples in the subset.

        Returns:
            Number of samples.
        """
        return len(self.dataset)

    def __getitem__(self, idx: int) -> Data:
        """
        Get a sample from the subset.

        Args:
            idx: Index of the sample to get.

        Returns:
            PyTorch Geometric Data object.
        """
        if idx >= len(self.dataset) or idx < 0:
            raise IndexError(
                f"Index {idx} out of range for dataset with {len(self.dataset)} samples"
            )

        return self.dataset[idx]
