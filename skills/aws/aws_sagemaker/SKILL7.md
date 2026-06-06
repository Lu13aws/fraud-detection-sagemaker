# ML Threshold Optimization Skill

## Purpose

Optimize classification thresholds for probability-based models.

Use this skill when the default threshold of 0.5 produces poor precision-recall trade-offs.

## Common Use Cases

* Fraud detection
* Risk scoring
* Anomaly detection
* Medical screening
* Customer churn prediction

## Objective

Find the best decision threshold based on business priorities.

## Required Steps

1. Train a probability-based classification model
2. Generate prediction probabilities
3. Evaluate thresholds from 0.01 to 0.99
4. Calculate metrics for each threshold
5. Identify optimal thresholds

## Metrics

Calculate:

* Precision
* Recall
* F1 Score
* ROC-AUC
* PR-AUC
* True Positives
* False Positives
* False Negatives
* Confusion Matrix

## Threshold Selection

Identify:

1. Threshold maximizing F1 Score
2. Threshold maximizing Recall
3. Threshold maximizing Precision

## Business Interpretation

Explain trade-offs:

High recall threshold:

* Finds more fraud cases
* Creates more false positives
* Increases manual review workload

High precision threshold:

* Reduces false positives
* Misses more fraud cases
* Better when false alarms are costly

Balanced threshold:

* Optimizes F1 score
* Often useful as a production starting point

## Output

Provide:

* Threshold comparison table
* Best threshold recommendation
* Business trade-off analysis
* Production recommendation
* Monitoring recommendations

# Example Code

# ============================================================================
# THRESHOLD OPTIMIZATION FOR FRAUD DETECTION
# Senior ML Engineer - Production-Ready Implementation
# ============================================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score, recall_score, f1_score, 
    roc_auc_score, average_precision_score,
    precision_recall_curve, roc_curve, confusion_matrix,
    classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("THRESHOLD OPTIMIZATION FOR FRAUD DETECTION - PRODUCTION IMPLEMENTATION")
print("=" * 100)
print()

# ============================================================================
# STEP 1: DATA PREPARATION
# ============================================================================
print("STEP 1: DATA PREPARATION")
print("-" * 100)

# Check if data is already loaded, otherwise load it
if 'df' not in locals() or df is None:
    s3_path = "s3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv"
    print(f"Loading data from: {s3_path}")
    df = pd.read_csv(s3_path)
    print(f"✓ Data loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
else:
    print(f"✓ Using existing dataframe: {df.shape[0]:,} rows, {df.shape[1]} columns")

# Remove duplicates
df_clean = df.drop_duplicates()
print(f"✓ Removed {df.shape[0] - df_clean.shape[0]:,} duplicate rows")
print(f"✓ Clean dataset: {df_clean.shape[0]:,} rows")
print()

# ============================================================================
# STEP 2: FEATURE ENGINEERING & SCALING
# ============================================================================
print("STEP 2: FEATURE ENGINEERING & SCALING")
print("-" * 100)

# Separate features and target
X = df_clean.drop('Class', axis=1)
y = df_clean['Class']

# Scale Amount and Time features (V1-V28 are already PCA-scaled)
scaler = StandardScaler()
X['Amount_scaled'] = scaler.fit_transform(X[['Amount']])
X['Time_scaled'] = scaler.fit_transform(X[['Time']])

# Use scaled features
feature_cols = [col for col in X.columns if col.startswith('V')] + ['Amount_scaled', 'Time_scaled']
X_processed = X[feature_cols]

print(f"✓ Features prepared: {len(feature_cols)} features")
print(f"✓ Feature set: {', '.join(feature_cols[:5])}... (showing first 5)")
print(f"✓ Target distribution: Fraud={y.sum():,} ({y.mean()*100:.4f}%), Legitimate={len(y)-y.sum():,}")
print()

# ============================================================================
# STEP 3: TRAIN-TEST SPLIT (STRATIFIED)
# ============================================================================
print("STEP 3: TRAIN-TEST SPLIT")
print("-" * 100)

X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, 
    test_size=0.3, 
    random_state=42, 
    stratify=y
)

