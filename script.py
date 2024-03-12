import logging
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
import winreg
from typing import List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def install_module(name: str) -> None:
    try:
        __import__(name)
    except ImportError:
        logging.info(f"Package '{name}' not found. Installing...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", name, "-q"], check=True
            )
            logging.info(f"Module '{name}' installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install module '{name}'. Error: {e}")
            raise


install_module("requests")
import requests

install_module("tqdm")
from tqdm import tqdm


@dataclass(slots=True)
class Uninstaller:
    name: str
    command: str

    def __post_init__(self) -> None:
        if self.command[0] == '"' and self.command[-1] == '"':
            self.command = self.command[1:-1]

    def run(self) -> None:
        logging.info(f"Uninstalling '{self.name}'...")

        if self.command.endswith(".exe"):
            cmd = [self.command, "/S"]
        elif self.command.lower().startswith("msiexec"):
            cmd = f"{self.command} /qn".split()
        else:
            logging.error(f"Unsupported uninstall command format for '{self.name}'.")
            return

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logging.info(
                f"Uninstalled '{self.name}' successfully. Output:\n{result.stdout}"
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to uninstall '{self.name}'. Error: {e}\n{e.stderr}")
            raise e


def load_uninstallers() -> List[Uninstaller]:
    registry_paths = [
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
        "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
    ]

    uninstallers = []

    for path in registry_paths:
        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ
            ) as key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                                command, _ = winreg.QueryValueEx(
                                    subkey, "UninstallString"
                                )
                                uninstallers.append(
                                    Uninstaller(name=name, command=command)
                                )
                            except FileNotFoundError:
                                pass
                    except OSError:
                        break
                    i += 1
        except FileNotFoundError:
            pass

    return uninstallers


@dataclass(slots=True)
class Program:
    CHUNK_SIZE: int = field(default=8192, init=False, repr=False)
    name: str
    url: str
    installer: Path = field(init=False)

    def __post_init__(self):
        self.installer = Path(self.url.split("/")[-1])

    def download(self) -> None:
        logging.info(f"Downloading '{self.name}'...")
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
                    logging.error("Download error, file size mismatch.")
            logging.info(f"Downloaded '{self.name}' successfully.")
        except requests.RequestException as e:
            logging.error(f"Error downloading '{self.name}'. Error: {e}")
            raise

    def install(self) -> None:
        logging.info(f"Installing '{self.name}'...")
        try:
            if self.installer.suffix == ".exe":
                subprocess.run([str(self.installer), "/S"], check=True)
            elif self.installer.suffix == ".msi":
                subprocess.run(
                    ["msiexec", "/i", str(self.installer), "/qn"], check=True
                )
            logging.info(f"Installed '{self.name}' successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Installation of '{self.name}' failed. Error: {e}")
            raise

    def clean(self) -> None:
        logging.info(f"Cleaning up installer for '{self.name}'...")
        self.installer.unlink()


def main():
    programs = [
        Program(
            name="PyCharm",
            url="https://download.jetbrains.com/python/pycharm-community-2023.1.exe",
        ),
        Program(
            name="BlueJ",
            url="https://www.bluej.org/download/files/BlueJ-windows-502.msi",
        ),
        Program(
            name="Wireshark",
            url="https://2.na.dl.wireshark.org/win64/Wireshark-latest-x64.exe",
        ),
        Program(
            name="Npcap",
            url="https://npcap.com/dist/npcap-1.79.exe",
        ),
    ]

    uninstallers = load_uninstallers()

    for program in programs:
        try:
            for uninstaller in uninstallers:
                if program.name in uninstaller.name:
                    uninstaller.run()
            program.download()
            program.install()
            program.clean()
        except KeyboardInterrupt:
            return
        except Exception:
            logging.debug("An exception encountered, contiuning to the next program.")

    modules = [
        "Pillow",
        "scapy[basic]",
        "pywin32",
        "psutil",
        "winregistry",
        "wxpython",
        "pygame",
        "matplotlib",
        "pytest",
        "pep8",
    ]

    for module in modules:
        install_module(module)


if __name__ == "__main__":
    main()
