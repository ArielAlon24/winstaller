@echo off

:: Check if Python is installed by attempting to run it
python --version
if %ERRORLEVEL% neq 0 goto installPython
goto runScript

:installPython
echo Python is not installed. Installing Python...

:: Download Python installer (adjust URL for specific version)
curl -L "https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe" -o python-installer.exe

:: Run the installer silently, add Python to PATH, and install pip
start /wait "" python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Clean up the installer
del /f /q python-installer.exe

echo Python has been installed.

goto runScript

:runScript
echo Downloading Python script...

:: Download the Python script
curl -L "https://raw.githubusercontent.com/ArielAlon24/winstaller/main/script.py" -o "script.py"

echo Running Python script...
python yourScript.py

