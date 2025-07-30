"""
Domain decomposition utilities for vascular simulation data.

This module provides functionality for decomposing vascular geometries into
subdomains for distributed processing, and reconstructing results from
processed subdomains using VTK's native capabilities.
"""

import json
import logging
import os
import shutil
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

import h5py
import numpy as np
import torch
from torch_geometric.data import Data
from tqdm import tqdm

# Import VTK - a required dependency for domain decomposition
try:
    import vtk
    from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy

    HAS_VTK = True
except ImportError:
    HAS_VTK = False
    raise ImportError("VTK is required for domain decomposition functionality")

from ..data.conversion import build_graph, vtu_to_pyg
from ..io.vtk_utils import extract_mesh_from_vtu

logger = logging.getLogger(__name__)


class DomainManager:
    """
    Class for managing domain decomposition and reconstruction using VTK's capabilities.

    This class provides methods to split a vascular geometry into smaller subdomains
    based on VTK's redistribution filter, and to reconstruct the complete domain from
    processed subdomains.

    Attributes:
        num_partitions (int): Number of partitions to create.
        cache_dir (Path): Directory to store temporary data.
        use_all_processors (bool): Whether to use all available processors for decomposition.
        boundary_mode (str): How to handle boundaries between partitions.
        preserve_partitions (bool): Whether to preserve partitions in output.
    """

    def __init__(
        self,
        num_partitions: int = 0,  # 0 means automatic based on system
        cache_dir: Optional[str] = None,
        use_all_processors: bool = True,
        boundary_mode: str = "assign_to_one_region",
        preserve_partitions: bool = True,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
    ):
        """
        Initialize the domain manager.

        Args:
            num_partitions: Number of partitions to create (0 for automatic).
            cache_dir: Directory to store temporary data.
            use_all_processors: Whether to use all available processors for decomposition.
            boundary_mode: How to handle boundaries between partitions.
            preserve_partitions: Whether to preserve partitions in output.
        """
        if not HAS_VTK:
            raise ImportError("VTK is required for domain decomposition functionality")

        self.num_partitions = num_partitions
        self.use_all_processors = use_all_processors
        self.boundary_mode = boundary_mode
        self.preserve_partitions = preserve_partitions

        # Set up cache directory
        if cache_dir is None:
            home_dir = os.path.expanduser("~")
            cache_dir = os.path.join(home_dir, ".vascusim", "partition_cache")

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize controller
        # self.controller = vtk.vtkMultiProcessController.GetGlobalController()
        # if not self.controller or self.controller.GetNumberOfProcesses() <= 1:
        #     logger.info("Running in serial mode. No MPI parallelism available.")
        #     self.controller = vtk.vtkDummyController()

        # Store partitioned meshes
        self.partitioned_mesh = None
        self.subdomains = []
        self.metadata = {}

    def decompose_vtu(self, vtu_file: Union[str, Path]) -> vtk.vtkPartitionedDataSet:
        """
        Decompose a VTU file directly into partitions using VTK.

        Args:
            vtu_file: Path to the VTU file.

        Returns:
            VTK partitioned dataset containing the subdomains.
        """
        self.controller = vtk.vtkMultiProcessController.GetGlobalController()
        if not self.controller or self.controller.GetNumberOfProcesses() <= 1:
            logger.info("Running in serial mode. No MPI parallelism available.")
            self.controller = vtk.vtkDummyController()

        logger.info(f"Decomposing VTU file: {vtu_file}")
        filename = os.path.basename(vtu_file)
        self.filename = filename.split(".")[0]

        vtu_file = str(vtu_file)
        metadata_file = vtu_file.replace(".vtu", ".json")
        if os.path.exists(metadata_file):
            logger.info(f"Loading metadata from {metadata_file}")
            with open(metadata_file, "r") as f:
                self.metadata = json.load(f)

        # Extract mesh from VTU file
        mesh, _, _ = extract_mesh_from_vtu(vtu_file)

        # Add global node IDs if not present
        mesh = self._assign_global_node_ids(mesh)

        # Configure redistribution filter
        distributed_filter = vtk.vtkRedistributeDataSetFilter()
        distributed_filter.SetController(self.controller)
        distributed_filter.SetInputData(mesh)
        distributed_filter.SetPreservePartitionsInOutput(self.preserve_partitions)

        # Set number of partitions
        if self.num_partitions > 0:
            distributed_filter.SetNumberOfPartitions(self.num_partitions)

        # Set boundary handling mode
        if self.boundary_mode == "assign_to_one_region":
            distributed_filter.SetBoundaryModeToAssignToOneRegion()
        elif self.boundary_mode == "assign_to_all_regions":
            distributed_filter.SetBoundaryModeToAssignToAllRegions()
        elif self.boundary_mode == "split_boundaries":
            distributed_filter.SetBoundaryModeToSplitBoundaryFaces()

        # Add progress observer
        progress_observer = ProgressObserver()
        distributed_filter.AddObserver("ProgressEvent", progress_observer)

        # Execute the partitioning
        logger.info("Running VTK redistribution filter...")
        distributed_filter.UpdateInformation()
        distributed_filter.Modified()
        distributed_filter.Update()

        # Get the output
        self.partitioned_mesh = distributed_filter.GetOutput()

        # Save info about the partitioning
        num_partitions = self.partitioned_mesh.GetNumberOfPartitions()
        self.metadata["num_partitions"] = num_partitions
        logger.info(f"Partitioned mesh into {num_partitions} subdomains")

        # Save the partitioned mesh to file
        self._save_partitioned_mesh()

        return self.partitioned_mesh

    def _assign_global_node_ids(self, mesh: vtk.vtkUnstructuredGrid) -> vtk.vtkUnstructuredGrid:
        """
        Assign global node IDs to a VTK mesh if not already present.

        Args:
            mesh: VTK unstructured grid.

        Returns:
            VTK unstructured grid with global node IDs.
        """
        # Check if global node IDs are already present
        if mesh.GetPointData().GetArray("GlobalNodeID") is not None:
            return mesh

        # Create global node IDs
        num_points = mesh.GetNumberOfPoints()
        global_node_id = vtk.vtkIdTypeArray()
        global_node_id.SetName("GlobalNodeID")
        global_node_id.SetNumberOfComponents(1)
        global_node_id.SetNumberOfTuples(num_points)

        for i in range(num_points):
            global_node_id.SetValue(i, i)

        mesh.GetPointData().AddArray(global_node_id)
        return mesh

    def _save_partitioned_mesh(self):
        """Save the partitioned mesh to a VTK file for later reference."""
        if self.partitioned_mesh is None:
            return

        # Generate unique filename based on timestamp
        partition_file = self.cache_dir / f"{self.filename}.vtpd"

        # Save the metadata
        self.metadata["partition_file"] = str(partition_file)

        # Write the partitioned dataset
        writer = vtk.vtkXMLPartitionedDataSetWriter()
        writer.SetFileName(str(partition_file))
        writer.SetInputData(self.partitioned_mesh)
        writer.Write()

        logger.info(f"Saved partitioned mesh to {partition_file}")

    def extract_pyg_subdomains(self) -> List[Data]:
        """
        Extract PyTorch Geometric subdomains from the partitioned VTK mesh.

        Returns:
            List of PyTorch Geometric Data objects for each subdomain.
        """
        if self.partitioned_mesh is None:
            raise ValueError("No partitioned mesh available. Call decompose_vtu first.")

        logger.info("Extracting PyTorch Geometric subdomains from partitioned mesh")

        # Extract subdomains
        subdomains = []
        for i in range(self.partitioned_mesh.GetNumberOfPartitions()):
            partition = self.partitioned_mesh.GetPartition(i)
            if not partition or partition.GetNumberOfPoints() == 0:
                logger.warning(f"Skipping empty partition {i}")
                continue

            # Convert subdomain to PyG
            subdomain = self._vtk_to_pyg(partition)

            # Store global node IDs for reconstruction
            node_id_array = partition.GetPointData().GetArray("GlobalNodeID")
            if node_id_array is None:
                logger.warning(f"Partition {i} missing GlobalNodeID")
                continue

            # Extract global node IDs
            global_node_ids = np.array(
                [node_id_array.GetValue(j) for j in range(node_id_array.GetNumberOfTuples())]
            )
            subdomain.original_indices = torch.tensor(global_node_ids, dtype=torch.long)
            subdomain.subdomain_id = i

            # Extract boundary information
            boundary_finder = vtk.vtkFeatureEdges()
            boundary_finder.SetInputData(partition)
            boundary_finder.BoundaryEdgesOn()
            boundary_finder.FeatureEdgesOff()
            boundary_finder.NonManifoldEdgesOff()
            boundary_finder.ManifoldEdgesOff()
            boundary_finder.Update()

            # Create boundary mask
            boundary_edges = boundary_finder.GetOutput()
            boundary_points = set()

            for j in range(boundary_edges.GetNumberOfCells()):
                cell = boundary_edges.GetCell(j)
                for k in range(cell.GetNumberOfPoints()):
                    point_id = cell.GetPointId(k)
                    boundary_points.add(point_id)

            # Set boundary mask
            boundary_mask = torch.zeros(subdomain.num_nodes, dtype=torch.bool)
            for point_id in boundary_points:
                if point_id < subdomain.num_nodes:
                    boundary_mask[point_id] = True

            subdomain.boundary_mask = boundary_mask

            # Add to subdomains list
            subdomains.append(subdomain)

        self.subdomains = subdomains
        self.metadata["num_subdomains"] = len(subdomains)

        logger.info(f"Extracted {len(subdomains)} PyG subdomains")
        return subdomains

    def _vtk_to_pyg(self, vtk_data: vtk.vtkUnstructuredGrid) -> Data:
        """
        Convert a VTK unstructured grid to a PyTorch Geometric Data object.

        Args:
            vtk_data: VTK unstructured grid.

        Returns:
            PyTorch Geometric Data object.
        """
        # Extract points
        num_points = vtk_data.GetNumberOfPoints()
        pos = np.array([vtk_data.GetPoint(i) for i in range(num_points)], dtype=np.float32)
        pos = torch.tensor(pos, dtype=torch.float)

        # Extract edge connectivity
        edge_set = set()
        for i in range(vtk_data.GetNumberOfCells()):
            cell = vtk_data.GetCell(i)
            num_points_ = cell.GetNumberOfPoints()

            for j in range(num_points_):
                for k in range(j + 1, num_points_):
                    p1, p2 = cell.GetPointId(j), cell.GetPointId(k)
                    # Add both directions for undirected graph
                    edge_set.add((p1, p2))
                    edge_set.add((p2, p1))

        edge_index = torch.tensor(list(edge_set), dtype=torch.long).t()

        # Create PyG data object
        data = Data(pos=pos, edge_index=edge_index)

        # Extract node attributes
        point_data = vtk_data.GetPointData()
        for i in range(point_data.GetNumberOfArrays()):
            # verify length of data matches number of points
            if point_data.GetArray(i).GetNumberOfTuples() != num_points:
                logger.warning(
                    f"Array {point_data.GetArrayName(i)} has inconsistent size with number of points"
                )
            array_name = point_data.GetArrayName(i)

            # Skip GlobalNodeID
            if array_name == "GlobalNodeID":
                continue

            array = point_data.GetArray(i)
            num_components = array.GetNumberOfComponents()

            if num_components == 1:
                # Scalar attribute
                attr_data = np.array(
                    [array.GetValue(j) for j in range(num_points)], dtype=np.float32
                )
                data[array_name] = torch.tensor(attr_data, dtype=torch.float)
            else:
                # Vector attribute
                attr_data = np.zeros((num_points, num_components), dtype=np.float32)
                for j in range(num_points):
                    for c in range(num_components):
                        attr_data[j, c] = array.GetComponent(j, c)

                data[array_name] = torch.tensor(attr_data, dtype=torch.float)

        return data

    def reconstruct_domain(
        self, processed_subdomains: List[torch.Tensor], original_partition_path: Union[str, Path]
    ) -> Data:
        """
        Reconstruct the complete domain from processed subdomains.

        Args:
            processed_subdomains: List of processed PyTorch Geometric Data objects.
            original_partition_path: Path to the original partitioned mesh file.

        Returns:
            Reconstructed PyTorch Geometric Data object.
        """
        if not processed_subdomains:
            raise ValueError("No subdomains provided for reconstruction")

        reader = vtk.vtkXMLPartitionedDataSetReader()
        reader.SetFileName(str(original_partition_path))
        reader.Update()

        # Get original partitioned mesh
        partitioned_mesh = reader.GetOutput()

        if len(processed_subdomains) != partitioned_mesh.GetNumberOfPartitions():
            raise ValueError(
                f"Expected {partitioned_mesh.GetNumberOfPartitions()} subdomains, got {len(processed_subdomains)}"
            )

        # Create an append filter to combine all partitions
        append_filter = vtk.vtkAppendFilter()

        # Process each subdomain
        logger.info("Reconstructing domain from subdomains")
        for i, processed_subdomain in enumerate(
            tqdm(processed_subdomains, desc="Reconstructing subdomains")
        ):
            # Get original partition
            partition = partitioned_mesh.GetPartition(i)
            if not partition:
                logger.warning(f"Original partition {i} not found. Skipping.")
                continue

            # Update partition with processed data
            updated_partition = self._update_partition_with_processed_data(
                partition, processed_subdomain
            )

            # Add to append filter
            append_filter.AddInputData(updated_partition)

        # Combine all partitions
        append_filter.Update()
        reconstructed_data = append_filter.GetOutput()

        # Apply post-processing for consistency
        # reconstructed_data = self._smooth_fields(reconstructed_data)

        logger.info("Domain reconstruction complete")
        return reconstructed_data

    def _update_partition_with_processed_data(
        self,
        partition: vtk.vtkUnstructuredGrid,
        processed_subdomain: torch.Tensor,
    ) -> vtk.vtkUnstructuredGrid:
        """
        Update a VTK partition with data from a processed subdomain.

        Args:
            partition: Original VTK partition.
            original_subdomain: Original PyG subdomain.
            processed_subdomain: Processed PyG subdomain.

        Returns:
            Updated VTK partition.
        """
        # Create a copy of the partition
        updated_partition = vtk.vtkUnstructuredGrid()
        updated_partition.DeepCopy(partition)

        # check number of physics points is equal to number of points in partition
        num_points = updated_partition.GetNumberOfPoints()
        if processed_subdomain.shape[0] != num_points:
            raise ValueError(
                f"Processed subdomain has {processed_subdomain.shape[0]} points, "
                f"but partition has {num_points} points"
            )

        # check coordinates of processed subdomain and partition match
        partition_coords = vtk_to_numpy(partition.GetPoints().GetData())
        processed_coords = processed_subdomain.pos.cpu().numpy()
        if not np.allclose(partition_coords, processed_coords):
            raise ValueError(
                "Coordinates of processed subdomain do not match partition coordinates"
            )

        # Get the attributes to update
        for key in processed_subdomain.keys():
            if key in [
                "pos",
                "edge_index",
                "edge_attr",
                "subdomain_id",
                "original_indices",
                "boundary_mask",
            ]:
                continue

            # Get processed attribute
            attr = processed_subdomain[key]
            if not isinstance(attr, torch.Tensor):
                continue

            # Create VTK array for the attribute
            if attr.dim() == 1:
                # Scalar attribute
                vtk_array = numpy_to_vtk(attr.cpu().numpy(), deep=True)
                vtk_array.SetName(key)
                updated_partition.GetPointData().AddArray(vtk_array)
            elif attr.dim() == 2:
                # Vector attribute
                components = attr.size(1)
                if components <= 3:
                    vtk_array = numpy_to_vtk(attr.cpu().numpy(), deep=True)
                    vtk_array.SetName(key)
                    vtk_array.SetNumberOfComponents(components)
                    updated_partition.GetPointData().AddArray(vtk_array)
                else:
                    # Multiple scalar components
                    for c in range(components):
                        vtk_array = numpy_to_vtk(attr[:, c].cpu().numpy(), deep=True)
                        vtk_array.SetName(f"{key}_{c}")
                        updated_partition.GetPointData().AddArray(vtk_array)

        return updated_partition

    def _smooth_fields(self, data: Data) -> Data:
        """
        Apply smoothing to fields to ensure consistency after reconstruction.

        Args:
            data: PyTorch Geometric Data object to smooth.

        Returns:
            Smoothed PyTorch Geometric Data object.
        """
        # Identify potential vector fields to smooth
        vector_fields = []
        for key in data.keys:
            attr = data[key]
            if isinstance(attr, torch.Tensor) and attr.dim() == 2 and attr.size(1) == 3:
                # Likely a vector field like velocity
                vector_fields.append(key)

        # Apply simple Laplacian smoothing to vector fields
        for field in vector_fields:
            # Skip if the field doesn't exist
            if not hasattr(data, field):
                continue

            # Get field data
            field_data = data[field].clone()

            # Create adjacency information from edge_index
            adj_list = {}
            edge_index = data.edge_index.cpu().numpy()
            for i in range(edge_index.shape[1]):
                src, dst = edge_index[0, i], edge_index[1, i]
                if src not in adj_list:
                    adj_list[src] = []
                adj_list[src].append(dst)

            # Apply simple Laplacian smoothing
            for _ in range(5):  # 5 smoothing iterations
                smoothed_data = field_data.clone()

                for node in range(data.num_nodes):
                    if node in adj_list and adj_list[node]:
                        # Average values of neighbors
                        neighbors = adj_list[node]
                        avg_value = torch.mean(field_data[neighbors], dim=0)

                        # Blend with original (0.3 is the smoothing factor)
                        smoothed_data[node] = 0.7 * field_data[node] + 0.3 * avg_value

                field_data = smoothed_data

            # Update the field
            data[field] = field_data

        return data

    def save_subdomains_to_hdf5(
        self, filename: Union[str, Path], streamer: Optional[Callable] = None
    ):
        """
        Save subdomains to an HDF5 file for efficient storage and retrieval.

        Args:
            filename: Path to the HDF5 file to create.
            streamer: Optional function to stream data during saving.
        """
        if not self.subdomains:
            raise ValueError("No subdomains to save")

        filename = Path(filename)
        basename = os.path.basename(filename)
        cache_name = self.cache_dir / basename

        if streamer:
            # Use streamer to save data
            streamer.create_directory(filename.parent.parent, name=filename.parent.name)
        else:
            filename.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Saving {len(self.subdomains)} subdomains to {filename}")

        with h5py.File(cache_name, "w") as f:
            # Save metadata
            metadata_group = f.create_group("metadata")
            for key, value in self.metadata.items():
                if isinstance(value, (int, float, str)):
                    metadata_group.attrs[key] = value

            # Save each subdomain
            for i, subdomain in enumerate(tqdm(self.subdomains, desc="Saving subdomains")):
                group = f.create_group(f"subdomain_{i}")

                # Save basic attributes
                group.attrs["subdomain_id"] = subdomain.subdomain_id

                # Save tensor attributes
                for key in subdomain.keys():
                    attr = subdomain[key]
                    if isinstance(attr, torch.Tensor):
                        group.create_dataset(key, data=attr.cpu().numpy())

        if streamer:
            try:
                # Upload the file to the remote server
                streamer.upload_file(local_path=cache_name, remote_path=filename, overwrite=True)
                logger.info(f"Uploaded {basename} to {filename}")
                os.remove(cache_name)
            except Exception as e:
                logger.error(
                    f"Failed to upload {filename} to {self.cache_dir}: {e}, saved locally at {cache_name}"
                )

        else:
            shutil.copy(cache_name, filename)
            os.remove(cache_name)
            logger.info(f"Saved {basename} to local cache")

    @classmethod
    def load_from_hdf5(cls, filename: Union[str, Path]) -> Tuple["DomainManager", List[Data]]:
        """
        Load subdomains from an HDF5 file.

        Args:
            filename: Path to the HDF5 file to load.

        Returns:
            Tuple of (DomainManager, List of subdomains).
        """
        filename = Path(filename)
        if not filename.exists():
            raise FileNotFoundError(f"HDF5 file not found: {filename}")

        logger.info(f"Loading subdomains from {filename}")

        # Create domain manager
        manager = cls()

        # Load data
        with h5py.File(filename, "r") as f:
            max_v = 0
            max_interpolated_v = 0
            max_p = 0
            max_interpolated_p = 0
            # Load metadata
            if "metadata" in f:
                metadata_group = f["metadata"]
                for key in metadata_group.attrs:
                    manager.metadata[key] = metadata_group.attrs[key]

            # Count subdomains
            subdomain_count = sum(1 for key in f.keys() if key.startswith("subdomain_"))

            # Load each subdomain
            subdomains = []
            for i in range(subdomain_count):
                group = f[f"subdomain_{i}"]

                # Create subdomain
                subdomain = Data()

                # Load basic attributes
                if "subdomain_id" in group.attrs:
                    subdomain.subdomain_id = group.attrs["subdomain_id"]
                else:
                    subdomain.subdomain_id = i

                # Load tensor attributes
                for key in group:
                    subdomain[key] = torch.tensor(group[key][()])
                    # by default, normalize the data if it's velocity or pressure
                    if key == "velocity":
                        max_v = max(max_v, torch.max(torch.abs(subdomain[key])))
                    elif key == "interpolated_velocity":
                        max_interpolated_v = max(
                            max_interpolated_v, torch.max(torch.abs(subdomain[key]))
                        )
                    elif key == "pressure":
                        max_p = max(max_p, torch.max(torch.abs(subdomain[key])))
                    elif key == "interpolated_pressure":
                        max_interpolated_p = max(
                            max_interpolated_p, torch.max(torch.abs(subdomain[key]))
                        )

                # if not edge_attr, create edge_attr as length of each edge
                if "edge_attr" not in subdomain:
                    edge_index = subdomain.edge_index
                    pos = subdomain.pos
                    edge_attr = torch.norm(pos[edge_index[0]] - pos[edge_index[1]], dim=1)
                    subdomain.edge_attr = edge_attr

                subdomains.append(subdomain)

            # Normalize velocity and pressure
            for subdomain in subdomains:
                if max_v > 0:
                    subdomain["velocity"] /= max_v
                if max_interpolated_v > 0:
                    subdomain["interpolated_velocity"] /= max_interpolated_v
                if max_p > 0:
                    subdomain["pressure"] /= max_p
                if max_interpolated_p > 0:
                    subdomain["interpolated_pressure"] /= max_interpolated_p
                subdomain.x = torch.cat(
                    (
                        subdomain["interpolated_velocity"],
                        subdomain["interpolated_pressure"].unsqueeze(1),
                    ),
                    dim=1,
                )
                subdomain.y = torch.cat(
                    (subdomain["velocity"], subdomain["pressure"].unsqueeze(1)), dim=1
                )

        manager.subdomains = subdomains
        manager.metadata["num_subdomains"] = len(subdomains)

        logger.info(f"Loaded {len(subdomains)} subdomains")
        return manager, subdomains


