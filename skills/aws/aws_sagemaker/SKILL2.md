# SageMaker Skill

name: initial_data_assessment
description: Perform an initial assessment of dataset structure and data quality before any cleaning, feature engineering, visualization, or machine learning.
---

# Initial Data Assessment

## Objective

Understand the dataset before making any modifications.

## Tasks

Perform:

- Dataset shape analysis
- Column inspection
- Data type inspection
- Sample record review
- Missing value detection
- Duplicate detection
- Basic descriptive statistics

## Deliverables

Provide:

### Dataset Overview

- Number of rows
- Number of columns
- Column names
- Data types

### Data Quality Overview

- Missing values
- Duplicate records
- Potential data quality risks

### Summary Statistics

For numerical columns:

- Count
- Mean
- Median
- Standard Deviation
- Min
- Max

## Rules

- Do not modify data
- Do not remove duplicates
- Do not treat missing values
- Do not generate visualizations
- Do not perform feature engineering
- Do not train models

## Output

Finish with:

- Key observations
- Risks identified
- Recommended next steps

## Code Example

# ============================================================================
# INITIAL DATA ASSESSMENT
# Credit Card Fraud Detection Dataset
# ============================================================================

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("INITIAL DATA ASSESSMENT - CREDIT CARD FRAUD DETECTION")
print("="*80)
print()

# ============================================================================
# 1. LOAD DATASET
# ============================================================================
print("1. DATA LOADING")
print("-" * 80)

s3_path = "s3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv"
print(f"Source: {s3_path}")
df = pd.read_csv(s3_path)
print(f"✓ Data loaded successfully")
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
df.head()

# ============================================================================
# 5. MISSING VALUES ANALYSIS
# ============================================================================
print("\n5. MISSING VALUES ANALYSIS")
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

# Check duplicates excluding 'Time' column (as transactions at different times might be identical)
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
df.describe()

# ============================================================================
# 8. DATASET OVERVIEW SUMMARY
# ============================================================================
print("\n8. DATASET OVERVIEW SUMMARY")
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
    "1. EXPLORATORY DATA ANALYSIS (EDA):",
    "   • Analyze distribution of all features (histograms, box plots)",
    "   • Examine correlations between features and target variable",
    "   • Identify outliers using IQR or z-score methods",
    "   • Visualize fraud vs legitimate transaction patterns",
    "",
    "2. FEATURE ENGINEERING:",
    "   • Consider log transformation for 'Amount' (reduce skewness)",
    "   • Extract time-based features (hour, day, etc.) from 'Time' if applicable",
    "   • Create interaction features between V-features if meaningful",
    "   • Standardize/normalize features if needed for modeling",
    "",
    "3. HANDLE CLASS IMBALANCE:",
    "   • Apply SMOTE (Synthetic Minority Over-sampling Technique)",
    "   • Consider random undersampling of majority class",
    "   • Use stratified train-test split to preserve class distribution",
    "   • Implement class weights in model training",
    "",
    "4. DATA VALIDATION:",
    "   • Investigate duplicate records (are they legitimate repeat transactions?)",
    "   • Verify data integrity across all features",
    "   • Check for any data leakage issues",
    "",
    "5. MODELING PREPARATION:",
    "   • Split data: 70% train, 15% validation, 15% test (stratified)",
    "   • Define evaluation metrics: Precision, Recall, F1-Score, AUC-ROC, PR-AUC",
    "   • Consider anomaly detection algorithms (Isolation Forest, Autoencoder)",
    "   • Baseline model: Logistic Regression with class weights"
]

for step in next_steps:
    print(step)

print()
print("="*80)
print("INITIAL DATA ASSESSMENT COMPLETE")
print("="*80)

## Result Example

================================================================================
INITIAL DATA ASSESSMENT - CREDIT CARD FRAUD DETECTION
================================================================================

1. DATA LOADING
--------------------------------------------------------------------------------
Source: s3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv
✓ Data loaded successfully

2. DATASET SHAPE
--------------------------------------------------------------------------------
Number of Rows (Records): 284,807
Number of Columns (Features): 31
Total Data Points: 8,829,017

3. COLUMN NAMES AND DATA TYPES
--------------------------------------------------------------------------------
Column Name     Data Type       Unique Values       
--------------------------------------------------------------------------------
Time            float64         124,592             
V1              float64         275,663             
V2              float64         275,663             
V3              float64         275,663             
V4              float64         275,663             
V5              float64         275,663             
V6              float64         275,663             
V7              float64         275,663             
V8              float64         275,663             
V9              float64         275,663             
V10             float64         275,663             
V11             float64         275,663             
V12             float64         275,663             
V13             float64         275,663             
V14             float64         275,663             
V15             float64         275,663             
V16             float64         275,663             
V17             float64         275,663             
V18             float64         275,663             
V19             float64         275,663             
V20             float64         275,663             
V21             float64         275,663             
V22             float64         275,663             
V23             float64         275,663             
V24             float64         275,663             
V25             float64         275,663             
V26             float64         275,663             
V27             float64         275,663             
V28             float64         275,663             
Amount          float64         32,767              
Class           int64           2                   

4. FIRST 5 ROWS OF DATASET
--------------------------------------------------------------------------------

5. MISSING VALUES ANALYSIS
--------------------------------------------------------------------------------
Column          Missing Count        Missing %      
--------------------------------------------------------------------------------
Time            0                    0.0000         %
V1              0                    0.0000         %
V2              0                    0.0000         %
V3              0                    0.0000         %
V4              0                    0.0000         %
V5              0                    0.0000         %
V6              0                    0.0000         %
V7              0                    0.0000         %
V8              0                    0.0000         %
V9              0                    0.0000         %
V10             0                    0.0000         %
V11             0                    0.0000         %
V12             0                    0.0000         %
V13             0                    0.0000         %
V14             0                    0.0000         %
V15             0                    0.0000         %
V16             0                    0.0000         %
V17             0                    0.0000         %
V18             0                    0.0000         %
V19             0                    0.0000         %
V20             0                    0.0000         %
V21             0                    0.0000         %
V22             0                    0.0000         %
V23             0                    0.0000         %
V24             0                    0.0000         %
V25             0                    0.0000         %
V26             0                    0.0000         %
V27             0                    0.0000         %
V28             0                    0.0000         %
Amount          0                    0.0000         %
Class           0                    0.0000         %

Total Missing Values Across Dataset: 0

6. DUPLICATE RECORDS ANALYSIS
--------------------------------------------------------------------------------
Number of Duplicate Rows: 1,081
Percentage of Duplicates: 0.3796%

Duplicate Rows (excluding Time column): 9,144
Percentage: 3.2106%

7. DESCRIPTIVE STATISTICS
--------------------------------------------------------------------------------
