# Machine Learning Class Imbalance Strategies Skill

## Purpose

This skill provides comprehensive guidance on detecting, evaluating, and handling severe class imbalance in classification problems.

Use this skill whenever:

* Fraud detection (0.1% - 5% fraud)
* Medical diagnosis (disease rare in population)
* Anomaly detection (normal >> abnormal)
* Churn prediction (most customers don't churn)
* Credit risk (most loans default-free)
* Any classification where one class is < 10% of data

---

## Core Problem: Why Class Imbalance Matters

### Example: Fraud Detection

```
Dataset: 284,807 transactions
- Legitimate: 284,315 (99.83%)
- Fraudulent: 492 (0.17%)

Naive Model: "Always predict legitimate"
- Accuracy: 99.83% ✓ Looks great!
- Fraud caught: 0 ✗ Completely useless
- Precision: undefined (no fraud predicted)
- Recall: 0% (catches 0% of fraud)
```

**The Problem:** Accuracy is meaningless for imbalanced data.

### Why It Happens

Models optimized for accuracy learn to:
1. Predict majority class as default
2. Ignore subtle minority class patterns
3. Treat minority examples as noise

**Result:** Good overall accuracy, terrible minority class performance.

---

## Detecting Class Imbalance

### Quick Check

```python
import numpy as np

# Method 1: Value counts
counts = y.value_counts()
imbalance_ratio = counts.iloc[0] / counts.iloc[1]
print(f'Imbalance ratio: 1:{imbalance_ratio:.0f}')

# Method 2: Percentage
minority_pct = (y == 1).sum() / len(y) * 100
print(f'Minority class: {minority_pct:.2f}%')

# Interpretation
if minority_pct < 1:
    print('SEVERE imbalance: need special handling')
elif minority_pct < 10:
    print('MODERATE imbalance: recommend handling')
else:
    print('MILD imbalance: standard approaches may work')
```

### Decision Tree: Do I Have Class Imbalance?

```
Is minority class < 10% of data?
├─ YES, < 1%: SEVERE → Must use dedicated strategies
├─ YES, 1-10%: MODERATE → Should use at least one strategy
└─ NO, > 10%: MILD → Standard ML techniques usually work
```

---

## The 5 Main Strategies

### Strategy 1: Do Nothing (Baseline)

**What:** Train normally, observe behavior.

**When:** For comparison purposes; document baseline performance.

**Code:**
```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_val)
y_proba = model.predict_proba(X_val)[:, 1]

from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_val, y_pred))
print(classification_report(y_val, y_pred))
```

**Result:** Typically predicts "majority class" for everything. High accuracy, zero minority predictions.

---

### Strategy 2: Class Weights (Recommended Starting Point)

**What:** Penalize minority class errors more than majority class errors.

**How:** Pass `class_weight='balanced'` to sklearn models.

**Intuition:** Model learns: "Getting one fraud wrong is worse than getting one legitimate wrong."

#### Implementation

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# Logistic Regression
lr = LogisticRegression(class_weight='balanced', max_iter=1000)
lr.fit(X_train, y_train)

# Random Forest
rf = RandomForestClassifier(class_weight='balanced', n_estimators=200)
rf.fit(X_train, y_train)

# XGBoost (compute scale_pos_weight manually)
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
xgb = XGBClassifier(scale_pos_weight=scale_pos_weight, n_estimators=200)
xgb.fit(X_train, y_train)
```

#### Pros & Cons

✅ **Pros:**
- Simplest to implement (one parameter)
- No data modification
- Fast (no resampling needed)
- Works with all sklearn models
- Good baseline

❌ **Cons:**
- Limited control (binary: balanced vs custom weights)
- May not work for extreme imbalance (1:1000)
- Requires tuning regularization separately

#### When to Use

**ALWAYS try this first.** If it works well, you're done.

---

### Strategy 3: SMOTE (Synthetic Minority Oversampling)

**What:** Create synthetic fraud examples by interpolating between existing fraud examples.

**How:**
1. Pick random fraud example
2. Find k nearest fraud neighbors
3. Draw line to neighbor
4. Create point somewhere along that line
5. Repeat until minority class balanced

**Visual:**
```
Original (imbalanced):          After SMOTE (balanced):
F     L L L L L                 F  F' F''  L L L L L
F       L L L L                 F'F   L    L L L L
F     L L L L L                 L     L L L L L
```

#### Implementation

```python
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

# Create balanced training set
smote = SMOTE(random_state=42, k_neighbors=5)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

print(f'Before: {y_train.sum()} fraud, {(y_train==0).sum()} legitimate')
print(f'After: {y_train_balanced.sum()} fraud, {(y_train_balanced==0).sum()} legitimate')

# Train on balanced data
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train_balanced, y_train_balanced)

