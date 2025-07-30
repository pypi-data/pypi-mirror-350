import os
import time
import mimetypes
import tempfile
from io import BytesIO
import pytest
from unittest.mock import patch, MagicMock

from splore_sdk.utils.file_uploader import FileUploader, ProgressUploader


def test_upload_file_raises_error_no_input():
    uploader = FileUploader(
        api_key="dummy_key", base_id="dummy_base", user_id="dummy_user"
    )
    with pytest.raises(
        ValueError, match="One of file_path or file_stream must be provided."
    ):
        uploader.upload_file()


def test_upload_file_with_file_path_success(tmp_path):
    # Create a temporary file to simulate a file to upload.
    test_file = tmp_path / "test.txt"
    test_file.write_text("dummy content")
    file_path = str(test_file.resolve())

    uploader = FileUploader(
        api_key="dummy_key", base_id="dummy_base", user_id="dummy_user"
    )

    # Patch ProgressUploader in the file uploader module to avoid real upload.
    with patch(
        "splore_sdk.utils.file_uploader.ProgressUploader"
    ) as MockProgressUploader:
        mock_uploader = MagicMock()
        # Simulate an uploader URL from which the file ID is extracted.
        mock_uploader.url = "https://dummy.upload.com/file_456+extra"
        MockProgressUploader.return_value = mock_uploader

        # Call upload_file with the file_path.
        file_id = uploader.upload_file(file_path=file_path)
        # The file ID should be "file_456" as parsed by splitting the URL.
        assert file_id == "file_456"
        # Since file_path was provided, no temporary file was created or tracked.
        assert uploader._get_temp_files() == []


def test_upload_file_with_file_stream_success(tmp_path):
    # Create a fake file stream using BytesIO and assign a name.
    fake_content = b"fake file content"
    fake_stream = BytesIO(fake_content)
    fake_stream.name = "test.pdf"

    uploader = FileUploader(
        api_key="dummy_key", base_id="dummy_base", user_id="dummy_user"
    )

    # Patch _write_stream_to_tmp to prevent actual file I/O.
    with patch.object(
        uploader, "_write_stream_to_tmp", return_value=None
    ) as mock_write:
        # Patch ProgressUploader to simulate the upload process.
        with patch(
            "splore_sdk.utils.file_uploader.ProgressUploader"
        ) as MockProgressUploader:
            mock_uploader = MagicMock()
            # Set a dummy URL that will be used to extract the file ID.
            mock_uploader.url = "https://dummy.upload.com/file_789+extra"
            MockProgressUploader.return_value = mock_uploader

            file_id = uploader.upload_file(file_stream=fake_stream)
            assert file_id == "file_789"
            # Ensure that the stream-to-temp writing was called.
            mock_write.assert_called_once()
            assert uploader._get_temp_files() == []


def test_generate_default_metadata_with_file_path(tmp_path):
    # Create a dummy file.
    test_file = tmp_path / "dummy.pdf"
    test_file.write_text("dummy")
    file_path = str(test_file.resolve())

    uploader = FileUploader(
        api_key="dummy_key", base_id="dummy_base", user_id="dummy_user"
    )
    metadata = uploader.generate_default_metadata(file_path=file_path)

    # Check that filename includes a timestamp prefix.
    assert "_" in metadata["filename"]
    # The filetype should be determined via mimetypes; it might be 'application/pdf' or 'pdf'
    assert metadata["filetype"] in [
        mimetypes.guess_type(file_path)[0] or "pdf",
        "pdf",
    ]


def test_encode_metadata():
    uploader = FileUploader(
        api_key="dummy_key", base_id="dummy_base", user_id="dummy_user"
    )
    input_metadata = {"filename": 123, "custom": True, "number": 3.14}
    encoded = uploader.encode_metadata(input_metadata)
    for key, value in encoded.items():
        assert isinstance(value, str)


def test_cleanup_temp_files(tmp_path):
    uploader = FileUploader(
        api_key="dummy_key", base_id="dummy_base", user_id="dummy_user"
    )
    # Create a temporary file in tmp_path and add its path to uploader.temp_files.
    temp_file = tmp_path / "temp.txt"
    temp_file.write_text("data")
    temp_file_path = str(temp_file.resolve())
    uploader._get_temp_files().append(temp_file_path)

    # Ensure file exists.
    assert os.path.exists(temp_file_path)
    uploader.cleanup_temp_files()
    # After cleanup, the file should be removed and temp_files list cleared.
    assert not os.path.exists(temp_file_path)
    assert uploader._get_temp_files() == []
