# Machine Learning Workflow Skill

## Purpose

This skill guides Claude through the complete lifecycle of a machine learning project.

Use this skill whenever:

* A machine learning project is created
* Data analysis is required
* Predictive models will be trained
* Classification, regression, forecasting, or anomaly detection tasks are involved
* A reproducible end-to-end workflow is needed

---

## Core Principle

Always follow a structured machine learning workflow.

Never jump directly into model training.

Understand the data first.

---

## Standard Project Lifecycle

1. Business Understanding
2. Data Understanding
3. Exploratory Data Analysis (EDA)
4. Data Cleaning
5. Feature Engineering
6. Model Development
7. Model Evaluation
8. Model Comparison
9. Model Selection
10. Deployment (Optional)

---

## Project Structure

Recommended layout:

project/

├── data/
│   ├── raw/
│   ├── processed/
│   └── splits/
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_baseline_models.ipynb
│   ├── 04_advanced_models.ipynb
│   └── 05_model_comparison.ipynb
│
├── src/
│   ├── preprocessing.py
│   └── train_*.py
│
├── config/
│   └── aws_config.py
│
├── scripts/
│
├── README.md
│
└── requirements.txt

---

## Real-World Example: Credit Card Fraud Detection

This skill is used in the **Fraud Detection with AWS SageMaker** project.

**Project mapping:**

| Phase | Step | Notebook | Goal |
|-------|------|----------|------|
| Phase 1 | Steps 1-3 | `01_eda.ipynb` | Understand 0.17% fraud rate, class imbalance, feature distributions |
| Phase 2-3 | Steps 4-5, 9 | `02_baseline.ipynb` | Scale features, compare 3 imbalance strategies (class weights, SMOTE, undersampling), train Logistic Regression |
| Phase 4 | Steps 6-8 | `03_tree_models.ipynb` | Train Random Forest + XGBoost via SageMaker, track experiments, compare 6 configurations |
| Phase 5 | Step 7 | `04_anomaly_detection.ipynb` | Compare unsupervised Random Cut Forest (cold-start alternative) |
| Phase 6-7 | Steps 8-10 | `05_threshold_tuning.ipynb` | Tune decision threshold using precision-recall curves, SHAP explainability analysis |

**Key constraint:** Fraud is rare (0.17%), so accuracy is useless — focus on AUC-PR, precision, recall, and business-driven threshold selection.

---

## Step 1: Business Understanding

Define:

* Problem statement
* Business objective
* Success criteria

Examples:

* Fraud Detection
* Churn Prediction
* Sales Forecasting
* Customer Segmentation
* Anomaly Detection

Always document:

* Goal
* Expected outcome
* Stakeholders
* Risks

---

## Step 2: Data Understanding

Inspect:

* Number of rows
* Number of columns
* Data types
* Missing values
* Duplicates
* Target variable

Generate:

* Data summary
* Initial observations

Questions:

* What is the target?
* What features are available?
* Is data quality acceptable?

---

## Step 3: Exploratory Data Analysis

Perform:

* Descriptive statistics
* Histograms
* Boxplots
* Correlation analysis
* Target distribution analysis

Investigate:

* Class imbalance
* Outliers
* Feature distributions
* Relationships between variables

Document findings.

---

## Step 4: Data Cleaning

Handle:

* Missing values
* Duplicate records
* Invalid data
* Extreme outliers

Document all cleaning decisions.

Maintain reproducibility.

---

## Step 5: Feature Engineering

Possible techniques:

* Scaling
* Normalization
* Encoding
* Aggregations
* Date transformations
* Interaction features

Create:

* Modeling dataset

Store processed outputs separately from raw data.

---

## Step 6: Train Baseline Models

Start simple. Baseline models establish a performance floor and help understand feature importance.

**Preferred baseline models:**

**Classification:**
* Logistic Regression
* Decision Tree

**Regression:**
* Linear Regression
* Decision Tree Regressor

