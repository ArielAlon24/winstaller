import logging
import subprocess
import sys
import os

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
        logging.info(f"Installing {self.name}.")
        try:
            if self.installer.endswith(".exe"):
                subprocess.run([self.installer, "/S"], check=True)
            elif self.installer.endswith(".msi"):
                subprocess.run(["msiexec", "/i", self.installer, "/qn"], check=True)
            logging.info(f"'{self.name}' installation initiated successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Installation of '{self.name}' failed: {e}")
            raise Exception(f"Installation of '{self.name}' failed: {e}")

    def clean(self) -> None:
        logging.info(f"Cleaning {self.name} installer.")
        os.remove(self.installer)


def main():
    programs = [
        Program(
            name="PyCharm",
            url="https://download.jetbrains.com/python/pycharm-community-2023.1.exe",
            installer="pycharm-community-installer.exe",
        ),
        Program(
            name="BlueJ",
            url="https://www.bluej.org/download/files/BlueJ-windows-502.msi",
            installer="bluej_installer.msi",
        ),
        Program(
            name="Wireshark",
            url="https://2.na.dl.wireshark.org/win64/Wireshark-4.2.2-x64.exe",
            installer="wireshark_installer.exe",
        ),
    ]

    for program in programs:
        program.download()
        program.install()
        program.clean()


if __name__ == "__main__":
    main()
