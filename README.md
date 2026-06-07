# Data Engineering AI Agent
## Credit Card Fraud Detection with AWS SageMaker + Reusable ML Frameworks

An end-to-end machine learning project combining **practical fraud detection** with **reusable ML workflows and automation frameworks**.

**🎯 Project Goals:**
- Learn ML fundamentals through a real fraud detection use case (284K transactions, 0.17% fraud rate)
- Develop reusable frameworks for imbalanced classification, feature engineering, and model evaluation
- Create parameterized automation scripts and Claude AI prompts for ML workflows
- Demonstrate production-ready data engineering practices and SageMaker integration

---

## ✨ What's New (Phase 3 Improvements)

✅ **Python 3.13+ Upgrade** — Updated all dependencies, verified Jupyter kernels  
✅ **7 SageMaker SKILL Files** — Complete ML workflow guidance (data assessment through threshold optimization)  
✅ **7 ML Workflow Prompts** — Reusable Claude AI prompts for each step of the pipeline  
✅ **4 Parameterized Python Scripts** — Automated data preparation (01_initial_assessment → 04_feature_engineering)  
✅ **Complete Workflow Guide** — WORKFLOW_GUIDE.md documenting the entire 7-step process  
✅ **Knowledge Synchronized** — All reusable assets synced to personal-data-engineering-toolkit  

---

## 🎯 Key Features

### 7-Phase ML Workflow (Fully Documented)

```
SKILL1: Initial Data Assessment     → Understand structure, quality, risks
   ↓
SKILL2: Duplicate Assessment         → Identify and assess duplicate records
   ↓
SKILL3: Missing Values Analysis      → Determine treatment strategies
   ↓
SKILL4: Feature Engineering & Scaling → Transform, scale (RobustScaler), stratified splits
   ↓
SKILL5: Visualization & EDA          → Explore patterns, correlations, outliers
   ↓
SKILL6: ML Baseline Modeling         → Compare imbalance strategies (class weights, SMOTE, undersampling)
   ↓
SKILL7: Threshold Optimization       → Find optimal threshold, business trade-offs
```

### Reusable Components

| Component | Purpose | Files |
|-----------|---------|-------|
| **SKILL Files** | Comprehensive ML frameworks with code examples | 7 SKILL.md files |
| **Claude Prompts** | Prompts for each workflow step to guide AI assistance | 7 prompts in sagemaker_prompts/ |
| **Python Scripts** | Parameterized, executable automation for data prep | 4 scripts in sagemaker_workflows/ |
| **Workflow Guide** | Complete orchestration guide with decision points | WORKFLOW_GUIDE.md |

---

## 📊 Project Overview

### The Fraud Detection Problem

This project uses the **Kaggle Credit Card Fraud Detection dataset** (284,807 transactions, 0.17% fraud rate) to explore:

- **Class imbalance challenges** — fraud is rare; naive models achieve 99.83% accuracy by always predicting "legitimate"
- **Beyond accuracy** — why AUC-PR is more informative than accuracy for imbalanced classification
- **Precision-recall tradeoff** — business logic determines the decision threshold, not just model probability
- **Multiple algorithms** — logistic regression baseline → Random Forest → XGBoost → unsupervised anomaly detection
- **Model explainability** — SHAP analysis to understand what features drive fraud predictions
- **AWS SageMaker workflow** — training jobs, experiments, and managed services

### Dataset

