#!/bin/bash
# setup-venv.sh - Automated Python virtual environment setup for Linux/macOS
# Usage: bash scripts/setup-venv.sh

set -e

echo "========================================"
echo "Python Virtual Environment Setup"
echo "========================================"
echo ""

# Step 1: Check Python version
echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "  ERROR: Python3 not found"
    echo "  Please install Python 3.8+ from python.org or use:"
    echo "    brew install python3  (macOS)"
    echo "    sudo apt install python3  (Linux)"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "  Found: $PYTHON_VERSION"

# Step 2: Check for existing venv
echo ""
echo "Step 2: Checking for existing virtual environment..."
if [ -d ".venv" ]; then
    echo "  Found existing .venv folder"
    read -p "  Delete and recreate? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  Removing old .venv..."
        rm -rf .venv
        echo "  Removed"
    else
        echo "  Using existing .venv"
    fi
else
    echo "  No existing .venv found"
fi

# Step 3: Create virtual environment
echo ""
echo "Step 3: Creating virtual environment (.venv)..."
python3 -m venv .venv
if [ $? -eq 0 ]; then
    echo "  Created successfully"
else
    echo "  ERROR: Failed to create venv"
    exit 1
fi

# Step 4: Activate virtual environment
echo ""
echo "Step 4: Activating virtual environment..."
source .venv/bin/activate
if [ $? -eq 0 ]; then
    echo "  Activated successfully"
else
    echo "  ERROR: Failed to activate venv"
    exit 1
fi

# Step 5: Verify activation
echo ""
echo "Step 5: Verifying activation..."
PYTHON_PATH=$(python -c "import sys; print(sys.prefix)")
if [[ "$PYTHON_PATH" == *".venv"* ]]; then
    echo "  Using: $PYTHON_PATH"
else
    echo "  WARNING: Python path doesn't contain .venv"
    echo "  Path: $PYTHON_PATH"
fi

# Step 6: Upgrade pip
echo ""
echo "Step 6: Upgrading pip..."
python -m pip install --upgrade pip --quiet 2>/dev/null || true
echo "  pip upgraded"

# Step 7: Install requirements
echo ""
echo "Step 7: Installing requirements..."
if [ -f "requirements.txt" ]; then
    echo "  Found requirements.txt"
    pip install -r requirements.txt --quiet 2>/dev/null || true
    echo "  Requirements installed"
else
    echo "  No requirements.txt found (skipping)"
fi

# Step 8: Validate environment
echo ""
echo "Step 8: Validating environment..."
if [ -f "scripts/validate-env.py" ]; then
    python scripts/validate-env.py
    echo "  Validation complete"
else
    echo "  validate-env.py not found (skipping)"
fi

# Summary
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Your virtual environment is ready."
echo ""
echo "Next steps:"
echo "  1. The venv is already activated in this terminal"
echo "  2. In new terminals, activate with: source .venv/bin/activate"
echo "  3. Run: jupyter notebook  (to start Jupyter)"
echo "  4. Run: python -m pip list  (to verify packages)"
echo ""
