#!/usr/bin/env python
"""
validate-env.py - Validate Python virtual environment setup
Checks: Python version, venv activation, installed packages
Usage: python scripts/validate-env.py
"""

import sys
import subprocess
from pathlib import Path

def print_header(text):
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}")

def check_python_version():
    """Verify Python 3.8 or higher."""
    print("\n1. Checking Python version...")
    major, minor = sys.version_info[:2]
    version_str = f"{major}.{minor}.{sys.version_info[2]}"

    if major < 3 or (major == 3 and minor < 8):
        print(f"   ERROR: Python {version_str} is too old (need 3.8+)")
        return False

    print(f"   OK: Python {version_str}")
    return True

def check_venv_active():
    """Verify virtual environment is activated."""
    print("\n2. Checking virtual environment activation...")

    # Check if venv is active by looking at sys.prefix
    venv_path = Path(sys.prefix)
    is_venv = (venv_path / "pyvenv.cfg").exists()

    if not is_venv:
        print(f"   ERROR: Virtual environment not active")
        print(f"   Using system Python at: {sys.prefix}")
        print(f"   Please activate: source .venv/bin/activate (Linux/macOS)")
        print(f"     or            .\.venv\Scripts\Activate.ps1 (Windows)")
        return False

    if ".venv" not in str(sys.prefix):
        print(f"   WARNING: Not using .venv folder")
        print(f"   Using: {sys.prefix}")
    else:
        print(f"   OK: {sys.prefix}")

    return True

def check_installed_packages():
    """Check if critical packages are installed."""
    print("\n3. Checking installed packages...")

    critical_packages = {
        "pandas": "Data manipulation",
        "numpy": "Numerical computing",
        "sklearn": "Machine learning (scikit-learn)",
        "xgboost": "Gradient boosting",
        "boto3": "AWS SDK",
        "sagemaker": "AWS SageMaker",
    }

    missing = []
    for pkg, desc in critical_packages.items():
        try:
            __import__(pkg)
            print(f"   OK: {pkg:20s} - {desc}")
        except ImportError:
            print(f"   MISSING: {pkg:20s} - {desc}")
            missing.append(pkg)

    if missing:
        print(f"\n   To install missing packages:")
        print(f"   pip install -r requirements.txt")
        if any(pkg in ["gevent", "greenlet"] for pkg in missing):
            print(f"   Or on Windows (if C++ compiler issues):")
            print(f"   pip install -r requirements.txt --only-binary :all:")
        return False

    return True

def check_optional_packages():
    """Check for optional packages."""
    print("\n4. Checking optional packages...")

    optional = {
        "jupyter": "Jupyter notebooks",
        "matplotlib": "Data visualization",
        "seaborn": "Statistical visualization",
        "shap": "Model explainability",
    }

    for pkg, desc in optional.items():
        try:
            __import__(pkg)
            print(f"   OK: {pkg:20s} - {desc}")
        except ImportError:
            print(f"   MISSING: {pkg:20s} - {desc} (optional)")

    return True

def main():
    print_header("Python Environment Validation")

    checks = [
        check_python_version,
        check_venv_active,
        check_installed_packages,
        check_optional_packages,
    ]

    results = [check() for check in checks]

    # Summary
    print_header("Validation Summary")

    if all(results):
        print("\nAll critical checks passed!")
        print("\nYour environment is ready to use:")
        print("  - Run: jupyter notebook")
        print("  - Run: python notebooks/01_eda.ipynb")
        print("  - Run: pip list  (to see all packages)")
        sys.exit(0)
    else:
        print("\nSome checks failed. Please see errors above.")
        print("\nCommon solutions:")
        print("  1. Not in virtual environment?")
        print("     Activate: source .venv/bin/activate")
        print("     Or:       .\.venv\Scripts\Activate.ps1")
        print("\n  2. Missing packages?")
        print("     Install: pip install -r requirements.txt")
        print("\n  3. Compilation errors on Windows?")
        print("     Use: pip install -r requirements.txt --only-binary :all:")
        sys.exit(1)

if __name__ == "__main__":
    main()