# Evaluate on ORIGINAL validation set (never SMOTE val/test!)
y_pred = model.predict(X_val)
```

⚠️ **CRITICAL:** Only SMOTE the training set. Validation and test sets must be real data.

#### Pros & Cons

✅ **Pros:**
- Creates realistic synthetic examples
- Increases minority class training examples
- Better recall often
- Good for moderate imbalance (1:50 to 1:200)

❌ **Cons:**
- Risk of overfitting synthetic patterns
- Slower training (larger training set)
- Requires tuning k_neighbors
- May not work for extreme imbalance
- Increases training time significantly

#### When to Use

**After class weights**, if you need better recall. Good middle ground.

---

### Strategy 4: Undersampling (Random Removal of Majority)

**What:** Delete majority class examples randomly until balanced.

**How:**
1. Count minority examples (e.g., 500 fraud)
2. Randomly sample same number of majority (500 legitimate)
3. Combine: 500 + 500 = 1,000 total examples
4. Train normally

#### Implementation

```python
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier

# Undersample to 1:1 ratio (or custom)
undersampler = RandomUnderSampler(
    sampling_strategy=1.0,  # 1.0 = 1:1 (equal class sizes)
    random_state=42
)
X_train_balanced, y_train_balanced = undersampler.fit_resample(X_train, y_train)

print(f'Before: {len(X_train)} examples')
print(f'After: {len(X_train_balanced)} examples (lost {len(X_train) - len(X_train_balanced):,})')

# Train on balanced data
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train_balanced, y_train_balanced)

# Evaluate on original val/test
y_pred = model.predict(X_val)
```

#### Pros & Cons

✅ **Pros:**
- Fastest strategy (smallest training set)
- Simple to understand
- No synthetic data complexity
- Fast training

❌ **Cons:**
- **Loses real data** — throws away legitimate examples
- High information loss
- Only good if data is huge
- May miss important majority patterns
- Variance increases (smaller dataset)

#### When to Use

**Only if:**
- Training dataset is VERY large (millions)
- Speed is critical
- You have plenty of majority examples

**NOT recommended for small/medium datasets.**

---

### Strategy 5: Threshold Tuning (Post-Prediction Adjustment)

**What:** Adjust decision boundary AFTER training, based on business logic.

**How:**
1. Train model normally
2. Get probability scores (not just 0/1 predictions)
3. Test different thresholds
4. Choose threshold maximizing your desired metric (recall, F1, etc.)

**Default threshold: 0.5**  
**Custom threshold: 0.1 - 0.9 depending on business needs**

#### Implementation

```python
from sklearn.metrics import precision_recall_curve
import numpy as np

# Train model (any model)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Get probability scores
y_proba = model.predict_proba(X_val)[:, 1]

# Generate precision-recall curve
precision, recall, thresholds = precision_recall_curve(y_val, y_proba)

# Find threshold for different strategies
idx_best_f1 = np.argmax(2 * (precision * recall) / (precision + recall + 1e-10))
idx_high_recall = np.argmax(recall >= 0.90)  # 90% recall target
idx_high_precision = np.argmax(precision >= 0.95)  # 95% precision target

threshold_f1 = thresholds[idx_best_f1]
threshold_recall = thresholds[idx_high_recall]
threshold_precision = thresholds[idx_high_precision]

