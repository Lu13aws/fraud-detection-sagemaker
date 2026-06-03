#!/bin/bash
# git-init.sh — Initialize a new git repository with security and consistency
# Usage: ./git-init.sh "Project Name" "email@example.com"

set -e

PROJECT_NAME="${1:-Data Engineering Project}"
GIT_EMAIL="${2:-data-engineer@example.com}"
GIT_USER="${GIT_EMAIL%@*}"

echo "Initializing git repository: $PROJECT_NAME"
echo "Email: $GIT_EMAIL"
echo ""

# Initialize repository
git init
git config user.email "$GIT_EMAIL"
git config user.name "$GIT_USER"
echo "✓ Git initialized"

# Copy .gitignore template if it exists
if [ -f ".gitignore-template" ]; then
    cp .gitignore-template .gitignore
    echo "✓ .gitignore created from template"
elif [ -f "scripts/.gitignore-template" ]; then
    cp scripts/.gitignore-template .gitignore
    echo "✓ .gitignore created from template"
else
    cat > .gitignore << 'EOF'
# Data
data/
raw/
processed/
*.csv
*.parquet

# Models & artifacts
*.pkl
*.joblib
*.model
models/

# Credentials (NEVER commit)
.env
.env.local
*.pem
*.key
credentials.json
~/.aws
.aws/

# Python
venv/
ENV/
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/

# Jupyter
.ipynb_checkpoints/
.jupyter/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Experiments
mlruns/
wandb/
EOF
    echo "✓ .gitignore created (default template)"
fi

# Create initial commit
git add .gitignore
git commit -m "Initial commit: Repository setup with .gitignore" 2>/dev/null || echo "ℹ No changes to commit"

echo ""
echo "✓ Repository initialized successfully"
echo ""
echo "Next steps:"
echo "  1. Add your project files"
echo "  2. Run: git add <files>"
echo "  3. Run: scripts/git-validate.sh"
echo "  4. Run: git commit -m '<message>'"
echo "  5. Run: scripts/git-publish.sh origin main"
