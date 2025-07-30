"""
Streaming module for efficiently accessing vascular simulation data.

This module provides functionality for streaming data from various sources,
including local files, network attached storage, and Hugging Face datasets.
"""

import json
import logging
import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from huggingface_hub import hf_hub_download, snapshot_download
from tqdm import tqdm

from .cache import CacheManager

logger = logging.getLogger(__name__)

# Optional imports for SMB support
try:
    from smb.SMBConnection import SMBConnection

    HAS_SMB = True
except ImportError:
    HAS_SMB = False

# Optional imports for synology-api
try:
    import urllib3
    from synology_api.downloadstation import DownloadStation
    from synology_api.filestation import FileStation

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    import requests

    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )

    HAS_SYNOLOGY_API = True
except ImportError:
    HAS_SYNOLOGY_API = False


class DataStreamer(ABC):
    """
    Abstract base class for data streaming functionality.

    This class provides the interface for all data streaming implementations,
    including methods for retrieving files, managing cache, and cleanup.

    Attributes:
        source_url (str): The URL or path to the data source.
        cache_dir (Path): Directory to store cached files.
        cache_manager (CacheManager): Manager for handling cache operations.
        max_cache_size (Optional[int]): Maximum cache size in bytes.
    """

    def __init__(
        self, source_url: str, cache_dir: Optional[str] = None, max_cache_size: Optional[int] = None
    ):
        """
        Initialize the data streamer.

        Args:
            source_url: URL or path to the data source.
            cache_dir: Directory to store cached files. If None, a default is used.
            max_cache_size: Maximum cache size in bytes. If None, no limit is applied.
        """
        self.source_url = source_url

        if cache_dir is None:
            home_dir = os.path.expanduser("~")
            cache_dir = os.path.join(home_dir, ".vascusim", "cache")

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache_manager = CacheManager(self.cache_dir, max_size=max_cache_size)
        self.max_cache_size = max_cache_size

    @abstractmethod
    def get_file(self, file_id: str, download_if_missing: bool = True) -> Path:
        """
        Get the path to a file, downloading it if necessary.

        Args:
            file_id: Identifier for the file to retrieve.
            download_if_missing: Whether to download the file if not in cache.

        Returns:
            Path to the requested file.

        Raises:
            FileNotFoundError: If the file is not in cache and download_if_missing is False.
            ConnectionError: If there's an issue downloading the file.
        """
        raise NotImplementedError("get_file method must be implemented in subclasses")

    @abstractmethod
    def get_metadata(self, file_id: str) -> Dict:
        """
        Get metadata for a specific file.

        Args:
            file_id: Identifier for the file whose metadata to retrieve.

        Returns:
            Dictionary containing the metadata.

        Raises:
            FileNotFoundError: If the metadata file doesn't exist.
        """
        raise NotImplementedError("get_metadata method must be implemented in subclasses")

    def cleanup(self, strategy: str = "lru") -> None:
        """
        Clean up cached files based on the specified strategy.

        Args:
            strategy: Strategy to use for cleanup.
                     "lru" - Least Recently Used
                     "all" - Remove all cached files
        """
        if strategy == "all":
            self.cache_manager.clear_all()
        else:  # Default to LRU
            self.cache_manager.cleanup()

    def __del__(self):
        """Clean up resources when the object is deleted."""
        try:
            self.cleanup()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


