# Python Environment Skill

## Purpose

This skill automates Python environment setup and standardizes local development environments for data engineering projects.

The goal is to reduce repetitive setup tasks and ensure consistent Python project initialization.

---

## Responsibilities

The skill should automatically:

* Create Python virtual environments
* Initialize dependency management
* Generate requirements.txt
* Configure .gitignore for Python projects
* Create environment variable templates
* Suggest package structures
* Prepare local development environments
* Validate Python installation and compatibility

---

## Standard Workflow

Typical workflow:

1. Create virtual environment
2. Activate virtual environment
3. Generate requirements.txt
4. Generate .env.example
5. Install base dependencies
6. Create initial package structure
7. Configure project defaults

---

## Preferred Environment Standards

The skill should:

* use virtual environments by default
* follow clean dependency management practices
* support scalable project structures
* prioritize reproducibility
* minimize unnecessary setup complexity

---

## Example Commands

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Example Use Cases

* Streaming applications
* Lambda development
* Analytics projects
* Machine learning experiments
* AWS SDK development
* OpenSearch integrations
* Data pipeline development
