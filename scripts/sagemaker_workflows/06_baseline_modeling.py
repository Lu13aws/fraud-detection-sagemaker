#!/usr/bin/env python3
"""
ML Baseline Modeling - Compare Imbalance Strategies
============================================================================
Train baseline models with different imbalance handling strategies.

Usage:
    python scripts/sagemaker_workflows/06_baseline_modeling.py

    Optional: Set custom S3 path via environment variable:
    export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
    python scripts/sagemaker_workflows/06_baseline_modeling.py
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    classification_report, confusion_matrix
)
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

S3_DATASET_PATH = os.getenv(
    'S3_DATASET_PATH',
    's3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv'
)

print("=" * 100)
print("ML BASELINE MODELING - IMBALANCE STRATEGY COMPARISON")
print("=" * 100)
print()

# ============================================================================
# 1. LOAD DATA & PREPARE SPLITS
# ============================================================================
print("1. LOADING DATA & PREPARING SPLITS")
print("-" * 100)

df = pd.read_csv(S3_DATASET_PATH)
df = df.drop_duplicates()

y = df['Class']
X = df.drop(columns=['Class', 'Time'])

# Stratified splits
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=42
)

# Scale features (fit on training data only)
scaler = RobustScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print(f"Training set: {len(X_train):,} samples ({y_train.mean()*100:.4f}% minority class)")
print(f"Validation set: {len(X_val):,} samples ({y_val.mean()*100:.4f}% minority class)")
print(f"Test set: {len(X_test):,} samples ({y_test.mean()*100:.4f}% minority class)")
print()

# ============================================================================
# 2. BASELINE MODEL 1: CLASS WEIGHTS
# ============================================================================
print("2. STRATEGY 1: CLASS WEIGHTS")
print("-" * 100)

class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

model_cw = LogisticRegression(class_weight=class_weight_dict, random_state=42, max_iter=1000)
model_cw.fit(X_train_scaled, y_train)

y_val_pred_cw = model_cw.predict(X_val_scaled)
y_val_pred_proba_cw = model_cw.predict_proba(X_val_scaled)[:, 1]

precision_cw = precision_score(y_val, y_val_pred_cw)
recall_cw = recall_score(y_val, y_val_pred_cw)
f1_cw = f1_score(y_val, y_val_pred_cw)
auc_pr_cw = average_precision_score(y_val, y_val_pred_proba_cw)
auc_roc_cw = roc_auc_score(y_val, y_val_pred_proba_cw)

print(f"Model: Logistic Regression with Class Weights")
print(f"Precision: {precision_cw:.4f} | Recall: {recall_cw:.4f} | F1: {f1_cw:.4f}")
print(f"AUC-PR: {auc_pr_cw:.4f} | AUC-ROC: {auc_roc_cw:.4f}")
print()

# ============================================================================
# 3. BASELINE MODEL 2: SMOTE OVERSAMPLING
# ============================================================================
print("3. STRATEGY 2: SMOTE OVERSAMPLING")
print("-" * 100)

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

model_smote = LogisticRegression(random_state=42, max_iter=1000)
model_smote.fit(X_train_smote, y_train_smote)

y_val_pred_smote = model_smote.predict(X_val_scaled)
y_val_pred_proba_smote = model_smote.predict_proba(X_val_scaled)[:, 1]

precision_smote = precision_score(y_val, y_val_pred_smote)
recall_smote = recall_score(y_val, y_val_pred_smote)
f1_smote = f1_score(y_val, y_val_pred_smote)
auc_pr_smote = average_precision_score(y_val, y_val_pred_proba_smote)
auc_roc_smote = roc_auc_score(y_val, y_val_pred_proba_smote)

print(f"Model: Logistic Regression with SMOTE")
print(f"Training set after SMOTE: {len(X_train_smote):,} samples ({y_train_smote.mean()*100:.2f}% minority)")
print(f"Precision: {precision_smote:.4f} | Recall: {recall_smote:.4f} | F1: {f1_smote:.4f}")
print(f"AUC-PR: {auc_pr_smote:.4f} | AUC-ROC: {auc_roc_smote:.4f}")
print()

# ============================================================================
# 4. BASELINE MODEL 3: RANDOM UNDERSAMPLING
# ============================================================================
print("4. STRATEGY 3: RANDOM UNDERSAMPLING")
print("-" * 100)

undersampler = RandomUnderSampler(random_state=42)
X_train_under, y_train_under = undersampler.fit_resample(X_train_scaled, y_train)

model_under = LogisticRegression(random_state=42, max_iter=1000)
model_under.fit(X_train_under, y_train_under)

y_val_pred_under = model_under.predict(X_val_scaled)
y_val_pred_proba_under = model_under.predict_proba(X_val_scaled)[:, 1]

precision_under = precision_score(y_val, y_val_pred_under)
recall_under = recall_score(y_val, y_val_pred_under)
f1_under = f1_score(y_val, y_val_pred_under)
auc_pr_under = average_precision_score(y_val, y_val_pred_proba_under)
auc_roc_under = roc_auc_score(y_val, y_val_pred_proba_under)

print(f"Model: Logistic Regression with Undersampling")
print(f"Training set after undersampling: {len(X_train_under):,} samples ({y_train_under.mean()*100:.2f}% minority)")
print(f"Precision: {precision_under:.4f} | Recall: {recall_under:.4f} | F1: {f1_under:.4f}")
print(f"AUC-PR: {auc_pr_under:.4f} | AUC-ROC: {auc_roc_under:.4f}")
print()

# ============================================================================
# 5. STRATEGY COMPARISON
# ============================================================================
print("5. STRATEGY COMPARISON")
print("=" * 100)
print()

comparison = pd.DataFrame({
    'Strategy': ['Class Weights', 'SMOTE', 'Undersampling'],
    'Precision': [precision_cw, precision_smote, precision_under],
    'Recall': [recall_cw, recall_smote, recall_under],
    'F1 Score': [f1_cw, f1_smote, f1_under],
    'AUC-PR': [auc_pr_cw, auc_pr_smote, auc_pr_under],
    'AUC-ROC': [auc_roc_cw, auc_roc_smote, auc_roc_under]
})

print("VALIDATION SET PERFORMANCE:")
print()
print(comparison.to_string(index=False))
print()

# Find best strategy by AUC-PR (best metric for imbalanced classification)
best_strategy_idx = comparison['AUC-PR'].idxmax()
best_strategy = comparison.loc[best_strategy_idx, 'Strategy']
best_auc_pr = comparison.loc[best_strategy_idx, 'AUC-PR']

print(f"🏆 BEST STRATEGY (by AUC-PR): {best_strategy} ({best_auc_pr:.4f})")
print()

# ============================================================================
# 6. TEST SET EVALUATION
# ============================================================================
print("6. TEST SET EVALUATION WITH BEST STRATEGY")
print("=" * 100)
print()

if best_strategy == 'Class Weights':
    best_model = model_cw
    X_train_best = X_train_scaled
    y_train_best = y_train
elif best_strategy == 'SMOTE':
    best_model = model_smote
    X_train_best = X_train_smote
    y_train_best = y_train_smote
else:
    best_model = model_under
    X_train_best = X_train_under
    y_train_best = y_train_under

y_test_pred = best_model.predict(X_test_scaled)
y_test_pred_proba = best_model.predict_proba(X_test_scaled)[:, 1]

precision_test = precision_score(y_test, y_test_pred)
recall_test = recall_score(y_test, y_test_pred)
f1_test = f1_score(y_test, y_test_pred)
auc_pr_test = average_precision_score(y_test, y_test_pred_proba)
auc_roc_test = roc_auc_score(y_test, y_test_pred_proba)

print(f"Model: Logistic Regression with {best_strategy}")
print()
print(f"TEST SET PERFORMANCE:")
print(f"  Precision: {precision_test:.4f} (% of flagged cases that are truly minority class)")
print(f"  Recall:    {recall_test:.4f} (% of actual minority class cases caught)")
print(f"  F1 Score:  {f1_test:.4f} (harmonic mean of precision and recall)")
print(f"  AUC-PR:    {auc_pr_test:.4f} (area under precision-recall curve) ⭐ PRIMARY METRIC")
print(f"  AUC-ROC:   {auc_roc_test:.4f} (area under ROC curve)")
print()

print("CLASSIFICATION REPORT:")
print(classification_report(y_test, y_test_pred, target_names=['Majority', 'Minority']))

print()
print("=" * 100)
print("BASELINE MODELING COMPLETE - READY FOR THRESHOLD OPTIMIZATION")
print("=" * 100)
print()

print(f"Recommendations:")
print(f"  ✓ Best strategy: {best_strategy}")
print(f"  ✓ Use this model for threshold optimization")
print(f"  ✓ Next: python scripts/sagemaker_workflows/07_threshold_optimization.py")