print(f'Best F1: threshold = {threshold_f1:.3f}')
print(f'90% recall: threshold = {threshold_recall:.3f}')
print(f'95% precision: threshold = {threshold_precision:.3f}')

# Apply custom threshold
y_pred_custom = (y_proba >= threshold_recall).astype(int)

# Evaluate
from sklearn.metrics import classification_report
print(classification_report(y_val, y_pred_custom))
```

#### Pros & Cons

✅ **Pros:**
- No retraining needed
- Directly controls precision/recall tradeoff
- Business-driven (not algorithm-driven)
- Fast to iterate
- Final tuning step

❌ **Cons:**
- Only adjusts existing model behavior
- Doesn't improve underlying model quality
- Threshold specific to validation set
- Need labeled validation data

#### When to Use

**Always use this as FINAL STEP** after choosing base strategy.

---

## Strategy Comparison Table

| Strategy | Imbalance Level | Complexity | Speed | Data Loss | Best For | Code Effort |
|----------|-----------------|-----------|-------|-----------|----------|------------|
| **Do Nothing** | Testing | Low | Fastest | None | Baseline | 0 |
| **Class Weights** | Mild-Moderate (1:10 to 1:100) | Low | Fast | None | First try | Minimal |
| **SMOTE** | Moderate (1:50 to 1:500) | Medium | Medium | None | When CW fails | Medium |
| **Undersampling** | Severe + huge data | Low | Very fast | High | Only if huge dataset | Low |
| **Threshold Tuning** | All (combined with others) | Medium | Fast | None | Final optimization | Medium |

---

## Real-World Fraud Detection Example

### Scenario

```
Training data: 284,315 legitimate, 492 fraud (1:578 ratio, 0.17% fraud)
Business goal: Catch 95% of fraud, but allow <5% false alarms
```

### Step 1: Establish Baseline

```python
# Do nothing
lr_baseline = LogisticRegression(max_iter=1000)
lr_baseline.fit(X_train, y_train)
y_pred = lr_baseline.predict(X_val)

from sklearn.metrics import confusion_matrix, recall_score, precision_score
cm = confusion_matrix(y_val, y_pred)
print(cm)
# [[40000     0]
#  [  100     0]]
# → Predicts no fraud! Recall = 0%, Precision = undefined
```

### Step 2: Try Class Weights

```python
lr_weighted = LogisticRegression(class_weight='balanced', max_iter=1000)
lr_weighted.fit(X_train, y_train)
y_pred = lr_weighted.predict(X_val)

cm = confusion_matrix(y_val, y_pred)
recall = recall_score(y_val, y_pred)
print(f'Recall: {recall:.1%}')
# Recall: 75% — Better! Caught 75% of fraud
# But might have false alarms too
```

### Step 3: Add SMOTE

```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

rf = RandomForestClassifier(n_estimators=200, class_weight='balanced')
rf.fit(X_train_smote, y_train_smote)
y_pred = rf.predict(X_val)

recall = recall_score(y_val, y_pred)
precision = precision_score(y_val, y_pred)
print(f'RF + SMOTE: Recall {recall:.1%}, Precision {precision:.1%}')
# RF + SMOTE: Recall 82%, Precision 73% — Better!
```

### Step 4: Fine-Tune Threshold

```python
y_proba = rf.predict_proba(X_val)[:, 1]

from sklearn.metrics import precision_recall_curve
prec, rec, thresholds = precision_recall_curve(y_val, y_proba)

# Business constraint: catch 95% of fraud
idx_target = np.argmax(rec >= 0.95)
threshold = thresholds[idx_target]

y_pred_tuned = (y_proba >= threshold).astype(int)

recall = recall_score(y_val, y_pred_tuned)
precision = precision_score(y_val, y_pred_tuned)
print(f'Final: Recall {recall:.1%}, Precision {precision:.1%}')
# Final: Recall 95%, Precision 65% — Meets business goal
```

---

## Evaluation Metrics: The Right Ones

### ❌ WRONG Metrics for Imbalanced Data

```python
# DON'T use accuracy
accuracy = (y_pred == y_val).mean()
# → Always 99%+ for imbalanced data, useless

