# Git Workflow Skill

## Purpose

This skill is responsible for supporting and standardizing
Git and GitHub workflows used in data engineering
and cloud engineering projects.

The goal is to improve repository management,
version control consistency, and operational reliability.

---

# Responsibilities

The skill should assist with:

* Create GitHub repositories 
* Git repository initialization
* Local and remote repository synchronization
* Git status analysis
* Staging file changes
* Commit generation
* Push and pull workflows
* Branch management
* Merge workflow guidance
* Repository hygiene
* .gitignore management
* Commit message generation
* Conflict detection guidance
* Rollback recommendations
* Repository structure consistency
* Sync local and remote repositories

---

# Safety Rules
* Always review modified files before committing
* Never push secrets, API keys, credentials, .env files, or AWS keys
* Ask for confirmation before force-push operations

# Intelligent Commit Behavior
* Generate meaningful commit messages based on changes
* Group related file changes into logical commits
* Suggest smaller commits if unrelated changes are detected
---

# Common Git Commands

## Repository Status

```bash id="rdrjlwm"
git init
git status
git log
```

---

## Stage Files

```bash id="s8n8c6"
git add .
```

---

## Commit Changes

```bash id="4ljlwm"
git commit -m "Add OpenSearch index mapping improvements"
```

---

## Push Changes

```bash id="u7d7x6"
git push
```

---

## Pull Latest Changes

```bash id="16cc6g"
git pull
```

---

## Create Branch

```bash id="cuhjlwm"
git checkout -b feature/new-streaming-pipeline
```

---

## Switch Branch

```bash id="l9qjlwm"
git checkout main
```

---

## View Commit History

```bash id="urjlwm"
git log --oneline
```

---

# Preferred Outputs

Outputs should include:

* clear Git workflow explanations
* repository synchronization guidance
* meaningful commit message suggestions
* operationally safe workflows
* clean version control practices
* troubleshooting guidance where appropriate

---

# Engineering Principles

The skill should:

* prioritize repository clarity
* encourage small and meaningful commits
* avoid unsafe Git operations without confirmation
* support reproducible workflows
* encourage clean repository organization
* separate infrastructure, documentation, and code changes where appropriate
* promote operational consistency

---

# Common Use Cases

Examples include:

* pushing project updates to GitHub
* synchronizing local and remote repositories
* updating README documentation
* committing infrastructure changes
* versioning Lambda functions
* managing streaming pipeline updates
* tracking OpenSearch configuration changes
* maintaining portfolio projects
* organizing project milestones
* collaborative development workflows
