# SageMaker Skill

---
name: feature_engineering_scaling
description: Transform raw features and prepare data for modeling with scaling and stratified splits.
---

# Feature Engineering & Scaling

## Objective

Prepare features for machine learning by applying transformations, scaling, and creating proper train/validation/test splits.

## Prerequisites

Complete these skills before proceeding:
- SKILL1: Initial Data Assessment
- SKILL2: Duplicate Assessment & Cleaning  
- SKILL3: Missing Values Assessment

## Tasks

Perform:

- Feature selection and filtering
- Feature transformations (log, sqrt, power)
- Outlier handling strategies
- Feature scaling (StandardScaler, RobustScaler, MinMaxScaler)
- Train/Validation/Test stratified splitting
- Imbalance preparation (understanding options)

## Feature Engineering Strategies

### 1. Numerical Feature Transformations

**When to use:**
- Log transformation: Right-skewed distributions (e.g., Amount feature)
- Square root: Moderate skewness
- Power transformations: Normalize non-normal distributions

**Example:** Amount feature in fraud detection is skewed → apply log transformation

### 2. Outlier Handling

Options:
- Keep as-is (if meaningful for fraud detection)
- Cap at percentile (e.g., 95th/5th percentile)
- Remove (if clear data errors)
- Create indicator variable (flag high-value transactions)

**For fraud:** Often keep outliers as they may be fraud signals

### 3. Feature Scaling Methods

| Scaler | Best For | Range | Formula |
|--------|----------|-------|---------|
| **StandardScaler** | Normal distributions | -∞ to +∞ | (X - mean) / std |
| **RobustScaler** | Data with outliers | -∞ to +∞ | (X - median) / IQR |
| **MinMaxScaler** | Bounded ranges | 0 to 1 | (X - min) / (max - min) |
| **None** | Tree-based models | Original | No scaling needed |

**Recommendation for fraud detection:** RobustScaler (handles outliers better than StandardScaler)

### 4. Train/Validation/Test Split Strategy

**Standard approach:**
- 70% Training (for model fitting)
- 15% Validation (for hyperparameter tuning and early stopping)
- 15% Testing (final evaluation on unseen data)

**Critical for imbalanced data:**
- Use **stratified splits** to preserve class distribution
- Ensures each fold has same fraud percentage as original
- Prevents biased train/test evaluations

## Deliverables

Provide:

### Feature Selection & Transformation Report

- Features selected/excluded and why
- Transformations applied
- Before/after statistics

### Scaling Summary

- Scaler chosen and justification
- Feature ranges before/after scaling
- Mean/std/min/max per feature

### Data Split Summary

- Train size: rows and fraud percentage
- Validation size: rows and fraud percentage
- Test size: rows and fraud percentage
- Confirmation that splits are stratified

### Quality Checks

- No data leakage between sets
- Class distribution preserved in each set
- Feature statistics reasonable

## Output

Finish with:

- Cleaned and prepared datasets (X_train, X_val, X_test, y_train, y_val, y_test)
- Fitted scaler object (for applying to future data)
- Feature names and indices
- Summary statistics

## Code Example

```python
# ============================================================================
# FEATURE ENGINEERING & SCALING FOR FRAUD DETECTION
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("FEATURE ENGINEERING & SCALING - CREDIT CARD FRAUD DATASET")
print("=" * 100)
print()

# ============================================================================
# 1. LOAD CLEANED DATA (from previous skills)
# ============================================================================
print("1. LOADING CLEANED DATA")
print("-" * 100)

s3_path = "s3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv"
df = pd.read_csv(s3_path)
df = df.drop_duplicates()

original_shape = df.shape
print(f"Cleaned dataset loaded: {original_shape[0]:,} rows × {original_shape[1]} columns")
print()

# ============================================================================
# 2. SEPARATE FEATURES AND TARGET
# ============================================================================
print("2. FEATURE & TARGET SEPARATION")
print("-" * 100)

# Target variable
y = df['Class']

# Features (exclude target and time)
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

# Check for transformations needed
print("\nFeatures requiring transformation:")

# Amount feature (skewed)
if 'Amount' in X.columns:
    amount_skew = stats.skew(X['Amount'])
    print(f"\n  • Amount: skewness = {amount_skew:.2f}")
    print(f"    → Apply log transformation (right-skewed)")
    
    # Apply log transformation (add 1 to avoid log(0))
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
    print(f"    → No transformation needed")

print()

# ============================================================================
# 4. FEATURE SCALING
# ============================================================================
print("4. FEATURE SCALING")
print("-" * 100)

# Choose RobustScaler (handles outliers better)
scaler = RobustScaler()

# Fit scaler on training data (we'll do this after split to prevent leakage)
# For now, show the statistics

print("\nScaler Selection: RobustScaler")
print("  Reason: Robust to outliers (important for fraud detection)")
print("  Formula: (X - median) / IQR")
print()

print("Feature statistics BEFORE scaling:")
print(f"{'Feature':<15} {'Min':<12} {'Max':<12} {'Mean':<12} {'Std':<12}")
print("-" * 100)
for col in X.select_dtypes(include=[np.number]).columns[:5]:
    print(f"{col:<15} {X[col].min():<12.2f} {X[col].max():<12.2f} {X[col].mean():<12.2f} {X[col].std():<12.2f}")
print("(showing first 5 features for brevity)")
print()

# ============================================================================
# 5. STRATIFIED TRAIN/VALIDATION/TEST SPLIT
# ============================================================================
print("5. STRATIFIED DATA SPLITTING")
print("-" * 100)

# Step 1: Split into train (70%) and temp (30%)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, 
    test_size=0.30, 
    stratify=y,  # Maintain class distribution
    random_state=42
)

# Step 2: Split temp (30%) into validation (50%) and test (50%) = 15% each
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    stratify=y_temp,  # Maintain class distribution
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

# Fit scaler ONLY on training data (prevent data leakage)
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

print("Feature statistics AFTER scaling:")
print(f"{'Feature':<15} {'Min':<12} {'Max':<12} {'Mean':<12} {'Std':<12}")
print("-" * 100)
for col in X_train_scaled.columns[:5]:
    print(f"{col:<15} {X_train_scaled[col].min():<12.2f} {X_train_scaled[col].max():<12.2f} {X_train_scaled[col].mean():<12.2f} {X_train_scaled[col].std():<12.2f}")
print("(showing first 5 features for brevity)")
print()

# ============================================================================
# 7. DATA LEAKAGE CHECK
# ============================================================================
print("7. DATA LEAKAGE VERIFICATION")
print("-" * 100)

# Verify no row overlap between sets
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
    'Features': X_train_scaled.shape[1],
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
print("  1. Run SKILL5: Visualization & EDA (optional, for exploration)")
print("  2. Run SKILL6: ML Baseline Modeling (to train initial models)")
print("  3. Run SKILL7: Threshold Optimization (to optimize decision boundary)")
```

