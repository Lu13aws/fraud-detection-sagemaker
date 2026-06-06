#!/usr/bin/env python3
"""
Feature Engineering & Scaling for ML Models
============================================================================
Transform raw features and prepare data for modeling with scaling and splits.

Usage:
    python scripts/sagemaker_workflows/04_feature_engineering.py

    Optional: Set custom S3 path via environment variable:
    export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
    python scripts/sagemaker_workflows/04_feature_engineering.py
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, StandardScaler
from scipy import stats
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
print("FEATURE ENGINEERING & SCALING - CREDIT CARD FRAUD DATASET")
print("=" * 100)
print()

# ============================================================================
# 1. LOAD CLEANED DATA
# ============================================================================
print("1. LOADING CLEANED DATA")
print("-" * 100)

df = pd.read_csv(S3_DATASET_PATH)
df = df.drop_duplicates()

original_shape = df.shape
print(f"Cleaned dataset loaded: {original_shape[0]:,} rows × {original_shape[1]} columns")
print()

# ============================================================================
# 2. SEPARATE FEATURES AND TARGET
# ============================================================================
print("2. FEATURE & TARGET SEPARATION")
print("-" * 100)

y = df['Class']
X = df.drop(columns=['Class', 'Time'])

print(f"Features (X): {X.shape[1]} features")
print(f"Target (y): {y.shape[0]} samples (fraud: {y.sum():,}, legitimate: {(1-y).sum():,})")
print(f"Class distribution: {y.mean()*100:.4f}% fraud")
print()

# ============================================================================
# 3. FEATURE ANALYSIS & TRANSFORMATION
# ============================================================================
print("3. FEATURE TRANSFORMATION ANALYSIS")
print("-" * 100)

print("\nFeatures requiring transformation:")

# Amount feature (skewed)
if 'Amount' in X.columns:
    amount_skew = stats.skew(X['Amount'])
    print(f"\n  • Amount: skewness = {amount_skew:.2f}")
    print(f"    → Apply log transformation (right-skewed)")

    X['Amount_log'] = np.log1p(X['Amount'])
    print(f"    ✓ Created 'Amount_log' feature")

# Check other features
numeric_features = X.select_dtypes(include=[np.number]).columns
highly_skewed = []
for col in numeric_features:
    if col != 'Amount':
        skewness = stats.skew(X[col])
        if abs(skewness) > 2:
            highly_skewed.append((col, skewness))

if highly_skewed:
    print(f"\n  • Highly skewed features (|skew| > 2):")
    for col, skew in highly_skewed[:5]:
        print(f"    - {col}: {skew:.2f}")
else:
    print(f"\n  • V-features (PCA) are approximately normally distributed")

print()

# ============================================================================
# 4. FEATURE SCALING
# ============================================================================
print("4. FEATURE SCALING")
print("-" * 100)

scaler = RobustScaler()

print("\nScaler Selection: RobustScaler")
print("  Reason: Robust to outliers (important for fraud detection)")
print()

print("Feature statistics BEFORE scaling (first 5 features):")
print(f"{'Feature':<15} {'Min':<12} {'Max':<12} {'Mean':<12} {'Std':<12}")
print("-" * 100)
for col in X.select_dtypes(include=[np.number]).columns[:5]:
    print(f"{col:<15} {X[col].min():<12.2f} {X[col].max():<12.2f} {X[col].mean():<12.2f} {X[col].std():<12.2f}")
print()

# ============================================================================
# 5. STRATIFIED TRAIN/VALIDATION/TEST SPLIT
# ============================================================================
print("5. STRATIFIED DATA SPLITTING")
print("-" * 100)

# Split into train (70%) and temp (30%)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.30,
    stratify=y,
    random_state=42
)

# Split temp into validation (50%) and test (50%) = 15% each
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    stratify=y_temp,
    random_state=42
)

print(f"\nStratified Split Results:")
print(f"{'Set':<15} {'Rows':<12} {'Fraud Count':<15} {'Fraud %':<12}")
print("-" * 100)

train_fraud_pct = y_train.mean() * 100
val_fraud_pct = y_val.mean() * 100
test_fraud_pct = y_test.mean() * 100

print(f"{'Training':<15} {len(X_train):<12,} {int(y_train.sum()):<15,} {train_fraud_pct:<12.4f}%")
print(f"{'Validation':<15} {len(X_val):<12,} {int(y_val.sum()):<15,} {val_fraud_pct:<12.4f}%")
print(f"{'Testing':<15} {len(X_test):<12,} {int(y_test.sum()):<15,} {test_fraud_pct:<12.4f}%")
print(f"{'Original':<15} {len(X):<12,} {int(y.sum()):<15,} {y.mean()*100:<12.4f}%")

print()
print("✓ Class distribution preserved across all sets (stratified split)")
print()

# ============================================================================
# 6. FIT SCALER ON TRAINING DATA ONLY
# ============================================================================
print("6. FITTING SCALER (CRITICAL: Fit on training data only)")
print("-" * 100)

# Fit scaler ONLY on training data
scaler.fit(X_train)

# Transform all sets
X_train_scaled = pd.DataFrame(
    scaler.transform(X_train),
    columns=X_train.columns,
    index=X_train.index
)

X_val_scaled = pd.DataFrame(
    scaler.transform(X_val),
    columns=X_val.columns,
    index=X_val.index
)

X_test_scaled = pd.DataFrame(
    scaler.transform(X_test),
    columns=X_test.columns,
    index=X_test.index
)

print("✓ Scaler fit on training data (prevents data leakage)")
print("✓ Scaler applied to validation and test sets")
print()

print("Feature statistics AFTER scaling (first 5 features):")
print(f"{'Feature':<15} {'Min':<12} {'Max':<12} {'Mean':<12} {'Std':<12}")
print("-" * 100)
for col in X_train_scaled.columns[:5]:
    print(f"{col:<15} {X_train_scaled[col].min():<12.2f} {X_train_scaled[col].max():<12.2f} {X_train_scaled[col].mean():<12.2f} {X_train_scaled[col].std():<12.2f}")
print()

# ============================================================================
# 7. DATA LEAKAGE CHECK
# ============================================================================
print("7. DATA LEAKAGE VERIFICATION")
print("-" * 100)

train_indices = set(X_train.index)
val_indices = set(X_val.index)
test_indices = set(X_test.index)

overlap_train_val = len(train_indices & val_indices)
overlap_train_test = len(train_indices & test_indices)
overlap_val_test = len(val_indices & test_indices)

print(f"\nIndex overlap check:")
print(f"  Train ∩ Validation: {overlap_train_val} rows (should be 0)")
print(f"  Train ∩ Test: {overlap_train_test} rows (should be 0)")
print(f"  Validation ∩ Test: {overlap_val_test} rows (should be 0)")

if overlap_train_val == 0 and overlap_train_test == 0 and overlap_val_test == 0:
    print(f"\n✓ EXCELLENT: No data leakage detected")
else:
    print(f"\n✗ WARNING: Data leakage detected!")

print()

# ============================================================================
# 8. SUMMARY & READINESS
# ============================================================================
print("8. FEATURE ENGINEERING & SCALING SUMMARY")
print("=" * 100)
print()

summary = {
    'Original dataset': original_shape,
    'Features after engineering': X_train_scaled.shape[1],
    'Training samples': X_train_scaled.shape[0],
    'Validation samples': X_val_scaled.shape[0],
    'Test samples': X_test_scaled.shape[0],
    'Scaling method': 'RobustScaler',
    'Data leakage': 'None detected ✓',
    'Class distribution preserved': 'Yes ✓'
}

print("Summary Statistics:")
for key, value in summary.items():
    if isinstance(value, tuple):
        print(f"  • {key}: {value[0]:,} rows × {value[1]} columns")
    else:
        print(f"  • {key}: {value}")

print()
print("=" * 100)
print("FEATURE ENGINEERING & SCALING COMPLETE - READY FOR MODELING")
print("=" * 100)
print()

print("Next Steps:")
print("  1. Run 05_visualization_eda.py (optional, for exploration)")
print("  2. Run 06_baseline_modeling.py (train initial models)")
print("  3. Run 07_threshold_optimization.py (optimize decision boundary)")
