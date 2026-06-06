# ML Baseline Modeling Skill

## Purpose

Create a reliable baseline machine learning model before using advanced algorithms.

Use this skill when a cleaned dataset is ready for initial modeling.

## Objectives

* Prepare features and target
* Create stratified train/validation/test splits
* Scale numerical features when needed
* Train a simple baseline model
* Evaluate model performance using appropriate metrics

## Recommended Baseline Models

Classification:

* Logistic Regression
* Decision Tree Classifier

Regression:

* Linear Regression
* Decision Tree Regressor

## Required Steps

1. Define feature matrix `X` and target variable `y`
2. Create stratified splits for classification problems
3. Apply scaling where appropriate
4. Train baseline model
5. Generate predictions and prediction probabilities
6. Evaluate performance

## Metrics

For classification:

* Precision
* Recall
* F1 Score
* ROC-AUC
* PR-AUC
* Confusion Matrix

For imbalanced classification, do not use accuracy as the primary metric.

## Output

Provide:

* Dataset split summary
* Baseline model performance
* Metric interpretation
* Limitations
* Recommended next step

## Code Example


# ============================================================================
# FRAUD DETECTION - BASELINE MODEL WITH IMBALANCE STRATEGIES
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    precision_score, recall_score, f1_score, 
    roc_auc_score, roc_curve, 
    precision_recall_curve, auc, average_precision_score
)
from sklearn.utils.class_weight import compute_class_weight
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("FRAUD DETECTION - BASELINE MODEL COMPARISON")
print("=" * 100)
print()

# ============================================================================
# 1. LOAD CLEANED DATA
# ============================================================================
print("1. LOADING CLEANED DATA")
print("-" * 100)

# Use df_cleaned from previous cell if available
if 'df_cleaned' not in locals():
    s3_path = 's3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv'
    df_cleaned = pd.read_csv(s3_path)
    df_cleaned = df_cleaned.drop_duplicates()
    print(f"✓ Data loaded from S3 and duplicates removed")
else:
    print(f"✓ Using existing cleaned dataset")

print(f"   Dataset shape: {df_cleaned.shape}")
print(f"   Fraud cases: {df_cleaned['Class'].sum():,} ({df_cleaned['Class'].mean()*100:.4f}%)")
print()

# ============================================================================
# 2. PREPARE FEATURES AND TARGET
# ============================================================================
print("2. FEATURE PREPARATION")
print("-" * 100)

# Separate features and target
X = df_cleaned.drop('Class', axis=1)
y = df_cleaned['Class']

# Identify feature types for scaling
v_features = [col for col in X.columns if col.startswith('V')]
other_features = ['Time', 'Amount']

print(f"✓ Total features: {X.shape[1]}")
print(f"   • PCA features (V1-V28): {len(v_features)}")
print(f"   • Other features: {other_features}")
print()

# ============================================================================
# 3. STRATIFIED TRAIN-VAL-TEST SPLIT
# ============================================================================
print("3. CREATING STRATIFIED TRAIN-VALIDATION-TEST SPLITS")
print("-" * 100)

# First split: 70% train, 30% temp (for val+test)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

# Second split: 50-50 of temp = 15% val, 15% test
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)

# Calculate fraud percentages
train_fraud_pct = y_train.mean() * 100
val_fraud_pct = y_val.mean() * 100
test_fraud_pct = y_test.mean() * 100

print(f"✓ Data split completed:")
print(f"   Train set: {X_train.shape[0]:,} samples ({X_train.shape[0]/len(X)*100:.1f}%) - Fraud: {train_fraud_pct:.4f}%")
print(f"   Val set:   {X_val.shape[0]:,} samples ({X_val.shape[0]/len(X)*100:.1f}%) - Fraud: {val_fraud_pct:.4f}%")
print(f"   Test set:  {X_test.shape[0]:,} samples ({X_test.shape[0]/len(X)*100:.1f}%) - Fraud: {test_fraud_pct:.4f}%")
print()

# ============================================================================
# 4. FEATURE SCALING
# ============================================================================
print("4. FEATURE SCALING")
print("-" * 100)

scaler_robust = RobustScaler()
scaler_standard = StandardScaler()

# Create copies for scaling
X_train_scaled = X_train.copy()
X_val_scaled = X_val.copy()
X_test_scaled = X_test.copy()

