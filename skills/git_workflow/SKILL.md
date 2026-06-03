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

## Initialization & Setup
* Create GitHub repositories 
* Git repository initialization (automated via `scripts/git-init.sh`)
* Repository structure consistency (use `.gitignore-template`)
* Branch naming conventions enforcement

## Daily Operations
* Git status analysis
* Safe staging of files (with validation via `scripts/git-validate.sh`)
* Commit generation with meaningful messages
* Branch creation and switching
* Pull workflows (handling conflicts, rebases)

## Push & Deployment
* **Safe push workflow** — standard push with pre-checks (via `scripts/git-publish.sh`)
* **Rebase and push** — handling diverged branches safely
* **Rejected push recovery** — pulling, rebasing, re-pushing
* Post-push verification (confirm commit reached remote)

## Repository Maintenance
* Merge workflow guidance
* Conflict resolution guidance
* Repository hygiene (cleanup stale branches)
* Rollback recommendations (soft vs hard reset)
* `.gitignore` management with templates

## Verification & Validation
* Pre-commit validation (secrets, large files, binary detection)
* Branch verification (correct branch checked out before push)
* Push target verification (pushing to intended remote/branch)
* Post-push confirmation (commit visible in remote history)

---

# Safety Rules

## Critical: Secrets & Credentials
* **NEVER** commit: `.env`, `*.pem`, `credentials.json`, `*.key`, AWS credentials, personal access tokens
* Always review modified files before committing — use `scripts/git-validate.sh` to auto-check
* Confirm file sizes before push — reject files > 50MB without explicit approval

## Push Operations
* **ALWAYS require confirmation** before:
  - `git push --force` or `git push --force-with-lease`
  - `git reset --hard`
  - Pushing to `main` or `master` branch
* Use `git push --force-with-lease` instead of `--force` (safer)

## GitHub Authentication
* Use SSH keys (recommended) or GitHub Personal Access Tokens
* **Never use password authentication** (deprecated since 2021)
* Store credentials securely — SSH keys in `~/.ssh/`, PAT in `~/.config/hub`

# Intelligent Commit Behavior
* Generate meaningful commit messages based on changes
* Group related file changes into logical commits
* Suggest smaller commits if unrelated changes are detected
* Use reusable scripts for deterministic operations (see "Automation Scripts" section)
---

# Automation Scripts

These deterministic scripts replace repetitive AI reasoning and ensure consistent, auditable workflows.

## `scripts/git-init.sh` — Repository Bootstrap

**Purpose:** Initialize a new git repository with security and consistency.

**Automated steps:**
1. `git init` and configure user name/email
2. Copy `.gitignore` from template
3. Create initial directory structure (if specified)
4. Create initial commit

**Usage:**
```bash
scripts/git-init.sh "Data Engineering Project" "lucia@example.com"
```

**Replaces:** Manual init + manual .gitignore creation + AI guidance on structure

---

## `scripts/git-validate.sh` — Pre-Commit Security Check

**Purpose:** Validate staged changes before commit — prevent secrets, large files, binaries.

**Checks:**
- Detects `.env`, `*.pem`, `*.key`, `credentials.json`, AWS keys
- Flags files > 50MB (binary/data files)
- Warns on uncommitted changes
- Checks for merge conflicts

**Usage:**
```bash
scripts/git-validate.sh
# Returns: 0 (pass) or 1 (fail with warnings)
```

**Replaces:** Manual file review + AI reasoning about what to exclude

---

## `scripts/git-publish.sh` — Safe Push Workflow

**Purpose:** Execute a complete push workflow with verification.

**Workflow:**
1. Validate staged/unstaged changes via `git-validate.sh`
2. Confirm branch name (prevent accidental push to main)
3. Confirm remote and target branch
4. Execute `git push`
5. Verify commit appears in remote history
6. Report success/failure

**Usage:**
```bash
scripts/git-publish.sh origin main
# Or: scripts/git-publish.sh  # Uses current branch
```

**Replaces:** Manual push + post-push verification + AI confirmation logic

---

## `scripts/git-feature-branch.sh` — Feature Branch Workflow

**Purpose:** Create and set up a feature branch following naming conventions.

**Workflow:**
1. Validate current branch is clean (no uncommitted changes)
2. Validate naming convention (`feature/`, `bugfix/`, `docs/`, etc.)
3. Create branch locally
4. Switch to new branch
5. Set upstream tracking

**Usage:**
```bash
scripts/git-feature-branch.sh feature/add-anomaly-detection
```

**Convention:**
- `feature/` — new functionality
- `bugfix/` — bug fixes
- `docs/` — documentation only
- `refactor/` — code refactoring (no logic changes)