print(f"✓ Training set: {X_train.shape[0]:,} samples")
print(f"✓ Test set: {X_test.shape[0]:,} samples")
print(f"✓ Train fraud rate: {y_train.mean()*100:.4f}%")
print(f"✓ Test fraud rate: {y_test.mean()*100:.4f}%")
print()

# ============================================================================
# STEP 4: TRAIN BASELINE MODEL (LOGISTIC REGRESSION)
# ============================================================================
print("STEP 4: TRAINING BASELINE MODEL")
print("-" * 100)

# Calculate class weights for imbalanced data
class_weight_ratio = len(y_train[y_train==0]) / len(y_train[y_train==1])
class_weights = {0: 1, 1: class_weight_ratio}

print(f"✓ Class imbalance ratio: 1:{class_weight_ratio:.0f}")
print(f"✓ Class weights: {class_weights}")
print("✓ Training Logistic Regression with balanced class weights...")

# Train model
baseline_model = LogisticRegression(
    class_weight='balanced',
    max_iter=1000,
    random_state=42,
    solver='lbfgs'
)

baseline_model.fit(X_train, y_train)
print("✓ Model training complete!")
print()

# Get prediction probabilities
y_train_proba = baseline_model.predict_proba(X_train)[:, 1]
y_test_proba = baseline_model.predict_proba(X_test)[:, 1]

print(f"✓ Prediction probabilities generated")
print(f"  - Train set probability range: [{y_train_proba.min():.4f}, {y_train_proba.max():.4f}]")
print(f"  - Test set probability range: [{y_test_proba.min():.4f}, {y_test_proba.max():.4f}]")
print()

# ============================================================================
# STEP 5: BASELINE MODEL PERFORMANCE (DEFAULT THRESHOLD = 0.5)
# ============================================================================
print("STEP 5: BASELINE MODEL PERFORMANCE (THRESHOLD = 0.5)")
print("-" * 100)

y_test_pred_default = (y_test_proba >= 0.5).astype(int)

print("Test Set Performance:")
print(classification_report(y_test, y_test_pred_default, target_names=['Legitimate', 'Fraud'], digits=4))

cm_default = confusion_matrix(y_test, y_test_pred_default)
print("\nConfusion Matrix (Threshold = 0.5):")
print(f"{'':12} {'Predicted Legit':>18} {'Predicted Fraud':>18}")
print(f"{'Actual Legit':12} {cm_default[0,0]:>18,} {cm_default[0,1]:>18,}")
print(f"{'Actual Fraud':12} {cm_default[1,0]:>18,} {cm_default[1,1]:>18,}")
print()

# ============================================================================
# STEP 6: COMPREHENSIVE THRESHOLD OPTIMIZATION
# ============================================================================
print("STEP 6: THRESHOLD OPTIMIZATION (0.01 to 0.99)")
print("=" * 100)

# Evaluate thresholds from 0.01 to 0.99
thresholds = np.arange(0.01, 1.0, 0.01)
results = []

print(f"Evaluating {len(thresholds)} threshold values...")

for threshold in thresholds:
    # Make predictions with current threshold
    y_pred = (y_test_proba >= threshold).astype(int)
    
    # Calculate metrics
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    # ROC-AUC and PR-AUC (threshold-independent)
    roc_auc = roc_auc_score(y_test, y_test_proba)
    pr_auc = average_precision_score(y_test, y_test_proba)
    
    # Confusion matrix components
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    results.append({
        'threshold': threshold,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'pr_auc': pr_auc,
        'true_positives': tp,
        'false_positives': fp,
        'true_negatives': tn,
        'false_negatives': fn
    })

