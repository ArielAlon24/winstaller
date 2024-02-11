import subprocess
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        logging.info(f"Package '{package}' installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install package '{package}': {e}")
        raise


def check_and_install_requests():
    try:
        import requests

        logging.info("The 'requests' package is already installed.")
    except ImportError:
        logging.info("The 'requests' package is not installed. Installing now...")
        install_package("requests")


def download_file(url, local_filename):
    import requests

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        logging.info(f"Downloaded '{local_filename}' successfully.")
    except requests.RequestException as e:
        logging.error(f"Error downloading file: {e}")
        raise e


def install_pycharm(installer_path):
    try:
        subprocess.run([installer_path, "/S"], check=True)
        logging.info("PyCharm installation initiated successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Installation failed: {e}")
        raise


if __name__ == "__main__":
    import sys

    check_and_install_requests()

    download_url = "https://download.jetbrains.com/python/pycharm-community-2023.1.exe"
    installer_name = "pycharm-community-installer.exe"

    logging.info(
        "Starting the download and installation of PyCharm Community Edition..."
    )
    try:
        logging.info("Downloading PyCharm Community Edition...")
        download_file(download_url, installer_name)

        logging.info("Installing PyCharm Community Edition...")
        install_pycharm(installer_name)

        logging.info(
            "PyCharm Community Edition installation process has been initiated."
        )
    except Exception as e:
        logging.error("An error occurred during the installation process.")