**Never start with complex models.** Baselines are fast to train and interpretable.

### Default Hyperparameters

**Logistic Regression (Classification)**
```python
from sklearn.linear_model import LogisticRegression

# For imbalanced data, use class_weight='balanced'
model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight='balanced'  # Critical for imbalanced classification
)
model.fit(X_train, y_train)
```

**Decision Tree (Classification)**
```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train, y_train)
```

**Linear Regression (Regression)**
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
```

**Decision Tree Regressor (Regression)**
```python
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)
```

**Key point:** Always fix `random_state=42` for reproducibility.

---

## Step 7: Advanced Models

Move to sophisticated algorithms after baselines. Use these to improve performance.

### Model Selection by Task

**Classification:**
* Random Forest
* XGBoost
* LightGBM

**Regression:**
* Random Forest Regressor
* XGBoost Regressor

**Anomaly Detection:**
* Isolation Forest
* One-Class SVM

**Forecasting:**
* Prophet
* XGBoost
* LSTM (if justified)

### Recommended Hyperparameters

**Random Forest (Classification)**
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=200,        # Number of trees
    max_depth=10,            # Tree depth
    min_samples_split=5,     # Minimum samples to split
    random_state=42,
    class_weight='balanced', # For imbalanced data
    n_jobs=-1                # Use all cores
)
model.fit(X_train, y_train)
```

**XGBoost (Classification)**
```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    eval_metric='logloss',
    scale_pos_weight=None,  # Set dynamically for imbalanced data
    n_jobs=-1
)
model.fit(X_train, y_train)
```

**For imbalanced classification:** Compute `scale_pos_weight = count_negative / count_positive`:
```python
# Compute scale_pos_weight dynamically
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
# Then pass to XGBClassifier(scale_pos_weight=scale_pos_weight)
```

**Key points:**
- XGBoost with `scale_pos_weight` often outperforms RF on imbalanced data
- Random Forest with `class_weight='balanced'` is simpler alternative
- Always use validation set to prevent overfitting

---

## Step 8: Model Evaluation

Classification Metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* PR-AUC

Regression Metrics:

* MAE
* RMSE
* R²

Always compare multiple metrics.

Never rely on accuracy alone.

Especially avoid accuracy for imbalanced datasets.

---

## Step 9: Class Imbalance Handling

**When to apply:** If minority class < 10% of data, special handling is critical.

**Why it matters:** Models trained on imbalanced data learn to ignore the minority class. Accuracy becomes meaningless.

**Example:** Fraud detection (0.17% fraud rate) — a model predicting "never fraud" achieves 99.83% accuracy but catches zero fraud.

### Strategy Comparison

| Strategy | When to use | Implementation | Pros | Cons | Code reference |
|----------|-------------|-----------------|------|------|-----------------|
| **Class weights** | Always try first (simplest) | Pass `class_weight='balanced'` to model | No data changes, built-in to sklearn | Limited control, may not work for extreme imbalance | sklearn default parameter |
| **SMOTE** | Moderate imbalance (1:50 or better) | Synthetic oversampling of minority | Creates synthetic diversity, improves recall | Risk of overfitting synthetic patterns | `imblearn.over_sampling.SMOTE` |
| **Undersampling** | Large majority class, huge dataset | Random removal of majority class | Fast, reduces training time | Loses real data, information loss | `imblearn.under_sampling.RandomUnderSampler` |
| **Threshold tuning** | After model training | Adjust decision boundary via precision-recall curve | No retraining needed, business-driven | Requires labeled validation set | Post-prediction adjustment |

### Code Examples

**Strategy 1: Class Weights (Recommended starting point)**
```python
from sklearn.linear_model import LogisticRegression

# Built-in: model handles imbalance automatically
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)
```

