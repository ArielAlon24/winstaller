Write-Host "Starting installation script."

$pythonVersion = &{python -V} 2>&1

# Attempt to get Python version
if ([string]::IsNullOrWhiteSpace($pythonVersion)) {
    Write-Host "Python is not installed, proceeding with installation..."

    # Download Python Installer
    $installerUri = "https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe"
    $installerPath = "$env:TEMP\python-3.10.9-amd64.exe"
    Invoke-WebRequest -Uri $installerUri -OutFile $installerPath -ErrorAction Stop

    # Install Python Installer
    Write-Host "Installing Python 3.10.9..."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:\Python310-64" -Wait -ErrorAction Stop
    Write-Host "Python 3.10.9 installation completed."

} else {
    Write-Host "Python is already installed: $pythonVersion"
}

# Add the python installation to the current env
$env:Path += ";C:\Python310-64"


$script = "script.py"
$executable = "C:\Python310-64\python.exe"

# Execute the Python script
Write-Host "Running script."
& $executable $script

