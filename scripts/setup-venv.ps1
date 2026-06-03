# setup-venv.ps1 - Automated Python virtual environment setup for Windows
# Usage: .\scripts\setup-venv.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python version
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found in PATH" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}

# Step 2: Delete existing venv if present
Write-Host ""
Write-Host "Step 2: Checking for existing virtual environment..." -ForegroundColor Yellow
if (Test-Path ".\.venv") {
    Write-Host "  Found existing .venv folder" -ForegroundColor Yellow
    $response = Read-Host "  Delete and recreate? (y/n)"
    if ($response -eq "y") {
        Write-Host "  Removing old .venv..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force ".\.venv" -ErrorAction SilentlyContinue
        Write-Host "  Removed" -ForegroundColor Green
    } else {
        Write-Host "  Using existing .venv" -ForegroundColor Green
    }
} else {
    Write-Host "  No existing .venv found" -ForegroundColor Green
}

# Step 3: Create virtual environment
Write-Host ""
Write-Host "Step 3: Creating virtual environment (.venv)..." -ForegroundColor Yellow
try {
    python -m venv .venv
    Write-Host "  Created successfully" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Failed to create venv" -ForegroundColor Red
    Write-Host $_ -ForegroundColor Red
    exit 1
}

# Step 4: Activate virtual environment
Write-Host ""
Write-Host "Step 4: Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\Activate.ps1
    Write-Host "  Activated successfully" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Failed to activate venv" -ForegroundColor Red
    Write-Host "  Try running: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    exit 1
}

# Step 5: Verify activation
Write-Host ""
Write-Host "Step 5: Verifying activation..." -ForegroundColor Yellow
$pythonPath = python -c "import sys; print(sys.prefix)"
if ($pythonPath -like "*\.venv*") {
    Write-Host "  Using: $pythonPath" -ForegroundColor Green
} else {
    Write-Host "  WARNING: Python path doesn't contain .venv" -ForegroundColor Red
    Write-Host "  Path: $pythonPath" -ForegroundColor Red
}

# Step 6: Upgrade pip
Write-Host ""
Write-Host "Step 6: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet 2>&1 | Where-Object { $_ -notmatch "^WARNING" } | Write-Host -ForegroundColor Gray
Write-Host "  pip upgraded" -ForegroundColor Green

# Step 7: Install requirements
Write-Host ""
Write-Host "Step 7: Installing requirements..." -ForegroundColor Yellow
if (Test-Path ".\requirements.txt") {
    Write-Host "  Found requirements.txt" -ForegroundColor Green
    Write-Host "  Note: If installation fails on Windows with C++ compiler errors," -ForegroundColor Yellow
    Write-Host "  try: pip install -r requirements.txt --only-binary :all:" -ForegroundColor Yellow
    Write-Host ""

    pip install -r requirements.txt --quiet 2>&1 | Where-Object { $_ -notmatch "^WARNING" -and $_ -notmatch "^Collecting" } | Write-Host -ForegroundColor Gray
    Write-Host "  Requirements installed" -ForegroundColor Green
} else {
    Write-Host "  No requirements.txt found (skipping)" -ForegroundColor Yellow
}

# Step 8: Validate environment
Write-Host ""
Write-Host "Step 8: Validating environment..." -ForegroundColor Yellow
if (Test-Path ".\scripts\validate-env.py") {
    python scripts\validate-env.py
    Write-Host "  Validation complete" -ForegroundColor Green
} else {
    Write-Host "  validate-env.py not found (skipping)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your virtual environment is ready." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. The venv is already activated in this terminal" -ForegroundColor Gray
Write-Host "  2. In new terminals, activate with: .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "  3. Run: jupyter notebook  (to start Jupyter)" -ForegroundColor Gray
Write-Host "  4. Run: python -m pip list  (to verify packages)" -ForegroundColor Gray
Write-Host ""
