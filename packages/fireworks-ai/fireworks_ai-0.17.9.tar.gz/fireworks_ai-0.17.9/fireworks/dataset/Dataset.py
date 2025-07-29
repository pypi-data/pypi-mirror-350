import io
import json
import logging
import os
from functools import cache as sync_cache
from fireworks._util import make_valid_resource_name
import httpx
import atexit
from typing import Optional, Union, BinaryIO
from fireworks.control_plane.generated.protos.gateway import (
    CreateDatasetRequest,
    ListDatasetsRequest,
    Dataset as DatasetProto,
)
from fireworks.control_plane.generated.protos_grpcio.gateway.dataset_pb2 import (
    Dataset as SyncDataset,
    ListDatasetsRequest as SyncListDatasetsRequest,
    CreateDatasetRequest as SyncCreateDatasetRequest,
)
import mmh3


from fireworks.gateway import Gateway

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False  # Prevent duplicate logs

if os.environ.get("FIREWORKS_SDK_DEBUG"):
    logger.setLevel(logging.DEBUG)


class Dataset:
    def __init__(
        self,
        api_key: Optional[str] = None,
        path: Optional[str] = None,
        data: Optional[Union[str, list]] = None,
        _internal=False,
    ):
        """
        A "smart" Dataset class that helps developers upload datasets and
        fine-tune on Fireworks. It has the following features:

        1. Works nicely with the `fireworks.llm.LLM` class.
        2. Automatically names dataset based on the contents of the dataset and the filename of the file if provided.
        3. Automatically uploads dataset to Fireworks if it doesn't already exist.

        To instantiate a Dataset, use the `from_*` class methods:
        - `from_dict(data: list)`
        - `from_file(path: str)`
        - `from_string(data: str)`

        Args:
            path: Path to the local directory containing the dataset.
            data: Data to be uploaded to the dataset. Can be a string in JSONL format with OpenAI chat completion
                  message compatible JSON, or a list of OpenAI chat completion message compatible objects.
        TODO: support various remote paths to cloud storage.
        """
        if not _internal:
            raise ValueError(
                "Dataset is not meant to be instantiated directly, use Dataset.from_dict() or Dataset.from_file() instead"
            )
        self._data: Optional[str] = None
        self._path: Optional[str] = None
        self._gateway = Gateway(api_key=api_key)
        self._file_stream: Optional[BinaryIO] = None
        atexit.register(self._gateway._channel.close)

        if path and data:
            raise ValueError("Cannot provide both path and data")
        if not path and not data:
            raise ValueError("Must provide either path or data")
        if path and not path.endswith(".jsonl"):
            raise ValueError("File must be a JSONL file")

        if path:
            self._path = path
        elif isinstance(data, list):
            # Convert list to newline delimited JSON string
            self._data = "\n".join(json.dumps(item) for item in data)
        elif isinstance(data, str):
            self._data = data

    @classmethod
    def from_string(cls, data: str):
        return cls(data=data, _internal=True)

    @classmethod
    def from_dict(cls, data: list):
        return cls(data=data, _internal=True)

    @classmethod
    def from_file(cls, path: str):
        if not path.endswith(".jsonl"):
            raise ValueError("File must be a JSONL file")
        return cls(path=path, _internal=True)

    def get(self):
        """
        Get this dataset from Fireworks by hash
        - If filename of dataset changes, it still matches the hash
        """
        request = SyncListDatasetsRequest(page_size=1000)
        datasets = self._gateway.list_datasets_sync(request)
        for dataset in datasets:
            if dataset.name.endswith(self.name):
                logger.debug(f"Found dataset with matching hash: {dataset.name}")
                return dataset
        logger.debug(f"No dataset found with matching hash: {hash(self)}")
        return None

    def sync(self):
        """
        Upload this dataset to Fireworks if it doesn't already exist.
        """
        # check if dataset exists by hash
        dataset = self.get()
        if dataset:
            logger.debug(f"Dataset already exists: {dataset.name}, no need to upload")
            return
        logger.debug(f"No dataset found with matching hash: {hash(self)}, creating new dataset")
        dataset = SyncDataset(
            format=self._detect_dataset_format(),
            example_count=min(self._line_count(), 50_000_000),
        )
        # upload dataset since it doesn't exist
        logger.debug(f"Creating dataset: {self.name}")
        request = SyncCreateDatasetRequest(dataset=dataset, dataset_id=self.name)
        dataset = self._gateway.create_dataset_sync(request)
        logger.debug(f"Dataset created: {dataset.name}")
        logger.debug(f"Uploading dataset: {self.name}")
        filename_to_size = {self.filename(): self.file_size()}
        signed_urls = self._gateway.get_dataset_upload_endpoint_sync(self.name, filename_to_size)
        self._upload_file_using_signed_url(signed_urls[self.filename()])
        logger.debug(f"Dataset uploaded: {self.name}")
        self._gateway.validate_dataset_sync(self.name)
        logger.debug(f"Dataset validated: {self.name}")

    def _upload_file_using_signed_url(self, signed_url: str) -> None:
        """
        Upload a file to a signed URL using async streaming to avoid loading the entire file into memory.

        Args:
            signed_url: The signed URL to upload the file to.
        """
        logger.debug(f"Uploading file to signed URL: {signed_url}")

        file = self._get_stream()
        try:
            # Get file size for content length
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)

            # Prepare the HTTP request
            headers = {
                "Content-Type": "application/octet-stream",
                "X-Goog-Content-Length-Range": f"{size},{size}",
            }

            # Upload the file with streaming
            with httpx.Client() as client:
                response = client.put(signed_url, content=file, headers=headers)
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to upload file: {response.status_code} - {response.text}")

            logger.debug("File upload completed successfully")
        finally:
            file.close()

    def filename(self) -> str:
        """
        Returns the filename of the dataset if path is provided, otherwise returns "inmemory"
        to indicate this dataset was created from an in-memory data structure rather than a file.
        """
        if self._path:
            return os.path.basename(self._path)
        return "inmemory.jsonl"

    @property
    def name(self):
        """
        Generates a name for this dataset in the form of "dataset-{hash(self)}-{filename}"
        """
        return f"dataset-{hash(self)}-{make_valid_resource_name(self.filename())}"

    @sync_cache
    def id(self):
        return self.construct_id(self._gateway.account_id(), self.name)

    @classmethod
    def construct_id(cls, account_id: str, name: str):
        if name.startswith("accounts/"):
            return name
        return f"accounts/{account_id}/datasets/{name}"

    @property
    def stream(self) -> BinaryIO:
        """
        Returns a cached file-like object for the dataset content.
        For backward compatibility - prefer using get_stream() with a context manager.
        """
        if self._file_stream is not None and not self._file_stream.closed:
            self._file_stream.seek(0)
            return self._file_stream

        self._file_stream = self._get_stream()
        return self._file_stream

    def _line_count(self) -> int:
        """
        Returns the number of lines in the dataset
        """
        with self._get_stream() as stream:
            count = 0
            for _ in stream:
                count += 1
            return count

    def _detect_dataset_format(self) -> SyncDataset.Format:
        """
        Detects the format of the dataset by examining its content.

        Returns:
            A string representing the dataset format:
            - "CHAT" for chat completion format
            - "COMPLETION" for completion format
            - "FORMAT_UNSPECIFIED" if the format cannot be determined
        """

        try:
            with self._get_stream() as file:
                for line in file:
                    try:
                        data = json.loads(line.decode("utf-8"))

                        # Check for completion format (prompt + completion)
                        if "prompt" in data and "completion" in data:
                            return SyncDataset.Format.COMPLETION

                        # Check for chat format (messages array)
                        if "messages" in data and isinstance(data["messages"], list) and len(data["messages"]) > 0:
                            return SyncDataset.Format.CHAT

                        # If we reach here, the format doesn't match either completion or chat
                        return SyncDataset.Format.FORMAT_UNSPECIFIED
                    except json.JSONDecodeError:
                        return SyncDataset.Format.FORMAT_UNSPECIFIED

                # If we've read the entire file without determining a format, it's unspecified
                return SyncDataset.Format.FORMAT_UNSPECIFIED
        except Exception as e:
            logger.error(f"Error detecting dataset format: {e}")
            return SyncDataset.Format.FORMAT_UNSPECIFIED

    def _get_stream(self) -> BinaryIO:
        """
        Returns a fresh file-like object for the dataset content.
        For in-memory data, returns a BytesIO object.
        For file paths, returns a file object.
        This is intended to be used with a context manager to ensure proper cleanup.
        """
        if self._data:
            return io.BytesIO(self._data.encode("utf-8"))
        elif self._path:
            return open(self._path, "rb")
        else:
            raise ValueError("No data or path provided")

    def file_size(self) -> int:
        """
        Returns the size of the dataset in bytes without reading the entire file
        """
        # Use optimized path for files since we can get size without reading
        if self._path:
            return os.path.getsize(self._path)

        # For in-memory data, get the size from the stream
        with self._get_stream() as stream:
            stream.seek(0, io.SEEK_END)
            size = stream.tell()
            return size

    def __hash__(self) -> int:
        """
        Computes a hash of the dataset contents
        """
        # Read the entire file content for hashing
        content = self.read()
        # Ensure the hash is positive by using the unsigned value (& with MAXINT)
        return mmh3.hash(content) & 0x7FFFFFFF

    def delete(self):
        """
        Delete this dataset from Fireworks
        """
        # if dataset doesn't exist, don't delete
        dataset = self.get()
        if not dataset:
            logger.debug(f"Dataset does not exist: {self.name}, no need to delete")
            return
        self._gateway.delete_dataset_sync(self.name)

    def read(self, size: Optional[int] = None) -> bytes:
        """
        Read content from the dataset

        Args:
            size: Number of bytes to read, or None to read the entire file
                 (use cautiously with large files)

        Returns:
            The content as bytes
        """
        with self._get_stream() as stream:
            if size is not None:
                return stream.read(size)
            return stream.read()