# Scale Amount with RobustScaler
X_train_scaled['Amount'] = scaler_robust.fit_transform(X_train[['Amount']])
X_val_scaled['Amount'] = scaler_robust.transform(X_val[['Amount']])
X_test_scaled['Amount'] = scaler_robust.transform(X_test[['Amount']])

# Scale Time with StandardScaler
X_train_scaled['Time'] = scaler_standard.fit_transform(X_train[['Time']])
X_val_scaled['Time'] = scaler_standard.transform(X_val[['Time']])
X_test_scaled['Time'] = scaler_standard.transform(X_test[['Time']])

print(f"✓ Feature scaling completed:")
print(f"   • Amount: RobustScaler (robust to outliers)")
print(f"   • Time: StandardScaler")
print(f"   • V1-V28: Already PCA-scaled (kept as-is)")
print()

# ============================================================================
# 5. PREPARE EVALUATION FUNCTION
# ============================================================================

def evaluate_model(model, X_val, y_val, X_test, y_test, strategy_name):
    """
    Comprehensive model evaluation function
    """
    results = {}
    
    # Validation predictions
    y_val_pred = model.predict(X_val)
    y_val_proba = model.predict_proba(X_val)[:, 1]
    
    # Test predictions
    y_test_pred = model.predict(X_test)
    y_test_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics for both validation and test
    for dataset_name, y_true, y_pred, y_proba in [
        ('Validation', y_val, y_val_pred, y_val_proba),
        ('Test', y_test, y_test_pred, y_test_proba)
    ]:
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_true, y_proba)
        pr_auc = average_precision_score(y_true, y_proba)
        
        results[dataset_name] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'pr_auc': pr_auc,
            'y_true': y_true,
            'y_pred': y_pred,
            'y_proba': y_proba
        }
    
    return results

# ============================================================================
# 6. CUSTOM SMOTE IMPLEMENTATION (SIMPLIFIED)
# ============================================================================

def simple_smote(X, y, k_neighbors=5, random_state=42):
    """
    Simplified SMOTE implementation for binary classification
    """
    np.random.seed(random_state)
    
    # Get minority class samples
    minority_class = 1
    majority_class = 0
    
    X_minority = X[y == minority_class]
    X_majority = X[y == majority_class]
    
    n_minority = len(X_minority)
    n_majority = len(X_majority)
    n_to_generate = n_majority - n_minority
    
    # Generate synthetic samples
    synthetic_samples = []
    
    for _ in range(n_to_generate):
        # Randomly select a minority sample
        idx = np.random.randint(0, n_minority)
        sample = X_minority.iloc[idx].values
        
        # Find k nearest neighbors
        distances = np.sum((X_minority.values - sample) ** 2, axis=1)
        nearest_indices = np.argsort(distances)[1:k_neighbors+1]
        
        # Randomly select one neighbor
        neighbor_idx = np.random.choice(nearest_indices)
        neighbor = X_minority.iloc[neighbor_idx].values
        
        # Generate synthetic sample
        alpha = np.random.random()
        synthetic_sample = sample + alpha * (neighbor - sample)
        synthetic_samples.append(synthetic_sample)
    
    # Combine original and synthetic samples
    X_synthetic = pd.DataFrame(synthetic_samples, columns=X.columns)
    y_synthetic = pd.Series([minority_class] * len(synthetic_samples))
    
    X_resampled = pd.concat([X, X_synthetic], ignore_index=True)
    y_resampled = pd.concat([y, y_synthetic], ignore_index=True)
    
    return X_resampled, y_resampled

# ============================================================================
# 7. CUSTOM RANDOM UNDERSAMPLING
# ============================================================================

def random_undersample(X, y, random_state=42):
    """
    Random undersampling of majority class
    """
    np.random.seed(random_state)
    
    minority_class = 1
    majority_class = 0
    
    X_minority = X[y == minority_class]
    y_minority = y[y == minority_class]
    
    X_majority = X[y == majority_class]
    y_majority = y[y == majority_class]
    
    # Undersample majority class
    n_minority = len(X_minority)
    undersample_indices = np.random.choice(len(X_majority), n_minority, replace=False)
    
    X_majority_under = X_majority.iloc[undersample_indices]
    y_majority_under = y_majority.iloc[undersample_indices]
    
    # Combine
    X_resampled = pd.concat([X_minority, X_majority_under], ignore_index=True)
    y_resampled = pd.concat([y_minority, y_majority_under], ignore_index=True)
    
    return X_resampled, y_resampled

