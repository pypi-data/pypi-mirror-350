from urllib.parse import urlparse
import requests
from splore_sdk.core.exceptions import APIError
from splore_sdk.core.logger import sdk_logger


def is_valid_url(self, url: str):
    """
    Checks if a string is a valid URL.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def download_remote_file(self, url: str, destination: str):
    """
    Downloads a remote file to a local destination.
    """
    try:
        sdk_logger.info(f"Downloading remote file: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        sdk_logger.error(f"Error downloading remote file: {e}")
        raise APIError(f"Error downloading remote file: {e}")
