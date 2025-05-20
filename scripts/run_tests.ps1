<##
    run_tests.ps1 - Execute the unit test suite for the pigen project on Windows.
    If required packages are missing the installation script is invoked.

    Usage: powershell -ExecutionPolicy Bypass -File scripts/run_tests.ps1
##>

$ErrorActionPreference = 'Stop'

if (-Not (Test-Path 'venv')) {
    Write-Output "[pigen] Virtual environment not found. Running installer..."
    .\scripts\install_windows.ps1
}

& .\venv\Scripts\Activate.ps1

$requirements = Get-Content requirements.txt
$missing = $false
foreach ($pkg in $requirements) {
    if (-not (pip show $pkg | Out-Null)) {
        $missing = $true
    }
}

if ($missing) {
    Write-Output "[pigen] Installing missing packages..."
    pip install -r requirements.txt
} else {
    Write-Output "[pigen] All requirements already satisfied."
}

Write-Output "[pigen] Running unit tests..."
python -m unittest discover -v -s tests