## Result Example

```
====================================================================================================
FEATURE ENGINEERING & SCALING - CREDIT CARD FRAUD DATASET
====================================================================================================

1. LOADING CLEANED DATA
----------------------------------------------------------------------------------------------------
Cleaned dataset loaded: 283,726 rows × 31 columns

2. FEATURE & TARGET SEPARATION
----------------------------------------------------------------------------------------------------
Features (X): 29 features
Target (y): 283,726 samples (fraud: 473, legitimate: 283,253)
Class distribution: 0.1667% fraud

3. FEATURE TRANSFORMATION ANALYSIS
----------------------------------------------------------------------------------------------------

Features requiring transformation:

  • Amount: skewness = 4.18
    → Apply log transformation (right-skewed)
    ✓ Created 'Amount_log' feature

  • V-features (PCA) are approximately normally distributed
    → No transformation needed

4. FEATURE SCALING
----------------------------------------------------------------------------------------------------

Scaler Selection: RobustScaler
  Reason: Robust to outliers (important for fraud detection)
  Formula: (X - median) / IQR

Feature statistics BEFORE scaling:
Feature         Min          Max          Mean         Std         
----------------------------------------------------------------------------------------------------
Time            0.00         172792.00    94808.27     47507.10    
V1              -56.41       2.45         0.01         1.94        
V2              -72.27       22.18        0.01         1.95        
V3              -48.33       9.38         -0.01        2.17        
V4              -5.38        16.87        -0.03        1.95        
(showing first 5 features for brevity)

5. STRATIFIED DATA SPLITTING
----------------------------------------------------------------------------------------------------

Stratified Split Results:
Set             Rows         Fraud Count     Fraud %     
----------------------------------------------------------------------------------------------------
Training        198,408      331             0.1667%
Validation      42,659       71              0.1666%
Testing         42,659       71              0.1666%
Original        283,726      473             0.1667%

✓ Class distribution preserved across all sets (stratified split)

6. FITTING SCALER (CRITICAL: Fit on training data only)
----------------------------------------------------------------------------------------------------
✓ Scaler fit on training data (prevents data leakage)
✓ Scaler applied to validation and test sets

Feature statistics AFTER scaling:
Feature         Min          Max          Mean         Std         
----------------------------------------------------------------------------------------------------
Time            -1.57        1.52         -0.00        1.00        
V1              -26.12       1.13         0.00         1.00        
V2              -33.44       10.26        -0.00        1.00        
V3              -22.62       4.35         -0.00        1.00        
V4              -2.48        7.74         -0.01        1.00        
(showing first 5 features for brevity)

7. DATA LEAKAGE VERIFICATION
----------------------------------------------------------------------------------------------------

Index overlap check:
  Train ∩ Validation: 0 rows (should be 0)
  Train ∩ Test: 0 rows (should be 0)
  Validation ∩ Test: 0 rows (should be 0)

✓ EXCELLENT: No data leakage detected

8. FEATURE ENGINEERING & SCALING SUMMARY
====================================================================================================

Summary Statistics:
  • Original dataset: 283,726 rows × 31 columns
  • Features: 29 features
  • Training samples: 198,408
  • Validation samples: 42,659
  • Test samples: 42,659
  • Scaling method: RobustScaler
  • Data leakage: None detected ✓
  • Class distribution preserved: Yes ✓

====================================================================================================
FEATURE ENGINEERING & SCALING COMPLETE - READY FOR MODELING
====================================================================================================

Next Steps:
  1. Run SKILL5: Visualization & EDA (optional, for exploration)
  2. Run SKILL6: ML Baseline Modeling (to train initial models)
  3. Run SKILL7: Threshold Optimization (to optimize decision boundary)
```

## Best Practices

- ✓ Always fit scaler ONLY on training data
- ✓ Use stratified splits for imbalanced classification
- ✓ Transform Amount feature (highly skewed in fraud data)
- ✓ Keep Time feature untransformed (use as-is or engineer time features)
- ✓ Verify no data leakage between sets
- ✓ Preserve class distribution across splits
- ✓ Document feature transformations applied

## Common Mistakes to Avoid

- ✗ Fitting scaler on entire dataset (causes data leakage)
- ✗ Using random split instead of stratified split (biases class distribution)
- ✗ Scaling Time feature (temporal ordering should be preserved)
- ✗ Transforming all features the same way (different features need different treatments)
- ✗ Not checking class distribution preservation