# ============================================================================
# 8. STRATEGY 1: CLASS WEIGHTS
# ============================================================================
print("5. STRATEGY 1: CLASS WEIGHTS")
print("-" * 100)

# Compute class weights
class_weights = compute_class_weight(
    'balanced', 
    classes=np.unique(y_train), 
    y=y_train
)
class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

print(f"✓ Class weights computed:")
print(f"   • Class 0 (Legitimate): {class_weight_dict[0]:.4f}")
print(f"   • Class 1 (Fraud): {class_weight_dict[1]:.4f}")
print(f"   • Weight ratio: 1:{class_weight_dict[1]/class_weight_dict[0]:.1f}")
print()

# Train Logistic Regression with class weights
print("Training Logistic Regression with class weights...")
lr_weighted = LogisticRegression(
    class_weight='balanced',
    max_iter=1000,
    random_state=42,
    solver='liblinear'
)
lr_weighted.fit(X_train_scaled, y_train)

results_weighted = evaluate_model(
    lr_weighted, X_val_scaled, y_val, X_test_scaled, y_test, 
    "Class Weights"
)

print(f"✓ Model trained successfully")
print()

# ============================================================================
# 9. STRATEGY 2: SMOTE OVERSAMPLING
# ============================================================================
print("6. STRATEGY 2: SMOTE OVERSAMPLING")
print("-" * 100)

# Apply SMOTE to training data only
X_train_smote, y_train_smote = simple_smote(X_train_scaled, y_train, k_neighbors=5, random_state=42)

print(f"✓ SMOTE oversampling completed:")
print(f"   • Original training set: {X_train_scaled.shape[0]:,} samples")
print(f"   • After SMOTE: {X_train_smote.shape[0]:,} samples")
print(f"   • Fraud cases before: {y_train.sum():,} ({y_train.mean()*100:.4f}%)")
print(f"   • Fraud cases after: {y_train_smote.sum():,} ({y_train_smote.mean()*100:.2f}%)")
print()

# Train Logistic Regression on SMOTE data
print("Training Logistic Regression with SMOTE data...")
lr_smote = LogisticRegression(
    max_iter=1000,
    random_state=42,
    solver='liblinear'
)
lr_smote.fit(X_train_smote, y_train_smote)

results_smote = evaluate_model(
    lr_smote, X_val_scaled, y_val, X_test_scaled, y_test,
    "SMOTE"
)

print(f"✓ Model trained successfully")
print()

# ============================================================================
# 10. STRATEGY 3: RANDOM UNDERSAMPLING
# ============================================================================
print("7. STRATEGY 3: RANDOM UNDERSAMPLING")
print("-" * 100)

# Apply Random Undersampling to training data
X_train_under, y_train_under = random_undersample(X_train_scaled, y_train, random_state=42)

print(f"✓ Random undersampling completed:")
print(f"   • Original training set: {X_train_scaled.shape[0]:,} samples")
print(f"   • After undersampling: {X_train_under.shape[0]:,} samples")
print(f"   • Fraud cases before: {y_train.sum():,} ({y_train.mean()*100:.4f}%)")
print(f"   • Fraud cases after: {y_train_under.sum():,} ({y_train_under.mean()*100:.2f}%)")
print(f"   • Data reduction: {(1 - X_train_under.shape[0]/X_train_scaled.shape[0])*100:.2f}%")
print()

# Train Logistic Regression on undersampled data
print("Training Logistic Regression with undersampled data...")
lr_under = LogisticRegression(
    max_iter=1000,
    random_state=42,
    solver='liblinear'
)
lr_under.fit(X_train_under, y_train_under)

results_under = evaluate_model(
    lr_under, X_val_scaled, y_val, X_test_scaled, y_test,
    "Undersampling"
)

print(f"✓ Model trained successfully")
print()

# ============================================================================
# 11. RESULTS COMPARISON TABLE
# ============================================================================
print("8. PERFORMANCE COMPARISON - ALL STRATEGIES")
print("=" * 100)
print()

# Create comparison dataframe
comparison_data = []

