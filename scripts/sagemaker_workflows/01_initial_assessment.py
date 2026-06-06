#!/usr/bin/env python3
"""
Initial Data Assessment for Fraud Detection
============================================================================
Perform an initial assessment of dataset structure and data quality
before any cleaning, feature engineering, visualization, or machine learning.

Usage:
    python scripts/sagemaker_workflows/01_initial_assessment.py

    Optional: Set custom S3 path via environment variable:
    export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
    python scripts/sagemaker_workflows/01_initial_assessment.py
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get S3 path from environment variable or use default
S3_DATASET_PATH = os.getenv(
    'S3_DATASET_PATH',
    's3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv'
)

print("=" * 80)
print("INITIAL DATA ASSESSMENT - CREDIT CARD FRAUD DETECTION")
print("=" * 80)
print()

# ============================================================================
# 1. LOAD DATASET
# ============================================================================
print("1. DATA LOADING")
print("-" * 80)

print(f"Source: {S3_DATASET_PATH}")
try:
    df = pd.read_csv(S3_DATASET_PATH)
    print(f"✓ Data loaded successfully")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit(1)
print()

# ============================================================================
# 2. DATASET SHAPE
# ============================================================================
print("2. DATASET SHAPE")
print("-" * 80)
n_rows, n_cols = df.shape
print(f"Number of Rows (Records): {n_rows:,}")
print(f"Number of Columns (Features): {n_cols}")
print(f"Total Data Points: {n_rows * n_cols:,}")
print()

# ============================================================================
# 3. COLUMN NAMES AND DATA TYPES
# ============================================================================
print("3. COLUMN NAMES AND DATA TYPES")
print("-" * 80)
print(f"{'Column Name':<15} {'Data Type':<15} {'Unique Values':<20}")
print("-" * 80)
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col:<15} {str(df[col].dtype):<15} {unique_count:<20,}")
print()

# ============================================================================
# 4. FIRST 5 ROWS
# ============================================================================
print("4. FIRST 5 ROWS OF DATASET")
print("-" * 80)
print(df.head())
print()

# ============================================================================
# 5. MISSING VALUES ANALYSIS
# ============================================================================
print("5. MISSING VALUES ANALYSIS")
print("-" * 80)
missing_data = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum(),
    'Missing_Percentage': (df.isnull().sum() / len(df)) * 100
})
missing_data = missing_data.sort_values('Missing_Count', ascending=False)

print(f"{'Column':<15} {'Missing Count':<20} {'Missing %':<15}")
print("-" * 80)
for idx, row in missing_data.iterrows():
    print(f"{row['Column']:<15} {int(row['Missing_Count']):<20,} {row['Missing_Percentage']:<15.4f}%")

total_missing = df.isnull().sum().sum()
print()
print(f"Total Missing Values Across Dataset: {total_missing:,}")
print()

# ============================================================================
# 6. DUPLICATE RECORDS ANALYSIS
# ============================================================================
print("6. DUPLICATE RECORDS ANALYSIS")
print("-" * 80)
n_duplicates = df.duplicated().sum()
duplicate_percentage = (n_duplicates / len(df)) * 100

print(f"Number of Duplicate Rows: {n_duplicates:,}")
print(f"Percentage of Duplicates: {duplicate_percentage:.4f}%")
print()

# Check duplicates excluding 'Time' column
if 'Time' in df.columns:
    n_duplicates_no_time = df.drop(columns=['Time']).duplicated().sum()
    duplicate_percentage_no_time = (n_duplicates_no_time / len(df)) * 100
    print(f"Duplicate Rows (excluding Time column): {n_duplicates_no_time:,}")
    print(f"Percentage: {duplicate_percentage_no_time:.4f}%")
print()

# ============================================================================
# 7. BASIC DESCRIPTIVE STATISTICS
# ============================================================================
print("7. DESCRIPTIVE STATISTICS")
print("-" * 80)
print(df.describe())
print()

# ============================================================================
# 8. DATASET OVERVIEW SUMMARY
# ============================================================================
print("8. DATASET OVERVIEW SUMMARY")
print("=" * 80)
print()

print("📊 DATASET CHARACTERISTICS:")
print(f"   • Total Records: {n_rows:,}")
print(f"   • Total Features: {n_cols}")
print(f"   • Memory Usage: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
print()

# Identify target variable
if 'Class' in df.columns:
    fraud_count = df['Class'].sum()
    fraud_percentage = (fraud_count / len(df)) * 100
    print(f"🎯 TARGET VARIABLE (Class):")
    print(f"   • Legitimate Transactions (Class=0): {len(df) - int(fraud_count):,} ({100-fraud_percentage:.2f}%)")
    print(f"   • Fraudulent Transactions (Class=1): {int(fraud_count):,} ({fraud_percentage:.4f}%)")
    print(f"   • Class Imbalance Ratio: 1:{(len(df) - fraud_count)/fraud_count:.0f}")
    print()

# Feature type distribution
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

print(f"📋 FEATURE TYPES:")
print(f"   • Numeric Features: {len(numeric_cols)}")
print(f"   • Categorical Features: {len(categorical_cols)}")
print()

# ============================================================================
# 9. DATA QUALITY OBSERVATIONS
# ============================================================================
print("9. DATA QUALITY OBSERVATIONS")
print("=" * 80)
print()

observations = []

# Missing values
if total_missing == 0:
    observations.append("✓ EXCELLENT: No missing values detected in any column")
else:
    observations.append(f"⚠ WARNING: {total_missing:,} missing values found across dataset")

# Duplicates
if n_duplicates == 0:
    observations.append("✓ EXCELLENT: No duplicate records found")
else:
    observations.append(f"⚠ WARNING: {n_duplicates:,} duplicate rows detected ({duplicate_percentage:.4f}%)")

# Class imbalance
if 'Class' in df.columns and fraud_percentage < 1:
    observations.append(f"⚠ CRITICAL: Severe class imbalance detected ({fraud_percentage:.4f}% fraud)")

# Data types consistency
if len(categorical_cols) == 0:
    observations.append("✓ GOOD: All features are numeric (consistent data types)")

# Anonymized features (V1-V28)
v_features = [col for col in df.columns if col.startswith('V')]
if len(v_features) > 0:
    observations.append(f"ℹ INFO: {len(v_features)} anonymized PCA-transformed features (V1-V{len(v_features)})")

# Amount feature
if 'Amount' in df.columns:
    max_amount = df['Amount'].max()
    min_amount = df['Amount'].min()
    observations.append(f"ℹ INFO: Transaction amounts range from ${min_amount:.2f} to ${max_amount:,.2f}")

for obs in observations:
    print(f"   {obs}")
print()

# ============================================================================
# 10. POTENTIAL RISKS
# ============================================================================
print("10. POTENTIAL RISKS")
print("=" * 80)
print()

risks = []

if 'Class' in df.columns and fraud_percentage < 1:
    risks.append("🔴 HIGH: Extreme class imbalance may cause model bias toward majority class")
    risks.append("🔴 HIGH: Standard accuracy metrics will be misleading (need precision/recall/F1)")
    risks.append("🔴 HIGH: Require specialized sampling techniques (SMOTE, undersampling, etc.)")

if n_duplicates > 0:
    risks.append(f"🟡 MEDIUM: {n_duplicates:,} duplicates may inflate model performance if not handled")

if 'Amount' in df.columns:
    skewness = df['Amount'].skew()
    if abs(skewness) > 2:
        risks.append(f"🟡 MEDIUM: 'Amount' feature highly skewed (skewness={skewness:.2f}) - may need transformation")

if 'Time' in df.columns:
    risks.append("🟡 MEDIUM: 'Time' feature may introduce temporal bias or data leakage")

if len(v_features) > 0:
    risks.append("🟢 LOW: Anonymized features (PCA) prevent direct feature interpretation")

for risk in risks:
    print(f"   {risk}")
print()

# ============================================================================
# 11. RECOMMENDED NEXT STEPS
# ============================================================================
print("11. RECOMMENDED NEXT STEPS")
print("=" * 80)
print()

next_steps = [
    "1. DUPLICATE ASSESSMENT (SKILL2):",
    "   • Run 02_duplicate_cleaning.py to analyze and remove duplicates if needed",
    "",
    "2. MISSING VALUES (SKILL3):",
    "   • Run 03_missing_values.py to handle any missing data",
    "",
    "3. FEATURE ENGINEERING (SKILL4):",
    "   • Apply scaling and prepare train/val/test splits",
    "   • Transform skewed features (especially Amount)",
    "   • Ensure stratified splits to preserve class distribution",
    "",
    "4. EXPLORATORY ANALYSIS (SKILL5 - Optional):",
    "   • Visualize feature distributions and correlations",
    "   • Identify potential predictive features",
    "",
    "5. BASELINE MODELING (SKILL6):",
    "   • Train initial models with imbalance-handling strategies",
    "   • Compare different approaches (class weights, SMOTE, undersampling)",
    "",
    "6. THRESHOLD OPTIMIZATION (SKILL7):",
    "   • Find optimal decision threshold based on business priorities"
]

for step in next_steps:
    print(step)

print()
print("=" * 80)
print("INITIAL DATA ASSESSMENT COMPLETE")
print("=" * 80)
print()
print("Next: Run python scripts/sagemaker_workflows/02_duplicate_cleaning.py")
