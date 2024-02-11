import logging
import subprocess
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
            logging.error(f"Error downloading file: {e}")
            raise e

    def install(self) -> None:
        try:
            subprocess.run([self.installer, "/S"], check=True)
            logging.info("PyCharm installation initiated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Installation failed: {e}")
            raise e