class ProgressObserver:
    """
    Class for monitoring progress of VTK filters.
    """

    def __call__(self, obj, event):
        """
        Callback for VTK filter progress events.
        """
        if not hasattr(obj, "GetProgress"):
            return

        progress = obj.GetProgress()
        if progress > 0 and progress < 1:
            logger.info(f"Processing: {progress * 100:.1f}%")


def decompose_vtu_file(
    vtu_file: Union[str, Path], num_partitions: int = 0, cache_dir: Optional[str] = None
) -> Tuple[List[Data], DomainManager]:
    """
    Decompose a VTU file into subdomains and convert to PyTorch Geometric format.

    Args:
        vtu_file: Path to the VTU file.
        num_partitions: Number of partitions to create (0 for automatic).
        cache_dir: Directory to store temporary data.

    Returns:
        Tuple of (list of subdomains, domain manager).
    """
    # Create domain manager
    manager = DomainManager(
        num_partitions=num_partitions,
        cache_dir=cache_dir,
        use_all_processors=True,
        boundary_mode="assign_to_one_region",
        preserve_partitions=True,
    )

    # Decompose VTU file
    manager.decompose_vtu(vtu_file)

    # Extract PyG subdomains
    subdomains = manager.extract_pyg_subdomains()

    return subdomains, manager