class LocalStreamer(DataStreamer):
    """
    Streamer for local file access.
    This class provides methods to access files stored locally on the filesystem.

    Attributes:
        source_dir: Directory containing source data.
    """

    def __init__(self, source_dir: Optional[str] = None, **kwargs):
        """
        Initialize the local streamer.

        Args:
            source_dir: Directory containing source data.
            **kwargs: Additional arguments passed to the parent class.
        """
        super().__init__(source_url="", **kwargs)
        self.source_dir = source_dir or os.getcwd()
        self.source_dir = Path(self.source_dir).resolve()

    def get_file(
        self,
        file_path: str,
        local_file_path: Optional[str] = None,
        download_if_missing: bool = True,
    ) -> Path:
        """
        Get the path to a file, downloading it if necessary.

        Args:
            file_id: Identifier for the file to retrieve.
            download_if_missing: Whether to download the file if not in cache.

        Returns:
            Path to the requested file.

        Raises:
            FileNotFoundError: If the file is not in cache and download_if_missing is False.
        """
        # Construct local path
        local_path = file_path

        # Check if file exists
        if local_path.exists():
            if local_file_path:
                # If a local file path is provided, copy the file to that location
                shutil.copy(local_path, local_file_path)
                return local_file_path

            return local_path

        if not download_if_missing:
            raise FileNotFoundError(f"File {file_path} not found in local directory")

        # Downloading is not applicable for local files
        raise ConnectionError(f"File {file_path} not found and cannot be downloaded locally")

    def get_metadata(self, file_id: str) -> Dict:
        """
        Get metadata for a specific file.

        Args:
            file_id: Identifier for the file whose metadata to retrieve.

        Returns:
            Dictionary containing the metadata.

        Raises:
            FileNotFoundError: If the metadata file doesn't exist.
        """
        # Metadata files should have the same name as the data file but with .json extension
        metadata_id = f"{os.path.splitext(file_id)[0]}.json"

        try:
            # Try to get the metadata file
            metadata_path = self.get_file(metadata_id)

            with open(metadata_path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            raise FileNotFoundError(f"Could not retrieve metadata for {file_id}: {e}")

    def list_directory(self, path: str) -> List[Dict[str, Any]]:
        """
        List contents of a directory.

        Args:
            path: Path to the directory.
        Returns:
            List of file/directory information dictionaries.
        """
        # Check if directory exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory {path} not found in local directory")

        # List files in the directory
        result = os.listdir(path)

        return result

    def get_pyg_file(
        self, file_id: str, download_if_missing: bool = True, convert_if_missing: bool = True
    ) -> Path:
        """
        Get the path to a PyG file, downloading or converting it if necessary.
        Args:
            file_id: Identifier for the file to retrieve (hash or path)
            download_if_missing: Whether to download the file if not in cache
            convert_if_missing: Whether to convert from VTU if PyG not available
        Returns:
            Path to the requested PyG file
        Raises:
            FileNotFoundError: If the file is not found and can't be downloaded/converted
        """
        # Construct local path
        local_path = self.source_dir / "processed" / file_id.lstrip("/")
        # Check if file exists
        if local_path.exists():
            return local_path
        if not download_if_missing:
            raise FileNotFoundError(f"File {file_id} not found in local directory")
        # Downloading is not applicable for local files
        raise ConnectionError(f"File {file_id} not found and cannot be downloaded locally")

    def get_domain_file(
        self, file_id: str, download_if_missing: bool = True, convert_if_missing: bool = True
    ) -> Path:
        """
        Get the path to a domain file, downloading or converting it if necessary.
        Args:
            file_id: Identifier for the file to retrieve (hash or path)
            download_if_missing: Whether to download the file if not in cache
            convert_if_missing: Whether to convert from VTU if domain not available
        Returns:
            Path to the requested domain file
        Raises:
            FileNotFoundError: If the file is not found and can't be downloaded/converted
        """
        # Construct local path
        local_path = self.source_dir / "processed" / file_id.lstrip("/")
        # Check if file exists
        if local_path.exists():
            return local_path
        if not download_if_missing:
            raise FileNotFoundError(f"File {file_id} not found in local directory")
        # Downloading is not applicable for local files
        raise ConnectionError(f"File {file_id} not found and cannot be downloaded locally")

    def create_directory(self, folder_path: str) -> None:
        """
        Create a folder in the local directory.

        Args:
            folder_path: Path to the folder to create.
        """
        # Normalize path separators
        folder_path = folder_path.replace("\\", "/")

        # Create the directory if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

    def upload_file(
        self, local_path: Union[str, Path], remote_path: str, overwrite: bool = False
    ) -> bool:
        """
        Upload a file to the local directory.

        Args:
            local_path: Path to the local file.
            remote_path: Path on the local directory where the file should be stored.
            overwrite: Whether to overwrite the file if it already exists.

        Returns:
            True if upload was successful, False otherwise.

        Raises:
            FileNotFoundError: If the local file doesn't exist.
        """
        local_path = Path(local_path)
        if not local_path.exists():
            raise FileNotFoundError(f"Local file not found: {local_path}")

        # Construct remote path
        remote_path = Path(remote_path)

        # Create parent directory if it doesn't exist
        remote_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file to the remote path
        shutil.copy(local_path, remote_path)

        return True


class NASStreamer(DataStreamer):
    """
    Enhanced Streamer for Synology NAS systems.

    This class provides methods to access files on a Synology NAS using
    the synology-api package or SMB/CIFS protocol as a fallback.

    Attributes:
        source_url (str): URL or IP address of the Synology NAS.
        source_dir: Directory containing source data.
        cache_dir (Path): Directory to store cached files.
        cache_manager (CacheManager): Manager for cached files.
        username (str, optional): Username for authentication.
        password (str, optional): Password for authentication.
        port (int): Port number for the connection.
        secure (bool): Whether to use HTTPS for API connections.
        access_mode (str): Mode to access the NAS ('api' or 'smb').
        domain (str, optional): Domain name for SMB authentication.
        client_name (str): Local NetBIOS name for SMB.
        server_name (str): Remote NetBIOS name for SMB.
        api_client: Synology API FileStation client.
        smb_conn: SMB connection object (for SMB mode).
    """

    def __init__(
        self,
        source_url: str,
        source_dir: Optional[str] = None,
        cache_dir: Optional[str] = None,
        max_cache_size: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        port: Optional[int] = None,
        secure: bool = True,
        access_mode: str = "api",
        dsm_version: int = 7,
        domain: str = "",
        client_name: str = "PythonClient",
        server_name: Optional[str] = None,
    ):
        """
        Initialize the Synology NAS streamer.

        Args:
            source_url: URL or IP address of the Synology NAS.
            source_dir: Directory containing source data.
            cache_dir: Directory to store cached files.
            max_cache_size: Maximum cache size in bytes.
            username: Username for authentication.
            password: Password for authentication.
            port: Port number for connection. Defaults to 5001 for API mode, 445 for SMB mode.
            secure: Whether to use HTTPS for API connections.
            access_mode: Access method, either 'api' or 'smb'.
            dsm_version: DSM version (6 or 7).
            domain: Domain name for SMB authentication.
            client_name: Local NetBIOS name for SMB connections.
            server_name: Remote NetBIOS name. If None, uses hostname from source_url.
        """
        super().__init__(source_url, cache_dir, max_cache_size)

        self.source_dir = source_dir
        self.username = username
        self.password = password
        self.access_mode = access_mode.lower()
        self.secure = secure
        self.dsm_version = dsm_version
        self.api_client = None  # Synology API client
        self.smb_conn = None  # SMB connection object

        # Set domain for SMB
        self.domain = domain

        # Set client and server name for SMB
        self.client_name = client_name
        if server_name:
            self.server_name = server_name
        else:
            # Extract hostname from URL
            self.server_name = self._extract_hostname(source_url)

        # Set default port based on access mode
        if port is None:
            if self.access_mode == "api":
                self.port = 5001
            else:  # SMB mode
                self.port = 445  # Default SMB port
        else:
            self.port = port

        # Verify requirements for the selected access mode
        if self.access_mode == "smb" and not HAS_SMB:
            raise ImportError("SMB access mode requires pysmb. " "Install with: pip install pysmb")
        elif self.access_mode == "api" and not HAS_SYNOLOGY_API:
            raise ImportError(
                "API access mode requires requests and synology-api. "
                "Install with: pip install requests synology-api"
            )

        # Initialize connection if credentials are provided
        if username and password:
            self.connect()

    def _extract_hostname(self, url: str) -> str:
        """Extract hostname from URL or return the input if it's already a hostname."""
        if "://" in url:
            from urllib.parse import urlparse

            return urlparse(url).netloc.split(":")[0]
        else:
            return url.split(":")[0]  # Handle case of "hostname:port"

    def _api_connect(self) -> bool:
        """
        Connect to the Synology NAS using the Synology API.

        Returns:
            bool: True if connection and authentication successful, False otherwise.
        """
        if not self.username or not self.password:
            raise ValueError("Username and password are required for API connection")

        if not HAS_SYNOLOGY_API:
            raise ImportError("Synology API access requires the synology-api package")

        try:
            # Create FileStation client
            self.api_client = FileStation(
                ip_address=self.source_url,
                port=self.port,
                username=self.username,
                password=self.password,
                secure=self.secure,
                cert_verify=False,
                dsm_version=self.dsm_version,
                debug=True,
                otp_code=None,
            )

            # Test connection
            test_result = self.api_client.get_info()
            if not test_result or "success" not in test_result or not test_result["success"]:
                logger.error(f"Failed to connect to Synology NAS: {test_result}")
                self.api_client = None
                return False

            self.sid = self.api_client._sid
            return True
        except Exception as e:
            logger.error(f"Error connecting to Synology API: {e}")
            self.api_client = None
            return False

        except Exception as e:
            logger.error(f"Error connecting to Synology API: {e}")
            return False

    def _smb_connect(self) -> bool:
        """
        Connect to the NAS using SMB/CIFS protocol.

        Returns:
            bool: True if connection successful, False otherwise.
        """
        if not HAS_SMB:
            raise ImportError("SMB support requires pysmb package")

        if not self.username:
            raise ValueError("Username is required for SMB connection")

        try:
            # Create SMB connection
            self.smb_conn = SMBConnection(
                username=self.username,
                password=self.password or "",
                my_name=self.client_name,
                remote_name=self.server_name,
                domain=self.domain,
                use_ntlm_v2=True,
                is_direct_tcp=True if self.port == 445 else False,
            )

            # Connect to server
            return self.smb_conn.connect(self.source_url, self.port)
        except Exception as e:
            logger.error(f"SMB connection error: {e}")
            return False

    def connect(self) -> bool:
        """
        Connect to the NAS using the selected access mode.

        Returns:
            bool: True if connection successful, False otherwise.
        """
        if self.access_mode == "api":
            return self._api_connect()
        elif self.access_mode == "smb":
            return self._smb_connect()
        else:
            raise ValueError(f"Unsupported access mode: {self.access_mode}")

    def disconnect(self) -> None:
        """Disconnect from the NAS."""
        if self.access_mode == "api" and self.api_client:
            try:
                # The synology-api package handles session cleanup automatically
                self.api_client = None
            except Exception as e:
                logger.warning(f"Error during API logout: {e}")

        if self.access_mode == "smb" and self.smb_conn:
            try:
                self.smb_conn.close()
            except Exception as e:
                logger.warning(f"Error closing SMB connection: {e}")
            finally:
                self.smb_conn = None

    def get_file(
        self,
        file_path: str,
        local_file_path: Optional[str] = None,
        download_if_missing: bool = True,
    ) -> Path:
        """
        Get the path to a file on the NAS, downloading it to cache if necessary.

        Args:
            file_path: Path to the file on the NAS.
            download_if_missing: Whether to download the file if not in cache.

        Returns:
            Path to the requested file in the local cache.

        Raises:
            FileNotFoundError: If the file is not in cache and download_if_missing is False.
            ConnectionError: If there's an issue connecting to the NAS.
        """
        # Construct local cache path
        file_base_name = os.path.basename(file_path)
        if not local_file_path:
            cache_path = self.cache_dir / file_base_name
        else:
            cache_path = Path(local_file_path)

        # Check if file is already in cache
        if cache_path.exists():
            # Update access time
            self.cache_manager.mark_accessed(cache_path)
            return cache_path

        if not download_if_missing:
            raise FileNotFoundError(f"File {file_path} not in cache")

        # Ensure cache directory exists
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        # Connect to NAS if not already connected
        if self.access_mode == "api" and self.api_client is None:
            if not self._api_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")
        elif self.access_mode == "smb" and self.smb_conn is None:
            if not self._smb_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")

        try:
            if self.access_mode == "api":
                self._download_file_api(file_path, cache_path)
            else:  # SMB mode
                self._download_file_smb(file_path, cache_path)

            # Register file with cache manager
            self.cache_manager.add_file(cache_path)
            return cache_path

        except Exception as e:
            # Clean up partial download if it exists
            if cache_path.exists():
                cache_path.unlink()
            raise ConnectionError(f"Failed to download {file_path}: {e}")

    def get_folder(
        self,
        folder_path: str,
        local_folder_path: Optional[str] = None,
        download_if_missing: bool = True,
    ):
        """
        Get the path to a folder on the NAS, downloading it to cache if necessary.
        Args:
            folder_path: Path to the folder on the NAS.
            download_if_missing: Whether to download the folder if not in cache.
        Returns:
            Path to the requested folder in the local cache.
        Raises:
            FileNotFoundError: If the folder is not in cache and download_if_missing is False.
            ConnectionError: If there's an issue connecting to the NAS.
        """
        # Construct local cache path
        folder_base_name = os.path.basename(folder_path)
        if not local_folder_path:
            cache_path = self.cache_dir / folder_base_name
        else:
            cache_path = Path(local_folder_path)
        # Check if folder is already in cache
        if cache_path.exists():
            # Update access time
            self.cache_manager.mark_accessed(cache_path)
            return cache_path

        if not download_if_missing:
            raise FileNotFoundError(f"Folder {folder_path} not in cache")

        # Ensure cache directory exists
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        # list all files in remote folder
        files = self.list_directory(folder_path)
        for file in files:
            # download each file
            file_path = os.path.join(str(folder_path), file)
            local_file_path = os.path.join(str(cache_path), file)
            self.get_file(file_path, local_file_path, download_if_missing)
        # Register folder with cache manager
        self.cache_manager.add_file(cache_path)
        return cache_path

    def _download_file_api(self, file_path: str, local_path: Path) -> None:
        """
        Download a file using the Synology API.

        Args:
            file_path: Path to the file on the NAS.
            local_path: Path to save the file locally.

        Raises:
            ConnectionError: If the download fails.
        """
        if not self.api_client:
            if not self._api_connect():
                raise ConnectionError("Failed to connect to Synology API")

        try:
            # Extract share name and file path
            parts = os.path.normpath(file_path).split("/", 1)
            if len(parts) == 1:
                share_name = parts[0]
                file_path = ""
            else:
                share_name, file_path = parts

            # Full path on NAS
            if not file_path:
                nas_path = f"/{share_name}"
            else:
                nas_path = f"/{share_name}/{file_path}"

            # Create parent directory if it doesn't exist
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path = local_path.parent

            # Use requests to directly download via the API
            download = self.api_client.get_file(
                path=str(nas_path), dest_path=str(local_path), mode="download"
            )

            # Ensure the file was downloaded
            if not local_path.exists() or local_path.stat().st_size == 0:
                raise FileNotFoundError(f"Downloaded file not found or empty: {local_path}")

        except Exception as e:
            raise ConnectionError(f"Failed to download file via API: {e}")

    def _download_file_smb(self, file_path: str, local_path: Path) -> None:
        """
        Download a file using SMB/CIFS protocol.

        Args:
            file_path: Path to the file on the NAS.
            local_path: Path to save the file locally.

        Raises:
            ConnectionError: If the download fails.
        """
        if not self.smb_conn or not self.smb_conn.echo(b"echo"):
            if not self._smb_connect():
                raise ConnectionError("Failed to connect to SMB server")

        try:
            # Split the path into share name and file path
            parts = file_path.strip("/").split("/", 1)
            if len(parts) == 1:
                share_name = parts[0]
                file_path = ""
            else:
                share_name, file_path = parts

            # Create local file
            with open(local_path, "wb") as file_obj:
                self.smb_conn.retrieveFile(share_name, file_path, file_obj)

        except Exception as e:
            raise ConnectionError(f"Failed to download file via SMB: {e}")

    def list_shares(self) -> List[str]:
        """
        Get a list of available shares on the NAS.

        Returns:
            List of share names.

        Raises:
            ConnectionError: If failed to connect to the NAS.
        """
        # Connect to NAS if not already connected
        if self.access_mode == "api" and self.api_client is None:
            if not self._api_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")
        elif self.access_mode == "smb" and self.smb_conn is None:
            if not self._smb_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")

        try:
            if self.access_mode == "api":
                return self._list_shares_api()
            else:  # SMB mode
                return self._list_shares_smb()
        except Exception as e:
            raise ConnectionError(f"Failed to list shares: {e}")

    def _list_shares_api(self) -> List[str]:
        """
        List shares using the Synology API.

        Returns:
            List of share names.
        """
        file_list = self.api_client.get_file_list(folder_path=self.source_dir)

        if not file_list.get("success"):
            raise ConnectionError(f"Failed to list shares: {file_list.get('error', {})}")

        return [share["name"] for share in file_list.get("data", {}).get("shares", [])]

    def _list_shares_smb(self) -> List[str]:
        """
        List shares using SMB/CIFS protocol.

        Returns:
            List of share names.
        """
        if not self.smb_conn or not self.smb_conn.echo(b"echo"):
            if not self._smb_connect():
                raise ConnectionError("Failed to connect to SMB server")

        try:
            shares = self.smb_conn.listShares()
            return [share.name for share in shares if not share.isHidden]
        except Exception as e:
            raise ConnectionError(f"Failed to list shares via SMB: {e}")

    def list_directory(self, path: str) -> List[Dict[str, Any]]:
        """
        List contents of a directory on the NAS.

        Args:
            path: Path to the directory on the NAS.

        Returns:
            List of file/directory information dictionaries.

        Raises:
            ConnectionError: If failed to connect to the NAS.
            FileNotFoundError: If the directory doesn't exist.
        """
        # Connect to NAS if not already connected
        if self.access_mode == "api" and self.api_client is None:
            if not self._api_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")
        elif self.access_mode == "smb" and self.smb_conn is None:
            if not self._smb_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")

        try:
            if self.access_mode == "api":
                return self._list_directory_api(path)
            else:  # SMB mode
                return self._list_directory_smb(path)
        except Exception as e:
            if "not found" in str(e).lower() or "no such file" in str(e).lower():
                raise FileNotFoundError(f"Directory not found: {path}")
            raise ConnectionError(f"Failed to list directory: {e}")

    def _list_directory_api(self, path: str) -> List[Dict[str, Any]]:
        """
        List directory contents using the Synology API.

        Args:
            path: Path to the directory on the NAS.

        Returns:
            List of file/directory information dictionaries.
        """
        folder_path = '"/' + str(path) + '"'  # Ensure path is properly formatted for API
        file_list = self.api_client.get_file_list(folder_path=folder_path)

        if not file_list.get("success"):
            error = file_list.get("error", {})
            if error.get("code") == 408:  # Item not found
                raise FileNotFoundError(f"Directory not found: {path}")
            raise ConnectionError(f"Failed to list directory: {error}")

        all_files_dict = file_list.get("data", {}).get("files", [])
        all_files = []
        for i in range(len(all_files_dict)):
            if all_files_dict[i]["isdir"] == False:
                all_files.append(all_files_dict[i]["name"])

        return all_files

    def _list_directory_smb(self, path: str) -> List[Dict[str, Any]]:
        """
        List directory contents using SMB/CIFS protocol.

        Args:
            path: Path to the directory on the NAS (format: share/path).

        Returns:
            List of file/directory information dictionaries.
        """
        if not self.smb_conn or not self.smb_conn.echo(b"echo"):
            if not self._smb_connect():
                raise ConnectionError("Failed to connect to SMB server")

        try:
            # Split the path into share name and directory path
            parts = path.strip("/").split("/", 1)
            if len(parts) == 1:
                share_name = parts[0]
                dir_path = ""
            else:
                share_name, dir_path = parts

            # Ensure dir_path starts with / for SMB
            if dir_path and not dir_path.startswith("/"):
                dir_path = "/" + dir_path

            # List files in the directory
            shared_files = self.smb_conn.listPath(share_name, dir_path)

            result = []
            for f in shared_files:
                # Skip '.' and '..' entries
                if f.filename in [".", ".."]:
                    continue

                file_info = {
                    "name": f.filename,
                    "path": f"{path.rstrip('/')}/{f.filename}",
                    "isdir": f.isDirectory,
                    "size": f.file_size,
                    "time": {
                        "ctime": int(f.create_time),
                        "mtime": int(f.last_write_time),
                        "atime": int(f.last_access_time),
                    },
                }
                result.append(file_info)

            return result

        except Exception as e:
            # Translate common errors
            if "No such file" in str(e):
                raise FileNotFoundError(f"Directory not found: {path}")
            raise ConnectionError(f"Failed to list directory via SMB: {e}")

    def get_metadata(self, file_id: str) -> Dict:
        """
        Get metadata for a specific file.

        Args:
            file_id: Identifier for the file whose metadata to retrieve.

        Returns:
            Dictionary containing the metadata.

        Raises:
            FileNotFoundError: If the metadata file doesn't exist.
        """
        # Metadata files should have the same name as the data file but with .json extension
        metadata_id = f"{os.path.splitext(file_id)[0]}.json"

        try:
            # Try to get the metadata file
            metadata_path = self.get_file(metadata_id)

            with open(metadata_path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            raise FileNotFoundError(f"Could not retrieve metadata for {file_id}: {e}")

    def upload_file(
        self, local_path: Union[str, Path], remote_path: str, overwrite: bool = False
    ) -> bool:
        """
        Upload a file to the NAS.

        Args:
            local_path: Path to the local file.
            remote_path: Path on the NAS where the file should be stored.
            overwrite: Whether to overwrite the file if it already exists.

        Returns:
            True if upload was successful, False otherwise.

        Raises:
            FileNotFoundError: If the local file doesn't exist.
            ConnectionError: If failed to connect to the NAS.
        """
        local_path = Path(local_path)
        if not local_path.exists():
            raise FileNotFoundError(f"Local file not found: {local_path}")

        # Connect to NAS if not already connected
        if self.access_mode == "api" and self.api_client is None:
            if not self._api_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")
        elif self.access_mode == "smb" and self.smb_conn is None:
            if not self._smb_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")

        try:
            if self.access_mode == "api":
                return self._upload_file_api(local_path, remote_path, overwrite)
            else:  # SMB mode
                return self._upload_file_smb(local_path, remote_path, overwrite)
        except Exception as e:
            raise ConnectionError(f"Failed to upload file: {e}")

    def _upload_file_api(self, local_path: Path, remote_path: str, overwrite: bool) -> bool:
        """
        Upload a file using the Synology API.

        Args:
            local_path: Path to the local file.
            remote_path: Path on the NAS where the file should be stored.
            overwrite: Whether to overwrite the file if it already exists.

        Returns:
            True if upload was successful.
        """
        remote_path_parent = Path(remote_path).parent
        remote_path_parent = str(remote_path_parent)

        data = self.api_client.upload_file(
            file_path=str(local_path),
            dest_path="/" + str(remote_path_parent),
            create_parents=True,
            overwrite=overwrite,
            progress_bar=True,
        )

        if not data.get("success"):
            error = data.get("error", {})
            if error.get("code") == 1600:  # File already exists
                if not overwrite:
                    logger.warning(f"File already exists: {remote_path}")
                    return False
            elif error.get("code") == 400:  # Invalid path
                raise FileNotFoundError(f"Invalid path: {remote_path}")
            elif error.get("code") == 401:  # Unauthorized
                raise ConnectionError("Unauthorized access to NAS")
            else:
                raise ConnectionError(f"Failed to upload file: {error}")

        return True

    def _upload_file_smb(self, local_path: Path, remote_path: str, overwrite: bool) -> bool:
        """
        Upload a file using SMB/CIFS protocol.

        Args:
            local_path: Path to the local file.
            remote_path: Path on the NAS where the file should be stored.
            overwrite: Whether to overwrite the file if it already exists.

        Returns:
            True if upload was successful.
        """
        if not self.smb_conn or not self.smb_conn.echo(b"echo"):
            if not self._smb_connect():
                raise ConnectionError("Failed to connect to SMB server")

        try:
            # Split the path into share name and file path
            parts = remote_path.strip("/").split("/", 1)
            if len(parts) == 1:
                share_name = parts[0]
                file_path = ""
            else:
                share_name, file_path = parts

            # Ensure file_path starts with / for SMB
            if file_path and not file_path.startswith("/"):
                file_path = "/" + file_path

            # Check if file exists
            try:
                file_attrs = self.smb_conn.getAttributes(share_name, file_path)
                if not overwrite:
                    logger.warning(f"File already exists: {remote_path}")
                    return False
            except Exception:
                # File doesn't exist, which is fine
                pass

            # Make sure parent directory exists
            if "/" in file_path:
                dir_path = "/".join(file_path.split("/")[:-1])
                if not dir_path:
                    dir_path = "/"

                try:
                    self.smb_conn.listPath(share_name, dir_path)
                except Exception:
                    # Directory doesn't exist, create it
                    self._create_directory_smb(f"{share_name}/{dir_path.lstrip('/')}")

            # Upload file
            with open(local_path, "rb") as file_obj:
                self.smb_conn.storeFile(share_name, file_path, file_obj)

            return True

        except Exception as e:
            raise ConnectionError(f"Failed to upload file via SMB: {e}")

    def _create_directory_api(self, path: str, name: str) -> bool:
        """
        Create a directory using the Synology API.

        Args:
            path: Path to the directory to create.

        Returns:
            True if the directory was created successfully.
        """
        folder_path = '"/' + str(path) + '"'  # Ensure path is properly formatted for API
        data = self.api_client.create_folder(
            folder_path=folder_path,
            name=name,
        )

        if not data.get("success"):
            error = data.get("error", {})
            if error.get("code") == 1602:  # Folder already exists
                return True
            raise ConnectionError(f"Failed to create directory: {error}")

        return True

    def _create_directory_smb(self, path: str) -> bool:
        """
        Create a directory using SMB/CIFS protocol.

        Args:
            path: Path to the directory to create (format: share/path).

        Returns:
            True if the directory was created successfully.
        """
        # Split the path into share name and directory path
        parts = path.strip("/").split("/", 1)
        if len(parts) == 1:
            # Can't create a top-level share
            raise ValueError(f"Cannot create top-level share: {path}")

        share_name, dir_path = parts

        # Ensure dir_path starts with /
        if not dir_path.startswith("/"):
            dir_path = "/" + dir_path

        # Create parent directories if needed
        components = dir_path.strip("/").split("/")
        current_path = ""

        for component in components:
            if not component:
                continue

            if current_path:
                current_path = f"{current_path}/{component}"
            else:
                current_path = f"/{component}"

            try:
                self.smb_conn.listPath(share_name, current_path)
            except Exception:
                # Directory doesn't exist, create it
                try:
                    self.smb_conn.createDirectory(share_name, current_path)
                except Exception as e:
                    if "NT_STATUS_OBJECT_NAME_COLLISION" not in str(
                        e
                    ):  # Ignore if dir already exists
                        raise

        return True

    def create_directory(self, folder_path: str, name: str) -> None:
        """
        Create a folder in the NAS.

        Args:
            folder_path: Path to the folder to create.
            name: Name of the folder to create.
        """
        # Connect to NAS if not already connected
        if self.access_mode == "api" and self.api_client is None:
            if not self._api_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")
        elif self.access_mode == "smb" and self.smb_conn is None:
            if not self._smb_connect():
                raise ConnectionError(f"Failed to connect to NAS at {self.source_url}")

        try:
            if self.access_mode == "api":
                return self._create_directory_api(folder_path, name)
            else:  # SMB mode
                return self._create_directory_smb(folder_path + "/" + name)
        except Exception as e:
            raise ConnectionError(f"Failed to create directory: {e}")

    def __del__(self):
        """Clean up resources."""
        try:
            self.disconnect()
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")

        # Call parent's destructor
        try:
            super().__del__()
        except:
            pass

    def get_pyg_file(
        self, file_id: str, download_if_missing: bool = True, convert_if_missing: bool = True
    ) -> Path:
        """
        Get the path to a PyG file, downloading or converting it if necessary.

        Args:
            file_id: Identifier for the file to retrieve (hash or path)
            download_if_missing: Whether to download the file if not in cache
            convert_if_missing: Whether to convert from VTU if PyG not available

        Returns:
            Path to the requested PyG file

        Raises:
            FileNotFoundError: If the file is not found and can't be downloaded/converted
        """
        # Convert VTU file ID to PyG file ID
        if file_id.endswith(".vtu"):
            base_id = file_id[:-4]
        else:
            base_id = file_id

        pyg_id = f"{base_id}.pyg"

        # Construct PyG path in cache
        pyg_dir = "processed"  # Parallel to "raw" directory
        pyg_cache_path = self.cache_dir / pyg_dir / pyg_id

        # Check if PyG file exists in cache
        if pyg_cache_path.exists():
            # Update access time
            self.cache_manager.mark_accessed(pyg_cache_path)
            return pyg_cache_path

        if not download_if_missing:
            raise FileNotFoundError(f"PyG file {pyg_id} not in cache")

        # Try to download PyG file from NAS (if it exists there)
        nas_pyg_path = f"{pyg_dir}/{pyg_id}"
        try:
            # Try to get the PyG file directly
            return self.get_file(nas_pyg_path, download_if_missing=True)
        except FileNotFoundError:
            # PyG file doesn't exist on NAS
            pass

        # If conversion is allowed, convert from VTU
        if convert_if_missing:
            # Ensure PyG cache directory exists
            pyg_cache_path.parent.mkdir(parents=True, exist_ok=True)

            # Get VTU file
            vtu_id = f"{base_id}.vtu"
            try:
                vtu_path = self.get_file(f"raw/{vtu_id}", download_if_missing=True)

                # Import the conversion function
                import torch

                from vascusim.data.conversion import vtu_to_pyg

                # Convert VTU to PyG
                data = vtu_to_pyg(str(vtu_path))

                # Save PyG file
                torch.save(data, pyg_cache_path)

                # Register with cache manager
                self.cache_manager.add_file(pyg_cache_path)

                return pyg_cache_path

            except Exception as e:
                raise FileNotFoundError(f"Failed to convert {vtu_id} to PyG: {e}")

        raise FileNotFoundError(f"PyG file {pyg_id} not available and conversion disabled")

    def get_domain_file(self, file_id: str, download_if_missing: bool = True) -> Path:
        """
        Get the path to a domain file, downloading it if necessary.

        Args:
            file_id: Identifier for the file to retrieve.
            download_if_missing: Whether to download the file if not in cache.

        Returns:
            Path to the requested domain file.

        Raises:
            FileNotFoundError: If the file is not in cache and download_if_missing is False.
            ConnectionError: If there's an issue downloading the file.
        """
        # Similar to get_file but for domain files
        # Implementation would depend on how domains are stored on the NAS
        # This would handle paths like 'domains/{file_id}.domains.h5'
        domain_path = f"processed/{file_id}.domains.h5"
        return self.get_file(domain_path, download_if_missing)


class HuggingFaceStreamer(DataStreamer):
    """
    Streamer for accessing data from Hugging Face datasets.

    This class implements the DataStreamer interface for Hugging Face,
    handling authentication and file retrieval from Hugging Face repositories.
    """

    def __init__(
        self,
        repo_id: str,
        token: Optional[str] = None,
        cache_dir: Optional[str] = None,
        max_cache_size: Optional[int] = None,
        revision: str = "main",
    ):
        """
        Initialize the Hugging Face streamer.

        Args:
            repo_id: Hugging Face repository ID.
            token: Hugging Face API token for private repositories.
            cache_dir: Directory to store cached files.
            max_cache_size: Maximum cache size in bytes.
            revision: Repository revision to use.
        """
        super().__init__(repo_id, cache_dir, max_cache_size)
        self.repo_id = repo_id
        self.token = token
        self.revision = revision
        self._file_listing = None

    def _ensure_file_listing(self) -> List[str]:
        """
        Ensure we have a listing of available files in the repository.

        Returns:
            List of available file IDs.
        """
        if self._file_listing is None:
            try:
                # Get repository info to build file listing
                # This approach avoids downloading the entire repository
                snapshot_info = snapshot_download(
                    repo_id=self.repo_id,
                    repo_type="dataset",
                    token=self.token,
                    revision=self.revision,
                    local_dir=None,  # Don't actually download, just get info
                    local_dir_use_symlinks=False,
                    max_workers=1,
                    tqdm_class=None,
                )
                self._file_listing = list(snapshot_info.keys())
            except Exception as e:
                logger.error(f"Failed to get file listing from Hugging Face: {e}")
                self._file_listing = []

        return self._file_listing

    def get_file(self, file_id: str, download_if_missing: bool = True) -> Path:
        """
        Get the path to a file from Hugging Face, downloading it to cache if necessary.

        Args:
            file_id: Identifier (relative path) for the file to retrieve.
            download_if_missing: Whether to download the file if not in cache.

        Returns:
            Path to the requested file.
        """
        cache_path = self.cache_dir / file_id

        # Check if file is already in cache
        if cache_path.exists():
            # Update access time
            self.cache_manager.mark_accessed(cache_path)
            return cache_path

        if not download_if_missing:
            raise FileNotFoundError(f"File {file_id} not in cache")

        # Ensure directory exists
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Download file from Hugging Face
            downloaded_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=file_id,
                repo_type="dataset",
                token=self.token,
                revision=self.revision,
                cache_dir=str(self.cache_dir),
                local_dir_use_symlinks=False,
            )

            # If the downloaded path is different from our expected cache path
            # (which can happen with the HF cache structure), copy or link it
            if Path(downloaded_path) != cache_path:
                # Create a symlink or copy the file
                if os.path.exists(cache_path):
                    os.remove(cache_path)

                # Try to create a symlink first
                try:
                    os.symlink(downloaded_path, cache_path)
                except (OSError, NotImplementedError):
                    # If symlink fails, copy the file
                    shutil.copy2(downloaded_path, cache_path)

            # Register file with cache manager
            self.cache_manager.add_file(cache_path)
            return cache_path

        except Exception as e:
            raise ConnectionError(f"Failed to download {file_id} from Hugging Face: {e}")

    def get_metadata(self, file_id: str) -> Dict:
        """
        Get metadata for a specific file from Hugging Face.

        Args:
            file_id: Identifier for the file whose metadata to retrieve.

        Returns:
            Dictionary containing the metadata.
        """
        # Metadata files should have the same name as the data file but with .json extension
        metadata_id = file_id.rsplit(".", 1)[0] + ".json"
        metadata_path = self.get_file(metadata_id)

        with open(metadata_path, "r") as f:
            return json.load(f)

    def list_files(self, pattern: Optional[str] = None) -> List[str]:
        """
        List all available files in the repository.

        Args:
            pattern: Optional glob pattern to filter files.

        Returns:
            List of file IDs.
        """
        files = self._ensure_file_listing()

        if pattern:
            import fnmatch

            return [f for f in files if fnmatch.fnmatch(f, pattern)]
        return files
