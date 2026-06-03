# Project Bootstrap Skill

## Purpose

This skill initializes production-oriented data engineering project structures and scaffolds reusable repository foundations.

The goal is to automate repetitive project initialization tasks and enforce consistent engineering standards across projects.

---

## Responsibilities

The skill should automatically:

* Create project folder structures
* Generate standard repository files
* Initialize engineering templates
* Scaffold reusable project layouts
* Prepare source code organization
* Create documentation directories
* Generate infrastructure directories
* Prepare analytics and monitoring folders

---

## Standard Project Structure

The skill should generate structures such as:

```text
architecture/
data/
  raw/
  processed/

docs/
infra/
monitoring/
notebooks/
scripts/

src/
  producer/
  consumer/
  transformations/
  utils/
  config/

tests/
logs/
venv/
```

---

## Standard Files

The skill should generate:

* README.md
* .gitignore
* requirements.txt
* .env
* .venv
* configuration templates
* architecture placeholders
* documentation placeholders
* and other project relevant files

---

## Preferred Principles

The skill should:

* prioritize clean project organization
* support scalability and maintainability
* follow practical engineering standards
* avoid unnecessary complexity
* generate reusable structures
* support cloud-native data engineering workflows
* **integrate with python_environment and python_dependencies skills**
* **include verification steps for environment setup**
* **document troubleshooting for common issues**

---

## Standard Workflow

**Integrated Project Initialization** (coordinates with related skills):

1. **Create project folder structure** (this skill)
2. **Create virtual environment** (→ python_environment skill)
3. **Activate virtual environment** (→ python_environment skill, verify activation)
4. **Generate requirements.txt** (→ python_dependencies skill)
5. **Install dependencies** with platform-aware strategy (→ python_dependencies skill)
6. **Validate environment** (→ python_environment skill, run `validate-env.py`)
7. Generate .env.example (this skill)
8. Generate .gitignore (this skill)
9. Create initial package structure (this skill)
10. Configure project defaults (this skill)

---

## Automation Scripts

Instead of manual setup steps, use deterministic scripts:

**Windows PowerShell:**
```powershell
.\scripts\setup-venv.ps1
```

**Linux/macOS Bash:**
```bash
bash scripts/setup-venv.sh
```

**Environment Validation (All platforms):**
```bash
python scripts/validate-env.py
```

These scripts:
- Automate venv creation + activation
- Install requirements with appropriate flags
- Validate Python version and packages
- Provide clear error messages if something fails
- Work across Windows, Linux, and macOS

---

## Platform-Specific Considerations

**Windows:**
- Use `.venv` (hidden, modern convention)
- Warn about C++ compiler for certain packages (gevent, greenlet)
- Recommend `--only-binary :all:` flag as fallback
- Use PowerShell activation script

**Linux/macOS:**
- Use `.venv` (hidden, modern convention)
- Most packages have pre-built wheels available
- Use bash activation script

See `python_environment/SKILL.md` for platform-specific troubleshooting.

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Venv not created | Permission denied or disk space | Check permissions, ensure ~500MB free |
| Installation fails (Windows) | C++ compiler missing | Use `pip install --only-binary :all:` |
| "ModuleNotFoundError" | Venv not activated | Re-activate: `Activate.ps1` or `source .venv/bin/activate` |
| Wrong Python path | Venv not in use | Run `where python` or `which python` to verify |
| Packages already exist globally | Using system Python instead of venv | Verify activation, delete venv, recreate |

For detailed troubleshooting, see `python_environment/SKILL.md`.

---

## Example Use Cases

* Streaming pipelines
* AWS-based architectures
* ETL/ELT projects
* Analytics platforms
* Data lake projects
* OpenSearch dashboards
* Event-driven systems