def process_subdomains(
    subdomains: List[Data],
    process_fn: Callable[[Data], Data],
    parallel: bool = True,
    num_workers: int = -1,
) -> List[Data]:
    """
    Process subdomains in parallel.

    Args:
        subdomains: List of PyTorch Geometric Data objects representing subdomains.
        process_fn: Function to apply to each subdomain.
        parallel: Whether to process subdomains in parallel.
        num_workers: Number of parallel workers (-1 for all available).

    Returns:
        List of processed PyTorch Geometric Data objects.
    """
    if not parallel:
        return [
            process_fn(subdomain) for subdomain in tqdm(subdomains, desc="Processing subdomains")
        ]

    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor

    if num_workers <= 0:
        num_workers = mp.cpu_count()

    logger.info(f"Processing {len(subdomains)} subdomains with {num_workers} workers")

    processed_subdomains = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for result in tqdm(
            executor.map(process_fn, subdomains),
            total=len(subdomains),
            desc="Processing subdomains",
        ):
            processed_subdomains.append(result)

    return processed_subdomains


def reconstruct_domain(processed_subdomains: List[Data], manager: DomainManager) -> Data:
    """
    Reconstruct a domain from processed subdomains.

    Args:
        processed_subdomains: List of processed PyTorch Geometric Data objects.
        manager: DomainManager used to create the subdomains.

    Returns:
        Reconstructed PyTorch Geometric Data object.
    """
    return manager.reconstruct_domain(processed_subdomains)
