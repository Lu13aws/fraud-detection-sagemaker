# Dependency Management Skill

## Purpose

This skill standardizes Python dependency management and library installation workflows for data engineering and cloud engineering projects.

The goal is to automate repetitive package setup tasks, reduce dependency-related issues, and maintain clean, reproducible development environments.

---

## Responsibilities

The skill should automatically:

* Suggest appropriate libraries based on project type
* Generate requirements.txt files
* Recommend minimal and production-oriented dependencies
* Avoid unnecessary package bloat
* Detect common dependency conflicts
* Organize dependencies logically
* Standardize installation workflows
* Support reproducible environments

---

## Windows-Specific Package Warnings

⚠️ **These packages require Microsoft Visual C++ 14.0+ on Windows:**

* `gevent` — asyncio library (pulls in greenlet)
* `greenlet` — low-level concurrency
* `certain numpy/scipy versions` — numerical computing
* `cryptography` — encryption (sometimes needs compilation)
* `psycopg2` — PostgreSQL driver (binary version available as psycopg2-binary)

**Solution:** Use `pip install --only-binary :all:` flag to install only pre-built wheels and avoid compilation.

---

## Typical Dependency Categories

The skill should recognize common categories such as:

### AWS & Cloud

* boto3
* awswrangler
* s3fs

### Streaming & Messaging

* websocket-client
* kafka-python
* confluent-kafka

### Data Processing

* pandas
* pyarrow
* polars
* duckdb

### Search & Analytics

* opensearch-py
* elasticsearch

### API & HTTP

* requests
* aiohttp

### Environment & Configuration

* python-dotenv
* pydantic

### Orchestration

* apache-airflow
* prefect

### Machine Learning

* scikit-learn
* xgboost
* mlflow

---

## Preferred Principles

The skill should:

* prefer lightweight and practical libraries
* minimize unnecessary dependencies
* prioritize maintainability
* recommend stable and widely adopted packages
* support scalable engineering workflows
* encourage reproducible environments
* avoid duplicate functionality across packages

---

## Installation Strategies

### Standard Installation (Linux/macOS or Windows with C++ compiler)
```bash
pip install -r requirements.txt
```

### Windows Pre-Built Wheels Only (Avoids C++ Compiler Requirement)
```bash
pip install -r requirements.txt --only-binary :all:
# OR for specific packages:
pip install gevent --only-binary :all:
```

### Separate Required vs Optional Dependencies

**requirements.txt** (required for all users):
```text
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
xgboost>=1.7.0
```

**requirements-dev.txt** (optional for developers):
```text
-r requirements.txt
pytest>=7.0
black>=22.0
mypy>=0.990
jupyter>=1.0.0
```

Install with: `pip install -r requirements-dev.txt`

---

## Standard Workflow

Typical workflow:

1. Analyze project requirements
2. Recommend dependencies
3. Identify Windows-problematic packages (gevent, greenlet, etc.)
4. Generate requirements.txt with platform notes
5. Suggest pre-built wheel strategy if needed
6. Install packages (with appropriate flags)
7. Validate compatibility
8. Separate optional vs required dependencies
9. Suggest version pinning where appropriate
10. Document transitive dependencies that may cause issues

---

## Example Use Cases

### AWS Streaming Pipeline

Suggested libraries:

```text id="7pqjlwm"
boto3
websocket-client
python-dotenv
opensearch-py
botocore
jmespath
python-dateutil
python-dotenv
s3transfer
six
urllib3
```

### Analytics Project

Suggested libraries:

```text id="jvzj4k"
pandas
duckdb
pyarrow
matplotlib
```

### ETL Pipeline and Orchestration

Suggested libraries:

```text id="nl1ov6"
pyspark
pyarrow
pandas
apache-airflow-providers-common-compat
apache-airflow-providers-common-io
apache-airflow-providers-common-sql
apache-airflow-providers-fab
apache-airflow-providers-ftp
apache-airflow-providers-http
apache-airflow-providers-imap
apache-airflow-providers-smtp
apache-airflow-providers-sqlite
```

### API-Based Data Ingestion

Suggested libraries:

```text id="06ixry"
requests
aiohttp
pydantic
```

---

## Dependency Management Standards

The skill should:

* use virtual environments by default
* support clean dependency isolation
* prefer pinned versions for production projects
* separate development and production dependencies where appropriate
* encourage modular package management

---

## Expected Outputs

The skill should be capable of generating:

* requirements.txt
* dependency installation commands
* package recommendations
* version suggestions
* dependency documentation
* installation checklists
* environment setup guidance