# Convert to DataFrame
threshold_results = pd.DataFrame(results)
print(f"✓ Evaluation complete!")
print()

# ============================================================================
# STEP 7: IDENTIFY OPTIMAL THRESHOLDS
# ============================================================================
print("STEP 7: OPTIMAL THRESHOLD IDENTIFICATION")
print("=" * 100)
print()

# Find optimal thresholds
best_f1_idx = threshold_results['f1_score'].idxmax()
best_recall_idx = threshold_results['recall'].idxmax()
best_precision_idx = threshold_results['precision'].idxmax()

best_f1_threshold = threshold_results.loc[best_f1_idx, 'threshold']
best_recall_threshold = threshold_results.loc[best_recall_idx, 'threshold']
best_precision_threshold = threshold_results.loc[best_precision_idx, 'threshold']

print("🎯 OPTIMAL THRESHOLDS IDENTIFIED:")
print("-" * 100)

# Best F1 Score
print(f"\n1️⃣  THRESHOLD MAXIMIZING F1-SCORE: {best_f1_threshold:.3f}")
print(f"    {'Metric':<20} {'Value':>15}")
print(f"    {'-'*36}")
print(f"    {'Precision':<20} {threshold_results.loc[best_f1_idx, 'precision']:>15.4f}")
print(f"    {'Recall':<20} {threshold_results.loc[best_f1_idx, 'recall']:>15.4f}")
print(f"    {'F1-Score':<20} {threshold_results.loc[best_f1_idx, 'f1_score']:>15.4f}")
print(f"    {'ROC-AUC':<20} {threshold_results.loc[best_f1_idx, 'roc_auc']:>15.4f}")
print(f"    {'PR-AUC':<20} {threshold_results.loc[best_f1_idx, 'pr_auc']:>15.4f}")
print(f"    {'True Positives':<20} {int(threshold_results.loc[best_f1_idx, 'true_positives']):>15,}")
print(f"    {'False Positives':<20} {int(threshold_results.loc[best_f1_idx, 'false_positives']):>15,}")
print(f"    {'False Negatives':<20} {int(threshold_results.loc[best_f1_idx, 'false_negatives']):>15,}")

# Best Recall
print(f"\n2️⃣  THRESHOLD MAXIMIZING RECALL: {best_recall_threshold:.3f}")
print(f"    {'Metric':<20} {'Value':>15}")
print(f"    {'-'*36}")
print(f"    {'Precision':<20} {threshold_results.loc[best_recall_idx, 'precision']:>15.4f}")
print(f"    {'Recall':<20} {threshold_results.loc[best_recall_idx, 'recall']:>15.4f}")
print(f"    {'F1-Score':<20} {threshold_results.loc[best_recall_idx, 'f1_score']:>15.4f}")
print(f"    {'ROC-AUC':<20} {threshold_results.loc[best_recall_idx, 'roc_auc']:>15.4f}")
print(f"    {'PR-AUC':<20} {threshold_results.loc[best_recall_idx, 'pr_auc']:>15.4f}")
print(f"    {'True Positives':<20} {int(threshold_results.loc[best_recall_idx, 'true_positives']):>15,}")
print(f"    {'False Positives':<20} {int(threshold_results.loc[best_recall_idx, 'false_positives']):>15,}")
print(f"    {'False Negatives':<20} {int(threshold_results.loc[best_recall_idx, 'false_negatives']):>15,}")

