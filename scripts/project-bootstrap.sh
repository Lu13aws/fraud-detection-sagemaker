#!/bin/bash

# project-bootstrap.sh
# Bootstrap a new data engineering ML project with standard directory structure
#
# Usage: bash scripts/project-bootstrap.sh [project-name]
#
# Creates:
# - Standard folder structure (data/, notebooks/, src/, config/, scripts/)
# - .gitignore template
# - requirements.txt template
# - README.md template
# - .env.example template

set -e  # Exit on error

PROJECT_NAME="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Project Bootstrap${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠ Git not initialized. Run: git init${NC}"
    echo ""
fi

# Create directory structure
echo -e "${GREEN}Creating directory structure...${NC}"

mkdir -p data/raw
mkdir -p data/splits
mkdir -p notebooks
mkdir -p src
mkdir -p config
mkdir -p scripts
mkdir -p skills
mkdir -p architecture

echo -e "${GREEN}✓ Directories created${NC}"

# Create .gitkeep files
touch data/.gitkeep
touch data/raw/.gitkeep
touch data/splits/.gitkeep
touch notebooks/.gitkeep
touch src/__init__.py
touch config/__init__.py
touch architecture/.gitkeep

echo -e "${GREEN}✓ .gitkeep files created${NC}"

# Check for .gitignore
if [ ! -f ".gitignore" ]; then
    echo -e "${GREEN}Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Data Engineering Project — Standard .gitignore Template

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA FILES (NEVER COMMIT RAW DATA)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

data/
raw/
processed/
*.csv
*.tsv
*.json
*.parquet
*.feather
*.ndjson

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CREDENTIALS & SECRETS (CRITICAL - NEVER COMMIT)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.env
.env.local
.env.*.local
.env.production.local
*.pem
*.key
*.crt
credentials.json
config.json
api_keys.txt
secrets/
.aws/

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODELS & ARTIFACTS (TOO LARGE - USE S3)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*.pkl
*.pickle
*.joblib
*.model
*.h5
*.pth
*.onnx
*.pb
models/
artifacts/

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PYTHON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

venv/
.venv
ENV/
env/
__pycache__/
*.pyc
*.pyo
*.pyd
*.so
*.egg-info/
*.egg
build/
dist/
.installed.cfg
*.egg-info

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TESTING & COVERAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.hypothesis/
*.cover

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# JUPYTER & NOTEBOOKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.ipynb_checkpoints/
*/.ipynb_checkpoints/*
.jupyter/
.jupyterlab/

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IDE & EDITORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXPERIMENTS & TRACKING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

mlruns/
wandb/
.wandb/
lightning_logs/
outputs/
logs/
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
else
    echo -e "${YELLOW}✓ .gitignore already exists${NC}"
fi

# Check for requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo -e "${GREEN}Creating requirements.txt template...${NC}"
    cat > requirements.txt << 'EOF'
# Data Engineering & ML Stack

# Data manipulation
pandas>=2.0.0
numpy>=1.24.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.0.0

# Machine Learning
scikit-learn>=1.3.0
xgboost>=2.0.0
lightgbm>=4.0.0
imbalanced-learn>=0.11.0  # For SMOTE

# Deep Learning (optional)
tensorflow>=2.12.0
torch>=2.0.0

# AWS & SageMaker
boto3>=1.28.0
sagemaker>=2.100.0
python-dotenv>=1.0.0

# Jupyter & Notebooks
jupyter>=1.0.0
ipykernel>=6.20.0
notebook>=6.5.0

# Explainability
shap>=0.42.0

# Utilities
tqdm>=4.65.0
pyyaml>=6.0
python-dateutil>=2.8.2

# Development
black>=23.0.0
flake8>=6.0.0
pytest>=7.0.0
EOF
    echo -e "${GREEN}✓ requirements.txt template created${NC}"
else
    echo -e "${YELLOW}✓ requirements.txt already exists${NC}"
fi

# Check for README.md
if [ ! -f "README.md" ]; then
    echo -e "${GREEN}Creating README.md template...${NC}"
    cat > README.md << 'EOF'
# Project Name

Brief project description.

## Quick Start

### 1. Clone Repository
\`\`\`bash
git clone <repository-url>
cd <project-name>
\`\`\`

### 2. Set Up Python Environment
\`\`\`bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate      # Windows

pip install --upgrade pip
pip install -r requirements.txt
\`\`\`

### 3. Configure AWS (if needed)
\`\`\`bash
aws configure
# Enter credentials and region
\`\`\`

### 4. Create .env File
\`\`\`bash
cp .env.example .env
# Edit .env with your credentials (NOT committed to git)
\`\`\`

## Project Structure

\`\`\`
project/
├── data/
│   ├── raw/          ← Original data
│   └── splits/       ← Train/val/test splits
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_baseline.ipynb
│   └── ...
│
├── src/
│   ├── preprocessing.py
│   ├── train_*.py
│   └── ...
│
├── config/
│   └── aws_config.py
│
├── scripts/
│   └── *.sh, *.py    ← Automation scripts
│
├── README.md
├── requirements.txt
└── CLAUDE.md         ← AI instructions
\`\`\`

## Running Notebooks

\`\`\`bash
# Activate virtual environment
source .venv/bin/activate

# Launch Jupyter
jupyter notebook notebooks/01_eda.ipynb
\`\`\`

## Team Guidelines

- Code review before merging
- Always document assumptions
- Use meaningful commit messages
- Never commit data, models, or credentials

## Resources

- [Project Wiki](wiki/)
- [Issue Tracker](issues/)
- [Documentation](docs/)
EOF
    echo -e "${GREEN}✓ README.md template created${NC}"
else
    echo -e "${YELLOW}✓ README.md already exists${NC}"
fi

# Check for .env.example
if [ ! -f ".env.example" ]; then
    echo -e "${GREEN}Creating .env.example template...${NC}"
    cat > .env.example << 'EOF'
# AWS Configuration (local development)
# Copy to .env and fill in your actual credentials
# .env is NOT committed to git

AWS_REGION=eu-central-1
S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=eu-central-1

# SageMaker (optional)
SAGEMAKER_ROLE_ARN=arn:aws:iam::ACCOUNT_ID:role/SageMakerRole
SAGEMAKER_EXECUTION_ROLE=arn:aws:iam::ACCOUNT_ID:role/SageMakerRole
EOF
    echo -e "${GREEN}✓ .env.example created${NC}"
else
    echo -e "${YELLOW}✓ .env.example already exists${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Bootstrap Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Create Python virtual environment:"
echo "   python -m venv .venv"
echo "   source .venv/bin/activate"
echo ""
echo "2. Install dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "3. Configure AWS:"
echo "   aws configure"
echo ""
echo "4. Create .env file (copy from .env.example)"
echo "   cp .env.example .env"
echo "   # Edit .env with your credentials"
echo ""
echo "5. Start developing!"
echo "   jupyter notebook notebooks/"
echo ""
