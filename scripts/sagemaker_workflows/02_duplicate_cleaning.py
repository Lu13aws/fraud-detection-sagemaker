#!/usr/bin/env python3
"""
Duplicate Records Analysis and Cleaning
============================================================================
Analyze duplicate records and remove them only when justified.

Usage:
    python scripts/sagemaker_workflows/02_duplicate_cleaning.py

    Optional: Set custom S3 path via environment variable:
    export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
    python scripts/sagemaker_workflows/02_duplicate_cleaning.py
"""

import pandas as pd
import numpy as np
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

print("=" * 80)
print("DUPLICATE RECORDS ANALYSIS - CREDIT CARD FRAUD DATASET")
print("=" * 80)

# Load dataset
df = pd.read_csv(S3_DATASET_PATH)

# Dataset shape before cleaning
original_shape = df.shape
print(f"\n📊 ORIGINAL DATASET SHAPE")
print(f"   Rows: {original_shape[0]:,}")
print(f"   Columns: {original_shape[1]}")

# 1. COUNT DUPLICATE ROWS
duplicate_mask = df.duplicated(keep=False)
num_duplicates = duplicate_mask.sum()
num_unique_duplicate_groups = df[duplicate_mask].duplicated(keep='first').sum()
num_duplicate_rows = df.duplicated().sum()

print(f"\n🔍 DUPLICATE ROW STATISTICS")
print(f"   Total duplicate rows (excluding first occurrence): {num_duplicate_rows:,}")
print(f"   Total rows involved in duplicates (including all): {num_duplicates:,}")
print(f"   Number of unique duplicate groups: {num_duplicates - num_duplicate_rows:,}")

# 2. CALCULATE DUPLICATE PERCENTAGE
duplicate_percentage = (num_duplicate_rows / len(df)) * 100
print(f"\n📈 DUPLICATE PERCENTAGE")
print(f"   {duplicate_percentage:.4f}% of dataset are exact duplicates")

# 3. COMPARE DUPLICATE AND NON-DUPLICATE RECORDS
if num_duplicates > 0:
    print(f"\n📋 COMPARISON: DUPLICATE vs NON-DUPLICATE RECORDS")

    duplicate_records = df[duplicate_mask]
    non_duplicate_records = df[~duplicate_mask]

    print(f"\n   Duplicate Records Statistics:")
    print(duplicate_records.describe())

    print(f"\n   Non-Duplicate Records Statistics:")
    print(non_duplicate_records.describe())

    # Check if duplicates contain fraud cases
    if 'Class' in df.columns:
        print(f"\n   🎯 FRAUD CLASS DISTRIBUTION")
        print(f"   Duplicates - Fraud cases: {duplicate_records['Class'].sum():,} ({duplicate_records['Class'].mean()*100:.2f}%)")
        print(f"   Non-Duplicates - Fraud cases: {non_duplicate_records['Class'].sum():,} ({non_duplicate_records['Class'].mean()*100:.2f}%)")
        print(f"   Overall - Fraud cases: {df['Class'].sum():,} ({df['Class'].mean()*100:.2f}%)")

# 4. ASSESS POTENTIAL IMPACT ON MODELING
print(f"\n⚠️  IMPACT ASSESSMENT FOR MODELING")
if num_duplicate_rows > 0:
    impact_level = "HIGH" if duplicate_percentage > 1 else "MODERATE" if duplicate_percentage > 0.1 else "LOW"
    print(f"   Impact Level: {impact_level}")
    print(f"   Potential Issues:")
    print(f"   • Duplicates can artificially inflate model performance on training data")
    print(f"   • Risk of data leakage if duplicates split across train/test sets")
    print(f"   • Biased importance weights for duplicated patterns")
    print(f"   • Overfitting to repeated observations")
else:
    print(f"   Impact Level: NONE")
    print(f"   ✅ No duplicates found - dataset is clean")

# 5. RECOMMENDATION
print(f"\n💡 RECOMMENDATION")
if num_duplicate_rows > 0:
    print(f"   ⚠️  REMOVE DUPLICATES")
    print(f"   Rationale:")
    print(f"   • {num_duplicate_rows:,} exact duplicate rows detected")
    print(f"   • These duplicates will bias model training and evaluation")
    print(f"   • Removing duplicates ensures each observation is unique")
    print(f"   • Critical for proper train/test split and cross-validation")

    # Remove duplicates
    df_cleaned = df.drop_duplicates()

    # Report removal results
    print(f"\n✅ DUPLICATES REMOVED")
    print(f"   Number of rows removed: {num_duplicate_rows:,}")
    print(f"   Percentage removed: {duplicate_percentage:.4f}%")

    # Show dataset shape after cleaning
    cleaned_shape = df_cleaned.shape
    print(f"\n📊 DATASET SHAPE AFTER CLEANING")
    print(f"   Before: {original_shape[0]:,} rows × {original_shape[1]} columns")
    print(f"   After:  {cleaned_shape[0]:,} rows × {cleaned_shape[1]} columns")
    print(f"   Reduction: {original_shape[0] - cleaned_shape[0]:,} rows")

    # Explain the impact
    print(f"\n📝 IMPACT EXPLANATION")
    print(f"   ✓ Each transaction is now represented exactly once")
    print(f"   ✓ Model will train on unique patterns only")
    print(f"   ✓ Reduced risk of overfitting to repeated observations")
    print(f"   ✓ More reliable performance metrics")
    print(f"   ✓ Proper statistical assumptions maintained")

    if 'Class' in df.columns:
        fraud_before = df['Class'].sum()
        fraud_after = df_cleaned['Class'].sum()
        print(f"   ✓ Fraud cases preserved: {fraud_after:,} (removed {fraud_before - fraud_after:,} duplicate fraud cases)")

    # Display sample of cleaned data
    print(f"\n📋 CLEANED DATASET PREVIEW")
    print(df_cleaned.head(10))

    # Save cleaned dataset
    print(f"\n✓ Use df_cleaned for next steps (SKILL3: Missing Values)")

else:
    print(f"   ✅ NO ACTION NEEDED")
    print(f"   • Dataset contains no duplicate rows")
    print(f"   • Data is ready for next step")
    print(f"\n📋 DATASET PREVIEW")
    print(df.head(10))

    df_cleaned = df

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - Next: python scripts/sagemaker_workflows/03_missing_values.py")
print("=" * 80)