# Best Precision
print(f"\n3️⃣  THRESHOLD MAXIMIZING PRECISION: {best_precision_threshold:.3f}")
print(f"    {'Metric':<20} {'Value':>15}")
print(f"    {'-'*36}")
print(f"    {'Precision':<20} {threshold_results.loc[best_precision_idx, 'precision']:>15.4f}")
print(f"    {'Recall':<20} {threshold_results.loc[best_precision_idx, 'recall']:>15.4f}")
print(f"    {'F1-Score':<20} {threshold_results.loc[best_precision_idx, 'f1_score']:>15.4f}")
print(f"    {'ROC-AUC':<20} {threshold_results.loc[best_precision_idx, 'roc_auc']:>15.4f}")
print(f"    {'PR-AUC':<20} {threshold_results.loc[best_precision_idx, 'pr_auc']:>15.4f}")
print(f"    {'True Positives':<20} {int(threshold_results.loc[best_precision_idx, 'true_positives']):>15,}")
print(f"    {'False Positives':<20} {int(threshold_results.loc[best_precision_idx, 'false_positives']):>15,}")
print(f"    {'False Negatives':<20} {int(threshold_results.loc[best_precision_idx, 'false_negatives']):>15,}")

print()
print("=" * 100)

# ============================================================================
# STEP 8: BUSINESS RECOMMENDATION
# ============================================================================
print("\n")
print("STEP 8: BUSINESS RECOMMENDATION FOR FRAUD DETECTION")
print("=" * 100)
print()

print("📊 RECOMMENDED THRESHOLD: Based on Business Context")
print("-" * 100)
print()

# Calculate cost metrics for different thresholds
print("💰 BUSINESS TRADE-OFF ANALYSIS:")
print()

print("1️⃣  HIGH RECALL STRATEGY (Threshold = {:.3f})".format(best_recall_threshold))
print("   ✅ PROS:")
print("      • Catches maximum number of fraud cases (minimizes missed fraud)")
print("      • Reduces financial losses from undetected fraud")
print("      • Best for high-value transactions or critical fraud prevention")
print("   ❌ CONS:")
print("      • Higher false positive rate → more legitimate transactions flagged")
print("      • Increased manual review workload")
print("      • Customer friction (legitimate users flagged)")
print(f"      • Expected FP rate: {threshold_results.loc[best_recall_idx, 'false_positives'] / (threshold_results.loc[best_recall_idx, 'false_positives'] + threshold_results.loc[best_recall_idx, 'true_negatives']) * 100:.2f}%")
print()

print("2️⃣  HIGH PRECISION STRATEGY (Threshold = {:.3f})".format(best_precision_threshold))
print("   ✅ PROS:")
print("      • Minimizes false alarms (high confidence in fraud flags)")
print("      • Reduces customer frustration from false blocks")
print("      • Lower operational costs for fraud investigation")
print("   ❌ CONS:")
print("      • Misses more actual fraud cases")
print("      • Higher financial losses from undetected fraud")
print("      • Not suitable if fraud cost is very high")
print(f"      • Expected missed fraud: {int(threshold_results.loc[best_precision_idx, 'false_negatives']):,} cases")
print()

print("3️⃣  BALANCED STRATEGY (F1-SCORE) (Threshold = {:.3f}) ⭐ RECOMMENDED".format(best_f1_threshold))
print("   ✅ PROS:")
print("      • Optimal balance between catching fraud and minimizing false alarms")
print("      • Good starting point for most fraud detection systems")
print("      • Balances operational costs with fraud prevention")
print("   ❌ CONS:")
print("      • May not be optimal if business priorities heavily favor precision/recall")
print(f"      • Catches {threshold_results.loc[best_f1_idx, 'true_positives']/threshold_results.loc[best_recall_idx, 'true_positives']*100:.1f}% of max possible fraud")
print(f"      • FP rate: {threshold_results.loc[best_f1_idx, 'false_positives'] / (threshold_results.loc[best_f1_idx, 'false_positives'] + threshold_results.loc[best_f1_idx, 'true_negatives']) * 100:.2f}%")
print()

