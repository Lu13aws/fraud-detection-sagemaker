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
* 

---

## Preferred Principles

The skill should:

* prioritize clean project organization
* support scalability and maintainability
* follow practical engineering standards
* avoid unnecessary complexity
* generate reusable structures
* support cloud-native data engineering workflows

---

## Example Use Cases

* Streaming pipelines
* AWS-based architectures
* ETL/ELT projects
* Analytics platforms
* Data lake projects
* OpenSearch dashboards
* Event-driven systems