**Strategy 2: SMOTE Oversampling**
```python
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

# Oversample minority class on TRAINING SET ONLY
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print(f'Before SMOTE: {y_train.sum()} fraud cases')
print(f'After SMOTE: {y_train_smote.sum()} fraud cases')

# Train on balanced data
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_smote, y_train_smote)

# Evaluate on ORIGINAL val/test sets (not SMOTE)
y_pred = model.predict(X_val)
```

**Strategy 3: Undersampling Majority Class**
```python
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier

# Undersample majority class on TRAINING SET ONLY
undersampler = RandomUnderSampler(sampling_strategy=0.1, random_state=42)
X_train_under, y_train_under = undersampler.fit_resample(X_train, y_train)

print(f'Before undersampling: {X_train.shape}')
print(f'After undersampling: {X_train_under.shape}')

# Train on balanced data
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_under, y_train_under)

# Evaluate on ORIGINAL val/test sets
y_pred = model.predict(X_val)
```

### Evaluation After Imbalance Handling

Always check these metrics:

```python
from sklearn.metrics import precision_recall_curve, average_precision_score

# AUC-PR is the PRIMARY metric for imbalanced classification
auc_pr = average_precision_score(y_val, y_pred_proba)

# Plot precision-recall curve to find best threshold
precision, recall, thresholds = precision_recall_curve(y_val, y_pred_proba)

# Decision: choose threshold based on business logic
# High recall (catch fraud): threshold ≈ 0.5
# High precision (minimize false alarms): threshold ≈ 0.7
```

### Real-World Example: Fraud Detection

```python
from src.preprocessing import apply_smote, undersample_majority, compute_class_weights

# Method 1: Class weights (fastest)
lr = LogisticRegression(class_weight='balanced', max_iter=1000)
lr.fit(X_train, y_train)
auc_pr_1 = average_precision_score(y_val, lr.predict_proba(X_val)[:, 1])

# Method 2: SMOTE
X_train_smote, y_train_smote = apply_smote(X_train, y_train)
rf = RandomForestClassifier(n_estimators=200)
rf.fit(X_train_smote, y_train_smote)
auc_pr_2 = average_precision_score(y_val, rf.predict_proba(X_val)[:, 1])

# Method 3: Undersampling
X_train_under, y_train_under = undersample_majority(X_train, y_train, ratio=0.1)
rf_under = RandomForestClassifier(n_estimators=200)
rf_under.fit(X_train_under, y_train_under)
auc_pr_3 = average_precision_score(y_val, rf_under.predict_proba(X_val)[:, 1])

# Compare: which strategy works best?
print(f'Class weights AUC-PR: {auc_pr_1:.4f}')
print(f'SMOTE AUC-PR: {auc_pr_2:.4f}')
print(f'Undersampling AUC-PR: {auc_pr_3:.4f}')
```

---

## Step 10: Model Comparison

Compare:

* Metrics
* Training time
* Complexity
* Interpretability

Select the best model based on business goals.

---

## Explainability

Whenever possible:

Use:

* Feature importance
* Permutation importance
* SHAP

Document key drivers.

---

## Reproducibility

Always:

* Fix random seeds
* Version datasets
* Version code
* Document assumptions

Results must be reproducible.

---

## Deliverables

Every project should produce:

* README.md
* Architecture diagram
* EDA notebook
* Feature engineering notebook
* Model comparison notebook
* Final evaluation report

---

## AWS Integration

If AWS services are used:

* S3 for storage
* SageMaker for training
* SageMaker Experiments
* SageMaker Model Registry

Then additionally load:

sagemaker_ml_workflow

and follow AWS-specific best practices.

---

## Preferred Libraries

Data:

* pandas
* numpy

Visualization:

* matplotlib
* seaborn

Machine Learning:

* scikit-learn
* xgboost

AWS:

* boto3
* sagemaker

---

## Final Objective

Produce a machine learning solution that is:

* Reproducible
* Explainable
* Maintainable
* Business-focused
* Production-ready where appropriate
