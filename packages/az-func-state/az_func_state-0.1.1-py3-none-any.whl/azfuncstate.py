from datetime import datetime, timezone
from typing import Optional

from azure.storage.blob import BlobServiceClient


class AzFuncState:
    """Azure Function state storage using Blob Storage as backend.

    Provides key-value storage with additional time marker functionality.
    Automatically handles container creation if it doesn't exist.

    Parameters
    ----------
    connection_string : str
        Azure Storage account connection string
    container_name : str
        Name of the container to use for storage
    """

    def __init__(self, connection_string: str, container_name: str):
        """Initialize the Azure Function state storage.

        Parameters
        ----------
        connection_string : str
            Azure Storage account connection string
        container_name : str
            Name of the container to use for storage

        Raises
        ------
        RuntimeError
            If container initialization fails
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container_name = container_name
        self.container_client = self.blob_service_client.get_container_client(
            container_name
        )

        # Create container if it doesn't exist
        try:
            if not self.container_client.exists():
                self.container_client.create_container()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize container: {str(e)}")

    def set(self, key: str, value: str) -> None:
        """Store a key-value pair as a blob.

        Parameters
        ----------
        key : str
            The key to store the value under
        value : str
            The value to store
        """
        blob_client = self.container_client.get_blob_client(key)
        blob_client.upload_blob(value, overwrite=True)

    def get(self, key: str) -> Optional[str]:
        """Retrieve a value by key.

        Parameters
        ----------
        key : str
            The key to retrieve

        Returns
        -------
        Optional[str]
            The stored value, or None if key doesn't exist
        """
        blob_client = self.container_client.get_blob_client(key)
        try:
            download_stream = blob_client.download_blob()
            return download_stream.readall().decode("utf-8")
        except Exception:
            return None

    def set_time_marker(self, key: str) -> None:
        """Store current UTC timestamp under the given key.

        Parameters
        ----------
        key : str
            The key to store the timestamp under
        """
        self.set(key=key, value=datetime.now(timezone.utc).isoformat())

    def get_time_marker(self, key: str) -> datetime:
        """Retrieve a stored timestamp.

        Parameters
        ----------
        key : str
            The key where timestamp is stored

        Returns
        -------
        datetime
            The stored timestamp

        Raises
        ------
        ValueError
            If no timestamp exists for the given key
        """
        value = self.get(key=key)
        if value is None:
            raise ValueError("No time marker found")

        return datetime.fromisoformat(value)
