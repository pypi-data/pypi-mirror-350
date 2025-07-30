import boto3
from urllib.parse import urlparse


def _extract_s3_bucket(s3_path: str):
    """
    Extracts the S3 bucket name from the S3 path.
    """
    parsed = urlparse(s3_path)
    return parsed.netloc


def _extract_s3_key(s3_path: str):
    """
    Extracts the S3 key from the S3 path.
    """
    parsed = urlparse(s3_path)
    return parsed.path.lstrip("/")


def download_from_s3(s3_uri: str, destination_file_path: str):
    """
    download file from s3 and put it to temp file destination.
    """
    s3 = boto3.client("s3")
    s3.download_file(
        bucket_name=_extract_s3_bucket(s3_path=s3_uri),
        key=_extract_s3_key(s3_path=s3_uri),
        file_path=destination_file_path,
    )