| Property | Value |
|----------|-------|
| **Source** | Kaggle: [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |
| **Total transactions** | 284,807 |
| **Fraudulent** | 492 (0.17%) |
| **Features** | V1–V28 (PCA-anonymized), `Amount`, `Time` |
| **License** | Open access (anonymous) |
| **Key challenge** | Extreme class imbalance (1:579 legitimate-to-fraud ratio) |

---

## 📁 Project Structure

```
Data Engineering Agent/
├── README.md                                    ← You are here
├── CLAUDE.md                                    ← Project instructions & guidelines
├── requirements.txt                             ← Python 3.13+ dependencies
├── .gitignore                                   ← Excludes data, credentials, models
│
├── 📚 notebooks/
│   ├── 01_eda.ipynb                            ← Phase 1: Exploratory Data Analysis
│   ├── 02_baseline.ipynb                       ← Phase 2-3: Feature Eng + Baseline Model
│   ├── 03_tree_models.ipynb                    ← Phase 4: Tree models via SageMaker
│   ├── 04_anomaly_detection.ipynb              ← Phase 5: Unsupervised anomaly detection
│   └── 05_threshold_tuning.ipynb               ← Phase 6-7: Threshold tuning + SHAP
│
├── 🤖 skills/
│   └── aws/
│       └── aws_sagemaker/
│           ├── SKILL.md                        ← Overview of all ML skills
│           ├── SKILL2.md                       ← Duplicate Assessment & Cleaning
│           ├── SKILL3.md                       ← Missing Values Assessment
│           ├── SKILL4.md                       ← Feature Engineering & Scaling ⭐
│           ├── SKILL5.md                       ← Visualization & EDA
│           ├── SKILL6.md                       ← ML Baseline Modeling
│           ├── SKILL7.md                       ← Threshold Optimization
│           └── WORKFLOW_GUIDE.md               ← Complete workflow orchestration ⭐
│
├── 💬 prompts/
│   └── sagemaker_prompts/
│       ├── 01_EDA_PROMPT.md                    ← Claude prompt for EDA
│       ├── 02_DUPLICATE_PROMPT.md              ← Claude prompt for duplicates
│       ├── 03_NULL_VALUE_PROMPT.md             ← Claude prompt for missing values
│       ├── 04_FEATURE_ENGINEERING_PROMPT.md    ← Claude prompt for feature eng ⭐
│       ├── 04_VISUALIZATION_PROMPT.md          ← Claude prompt for EDA visualization
│       ├── 05_BASELINE_MODELING_PROMPT.md      ← Claude prompt for baseline models
│       └── 06_THRESHOLD_OPTIMIZATION_PROMPT.md ← Claude prompt for threshold tuning
│
├── 🔧 scripts/
│   └── sagemaker_workflows/
│       ├── 01_initial_assessment.py            ← Data shape, quality, risks analysis
│       ├── 02_duplicate_cleaning.py            ← Duplicate detection & removal
│       ├── 03_missing_values.py                ← Missing value analysis & treatment
│       ├── 04_feature_engineering.py           ← Scaling, splitting, leakage checks ⭐
│       ├── README.md                           ← Complete script documentation
│       └── EXTRACTION_NOTES.md                 ← Code extraction rationale
│
├── 📦 src/
│   ├── preprocessing.py                        ← Feature scaling, splitting utilities
│   ├── train_xgboost.py                        ← SageMaker XGBoost training script
│   └── train_rf.py                             ← SageMaker Random Forest training script
│
├── 📊 data/
│   ├── raw/                                    ← Original CSV (download from Kaggle)
│   └── processed/                              ← Processed data, train/val/test splits
│
└── monitoring/
    └── [SageMaker monitoring & experiment tracking]
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+** (boto3 support deadline: April 29, 2026)
- **AWS Account** with SageMaker and S3 access
- **AWS CLI** configured (`aws configure`)
- **Jupyter** (local or SageMaker Studio)
- **Git** and GitHub account

### Quick Start (5 minutes)

#### 1. Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/Data-Engineering-Agent.git
cd Data-Engineering-Agent
```

#### 2. Create Python Environment
```bash
# Create virtual environment with Python 3.13+
python -m venv .venv

# Activate (choose your OS)
source .venv/bin/activate       # macOS/Linux
# or
.venv\Scripts\activate          # Windows (PowerShell)

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Download Dataset
```bash
# Install Kaggle CLI if needed
pip install kaggle

# Download dataset (requires Kaggle API credentials)
kaggle datasets download -d mlg-ulb/creditcardfraud
unzip creditcardfraud.zip -d data/raw/
```

#### 4. Start Jupyter
```bash
jupyter notebook
```

Then open `notebooks/01_eda.ipynb` to begin.

---

## 📚 Available Workflows

### Option 1: Quick Path (Use Scripts Only)
**For existing clean data:**
```bash
export S3_DATASET_PATH="s3://your-bucket/data.csv"
python scripts/sagemaker_workflows/01_initial_assessment.py
python scripts/sagemaker_workflows/02_duplicate_cleaning.py
python scripts/sagemaker_workflows/03_missing_values.py
python scripts/sagemaker_workflows/04_feature_engineering.py
```
**Time: ~65 minutes**

### Option 2: Exploratory Path (Skills + Prompts)
**For learning and understanding:**
1. Read SKILL1.md (Initial Assessment)
2. Use 01_EDA_PROMPT.md with Claude for guidance
3. Follow through SKILL2 → SKILL7 in sequence
4. Use corresponding prompts at each step
**Time: ~2-3 hours**

### Option 3: Full Project (Notebooks + Skills)
**For complete learning:**
1. Run notebooks/01_eda.ipynb
2. Run notebooks/02_baseline.ipynb
3. Reference SKILL files for deep dives
4. Use prompts to enhance Claude assistance
**Time: ~4-5 hours**

---

## 🔧 Scripts & Automation

### 01_initial_assessment.py
**Purpose:** Analyze dataset structure and quality
```bash
python scripts/sagemaker_workflows/01_initial_assessment.py
```
**Tasks:** Shape analysis, missing values, duplicates, statistics, risk identification

### 02_duplicate_cleaning.py
**Purpose:** Detect and remove duplicate records
```bash
python scripts/sagemaker_workflows/02_duplicate_cleaning.py
```
**Tasks:** Duplicate detection, impact assessment, removal guidance

### 03_missing_values.py
**Purpose:** Analyze missing values and recommend treatment
```bash
python scripts/sagemaker_workflows/03_missing_values.py
```
**Tasks:** Missing value detection, severity assessment, treatment recommendations

### 04_feature_engineering.py
**Purpose:** Scale features and create stratified splits
```bash
python scripts/sagemaker_workflows/04_feature_engineering.py
```
**Tasks:** Feature transformation, RobustScaler, stratified split (70/15/15), leakage verification

**Configuration via environment variables:**
```bash
export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
python scripts/sagemaker_workflows/04_feature_engineering.py
```

All scripts are parameterizable and reusable across projects.

---

## 💬 Using Claude Prompts

Each workflow step has a corresponding prompt for Claude AI assistance:

### Example: Feature Engineering
```bash
# Copy the prompt content from:
# prompts/sagemaker_prompts/04_FEATURE_ENGINEERING_PROMPT.md

# Paste into Claude Code or Claude.ai and:
# - Provide your cleaned dataset
# - Get guided feature engineering steps
# - Receive transformation recommendations
# - Validate scaling and split strategies
```

**Benefits:**
- Step-by-step guidance from an AI expert
- Customized recommendations for your data
- Error checking and best practice reminders
- Saves hours of research and debugging

---

## 📖 Documentation

### For Learning
- **SKILL Files** — Read for deep understanding of each step
- **notebooks/** — Interactive exploration of concepts
- **WORKFLOW_GUIDE.md** — Complete pipeline orchestration

### For Implementation
- **scripts/** — Copy/adapt for your projects
- **README.md in scripts/sagemaker_workflows/** — Detailed script reference
- **prompts/** — Use with Claude for guided implementation

### For Reference
- **CLAUDE.md** — Project instructions and guidelines
- **requirements.txt** — Dependencies and versions
- **.gitignore** — What's excluded and why

---

## 🎓 Key Concepts

### Class Imbalance
**Problem:** Fraud is rare (0.17%). A naive model achieves 99.83% accuracy by always predicting "legitimate."

**Solution:** Compared in SKILL6:
- **Class weights** — Penalize minority class errors
- **SMOTE** — Synthetic oversampling of fraud
- **Undersampling** — Reduce majority class
- **Threshold tuning** — Adjust decision boundary (SKILL7)

### Evaluation Metrics
For imbalanced data:
- ✅ **AUC-PR** — Best metric (focuses on fraud detection)
- ✅ **Precision & Recall** — Shows the tradeoff
- ❌ **Accuracy** — Misleading (99.83% baseline)

### Precision-Recall Tradeoff
No perfect threshold. Choose based on business logic:
- **High Recall (95%)** — Catch almost all fraud, flag some legit txns
- **High Precision (95%)** — Most flags are real fraud, miss some fraud
- **Balanced (80/80)** — Practical middle ground

---

## 🔄 Recent Improvements (Phases 3-4 Complete)

### Infrastructure & Python
- ✅ Python 3.10 → 3.13 upgrade (boto3 deadline: April 29, 2026)
- ✅ Jupyter kernel verification with Python 3.13
- ✅ Updated all notebooks with 3.13+ kernels

### Skills & Workflow Documentation
- ✅ Created SKILL4.md (Feature Engineering & Scaling) — 1,200+ lines
- ✅ Created WORKFLOW_GUIDE.md — Complete 7-step workflow orchestration
- ✅ Audited & reorganized all 7 SageMaker SKILL files

### Prompts (Generalized for Reusability)
- ✅ Generalized all 7 ML prompts (removed fraud-specific terminology)
- ✅ Prompts now applicable to any classification task
- ✅ Increased toolkit reusability across domains

### Complete ML Automation Pipeline (7 Scripts) ⭐
- ✅ Script 01: Initial Data Assessment
- ✅ Script 02: Duplicate Assessment & Cleaning
- ✅ Script 03: Missing Values Analysis
- ✅ Script 04: Feature Engineering & Scaling
- ✅ **Script 05: Visualization & EDA** (NEW Phase 4)
- ✅ **Script 06: Baseline Modeling** (NEW Phase 4)
- ✅ **Script 07: Threshold Optimization** (NEW Phase 4)

### Knowledge Management
- ✅ Synchronized all reusable assets to personal-data-engineering-toolkit
- ✅ Established toolkit as canonical source for ML frameworks

---

## 🤝 Contributing & Future Work

### Completed Phase 4 Enhancements ✅
- ✅ Extracted SKILL5-7 code to parameterized Python scripts (scripts 05-07 complete)
- ✅ Generalized all prompts to classification task terminology (domain-agnostic)

### Remaining Future Enhancements
- Extract remaining SKILL5-7 code patterns (visualization variations, advanced models)
- Create advanced model scripts (Random Forest, XGBoost, AutoML)
- Add hyperparameter optimization guidance
- Implement monitoring and drift detection patterns
- Add database connection support to scripts
- Create reusable feature engineering pipelines
- Add monitoring and retraining workflows

### Toolkit Synchronization
All reusable assets are synchronized to: [personal-data-engineering-toolkit](https://github.com/YOUR-USERNAME/personal-data-engineering-toolkit)

This keeps your fraud detection project focused while maintaining a separate canonical source for reusable frameworks.

---

## 📊 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Cloud** | AWS (SageMaker, S3, Athena) |
| **Data Processing** | pandas, numpy |
| **ML Frameworks** | scikit-learn, XGBoost, imbalanced-learn |
| **Explainability** | SHAP |
| **Notebooks** | Jupyter |
| **Python Version** | 3.13+ |
| **Version Control** | Git, GitHub |

---

## 📧 Contact & Questions

**Project Purpose:** Portfolio demonstration of end-to-end ML engineering + reusable frameworks

**For Issues/Questions:**
1. Check WORKFLOW_GUIDE.md for workflow decisions
2. Review SKILL files for deep understanding
3. See scripts/sagemaker_workflows/README.md for script details
4. Check CLAUDE.md for project guidelines

**Data Source:** Kaggle Credit Card Fraud Detection (open access, anonymized)

---

## 📝 License

This project is open source for portfolio and educational purposes. The dataset is from Kaggle (anonymized, open access).

---

**Last Updated:** June 2026  
**Python Version:** 3.13+  
**Status:** Active development with focus on reusable frameworks  

🚀 **Ready to explore the ML pipeline?** Start with `notebooks/01_eda.ipynb`

