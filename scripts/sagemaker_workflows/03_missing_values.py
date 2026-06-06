#!/usr/bin/env python3
"""
Missing Values Assessment and Treatment
============================================================================
Analyze missing values and recommend appropriate treatment strategies.

Usage:
    python scripts/sagemaker_workflows/03_missing_values.py

    Optional: Set custom S3 path via environment variable:
    export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
    python scripts/sagemaker_workflows/03_missing_values.py
"""

import pandas as pd
import numpy as np
import os
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

print("=" * 80)
print("MISSING VALUE ANALYSIS - CREDIT CARD FRAUD DATASET")
print("=" * 80)

# Load and clean data
df = pd.read_csv(S3_DATASET_PATH)
df = df.drop_duplicates()

print(f"\nDataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Total Cells: {df.shape[0] * df.shape[1]:,}")

# ============================================================================
# 1. IDENTIFY MISSING VALUES PER COLUMN
# ============================================================================
print("\n" + "=" * 80)
print("1. MISSING VALUES IDENTIFICATION")
print("=" * 80)

missing_summary = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum(),
    'Missing_Percentage': (df.isnull().sum() / len(df) * 100).round(2),
    'Data_Type': df.dtypes,
    'Non_Null_Count': df.notnull().sum(),
    'Unique_Values': df.nunique()
})

missing_summary = missing_summary.sort_values('Missing_Percentage', ascending=False)
missing_summary['Severity'] = missing_summary['Missing_Percentage'].apply(
    lambda x: 'CRITICAL' if x > 50 else ('HIGH' if x > 20 else ('MODERATE' if x > 5 else ('LOW' if x > 0 else 'NONE')))
)

print("\nMissing Value Summary:")
print(missing_summary)

# ============================================================================
# 2. ASSESS SEVERITY AND IMPACT
# ============================================================================
print("\n" + "=" * 80)
print("2. SEVERITY ASSESSMENT")
print("=" * 80)

severity_stats = missing_summary['Severity'].value_counts()
print("\nSeverity Distribution:")
for severity in ['CRITICAL', 'HIGH', 'MODERATE', 'LOW', 'NONE']:
    count = severity_stats.get(severity, 0)
    print(f"  {severity}: {count} columns")

total_missing = df.isnull().sum().sum()
total_cells = df.shape[0] * df.shape[1]
overall_missing_pct = (total_missing / total_cells * 100)

print(f"\nOverall Data Completeness:")
print(f"  Total Missing Values: {total_missing:,}")
print(f"  Overall Missing Percentage: {overall_missing_pct:.2f}%")
print(f"  Data Completeness: {100 - overall_missing_pct:.2f}%")

# ============================================================================
# 3. DETAILED ANALYSIS FOR COLUMNS WITH MISSING VALUES
# ============================================================================
columns_with_missing = missing_summary[missing_summary['Missing_Count'] > 0]['Column'].tolist()

if columns_with_missing:
    print("\n" + "=" * 80)
    print("3. DETAILED COLUMN ANALYSIS & TREATMENT RECOMMENDATIONS")
    print("=" * 80)

    for col in columns_with_missing:
        missing_pct = missing_summary[missing_summary['Column'] == col]['Missing_Percentage'].values[0]
        severity = missing_summary[missing_summary['Column'] == col]['Severity'].values[0]
        dtype = df[col].dtype

        print(f"\n{'─' * 80}")
        print(f"Column: {col} | Missing: {missing_pct:.2f}% | Severity: {severity}")
        print(f"{'─' * 80}")

        # Treatment determination based on severity and data type
        if missing_pct > 70:
            treatment = "Feature Removal"
            reasoning = f"Over 70% missing ({missing_pct:.2f}%). Insufficient data for reliable imputation."
        elif pd.api.types.is_numeric_dtype(dtype):
            if missing_pct < 5:
                treatment = "Mean or Median Imputation"
                reasoning = f"Low missingness ({missing_pct:.2f}%) in numeric feature. Simple imputation sufficient."
            else:
                treatment = "KNN Imputation"
                reasoning = f"Moderate missingness ({missing_pct:.2f}%). KNN leverages feature relationships."
        else:
            treatment = "Mode Imputation or Feature Removal"
            reasoning = f"Categorical feature with {missing_pct:.2f}% missing. Mode imputation or removal."

        print(f"  RECOMMENDED: {treatment}")
        print(f"  REASONING: {reasoning}")

else:
    print("\n" + "=" * 80)
    print("✓ EXCELLENT DATA QUALITY - NO MISSING VALUES DETECTED")
    print("=" * 80)
    print("\nThis dataset is complete with no missing values.")
    print("No imputation or treatment required.")
    print("\nData Quality Score: 100%")

# ============================================================================
# 5. DATA QUALITY SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("5. DATA QUALITY SUMMARY & RECOMMENDATIONS")
print("=" * 80)

if len(columns_with_missing) == 0:
    print("\n✓ Dataset Quality: EXCELLENT")
    print("  • All columns are complete with no missing values")
    print("  • Dataset is ready for feature engineering (SKILL4)")
    df_cleaned = df
else:
    critical_cols = missing_summary[missing_summary['Severity'] == 'CRITICAL'].shape[0]
    print(f"\n✓ Dataset Quality: {critical_cols} columns require attention")
    print(f"  • Columns with missing values: {len(columns_with_missing)}")
    print(f"  • Overall data completeness: {100 - overall_missing_pct:.2f}%")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - Next: python scripts/sagemaker_workflows/04_feature_engineering.py")
print("=" * 80)