print("=" * 100)
print("🎯 FINAL RECOMMENDATION:")
print("=" * 100)
print()
print(f"✅ RECOMMENDED THRESHOLD: {best_f1_threshold:.3f}")
print()
print("📋 JUSTIFICATION:")
print("   • For fraud detection, F1-Score balanced approach is typically optimal")
print("   • Prevents significant fraud losses while maintaining customer experience")
print("   • Manageable false positive rate for fraud investigation teams")
print()
print("🔄 DEPLOYMENT STRATEGY:")
print("   1. Start with F1-optimal threshold ({:.3f})".format(best_f1_threshold))
print("   2. Monitor precision/recall metrics in production")
print("   3. If fraud losses are too high → lower threshold (increase recall)")
print("   4. If customer complaints increase → raise threshold (increase precision)")
print("   5. A/B test different thresholds with business metrics (revenue impact, customer satisfaction)")
print()
print("💡 BUSINESS CONTEXT CONSIDERATIONS:")
print("   • Average fraud transaction value vs. customer lifetime value")
print("   • Cost of manual fraud review per transaction")
print("   • Customer tolerance for false positives (payment blocks)")
print("   • Regulatory requirements for fraud detection")
print()

print("=" * 100)

# Store results for visualization
globals()['threshold_results'] = threshold_results
globals()['best_f1_threshold'] = best_f1_threshold
globals()['best_recall_threshold'] = best_recall_threshold
globals()['best_precision_threshold'] = best_precision_threshold

print("\n✓ Threshold optimization complete!")
print("✓ Results saved to 'threshold_results' DataFrame for further analysis")
print("✓ Use threshold_results.head() to view detailed metrics")
print()
print("=" * 100)

# Example Result

====================================================================================================
THRESHOLD OPTIMIZATION FOR FRAUD DETECTION - PRODUCTION IMPLEMENTATION
====================================================================================================

STEP 1: DATA PREPARATION
----------------------------------------------------------------------------------------------------
✓ Using existing dataframe: 284,807 rows, 31 columns
✓ Removed 1,081 duplicate rows
✓ Clean dataset: 283,726 rows

STEP 2: FEATURE ENGINEERING & SCALING
----------------------------------------------------------------------------------------------------
✓ Features prepared: 30 features
✓ Feature set: V1, V2, V3, V4, V5... (showing first 5)
✓ Target distribution: Fraud=473 (0.1667%), Legitimate=283,253

STEP 3: TRAIN-TEST SPLIT
----------------------------------------------------------------------------------------------------
✓ Training set: 198,608 samples
✓ Test set: 85,118 samples
✓ Train fraud rate: 0.1667%
✓ Test fraud rate: 0.1668%

STEP 4: TRAINING BASELINE MODEL
----------------------------------------------------------------------------------------------------
✓ Class imbalance ratio: 1:599
✓ Class weights: {0: 1, 1: 599.02416918429}
✓ Training Logistic Regression with balanced class weights...
✓ Model training complete!

✓ Prediction probabilities generated
  - Train set probability range: [0.0000, 1.0000]
  - Test set probability range: [0.0000, 1.0000]

STEP 5: BASELINE MODEL PERFORMANCE (THRESHOLD = 0.5)
----------------------------------------------------------------------------------------------------
Test Set Performance:
              precision    recall  f1-score   support

  Legitimate     0.9998    0.9734    0.9864     84976
       Fraud     0.0528    0.8873    0.0996       142

    accuracy                         0.9732     85118
   macro avg     0.5263    0.9304    0.5430     85118
weighted avg     0.9982    0.9732    0.9849     85118


Confusion Matrix (Threshold = 0.5):
                Predicted Legit    Predicted Fraud
Actual Legit             82,715              2,261
Actual Fraud                 16                126

STEP 6: THRESHOLD OPTIMIZATION (0.01 to 0.99)
====================================================================================================
Evaluating 99 threshold values...
✓ Evaluation complete!

STEP 7: OPTIMAL THRESHOLD IDENTIFICATION
====================================================================================================

🎯 OPTIMAL THRESHOLDS IDENTIFIED:
----------------------------------------------------------------------------------------------------