**Replaces:** Manual branch creation + manual upstream tracking setup

---

## `.gitignore-template` — Standard Exclusions

Pre-built template for data engineering projects (excludes data, models, notebooks, secrets).

**Usage:** Copy during `git-init.sh` or manually:
```bash
cp .gitignore-template .gitignore
```

**Standard exclusions:**
- Data: `data/`, `raw/`, `processed/`, `*.csv`, `*.parquet`
- Models: `*.pkl`, `*.joblib`, `*.model`, `models/`
- Credentials: `.env`, `*.pem`, `*.key`, `credentials.json`
- Python: `venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`
- Notebooks: `.ipynb_checkpoints/`, `.jupyter/`
- AWS: `.aws/`, `.env.local`

---

# Standard Git Command Reference

## Repository Status

```bash
git init
git status
git log --oneline
```

---

## Safe Staging & Commit Workflow

```bash
git add <file>              # Stage specific files only
scripts/git-validate.sh     # Validate before commit
git commit -m "<message>"   # Create commit
```

**ALWAYS:** Review changes before committing
```bash
git diff --cached           # See staged changes
git diff                    # See unstaged changes
```

---

## Safe Push Workflow

```bash
scripts/git-publish.sh      # Automated safe push with verification
# OR manual:
git fetch origin
git log --oneline -5 origin/main  # Verify before push
git push origin <branch>
git log origin/<branch> -1  # Verify pushed
```

---

## Safe Branch Operations

```bash
scripts/git-feature-branch.sh feature/my-feature  # Create + set upstream
git checkout <branch>                             # Switch branch
git branch -v                                     # List branches with tracking
```

---

## Rebase & Push (Handling Diverged Branches)

```bash
git fetch origin
git rebase origin/main      # Rebase your commits on top of main
scripts/git-publish.sh      # Push (may need --force-with-lease)
```

---

## Conflict Resolution

```bash
git status                  # See conflicted files
# Edit conflicted files to resolve
git add <resolved-file>
git rebase --continue       # Continue rebase after resolving
# Or: git merge --continue  # If in merge workflow
```

---

## Rollback & Recovery

```bash
git log --oneline           # Find the commit to revert to
git reset --soft <commit>   # Undo commit, keep changes staged
git reset <commit>          # Undo commit, keep changes unstaged
# DANGEROUS - requires confirmation: git reset --hard <commit>
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
* **references to automation scripts** (not manual steps)
* **pre-flight verification checklists** before destructive operations
* **post-operation confirmation** (commit reached remote, branch correct, etc.)

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
* **prefer deterministic scripts over manual prompting**
* **enforce verification before push/force operations**
* **guide users toward automation scripts for repetitive tasks**
* **detect and prevent secrets/large files automatically**

---

# Common Use Cases

Examples include:

* **Repository initialization** → use `scripts/git-init.sh` for consistent setup
* **Starting a feature branch** → use `scripts/git-feature-branch.sh` for naming convention enforcement
* **Pushing changes safely** → use `scripts/git-publish.sh` for verification
* Pushing project updates to GitHub with safety checks
* Synchronizing local and remote repositories after conflicts
* Updating README documentation (merge with other docs changes)
* Committing infrastructure changes (separate from code changes)
* Versioning Lambda functions (tag releases)
* Managing streaming pipeline updates
* Tracking OpenSearch configuration changes
* Maintaining portfolio projects
* Organizing project milestones (use GitHub releases)
* Collaborative development workflows with merge conflict resolution

---

# Troubleshooting Guide

## "Rejected push — remote has newer commits"

**Cause:** You're behind the remote branch.

**Recovery:**
```bash
git fetch origin
git rebase origin/main
scripts/git-publish.sh
```

---

## "Accidentally committed secrets"

**Immediate action:**
```bash
git log --oneline  # Find the commit
git reset --soft <commit-before-secret>
# Remove the secret file
git add <cleaned-files>
git commit -m "Remove secret [security fix]"
scripts/git-publish.sh --force-with-lease
# NOTIFY: Force push occurred; collaborators should pull
```

**Prevention:** Always run `scripts/git-validate.sh` before commit.

---

## "Pushed to wrong branch"

**If not yet pulled by others:**
```bash
git reset --soft HEAD~1  # Undo last commit
git checkout <correct-branch>
git commit -m "..."
scripts/git-publish.sh
```

**If already pulled:**
```bash
git revert HEAD  # Create a revert commit
git push
```

---

## "Merge conflicts during rebase"

```bash
git status  # See conflicted files
# Edit files to resolve conflicts
git add <resolved-file>
git rebase --continue
```

**Or abort if unsure:**
```bash
git rebase --abort
```
