import os
import tempfile
import threading
from typing import Optional, IO, Dict
from splore_sdk.core.constants import FILE_UPLOAD_URL
from tusclient import client
from tusclient.uploader import Uploader
import mimetypes
import time


class ProgressUploader(Uploader):
    def __init__(self, *args, progress=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.uploaded_bytes = 0
        self.progress = progress

    def upload_chunk(self):
        super().upload_chunk()
        self.uploaded_bytes += self.chunk_size
        if self.progress:
            self.progress_callback(self.uploaded_bytes, self.get_file_size())

    def progress_callback(self, uploaded_bytes, total_bytes):
        # file size will be less than total_bytes as we are uploading the metadata
        # with file chunk.
        progress = min(1.00, (uploaded_bytes / total_bytes)) * 100
        print(f"Uploaded: {uploaded_bytes} / {total_bytes} bytes ({progress: .2f}%)")


class FileUploader:
    _thread_local = threading.local()

    def __init__(
        self,
        api_key: str,
        base_id: str,
        user_id: Optional[str] = None,
        auto_cleanup: bool = True,
    ):
        """
        Initializes the FileUploader instance.

        Args:
            auto_cleanup (bool): Whether to automatically clean up temporary files.
            base_id (str): The base id of the Splore base.
            api_key (str): The API key for the Splore base.
        """
        self.tus_client = client.TusClient(
            FILE_UPLOAD_URL, headers={"X-API-KEY": api_key}
        )
        # Thread-local state
        if not hasattr(self._thread_local, "temp_files"):
            self._thread_local.temp_files = []
        if not hasattr(self._thread_local, "temp_files_lock"):
            self._thread_local.temp_files_lock = threading.Lock()
        self.auto_cleanup = auto_cleanup
        self.base_id = base_id
        self.user_id = user_id

    def _get_temp_files(self):
        if not hasattr(self._thread_local, "temp_files"):
            self._thread_local.temp_files = []
        return self._thread_local.temp_files

    def _get_temp_files_lock(self):
        if not hasattr(self._thread_local, "temp_files_lock"):
            self._thread_local.temp_files_lock = threading.Lock()
        return self._thread_local.temp_files_lock

    def _is_temp_file(self, file_path: str) -> bool:
        with self._get_temp_files_lock():
            return file_path in self._get_temp_files()

    def create_temp_file_destination(self, file_extension: str) -> str:
        """
        Creates a temporary file destination path to be used for downloads.

        Args:
            file_extension (str): The desired file extension for the temporary file.

        Returns:
            str: Path to the temporary file.
        """
        print("file_extension", file_extension)
        _, extension = os.path.splitext(file_extension)
        # Get the directory where the script using the SDK is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Ensure the directory exists
        temp_dir = os.path.join(script_directory, "temp_files")
        try:
            os.makedirs(temp_dir, exist_ok=True)
        except FileExistsError:
            pass  # Directory already exists, safe to ignore
        tmp_file = tempfile.NamedTemporaryFile(
            suffix=extension, dir=temp_dir, delete=False
        )
        tmp_file.close()
        with self._get_temp_files_lock():
            self._get_temp_files().append(tmp_file.name)
        return tmp_file.name

    def generate_default_metadata(
        self, file_path: Optional[str] = None, file_stream: Optional[IO] = None
    ) -> Dict[str, str]:
        """
        Generates default metadata for the uploaded file.

        Args:
            file_path (str): The path of the file to upload.
            file_stream (IO): The file stream to upload.
        Returns:
            Dict[str, str]: Default metadata including filename, filetype, and customExtractionEnabled.
        """
        # patch to support oldr versions of mimetypes
        if not hasattr(mimetypes, "guess_file_type"):
            mimetypes.guess_file_type = mimetypes.guess_type
        if file_path:
            filename = os.path.basename(file_path)
            filetype = os.path.splitext(filename)[1][1:]
            mime_type, _ = mimetypes.guess_file_type(file_path)
        elif file_stream:
            filename = os.path.basename(file_stream.name)
            filetype = os.path.splitext(filename)[1][1:]
            mime_type, _ = mimetypes.guess_file_type(file_stream.name)
        filetype = mime_type if mime_type else filetype
        timestamp = int(time.time())
        filename = f"{timestamp}_{filename}"
        metadata = {
            "filename": filename,
            "filetype": filetype,
            "customExtractionEnabled": True,
            "isDataFile": True,
            "baseId": self.base_id,
        }
        if self.user_id:
            metadata["userId"] = self.user_id
        return metadata

    def encode_metadata(self, metadata: Dict[str, any]) -> Dict[str, str]:
        """
        Ensures metadata is in a string-encoded format suitable for upload.

        Args:
            metadata (Dict[str, any]): Metadata dictionary.

        Returns:
            Dict[str, str]: String-encoded metadata dictionary.
        """
        return {key: str(value) for key, value in metadata.items()}

    def upload_file(
        self,
        file_path: Optional[str] = None,
        file_stream: Optional[IO] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """
        Uploads a file to the TUS server using various input options.

        Args:
            file_path (Optional[str]): Local file path to upload.
            file_stream (Optional[IO]): File stream (e.g., from blob storage).
            metadata (Optional[dict]): Metadata to include with the upload.

        Returns:
            str: return file_id.

        Raises:
            ValueError: If neither file_path nor file_stream is provided.
        """
        if not (file_path or file_stream):
            raise ValueError("One of file_path or file_stream must be provided.")

        temp_file_path = None

        try:
            # Determine the file path
            if file_path:
                temp_file_path = os.path.normpath(os.path.abspath(file_path))
                default_metadata = self.generate_default_metadata(
                    file_path=temp_file_path
                )
            elif file_stream:
                temp_file_path = self.create_temp_file_destination(
                    file_extension=file_stream.name
                )
                default_metadata = self.generate_default_metadata(
                    file_stream=file_stream
                )
                self._write_stream_to_tmp(file_stream, temp_file_path)

            # Generate default metadata and merge with user-provided metadata

            if metadata and "filename" in metadata:
                timestamp = int(time.time())
                metadata["filename"] = f"{timestamp}_{metadata['filename']}"
            final_metadata = {**default_metadata, **(metadata or {})}
            encoded_metadata = self.encode_metadata(final_metadata)

            # Upload to TUS server
            chunk_size = 5 * 1024 * 1024  # 5MB chunk size
            uploader = ProgressUploader(
                client=self.tus_client,
                file_path=temp_file_path,
                metadata=encoded_metadata,
                chunk_size=chunk_size,
            )
            uploader.upload()

            # Return the file id
            url_with_file_id = uploader.url.split("+")[0]
            return url_with_file_id.split("/")[-1]

        finally:
            if (
                self.auto_cleanup
                and temp_file_path
                and self._is_temp_file(temp_file_path)
            ):
                self.cleanup_temp_files()

    def _write_stream_to_tmp(self, file_stream: IO, tmp_path: str):
        """
        Writes a file stream to a temporary file.

        Args:
            file_stream (IO): The input file stream.
            tmp_path (str): Path to the temporary file.
        """
        with open(tmp_path, "wb") as tmp_file:
            tmp_file.write(file_stream.read())

    def cleanup_temp_files(self):
        """
        Deletes all temporary files tracked by the uploader.
        """
        with self._get_temp_files_lock():
            temp_files_copy = list(self._get_temp_files())
            self._get_temp_files().clear()
        for file_path in temp_files_copy:
            try:
                os.remove(file_path)
            except OSError:
                pass
