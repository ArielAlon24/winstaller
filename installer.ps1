Write-Host "Starting installation script."

# Attempt to get Python version
try {
    $pythonVersion = Invoke-Expression "python --version 2>&1"
    if ($pythonVersion -notmatch "Python") {
        throw "Python not found"
    }
    Write-Host "Python is already installed: $pythonVersion"
} catch {
    Write-Host "Python is not installed, proceeding with installation..."

    # Download Python Installer
    $installerUri = "https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe"
    $installerPath = "$env:TEMP\python-3.10.9-amd64.exe"
    Invoke-WebRequest -Uri $installerUri -OutFile $installerPath -ErrorAction Stop

    Write-Host "Installing Python 3.10.9..."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:\Python310-64" -Wait -ErrorAction Stop
    Write-Host "Python 3.10.9 installation completed."
}

# Ensure Python is added to the current session's PATH
$env:Path += ";C:\Python310-64"

# Execute the Python script
$script = "installer.py"
$executable = "C:\Python310-64\python.exe"

if (Test-Path $executable) {
    & $executable $script
} else {
    Write-Host "Error: Python executable not found."
}

