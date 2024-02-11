import logging
import subprocess
import sys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    import requests
except ImportError:
    logging.info("Package 'requests' not found. Installing...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        logging.info("Requests was installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install package 'requests': {e}")
        sys.exit(1)

    import requests


class Program:
    CHUNK_SIZE = 8192

    def __init__(self, name: str, url: str, installer: str) -> None:
        self.name = name
        self.url = url
        self.installer = installer

    def download(self) -> None:
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                with open(self.installer, "wb") as f:
                    for chunk in r.iter_content(chunk_size=self.CHUNK_SIZE):
                        f.write(chunk)
            logging.info(f"Downloaded '{self.name}' successfully.")
        except requests.RequestException as e:
            logging.error(f"Error downloading '{self.name}': {e}")
            raise Exception(f"Error downloading '{self.name}': {e}")

    def install(self) -> None:
        try:
            subprocess.run([self.installer, "/S"], check=True)
            logging.info(f"'{self.name}' installation initiated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Installation of '{self.name}' failed: {e}")
            raise Exception(f"Installation of '{self.name}' failed: {e}")

    def __repr__(self) -> str:
        return f"Program(name={self.name}, url={self.url}, installer={self.installer})"
