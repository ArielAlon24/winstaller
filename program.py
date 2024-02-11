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

try:
    from tqdm import tqdm
except ImportError:
    logging.info("Package 'tqdm' not found. Installing...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "tqdm"], check=True)
        logging.info("'tqdm' was installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install package 'tqdm': {e}")
        sys.exit(1)

    from tqdm import tqdm


class Program:
    CHUNK_SIZE = 8192

    def __init__(self, name: str, url: str, installer: str) -> None:
        self.name = name
        self.url = url
        self.installer = installer

    def download(self) -> None:
        logging.info(f"Downloading {self.name}.")
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                total_size_in_bytes = int(r.headers.get("content-length", 0))
                progress_bar = tqdm(
                    total=total_size_in_bytes, unit="iB", unit_scale=True
                )
                with open(self.installer, "wb") as f:
                    for chunk in r.iter_content(chunk_size=self.CHUNK_SIZE):
                        progress_bar.update(len(chunk))
                        f.write(chunk)
                progress_bar.close()
                if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                    logging.error("ERROR, something went wrong")
            logging.info(f"Downloaded '{self.name}' successfully.")
        except requests.RequestException as e:
            logging.error(f"Error downloading '{self.name}': {e}")
            raise Exception(f"Error downloading '{self.name}': {e}")

    def install(self) -> None:
        self.download()
        logging.info(f"Installing {self.name}.")
        try:
            subprocess.run([self.installer, "/S"], check=True)
            logging.info(f"'{self.name}' installation initiated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Installation of '{self.name}' failed: {e}")
            raise Exception(f"Installation of '{self.name}' failed: {e}")

    def __repr__(self) -> str:
        return f"Program(name={self.name}, url={self.url}, installer={self.installer})"
