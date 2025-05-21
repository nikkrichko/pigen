<##
    install_windows.ps1 - Setup Python virtual environment and install dependencies
    for the pigen project on Windows using PowerShell.

    Usage: powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1
##>

$ErrorActionPreference = 'Stop'

Write-Output "[pigen] Creating Python virtual environment..."

if (-Not (Test-Path 'venv')) {
    python -m venv venv
    Write-Output "[pigen] Virtual environment created."
} else {
    Write-Output "[pigen] Virtual environment already exists."
}

# Activate the environment for the current script scope
& .\venv\Scripts\Activate.ps1

Write-Output "[pigen] Installing dependencies from requirements.txt..."
pip install --upgrade -r requirements.txt

Write-Output "[pigen] Environment setup complete."
