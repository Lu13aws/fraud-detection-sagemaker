# SageMaker Workflow Scripts

Reusable Python scripts for building end-to-end machine learning pipelines for fraud detection and similar imbalanced classification problems.

## Overview

These scripts extract the code examples from the SageMaker SKILL files and make them:
- **Testable** — Executable Python scripts, not markdown
- **Versionable** — Tracked in git, easy to update
- **Parameterizable** — Use environment variables for customization
- **Reusable** — Can be used across projects with different datasets

## Complete Workflow

```
01_initial_assessment.py
    ↓
02_duplicate_cleaning.py
    ↓
03_missing_values.py
    ↓
04_feature_engineering.py
    ↓
05_visualization_eda.py (Optional)
    ↓
06_baseline_modeling.py
    ↓
07_threshold_optimization.py
```

## Scripts

### 01_initial_assessment.py

**Purpose:** Perform initial assessment of dataset structure and quality

**Tasks:**
- Dataset shape analysis
- Column inspection and data types
- Missing value detection
- Duplicate detection
- Basic descriptive statistics
- Data quality observations
- Risk identification
- Recommended next steps

**Usage:**
```bash
python scripts/sagemaker_workflows/01_initial_assessment.py
```

**Custom S3 path:**
```bash
export S3_DATASET_PATH="s3://my-bucket/my-data.csv"
python scripts/sagemaker_workflows/01_initial_assessment.py
```

**Time:** 10-15 minutes

---

### 02_duplicate_cleaning.py

**Purpose:** Analyze duplicate records and remove them only when justified

**Tasks:**
- Duplicate count and percentage calculation
- Pattern analysis
- Impact assessment on modeling
- Fraud distribution in duplicates
- Decision-guided removal

**Usage:**
```bash
python scripts/sagemaker_workflows/02_duplicate_cleaning.py
```

**Time:** 15-20 minutes

---

### 03_missing_values.py

**Purpose:** Analyze missing values and recommend treatment strategies

**Tasks:**
- Missing value detection and severity assessment
- Treatment evaluation (imputation vs removal)
- Data quality scoring
- Recommendations per column

**Usage:**
```bash
python scripts/sagemaker_workflows/03_missing_values.py
```

**Time:** 15-20 minutes

---

### 04_feature_engineering.py

**Purpose:** Transform raw features and prepare data for modeling

**Tasks:**
- Feature selection and filtering
- Feature transformations (log, sqrt, power)
- Outlier handling
- Feature scaling (RobustScaler recommended)
- Stratified train/validation/test splits
- Data leakage prevention

**Critical Operations:**
- ✓ Fit scaler ONLY on training data
- ✓ Use stratified splits (preserve class distribution)
- ✓ Verify no data leakage between sets

**Usage:**
```bash
python scripts/sagemaker_workflows/04_feature_engineering.py
```

**Outputs:**
- X_train_scaled, X_val_scaled, X_test_scaled
- y_train, y_val, y_test
- Fitted scaler object

**Time:** 20-30 minutes

---

### 05_visualization_eda.py

**Purpose:** Create visualizations and identify patterns (Optional but recommended)

**Tasks:**
- Class distribution and imbalance analysis
- Feature correlation analysis
- Outlier detection and visualization
- Predictive feature identification
- Risk assessment for machine learning

**Usage:**
```bash
python scripts/sagemaker_workflows/05_visualization_eda.py
```

**Custom S3 path:**
```bash
export S3_DATASET_PATH="s3://my-bucket/my-data.csv"
python scripts/sagemaker_workflows/05_visualization_eda.py
```

**Notes:** This step provides critical insights but can be skipped if time-constrained. Outputs summary statistics and findings about data patterns.

**Time:** 15-25 minutes

---

### 06_baseline_modeling.py

**Purpose:** Train baseline models and compare imbalance-handling strategies

**Tasks:**
- Create stratified train/validation/test splits
- Scale features using RobustScaler
- Compare three imbalance strategies:
  1. Class Weights — Penalize minority class errors
  2. SMOTE Oversampling — Synthetic minority oversampling
  3. Random Undersampling — Reduce majority class
- Train Logistic Regression with each strategy
- Evaluate and identify best approach

**Usage:**
```bash
python scripts/sagemaker_workflows/06_baseline_modeling.py
```

**Key Metrics:**
- **Precision** — % of flagged cases that are true minority class
- **Recall** — % of actual minority class cases caught
- **F1 Score** — Harmonic mean (balanced metric)
- **AUC-PR** — Area under precision-recall curve ⭐ PRIMARY for imbalanced data
- **AUC-ROC** — Area under ROC curve

**Output:**
- Performance comparison table across all three strategies
- Best strategy recommendation (by AUC-PR)
- Test set evaluation with best model
- Classification report

**Time:** 20-30 minutes

---

### 07_threshold_optimization.py

**Purpose:** Find optimal decision thresholds based on business priorities

**Tasks:**
- Load trained baseline model from script 06
- Generate prediction probabilities for validation set
- Evaluate thresholds from 0.01 to 0.99
- Calculate Precision, Recall, F1 for each threshold
- Identify optimal thresholds:
  1. **F1 Maximization** — Balance precision and recall
  2. **Recall Maximization** — Catch as much minority class as possible
  3. **Precision Maximization** — Minimize false alarms
- Perform business tradeoff analysis
- Evaluate on test set and provide recommendations

