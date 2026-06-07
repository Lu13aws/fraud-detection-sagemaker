#!/usr/bin/env python3
"""
Threshold Optimization for Classification
============================================================================
Find optimal decision thresholds based on business priorities.

Usage:
    python scripts/sagemaker_workflows/07_threshold_optimization.py

    Optional: Set custom S3 path via environment variable:
    export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
    export BUSINESS_PRIORITY="recall"  # Options: "recall", "precision", "balanced"
    python scripts/sagemaker_workflows/07_threshold_optimization.py
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    precision_recall_curve, roc_curve
)
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

S3_DATASET_PATH = os.getenv(
    'S3_DATASET_PATH',
    's3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv'
)

BUSINESS_PRIORITY = os.getenv(
    'BUSINESS_PRIORITY',
    'balanced'  # Options: "recall", "precision", "balanced"
)

print("=" * 100)
print("THRESHOLD OPTIMIZATION - MINORITY CLASS DETECTION")
print("=" * 100)
print()

# ============================================================================
# 1. LOAD DATA & TRAIN BASELINE MODEL
# ============================================================================
print("1. LOADING DATA & TRAINING BASELINE MODEL")
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

# Scale features
scaler = RobustScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Train best model (using SMOTE from baseline modeling)
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_smote, y_train_smote)

print("✓ Model trained with SMOTE strategy")
print()

# ============================================================================
# 2. GENERATE PREDICTIONS & PROBABILITIES
# ============================================================================
print("2. GENERATING PREDICTIONS & PROBABILITIES")
print("-" * 100)

y_val_pred_proba = model.predict_proba(X_val_scaled)[:, 1]
y_test_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

print(f"Prediction probabilities range: {y_val_pred_proba.min():.4f} to {y_val_pred_proba.max():.4f}")
print(f"Default threshold (0.5) predictions: {(y_val_pred_proba >= 0.5).sum():,} flagged out of {len(y_val):,}")
print()

# ============================================================================
# 3. EVALUATE THRESHOLDS
# ============================================================================
print("3. EVALUATING THRESHOLDS (0.01 to 0.99)")
print("-" * 100)

thresholds = np.arange(0.01, 1.00, 0.01)
metrics_list = []

for threshold in thresholds:
    y_val_pred = (y_val_pred_proba >= threshold).astype(int)

    # Handle edge case: all zeros
    if y_val_pred.sum() == 0:
        precision = 0
        recall = 0
        f1 = 0
    else:
        precision = precision_score(y_val, y_val_pred, zero_division=0)
        recall = recall_score(y_val, y_val_pred, zero_division=0)
        f1 = f1_score(y_val, y_val_pred, zero_division=0)

    metrics_list.append({
        'Threshold': threshold,
        'Precision': precision,
        'Recall': recall,
        'F1': f1,
        'Flagged': y_val_pred.sum()
    })

metrics_df = pd.DataFrame(metrics_list)

print(f"Evaluated {len(thresholds)} thresholds")
print()

# ============================================================================
# 4. IDENTIFY OPTIMAL THRESHOLDS
# ============================================================================
print("4. OPTIMAL THRESHOLDS BY PRIORITY")
print("=" * 100)
print()

# F1 maximization
f1_max_idx = metrics_df['F1'].idxmax()
f1_optimal = metrics_df.loc[f1_max_idx]

print(f"🎯 F1 SCORE MAXIMIZATION (Balanced Precision-Recall):")
print(f"   Threshold: {f1_optimal['Threshold']:.2f}")
print(f"   Precision: {f1_optimal['Precision']:.4f}")
print(f"   Recall:    {f1_optimal['Recall']:.4f}")
print(f"   F1 Score:  {f1_optimal['F1']:.4f}")
print(f"   Flagged:   {int(f1_optimal['Flagged']):,} cases")
print()

# Recall maximization
recall_max_idx = metrics_df['Recall'].idxmax()
recall_optimal = metrics_df.loc[recall_max_idx]

print(f"🎯 RECALL MAXIMIZATION (Catch All Minority Cases):")
print(f"   Threshold: {recall_optimal['Threshold']:.2f}")
print(f"   Precision: {recall_optimal['Precision']:.4f}")
print(f"   Recall:    {recall_optimal['Recall']:.4f}")
print(f"   F1 Score:  {recall_optimal['F1']:.4f}")
print(f"   Flagged:   {int(recall_optimal['Flagged']):,} cases")
print()

# Precision maximization
precision_max_idx = metrics_df['Precision'].idxmax()
precision_optimal = metrics_df.loc[precision_max_idx]

print(f"🎯 PRECISION MAXIMIZATION (Minimize False Alarms):")
print(f"   Threshold: {precision_optimal['Threshold']:.2f}")
print(f"   Precision: {precision_optimal['Precision']:.4f}")
print(f"   Recall:    {precision_optimal['Recall']:.4f}")
print(f"   F1 Score:  {precision_optimal['F1']:.4f}")
print(f"   Flagged:   {int(precision_optimal['Flagged']):,} cases")
print()

# ============================================================================
# 5. BUSINESS PRIORITY RECOMMENDATION
# ============================================================================
print("5. BUSINESS PRIORITY ANALYSIS")
print("=" * 100)
print()

if BUSINESS_PRIORITY == "recall":
    recommended = recall_optimal
    reason = "Maximize minority class detection"
elif BUSINESS_PRIORITY == "precision":
    recommended = precision_optimal
    reason = "Minimize false alarms / false positives"
else:  # balanced
    recommended = f1_optimal
    reason = "Balance between precision and recall"

print(f"BUSINESS PRIORITY: {BUSINESS_PRIORITY.upper()}")
print(f"Reason: {reason}")
print()
print(f"✅ RECOMMENDED THRESHOLD: {recommended['Threshold']:.2f}")
print(f"   Precision: {recommended['Precision']:.4f} ({recommended['Precision']*100:.2f}% of flagged are true minority class)")
print(f"   Recall:    {recommended['Recall']:.4f} ({recommended['Recall']*100:.2f}% of actual minority class caught)")
print(f"   F1 Score:  {recommended['F1']:.4f}")
print(f"   Flagged:   {int(recommended['Flagged']):,} cases on validation set")
print()

# ============================================================================
# 6. TEST SET EVALUATION
# ============================================================================
print("6. TEST SET EVALUATION AT RECOMMENDED THRESHOLD")
print("=" * 100)
print()

recommended_threshold = recommended['Threshold']
y_test_pred = (y_test_pred_proba >= recommended_threshold).astype(int)

test_precision = precision_score(y_test, y_test_pred, zero_division=0)
test_recall = recall_score(y_test, y_test_pred, zero_division=0)
test_f1 = f1_score(y_test, y_test_pred, zero_division=0)
test_auc_pr = average_precision_score(y_test, y_test_pred_proba)

print(f"Using threshold {recommended_threshold:.2f} on TEST SET:")
print(f"  Precision: {test_precision:.4f}")
print(f"  Recall:    {test_recall:.4f}")
print(f"  F1 Score:  {test_f1:.4f}")
print(f"  AUC-PR:    {test_auc_pr:.4f}")
print(f"  Flagged:   {y_test_pred.sum():,} out of {len(y_test):,} cases")
print()

# ============================================================================
# 7. BUSINESS TRADEOFF ANALYSIS
# ============================================================================
print("7. PRECISION-RECALL TRADEOFF ANALYSIS")
print("=" * 100)
print()

print("⚖️  TRADEOFF SUMMARY:")
print()
print("HIGH RECALL (Low Threshold):")
print(f"  ✓ Catch more minority class cases")
print(f"  ✗ More false alarms (lower precision)")
print(f"  → Best when: Cost of missing minority class >> Cost of false alarms")
print()
print("HIGH PRECISION (High Threshold):")
print(f"  ✓ Fewer false alarms")
print(f"  ✗ Miss some minority class cases")
print(f"  → Best when: Cost of false alarms >> Cost of missing minority class")
print()
print(f"BALANCED (F1 Optimized at {f1_optimal['Threshold']:.2f}):")
print(f"  ✓ Reasonable balance between precision and recall")
print(f"  → Best when: Both false alarms and missed cases are important")
print()

print("=" * 100)
print("THRESHOLD OPTIMIZATION COMPLETE - READY FOR PRODUCTION")
print("=" * 100)
print()

print(f"✅ PRODUCTION THRESHOLD: {recommended_threshold:.2f}")
print(f"   Business Priority: {BUSINESS_PRIORITY.upper()}")
print(f"   Test Set Performance:")
print(f"     - Precision: {test_precision:.4f}")
print(f"     - Recall:    {test_recall:.4f}")
print(f"     - F1 Score:  {test_f1:.4f}")
print()
print("Next steps:")
print("  1. Deploy model with recommended threshold")
print("  2. Monitor performance on production data")
print("  3. Retrain when drift detected")
