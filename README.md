# Winstaller

A script that automatically installs / updates various software for Windows and Python Libraries.

## Usage

Run the following command, inside an editable directory (`C:\` for example)

```ps1
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ArielAlon24/winstaller/main/winstaller.bat" -OutFile "winstaller.bat"; .\"winstaller.bat"
```

## Installations

### Software

| software                     | source                                                             |
| ---------------------------- | ------------------------------------------------------------------ |
| Python 3.10.9                | https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe   |
| PyCharm Community            | https://download.jetbrains.com/python/pycharm-community-2023.1.exe |
| BlueJ                        | https://www.bluej.org/download/files/BlueJ-windows-502.msi         |
| WireShark                    | https://2.na.dl.wireshark.org/win64/Wireshark-latest-x64.exe       |
| Npcap (Wireshark Dependency) | https://npcap.com/dist/npcap-0.96.exe                              |

### Libraries

- Pillow
- scapy[basic]
- pywin32
- psutil
- winregistry
- wxpython
- pygame
- matplotlib
- pytest
- pep8
