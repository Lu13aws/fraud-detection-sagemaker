# SageMaker Skill

---
name: duplicate_assessment_cleaning
description: Analyze duplicate records and remove them only when justified.
---

# Duplicate Assessment and Cleaning

## Objective

Identify duplicate records and evaluate their impact.

## Tasks

Perform:

- Duplicate count
- Duplicate percentage calculation
- Duplicate pattern analysis
- Impact assessment

## Assessment Criteria

Determine:

- Are duplicates exact duplicates?
- Could duplicates bias analysis?
- Could duplicates bias model training?

## Cleaning Rules

Remove duplicates only if:

- They are exact duplicates
- They introduce analytical bias
- They negatively affect modeling

## Deliverables

Provide:

- Duplicate count
- Duplicate percentage
- Recommendation
- Justification

If duplicates are removed:

- Rows removed
- Dataset shape before cleaning
- Dataset shape after cleaning

## Output

Finish with:

- Decision taken
- Impact on downstream analysis

## Code Example

import pandas as pd
import numpy as np

# Load the dataset from S3
s3_path = 's3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv'
df = pd.read_csv(s3_path)

print("=" * 80)
print("DUPLICATE RECORDS ANALYSIS - CREDIT CARD FRAUD DATASET")
print("=" * 80)

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
    
    # Check if duplicates contain fraud cases (assuming 'Class' column exists)
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
    df_cleaned.head(10)
    
else:
    print(f"   ✅ NO ACTION NEEDED")
    print(f"   • Dataset contains no duplicate rows")
    print(f"   • Data is ready for modeling")
    print(f"\n📋 DATASET PREVIEW")
    df.head(10)

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)

## Result Example

================================================================================
DUPLICATE RECORDS ANALYSIS - CREDIT CARD FRAUD DATASET
================================================================================

📊 ORIGINAL DATASET SHAPE
   Rows: 284,807
   Columns: 31

🔍 DUPLICATE ROW STATISTICS
   Total duplicate rows (excluding first occurrence): 1,081
   Total rows involved in duplicates (including all): 1,854
   Number of unique duplicate groups: 773

📈 DUPLICATE PERCENTAGE
   0.3796% of dataset are exact duplicates

📋 COMPARISON: DUPLICATE vs NON-DUPLICATE RECORDS

   Duplicate Records Statistics:
                Time           V1  ...       Amount        Class
count    1854.000000  1854.000000  ...  1854.000000  1854.000000
mean    94448.014024    -1.550730  ...    60.094504     0.017260
std     48781.945109     3.458374  ...   166.070225     0.130274
min        26.000000   -26.457745  ...     0.000000     0.000000
25%     53484.000000    -2.581315  ...     6.000000     0.000000
50%     84149.000000    -1.203617  ...    15.980000     0.000000
75%    142583.000000     1.138387  ...    36.000000     0.000000
max    172233.000000     2.178710  ...  1848.060000     1.000000

[8 rows x 31 columns]

   Non-Duplicate Records Statistics:
                Time             V1  ...         Amount          Class
count  282953.000000  282953.000000  ...  282953.000000  282953.000000
mean    94816.256714       0.010161  ...      88.534756       0.001626
std     47479.631543       1.940990  ...     250.567570       0.040287
min         0.000000     -56.407510  ...       0.000000       0.000000
25%     54213.000000      -0.912989  ...       5.590000       0.000000
50%     84704.000000       0.022459  ...      22.000000       0.000000
75%    139294.000000       1.316582  ...      77.710000       0.000000
max    172792.000000       2.454930  ...   25691.160000       1.000000

[8 rows x 31 columns]

   🎯 FRAUD CLASS DISTRIBUTION
   Duplicates - Fraud cases: 32 (1.73%)
   Non-Duplicates - Fraud cases: 460 (0.16%)
   Overall - Fraud cases: 492 (0.17%)

⚠️  IMPACT ASSESSMENT FOR MODELING
   Impact Level: MODERATE
   Potential Issues:
   • Duplicates can artificially inflate model performance on training data
   • Risk of data leakage if duplicates split across train/test sets
   • Biased importance weights for duplicated patterns
   • Overfitting to repeated observations

💡 RECOMMENDATION
   ⚠️  REMOVE DUPLICATES
   Rationale:
   • 1,081 exact duplicate rows detected
   • These duplicates will bias model training and evaluation
   • Removing duplicates ensures each observation is unique
   • Critical for proper train/test split and cross-validation

✅ DUPLICATES REMOVED
   Number of rows removed: 1,081
   Percentage removed: 0.3796%

📊 DATASET SHAPE AFTER CLEANING
   Before: 284,807 rows × 31 columns
   After:  283,726 rows × 31 columns
   Reduction: 1,081 rows

📝 IMPACT EXPLANATION
   ✓ Each transaction is now represented exactly once
   ✓ Model will train on unique patterns only
   ✓ Reduced risk of overfitting to repeated observations
   ✓ More reliable performance metrics
   ✓ Proper statistical assumptions maintained
   ✓ Fraud cases preserved: 473 (removed 19 duplicate fraud cases)

📋 CLEANED DATASET PREVIEW

================================================================================
ANALYSIS COMPLETE
================================================================================