# DON'T use just AUC-ROC
auc_roc = roc_auc_score(y_val, y_proba)
# → Inflated by huge number of true negatives
```

### ✅ RIGHT Metrics

```python
from sklearn.metrics import (
    average_precision_score,  # AUC-PR (primary metric)
    precision_recall_curve,   # For visualization
    recall_score,             # Catches fraud?
    precision_score,          # False alarms?
    f1_score                  # Balanced measure
)

# Primary metric: AUC-PR
auc_pr = average_precision_score(y_val, y_proba)
print(f'AUC-PR: {auc_pr:.4f}')  # Target: > 0.80 for fraud

# Secondary metrics
recall = recall_score(y_val, y_pred)  # Catch fraud %
precision = precision_score(y_val, y_pred)  # False alarm %
f1 = f1_score(y_val, y_pred)  # Balanced

print(f'Recall: {recall:.1%} (fraud caught)')
print(f'Precision: {precision:.1%} (true alarms)')
print(f'F1: {f1:.4f} (balanced)')
```

### Interpretation Guide

| Metric | Target Value | Interpretation |
|--------|--------------|-----------------|
| **AUC-PR** | > 0.80 | Model well-separates fraud from legitimate |
| **Recall** | > 80% | Catches most fraud (some slip through) |
| **Precision** | > 70% | Most alerts are real fraud (some false alarms) |
| **F1** | > 0.70 | Reasonable balance between recall and precision |

---

## Decision Tree: Which Strategy Should I Use?

```
START
│
├─ Is minority class < 10%?
│  ├─ NO → Use standard ML (no special handling needed)
│  └─ YES, continue...
│
├─ Do I have huge dataset (millions)?
│  ├─ YES → Try undersampling (fast)
│  └─ NO, continue...
│
├─ Is imbalance < 1:100?
│  ├─ YES → Try class weights first
│  │  └─ Works well? DONE
│  │  └─ Recall < 80%? Try SMOTE
│  └─ NO, continue...
│
├─ Is imbalance < 1:500?
│  ├─ YES → Start with SMOTE + class weights
│  │  └─ Good results? Add threshold tuning for final optimization
│  └─ NO, continue...
│
└─ Extreme imbalance (> 1:1000)?
   ├─ Combine everything: SMOTE + class weights + undersampling
   ├─ Or consider: anomaly detection instead of classification
   └─ Or: Get more minority examples (data collection)

FINAL STEP: Always add threshold tuning to meet business goals
```

---

## Common Mistakes to Avoid

### ❌ SMOTE Leakage

```python
# WRONG: SMOTE on entire dataset first
smote = SMOTE()
X_balanced, y_balanced = smote.fit_resample(X, y)
X_train, X_val, y_train, y_val = train_test_split(X_balanced, y_balanced)
# → Synthetic data in validation! Results will be overoptimistic

# RIGHT: SMOTE only training set
X_train, X_val, y_train, y_val = train_test_split(X, y)
smote = SMOTE()
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
# → Only training has synthetic data, validation is real
```

### ❌ Optimizing for Accuracy

```python
# WRONG
accuracy = (y_pred == y_val).mean()
# → Misleading for imbalanced data

# RIGHT
auc_pr = average_precision_score(y_val, y_proba)
# → Tells truth about minority class performance
```

### ❌ Threshold Fixed at 0.5

```python
# WRONG: Always predict > 0.5 as positive
y_pred = (y_proba > 0.5).astype(int)

# RIGHT: Choose threshold based on business logic
threshold = 0.3  # Lower = more fraud predictions, higher recall
y_pred = (y_proba > threshold).astype(int)
```

---

## Summary: One-Liner Recommendations

1. **First attempt:** Use `class_weight='balanced'` parameter
2. **If not enough recall:** Add SMOTE to training data
3. **If still not good:** Combine SMOTE + class weights + threshold tuning
4. **Last resort:** Anomaly detection or data collection

**Always measure:** AUC-PR, Recall, Precision — never just accuracy.