**Usage:**
```bash
python scripts/sagemaker_workflows/07_threshold_optimization.py
```

**Configuration:**
```bash
export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
export BUSINESS_PRIORITY="recall"  # Options: "recall", "precision", "balanced"
python scripts/sagemaker_workflows/07_threshold_optimization.py
```

**Business Questions Answered:**
- How many false alarms can we accept?
- How much minority class must we catch?
- What's the cost of false alarm vs. missing minority class?

**Output:**
- Threshold analysis across 0.01-0.99 range
- Optimal thresholds for each strategy
- Business tradeoff analysis
- Test set performance recommendations

**Time:** 15-20 minutes

---

## Configuration

All scripts support customization via environment variables:

```bash
# Set custom S3 dataset path
export S3_DATASET_PATH="s3://your-bucket/your-data.csv"

# Run any script
python scripts/sagemaker_workflows/01_initial_assessment.py
```

### Supported Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `S3_DATASET_PATH` | `s3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv` | Path to dataset |

---

## Workflow Strategies

### Quick Path (Clean Data)
```
01 (5 min) → skip 02/03 → 04 (20 min) → 06 (25 min) → 07 (15 min)
Total: ~65 minutes
```

### Exploratory Path (Learning)
```
01 (15 min) → 02 (15 min) → 03 (15 min) → 04 (25 min) → 05 (20 min) → 06 (25 min) → 07 (15 min)
Total: ~130 minutes
```

### Production Path (Automated)
```
01 (5 min) → 02 (10 min) → 03 (5 min) → 04 (20 min) → 06 (25 min) → 07 (15 min)
Total: ~80 minutes
```

---

## Best Practices

### Data Integrity
✓ Always fit scalers ONLY on training data  
✓ Use stratified splits for classification  
✓ Never modify original data unexpectedly  
✓ Verify no data leakage between sets  

### Metrics & Evaluation
✓ For fraud detection: Use AUC-PR, not accuracy  
✓ Use Precision and Recall for imbalanced data  
✓ Compare multiple imbalance-handling strategies  
✓ Document metric interpretation  

### Reproducibility
✓ Set random_state=42 for reproducibility  
✓ Document all transformations applied  
✓ Save scaler object for future predictions  
✓ Preserve class distribution in splits  

---

## Troubleshooting

### Problem: Class distribution not preserved
**Solution:** Check that stratified split is used correctly in 04_feature_engineering.py

### Problem: Model performance drops on test set
**Possible causes:**
- Data leakage (scaler fit on entire dataset)
- Non-stratified split
- Feature scaling mismatch

**Solution:** Review data leakage checks in 04_feature_engineering.py

### Problem: Script can't find S3 data
**Solution:** Verify S3 path with:
```bash
aws s3 ls s3://your-bucket/your-data.csv
```

Or set custom path:
```bash
export S3_DATASET_PATH="s3://your-bucket/your-data.csv"
python scripts/sagemaker_workflows/01_initial_assessment.py
```

---

## Integration with SKILL Files

These scripts implement the code examples from the SageMaker SKILL files:
- `skills/aws/aws_sagemaker/SKILL1.md` → `01_initial_assessment.py`
- `skills/aws/aws_sagemaker/SKILL2.md` → `02_duplicate_cleaning.py`
- `skills/aws/aws_sagemaker/SKILL3.md` → `03_missing_values.py`
- `skills/aws/aws_sagemaker/SKILL4.md` → `04_feature_engineering.py`
- `skills/aws/aws_sagemaker/SKILL5.md` → `05_visualization_eda.py`
- `skills/aws/aws_sagemaker/SKILL6.md` → `06_baseline_modeling.py`
- `skills/aws/aws_sagemaker/SKILL7.md` → `07_threshold_optimization.py`

For conceptual guidance, always refer to the SKILL files. For practical execution, use these scripts.

---

## Next Steps

After completing the workflow:

### Option 1: Advanced Models
```
If baseline model isn't good enough:
→ Try tree-based models (Random Forest, XGBoost)
→ Use SageMaker training jobs for scalability
→ Implement hyperparameter tuning
```

### Option 2: Deploy & Monitor
```
If baseline model is satisfactory:
→ Register model in SageMaker Model Registry
→ Deploy to SageMaker Endpoint
→ Set up monitoring and retraining pipeline
```

### Option 3: Explainability
```
For business adoption:
→ Use SHAP for feature importance
→ Explain fraud detection decisions
→ Build stakeholder trust
```

---

## Requirements

- Python 3.13+
- pandas
- numpy
- scikit-learn
- scipy
- matplotlib (optional, for 05_visualization_eda.py)
- seaborn (optional, for 05_visualization_eda.py)

Install with:
```bash
pip install -r requirements.txt
```

---

## Author Notes

These scripts were extracted from the SageMaker SKILL files to improve:
- **Testability** — Code is now executable and versionable
- **Reusability** — Can be used with any dataset
- **Maintainability** — Easier to update and track changes
- **Reproducibility** — Deterministic execution with fixed parameters

---

## Success Criteria

You've successfully completed the workflow when:

✓ Data is clean and ready for modeling  
✓ Features are properly scaled  
✓ Splits are stratified (class distribution preserved)  
✓ Baseline model performance is documented  
✓ Imbalance handling strategy is chosen  
✓ Optimal decision threshold is identified  
✓ Business trade-offs are clear  

---

**Happy modeling! 🚀**
