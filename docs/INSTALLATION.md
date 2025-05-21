# Installation Guide

This document explains how to set up the `pigen` project using the provided
helper scripts. The scripts create a Python virtual environment and install all
required packages listed in `requirements.txt`.

## Linux/macOS

Run the shell script from the repository root:

```bash
./scripts/install_linux.sh
```

This creates a `venv` folder and installs the dependencies inside it.
The requirements file includes optional OpenTelemetry packages that enable
tracing support when configured.

## Windows

Execute the PowerShell script in a terminal with sufficient privileges:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1
```

A `venv` directory is created and all requirements are installed.
Like the Linux script, it also installs the optional OpenTelemetry packages.

## Preflight Check

Run the preflight script to verify that dependencies and environment variables
are correctly configured.

- **Linux/macOS**
  ```bash
  ./scripts/preflight.sh
  ```
- **Windows**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/preflight.ps1
  ```
This step is optional because `pg.py` executes the same validation on startup.

## Running the Tests

After installation you can run the offline test suite.

- **Linux/macOS**
  ```bash
  ./scripts/run_tests.sh
  ```
- **Windows**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/run_tests.ps1
  ```

The scripts ensure all packages are available before executing the tests.