1️⃣  THRESHOLD MAXIMIZING F1-SCORE: 0.990
    Metric                         Value
    ------------------------------------
    Precision                     0.6011
    Recall                        0.7958
    F1-Score                      0.6848
    ROC-AUC                       0.9663
    PR-AUC                        0.6877
    True Positives                   113
    False Positives                   75
    False Negatives                   29

2️⃣  THRESHOLD MAXIMIZING RECALL: 0.010
    Metric                         Value
    ------------------------------------
    Precision                     0.0023
    Recall                        0.9859
    F1-Score                      0.0046
    ROC-AUC                       0.9663
    PR-AUC                        0.6877
    True Positives                   140
    False Positives               61,072
    False Negatives                    2

3️⃣  THRESHOLD MAXIMIZING PRECISION: 0.990
    Metric                         Value
    ------------------------------------
    Precision                     0.6011
    Recall                        0.7958
    F1-Score                      0.6848
    ROC-AUC                       0.9663
    PR-AUC                        0.6877
    True Positives                   113
    False Positives                   75
    False Negatives                   29

====================================================================================================


STEP 8: BUSINESS RECOMMENDATION FOR FRAUD DETECTION
====================================================================================================

📊 RECOMMENDED THRESHOLD: Based on Business Context
----------------------------------------------------------------------------------------------------

💰 BUSINESS TRADE-OFF ANALYSIS:

1️⃣  HIGH RECALL STRATEGY (Threshold = 0.010)
   ✅ PROS:
      • Catches maximum number of fraud cases (minimizes missed fraud)
      • Reduces financial losses from undetected fraud
      • Best for high-value transactions or critical fraud prevention
   ❌ CONS:
      • Higher false positive rate → more legitimate transactions flagged
      • Increased manual review workload
      • Customer friction (legitimate users flagged)
      • Expected FP rate: 71.87%

2️⃣  HIGH PRECISION STRATEGY (Threshold = 0.990)
   ✅ PROS:
      • Minimizes false alarms (high confidence in fraud flags)
      • Reduces customer frustration from false blocks
      • Lower operational costs for fraud investigation
   ❌ CONS:
      • Misses more actual fraud cases
      • Higher financial losses from undetected fraud
      • Not suitable if fraud cost is very high
      • Expected missed fraud: 29 cases

3️⃣  BALANCED STRATEGY (F1-SCORE) (Threshold = 0.990) ⭐ RECOMMENDED
   ✅ PROS:
      • Optimal balance between catching fraud and minimizing false alarms
      • Good starting point for most fraud detection systems
      • Balances operational costs with fraud prevention
   ❌ CONS:
      • May not be optimal if business priorities heavily favor precision/recall
      • Catches 80.7% of max possible fraud
      • FP rate: 0.09%

====================================================================================================
🎯 FINAL RECOMMENDATION:
====================================================================================================

✅ RECOMMENDED THRESHOLD: 0.990

📋 JUSTIFICATION:
   • For fraud detection, F1-Score balanced approach is typically optimal
   • Prevents significant fraud losses while maintaining customer experience
   • Manageable false positive rate for fraud investigation teams

🔄 DEPLOYMENT STRATEGY:
   1. Start with F1-optimal threshold (0.990)
   2. Monitor precision/recall metrics in production
   3. If fraud losses are too high → lower threshold (increase recall)
   4. If customer complaints increase → raise threshold (increase precision)
   5. A/B test different thresholds with business metrics (revenue impact, customer satisfaction)

💡 BUSINESS CONTEXT CONSIDERATIONS:
   • Average fraud transaction value vs. customer lifetime value
   • Cost of manual fraud review per transaction
   • Customer tolerance for false positives (payment blocks)
   • Regulatory requirements for fraud detection

====================================================================================================

✓ Threshold optimization complete!
✓ Results saved to 'threshold_results' DataFrame for further analysis
✓ Use threshold_results.head() to view detailed metrics

====================================================================================================
