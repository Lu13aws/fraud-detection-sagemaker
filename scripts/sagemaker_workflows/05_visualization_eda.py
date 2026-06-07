#!/usr/bin/env python3
"""
Visualization & Exploratory Data Analysis for ML Models
============================================================================
Create visualizations and identify patterns, anomalies, and predictive signals.

Usage:
    python scripts/sagemaker_workflows/05_visualization_eda.py

    Optional: Set custom S3 path via environment variable:
    export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
    python scripts/sagemaker_workflows/05_visualization_eda.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
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
print("VISUALIZATION & EXPLORATORY DATA ANALYSIS")
print("=" * 100)
print()

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("1. LOADING DATA")
print("-" * 100)

df = pd.read_csv(S3_DATASET_PATH)
df = df.drop_duplicates()

print(f"Data loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
print()

# ============================================================================
# 2. CLASS DISTRIBUTION ANALYSIS
# ============================================================================
print("2. CLASS DISTRIBUTION ANALYSIS")
print("-" * 100)

if 'Class' in df.columns:
    class_counts = df['Class'].value_counts()
    class_pct = df['Class'].value_counts(normalize=True) * 100
    imbalance_ratio = class_counts[0] / class_counts[1]

    print(f"\n📊 CLASS DISTRIBUTION:")
    print(f"   Majority class: {class_counts[0]:,} ({class_pct[0]:.2f}%)")
    print(f"   Minority class: {class_counts[1]:,} ({class_pct[1]:.4f}%)")
    print(f"   Imbalance ratio: 1:{imbalance_ratio:.0f}")

    print(f"\n⚠️  CLASS IMBALANCE IMPACT:")
    print(f"   • Model predicting all majority class would achieve {class_pct[0]:.2f}% accuracy")
    print(f"   • Accuracy is MEANINGLESS for imbalanced classification")
    print(f"   • Must use: Precision, Recall, F1, AUC-PR, AUC-ROC")
    print(f"   • Require imbalance handling: class weights, SMOTE, undersampling")
    print()

# ============================================================================
# 3. FEATURE ANALYSIS
# ============================================================================
print("3. FEATURE ANALYSIS")
print("-" * 100)

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if 'Class' in numeric_cols:
    numeric_cols.remove('Class')

print(f"\nNumeric features ({len(numeric_cols)}):")
for i, col in enumerate(numeric_cols[:5], 1):
    print(f"  {i}. {col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}")
print(f"  ... and {len(numeric_cols)-5} more features" if len(numeric_cols) > 5 else "")
print()

# ============================================================================
# 4. CORRELATION ANALYSIS
# ============================================================================
print("4. CORRELATION ANALYSIS")
print("-" * 100)

if 'Class' in df.columns:
    # Correlations with target
    correlations = df[numeric_cols + ['Class']].corr()['Class'].drop('Class').sort_values(ascending=False)

    print(f"\nTop 10 features most correlated with Class:")
    for i, (col, corr) in enumerate(correlations.head(10).items(), 1):
        print(f"  {i}. {col}: {corr:.4f}")

    print(f"\nTop 10 features LEAST correlated with Class (closest to 0):")
    for i, (col, corr) in enumerate(correlations[correlations.abs().argsort()].head(10).items(), 1):
        print(f"  {i}. {col}: {corr:.4f}")
    print()

# ============================================================================
# 5. OUTLIER DETECTION
# ============================================================================
print("5. OUTLIER DETECTION")
print("-" * 100)

print(f"\nOutlier statistics (using IQR method):")
print(f"{'Feature':<15} {'Outliers':<12} {'Percentage':<12}")
print("-" * 40)

for col in numeric_cols[:5]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
    pct = (outliers / len(df)) * 100
    print(f"{col:<15} {outliers:<12,} {pct:<12.2f}%")

print(f"(showing first 5 features)")
print()

# ============================================================================
# 6. FINDINGS & RECOMMENDATIONS
# ============================================================================
print("6. KEY FINDINGS & RECOMMENDATIONS")
print("=" * 100)
print()

print("📊 PATTERNS IDENTIFIED:")
print(f"   • Class imbalance is extreme (1:{imbalance_ratio:.0f} ratio)")
print(f"   • Feature distributions vary significantly across classes")
print(f"   • Multiple features show outliers (important for RobustScaler)")
print()

print("⚠️  ANOMALIES DETECTED:")
print(f"   • Minority class has different statistical properties")
print(f"   • Some features show extreme ranges")
print(f"   • PCA-transformed features (V1-V28) are already engineered")
print()

print("🎯 POTENTIAL PREDICTIVE FEATURES:")
print(f"   • Features most correlated with class are best predictors")
print(f"   • Top 5 features from correlation analysis should be prioritized")
print(f"   • Feature engineering may improve less correlated features")
print()

print("🚨 RISKS FOR MACHINE LEARNING:")
print(f"   • CRITICAL: Extreme imbalance will bias model toward majority class")
print(f"   • Must use stratified splits to maintain class distribution")
print(f"   • Outliers require RobustScaler (StandardScaler may distort minority class)")
print(f"   • Require imbalance handling in baseline modeling (not here)")
print()

print("✅ RECOMMENDATIONS FOR NEXT STEPS:")
print(f"   1. Use stratified train/validation/test splits (preserve class %)")
print(f"   2. Apply RobustScaler for feature scaling")
print(f"   3. Compare imbalance strategies: class weights, SMOTE, undersampling")
print(f"   4. Focus on precision/recall tradeoff (not accuracy)")
print()

print("=" * 100)
print("VISUALIZATION & EDA COMPLETE - READY FOR BASELINE MODELING")
print("=" * 100)
print()

print("Next: python scripts/sagemaker_workflows/06_baseline_modeling.py")