for strategy_name, results in [
    ("Class Weights", results_weighted),
    ("SMOTE", results_smote),
    ("Undersampling", results_under)
]:
    for dataset in ['Validation', 'Test']:
        comparison_data.append({
            'Strategy': strategy_name,
            'Dataset': dataset,
            'Precision': results[dataset]['precision'],
            'Recall': results[dataset]['recall'],
            'F1-Score': results[dataset]['f1'],
            'ROC-AUC': results[dataset]['roc_auc'],
            'PR-AUC': results[dataset]['pr_auc']
        })

comparison_df = pd.DataFrame(comparison_data)

# Display results
print("VALIDATION SET PERFORMANCE")
print("-" * 100)
val_results = comparison_df[comparison_df['Dataset'] == 'Validation'].drop('Dataset', axis=1)
val_results = val_results.set_index('Strategy')
print(val_results.to_string())
print()

print("TEST SET PERFORMANCE")
print("-" * 100)
test_results = comparison_df[comparison_df['Dataset'] == 'Test'].drop('Dataset', axis=1)
test_results = test_results.set_index('Strategy')
print(test_results.to_string())
print()

# Store for visualization
results_dict = {
    'Class Weights': results_weighted,
    'SMOTE': results_smote,
    'Undersampling': results_under
}

print("✓ All models trained and evaluated successfully!")
print()

## Example Result

====================================================================================================
FRAUD DETECTION - BASELINE MODEL COMPARISON
====================================================================================================

1. LOADING CLEANED DATA
----------------------------------------------------------------------------------------------------
✓ Using existing cleaned dataset
   Dataset shape: (283726, 31)
   Fraud cases: 473 (0.1667%)

2. FEATURE PREPARATION
----------------------------------------------------------------------------------------------------
✓ Total features: 30
   • PCA features (V1-V28): 28
   • Other features: ['Time', 'Amount']

3. CREATING STRATIFIED TRAIN-VALIDATION-TEST SPLITS
----------------------------------------------------------------------------------------------------
✓ Data split completed:
   Train set: 198,608 samples (70.0%) - Fraud: 0.1667%
   Val set:   42,559 samples (15.0%) - Fraud: 0.1668%
   Test set:  42,559 samples (15.0%) - Fraud: 0.1668%

4. FEATURE SCALING
----------------------------------------------------------------------------------------------------
✓ Feature scaling completed:
   • Amount: RobustScaler (robust to outliers)
   • Time: StandardScaler
   • V1-V28: Already PCA-scaled (kept as-is)

5. STRATEGY 1: CLASS WEIGHTS
----------------------------------------------------------------------------------------------------
✓ Class weights computed:
   • Class 0 (Legitimate): 0.5008
   • Class 1 (Fraud): 300.0121
   • Weight ratio: 1:599.0

Training Logistic Regression with class weights...
✓ Model trained successfully

6. STRATEGY 2: SMOTE OVERSAMPLING
----------------------------------------------------------------------------------------------------
✓ SMOTE oversampling completed:
   • Original training set: 198,608 samples
   • After SMOTE: 396,554 samples
   • Fraud cases before: 331 (0.1667%)
   • Fraud cases after: 198,277 (50.00%)

Training Logistic Regression with SMOTE data...
✓ Model trained successfully

7. STRATEGY 3: RANDOM UNDERSAMPLING
----------------------------------------------------------------------------------------------------
✓ Random undersampling completed:
   • Original training set: 198,608 samples
   • After undersampling: 662 samples
   • Fraud cases before: 331 (0.1667%)
   • Fraud cases after: 331 (50.00%)
   • Data reduction: 99.67%

Training Logistic Regression with undersampled data...
✓ Model trained successfully

8. PERFORMANCE COMPARISON - ALL STRATEGIES
====================================================================================================

VALIDATION SET PERFORMANCE
----------------------------------------------------------------------------------------------------
               Precision    Recall  F1-Score   ROC-AUC    PR-AUC
Strategy                                                        
Class Weights   0.050766  0.887324  0.096037  0.971798  0.698750
SMOTE           0.050279  0.887324  0.095166  0.973326  0.698456
Undersampling   0.033298  0.873239  0.064149  0.977657  0.503248

TEST SET PERFORMANCE
----------------------------------------------------------------------------------------------------
               Precision    Recall  F1-Score   ROC-AUC    PR-AUC
Strategy                                                        
Class Weights   0.055070  0.887324  0.103704  0.960863  0.681007
SMOTE           0.052498  0.873239  0.099042  0.958487  0.687789
Undersampling   0.033962  0.887324  0.065421  0.949008  0.500927

✓ All models trained and evaluated successfully!

