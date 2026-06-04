#!/usr/bin/env python
"""
setup-s3-notebooks.py
Updates Jupyter notebooks to read data from S3 instead of local files.

This script modifies:
- 01_eda.ipynb: Load creditcard.csv from S3
- 02_baseline.ipynb: Load creditcard.csv from S3
- 03_tree_models.ipynb: Use S3 bucket configuration

Usage:
    python scripts/setup-s3-notebooks.py
"""

import json
import sys
from pathlib import Path

def update_notebook(notebook_path, updates):
    """
    Update a Jupyter notebook with new cell content.

    Args:
        notebook_path: Path to .ipynb file
        updates: Dict of {cell_index: new_source_content}
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    for cell_idx, new_source in updates.items():
        if cell_idx < len(notebook['cells']):
            cell = notebook['cells'][cell_idx]
            if isinstance(new_source, str):
                cell['source'] = new_source.splitlines(keepends=True)
            else:
                cell['source'] = new_source

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    return True

def setup_notebooks():
    """Update all notebooks for S3 access."""

    notebook_dir = Path(__file__).parent.parent / 'notebooks'

    # Update 01_eda.ipynb
    print("Updating 01_eda.ipynb...")
    eda_cell_0 = """# Phase 1: Exploratory Data Analysis

**Goal:** Understand the dataset structure, the severity of class imbalance, and the relationships between features and the fraud label.
**Dataset:** Kaggle Credit Card Fraud Detection — 284,807 transactions, 492 fraudulent (0.17%)

**Data source:** AWS S3 bucket (configured in `config/aws_config.py`)"""

    eda_cell_1 = """import sys
sys.path.insert(0, '..')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')
%matplotlib inline"""

    eda_cell_3 = """# Load data from S3
from config.aws_config import read_csv_from_s3, S3_BUCKET, S3_DATA_PREFIX

s3_key = f"{S3_DATA_PREFIX}/creditcard.csv"
df = read_csv_from_s3(s3_key)

print(f'Loaded from S3: s3://{S3_BUCKET}/{s3_key}')
print(f'Shape: {df.shape}')
df.head()"""

    try:
        update_notebook(
            notebook_dir / '01_eda.ipynb',
            {0: eda_cell_0, 1: eda_cell_1, 3: eda_cell_3}
        )
        print("  [OK] Updated 01_eda.ipynb")
    except Exception as e:
        print(f"  [FAILED] 01_eda.ipynb: {e}")
        return False

    # Update 02_baseline.ipynb
    print("Updating 02_baseline.ipynb...")
    baseline_cell_0 = """# Phase 2 & 3: Feature Engineering + Logistic Regression Baseline

**Goals:**
1. Scale features and create stratified train/val/test splits
2. Compare three imbalance-handling strategies (class weights, SMOTE, undersampling)
3. Train a logistic regression baseline — understand *why accuracy is useless*
4. Establish AUC-PR as the primary metric going forward

**Data source:** AWS S3 (configured in `config/aws_config.py`)"""

    baseline_cell_1 = """import sys
sys.path.insert(0, '..')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    roc_auc_score, average_precision_score,
    precision_recall_curve, RocCurveDisplay, PrecisionRecallDisplay
)
from src.preprocessing import load_data, scale_features, split_data, apply_smote, undersample_majority
from config.aws_config import read_csv_from_s3, S3_DATA_PREFIX, S3_BUCKET

sns.set_theme(style='whitegrid')
%matplotlib inline"""

    baseline_cell_3 = """# Load data from S3
s3_key = f"{S3_DATA_PREFIX}/creditcard.csv"
df = read_csv_from_s3(s3_key)

print(f'Loaded from S3: s3://{S3_BUCKET}/{s3_key}')

# Preprocess
from src.preprocessing import scale_features, split_data
df = scale_features(df)

X_train, X_val, X_test, y_train, y_val, y_test = split_data(df)

print(f'Train: {X_train.shape}, fraud={y_train.sum()} ({y_train.mean()*100:.3f}%)')
print(f'Val:   {X_val.shape},   fraud={y_val.sum()} ({y_val.mean()*100:.3f}%)')
print(f'Test:  {X_test.shape},  fraud={y_test.sum()} ({y_test.mean()*100:.3f}%)')"""

    try:
        update_notebook(
            notebook_dir / '02_baseline.ipynb',
            {0: baseline_cell_0, 1: baseline_cell_1, 3: baseline_cell_3}
        )
        print("  [OK] Updated 02_baseline.ipynb")
    except Exception as e:
        print(f"  [FAILED] 02_baseline.ipynb: {e}")
        return False

    # Update 03_tree_models.ipynb
    print("Updating 03_tree_models.ipynb...")
    tree_cell_1 = """import sys
sys.path.insert(0, '..')

import boto3
import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.xgboost import XGBoost
from sagemaker.experiments.run import Run

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import AWS config
from config.aws_config import AWS_REGION, S3_BUCKET, S3_DATA_PREFIX
from src.preprocessing import load_data, scale_features, split_data, save_splits_csv

%matplotlib inline"""

    tree_cell_3 = """# Import AWS config
from config.aws_config import AWS_REGION, S3_BUCKET, S3_DATA_PREFIX

# AWS Configuration - Use settings from config
BUCKET = S3_BUCKET
REGION = AWS_REGION
PREFIX = "fraud-detection"
EXPERIMENT_NAME = "fraud-detection-models"

session = sagemaker.Session()
role = sagemaker.get_execution_role()

print(f"Region: {REGION}")
print(f"Bucket: {BUCKET}")
print(f"Role:   {role}")"""

    try:
        update_notebook(
            notebook_dir / '03_tree_models.ipynb',
            {1: tree_cell_1, 3: tree_cell_3}
        )
        print("  [OK] Updated 03_tree_models.ipynb")
    except Exception as e:
        print(f"  [FAILED] 03_tree_models.ipynb: {e}")
        return False

    return True

if __name__ == '__main__':
    print("Setting up Jupyter notebooks for S3 access...\n")

    if setup_notebooks():
        print("\n[SUCCESS] All notebooks updated!")
        print("\nNext steps:")
        print("  1. Ensure AWS credentials: aws configure")
        print("  2. Verify S3 access: aws s3 ls")
        print("  3. Run: jupyter notebook notebooks/01_eda.ipynb")
        sys.exit(0)
    else:
        print("\n[ERROR] Some notebooks failed to update")
        sys.exit(1)
