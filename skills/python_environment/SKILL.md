# Python Environment Skill

## Purpose

This skill automates Python environment setup and standardizes local development environments for data engineering projects.

The goal is to reduce repetitive setup tasks, ensure consistent Python project initialization, and provide **platform-specific guidance** for common installation issues.

---

## Responsibilities

The skill should automatically:

* Create Python virtual environments (use `.venv` per PEP 405)
* Initialize dependency management
* Generate requirements.txt
* Configure .gitignore for Python projects
* Create environment variable templates
* Suggest package structures
* Prepare local development environments
* **Validate Python installation and compatibility BEFORE setup**
* **Provide Windows-specific warnings** (C++ compiler for certain packages)
* **Verify venv activation** before installing packages
* **Document platform-specific fallback strategies** (e.g., `--only-binary` flag)

---

## Standard Workflow

Typical workflow:

1. **Verify Python version** (3.8+) and platform
2. **Create virtual environment** (use `.venv`)
3. **Activate virtual environment** (verify activation)
4. **Install requirements** (with platform-specific flags if needed)
5. **Validate installation** (test imports, check versions)
6. Generate requirements.txt
7. Generate .env.example
8. Create initial package structure
9. Configure project defaults

---

## Preferred Environment Standards

The skill should:

* use `.venv` virtual environment by default (PEP 405 convention, hidden)
* follow clean dependency management practices
* support scalable project structures
* prioritize reproducibility
* minimize unnecessary setup complexity
* **provide platform-aware guidance** (Windows vs Linux/macOS differences)
* **include troubleshooting for common failures**
* **separate required vs optional dependencies**

---

## Platform-Specific Guidance

### Windows (PowerShell)

**⚠️ Important: C++ Compiler Required for Some Packages**

Some Python packages (gevent, greenlet, certain numpy/scipy versions) require compilation on Windows and need **Microsoft Visual C++ 14.0 or greater**.

**Option 1: Install C++ Build Tools (Recommended)**
```powershell
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Or install via Chocolatey:
choco install visualstudio2022-workload-vctools
```

**Option 2: Use Pre-Built Wheels (Fastest)**
```powershell
pip install -r requirements.txt --only-binary :all:
# This installs only pre-compiled wheels, skipping compilation
```

**Steps:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Verify activation (prompt should show (.venv) prefix)
python -c "import sys; print(sys.prefix)"

# Install with pre-built wheels flag
pip install --upgrade pip
pip install -r requirements.txt --only-binary :all:

# Validate environment
python scripts/validate-env.py
```

**Common Issues:**
- **"Error: Microsoft Visual C++ 14.0 is required"** → Use `--only-binary :all:` flag above
- **"ModuleNotFoundError"** → Venv not activated. Re-run `Activate.ps1`
- **Packages installing to system Python** → Check activation with `where python`

---

### Linux/macOS (Bash)

**Steps:**
```bash
python3 -m venv .venv
source .venv/bin/activate

# Verify activation (prompt should show (.venv) prefix)
python -c "import sys; print(sys.prefix)"

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Validate environment
python scripts/validate-env.py
```

**Common Issues:**
- **"python: command not found"** → Use `python3` explicitly
- **"Permission denied"** → May need `chmod +x .venv/bin/activate`
- **"ModuleNotFoundError"** → Check activation with `which python`

---

## Verification Checklist

After setup, confirm:

1. **Python version is 3.8+**
   ```powershell
   python --version
   ```

2. **Virtual environment is active**
   ```powershell
   python -c "import sys; print(sys.prefix)"  # Should show .venv path
   ```

3. **All required packages installed**
   ```powershell
   python scripts/validate-env.py
   ```

4. **Using correct Python**
   ```powershell
   where python  # Should show .venv\Scripts\python.exe (Windows)
   which python  # Should show .venv/bin/python (Linux/macOS)
   ```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "ModuleNotFoundError: No module named X" | Venv not activated or packages not installed | Re-run Activate.ps1/activate, then `pip install -r requirements.txt` |
| "Microsoft Visual C++ 14.0 is required" | Packages need compilation on Windows | Run `pip install -r requirements.txt --only-binary :all:` |
| Prompt doesn't show (.venv) | Activation failed | Try: Deactivate, delete .venv, recreate with `python -m venv .venv`, reactivate |
| "pip: command not found" | pip not in PATH | Upgrade pip: `python -m pip install --upgrade pip` |
| Requirements with gevent/greenlet | Windows C++ compiler missing | Use pre-built wheels (see Windows section above) |

---

## Using Automation Scripts

Instead of manual steps, use deterministic scripts:

**Windows:**
```powershell
.\scripts\setup-venv.ps1
```

**Linux/macOS:**
```bash
bash scripts/setup-venv.sh
```

These scripts automate all steps above and include verification.

---

## Example Use Cases

* Streaming applications
* Lambda development
* Analytics projects
* Machine learning experiments
* AWS SDK development
* OpenSearch integrations
* Data pipeline development
