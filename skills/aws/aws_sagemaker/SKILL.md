# SageMaker ML Workflow Skill

## Purpose

This skill guides Claude through building machine learning projects using AWS SageMaker.

Use this skill whenever:

* Data is stored in Amazon S3
* Machine learning models will be trained
* Model experiments need tracking
* Hyperparameter tuning is required
* Models should be registered or deployed
* AWS-native ML workflows are preferred

---

## Project Architecture

Typical workflow:

S3 (Raw Data)
→ EDA Notebook
→ Feature Engineering
→ Train/Test Split
→ Model Training
→ Evaluation
→ Hyperparameter Tuning
→ Model Registry
→ Deployment (Optional)

---

## Preferred Development Flow

Phase 1:
Develop locally using:

* VS Code
* Jupyter Notebooks
* Python Virtual Environment

Data source:

* Amazon S3

Phase 2:
Move workloads to SageMaker when:

* Training becomes computationally expensive
* Hyperparameter tuning is needed
* Experiments need tracking
* Models must be deployed

---

## Notebook Structure

01_eda.ipynb

Objectives:

* Dataset inspection
* Missing values
* Class imbalance analysis
* Correlation analysis
* Distribution analysis
* Data quality assessment

Outputs:

* Summary statistics
* Visualizations
* Initial findings

---

02_feature_engineering.ipynb

Objectives:

* Feature selection
* Feature transformations
* Outlier handling
* Scaling
* Train/Validation/Test split

Outputs:

* Clean modeling dataset

---

03_baseline_models.ipynb

Objectives:

Train simple baseline models:

* Logistic Regression
* Decision Tree
* Random Forest

Metrics:

* Precision
* Recall
* F1
* ROC-AUC
* PR-AUC

---

04_xgboost.ipynb

Objectives:

Train advanced gradient boosting model.

Preferred framework:

* XGBoost

Track:

* Parameters
* Metrics
* Feature importance

---

05_hyperparameter_tuning.ipynb

Use:

* SageMaker Hyperparameter Tuning Jobs

Optimize:

* Learning rate
* Max depth
* Number of estimators
* Regularization parameters

Goal:

* Improve recall while maintaining precision

---

06_model_registry.ipynb

Register best-performing model.

Store:

* Metrics
* Artifacts
* Metadata

Use SageMaker Model Registry.

---

07_deployment.ipynb

Optional.

Deploy model to:

* SageMaker Endpoint

Evaluate:

* Latency
* Cost
* Throughput

---

## SageMaker Services

### Training Jobs

Use when:

* Local training becomes slow (>30 min)
* Large datasets exist
* Need automatic CloudWatch logging
* Want to scale to larger instances without local resource constraints

**Benefits:**
* Managed infrastructure (no manual setup)
* Automatic CloudWatch logging
* Reproducibility (same code = same results)
* Can use GPU/distributed training
* Hyperparameter tuning integration
* Automatic metrics capture

#### Choosing a Training Framework

| Framework | Best For | When to use | Setup |
|-----------|----------|------------|-------|
| **SKLearn Estimator** | scikit-learn, XGBoost, custom Python | Classification, regression, standard ML | Simplest; pass entry_point script |
| **XGBoost Estimator** | Native XGBoost (optimized) | Want optimal XGBoost performance | XGBoost-specific optimizations |
| **Custom Docker** | Proprietary models, complex logic | Anything that doesn't fit above | Most control, more setup |

**Recommendation:** Start with SKLearn Estimator — it handles scikit-learn AND XGBoost.

**SKLearn Estimator Example:**
```python
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.inputs import TrainingInput
import sagemaker

role = sagemaker.get_execution_role()
session = sagemaker.Session()
bucket = session.default_bucket()

# Define estimator
estimator = SKLearn(
    entry_point='src/train_xgboost.py',  # Your training script
    role=role,
    instance_type='ml.m5.large',
    instance_count=1,
    framework_version='1.2-1',
    hyperparameters={
        'n-estimators': 200,
        'max-depth': 6,
        'learning-rate': 0.1,
    },
    metric_definitions=[
        {'Name': 'validation:auc_pr', 'Regex': r'auc_pr=([0-9\.]+)'},
    ]
)

# Launch training job
estimator.fit(
    inputs={
        'train': TrainingInput(f's3://{bucket}/fraud-detection/data/train/train.csv'),
        'validation': TrainingInput(f's3://{bucket}/fraud-detection/data/val/val.csv'),
    },
    job_name='fraud-detection-xgb-1',
    wait=False  # Non-blocking
)
```

---

### SageMaker Experiments

Automatically track and compare multiple model training runs.

**What to track:**
* Model type and hyperparameters
* Evaluation metrics (AUC-PR, AUC-ROC, precision, recall)
* Training time
* Feature importance

**Why it matters:** Compare 6+ configurations side-by-side in AWS console. No manual spreadsheet tracking.

#### Automated Experiment Tracking Pattern

```python
from sagemaker.experiments.run import Run
from sagemaker.sklearn.estimator import SKLearn
import boto3

experiment_name = 'fraud-detection-models'
bucket = 'your-bucket'
role = sagemaker.get_execution_role()

# Create experiment (once)
from sagemaker.experiments import Experiment
Experiment.create(
    experiment_name=experiment_name,
    description='Fraud detection: comparing RF and XGBoost with imbalance strategies'
)

# Configuration 1: XGBoost with auto scale_pos_weight
with Run.create(
    experiment_name=experiment_name,
    run_name='xgb-auto-weight',
    sagemaker_session=session
) as run:
    estimator = SKLearn(
        entry_point='src/train_xgboost.py',
        role=role,
        instance_type='ml.m5.large',
        hyperparameters={
            'n-estimators': 200,
            'max-depth': 6,
            'learning-rate': 0.1,
        },
        metric_definitions=[
            {'Name': 'auc_pr', 'Regex': r'auc_pr=([0-9\.]+)'},
        ]
    )
    
    estimator.fit(
        inputs={
            'train': TrainingInput(f's3://{bucket}/fraud-detection/data/train/train.csv'),
            'validation': TrainingInput(f's3://{bucket}/fraud-detection/data/val/val.csv'),
        },
        job_name='xgb-auto-weight'
    )
    
    # Log metrics to experiment
    run.log_metric(name='auc_pr', value=0.82)
    run.log_parameter(name='scale_pos_weight', value='auto')

# Configuration 2: Random Forest with class_weight
with Run.create(
    experiment_name=experiment_name,
    run_name='rf-balanced',
    sagemaker_session=session
) as run:
    estimator = SKLearn(
        entry_point='src/train_rf.py',
        role=role,
        instance_type='ml.m5.large',
        hyperparameters={
            'n-estimators': 200,
            'class-weight': 'balanced',
        }
    )
    
    estimator.fit(
        inputs={'train': TrainingInput(f's3://{bucket}/fraud-detection/data/train/train.csv')},
        job_name='rf-balanced'
    )
    
    run.log_metric(name='auc_pr', value=0.79)
    run.log_parameter(name='class_weight', value='balanced')

# Compare all runs
from sagemaker.analytics import ExperimentAnalytics

analytics = ExperimentAnalytics(
    experiment_name=experiment_name,
    metric_names=['auc_pr'],
    sort_by='metrics.auc_pr.max',
    sort_order='Descending'
)

results_df = analytics.dataframe()
print(results_df[['TrialComponentName', 'metrics.auc_pr.max']].to_string(index=False))
```

**Result:** SageMaker console shows side-by-side comparison of all 6+ runs with metrics and parameters.

---

### SageMaker Model Registry

Store:

* Approved models
* Version history
* Evaluation metadata

---

### SageMaker Endpoints

Use only when:

* Real-time inference is required

Avoid deploying endpoints during development.

Endpoints generate continuous costs.

Always delete unused endpoints.

---

## Cost Awareness

**Golden Rule:** AWS charges per SECOND of compute usage. A forgotten endpoint costs $50+/month.

### Typical SageMaker Costs (US East, 2025)

| Resource | Instance Type | Cost | Notes |
|----------|---------------|------|-------|
| **Training Job** | ml.m5.large | $0.384/hour | Typical ML training |
| **Training Job** | ml.m5.xlarge | $0.768/hour | Double the CPU/memory |
| **Training Job** | ml.p3.2xlarge (GPU) | $3.06/hour | For deep learning |
| **Notebook Instance** | ml.t3.medium | $0.048/hour | Development notebooks |
| **Notebook Instance** | ml.t3.large | $0.096/hour | Medium workloads |
| **Endpoint** | ml.t2.medium | ~$37/month | NEVER forget to delete! |
| **Endpoint** | ml.m5.large | ~$290/month | NEVER forget to delete! |

**Cost estimation:**
- 1 hour training on ml.m5.large = $0.384
- 8 experiments × 10 min each = 1.33 hours = $0.51
- Leaving endpoint running 1 month = $290+

### Cost Optimization Tips

1. **During Development:**
   - Use local notebooks (free)
   - Use S3 for data storage (cheap: ~$0.023/GB/month)
   - Only move to SageMaker Training when necessary

2. **Before Launching Training Job:**
   ```python
   # Estimate cost
   hours = (expected_training_minutes) / 60
   hourly_rate = 0.384  # ml.m5.large
   cost = hours * hourly_rate
   print(f'Expected cost: ${cost:.2f}')
   ```

3. **After Using SageMaker:**
   ```python
   # ALWAYS delete endpoints when done
   predictor.delete_endpoint()
   predictor.delete_model()
   
   # ALWAYS stop notebook instances
   # Do this via AWS console or boto3
   ```

4. **Monitor Costs:**
   - Use AWS Cost Explorer
   - Set up billing alerts (AWS Budgets)
   - Regular cleanup (AWS Config)

### Fraud Detection Project Cost Estimate

| Task | Instance | Duration | Cost |
|------|----------|----------|------|
| 5 EDA notebooks (local) | Free tier | 10 hours | $0 |
| Train 6 models | ml.m5.large | 1 hour total | $0.38 |
| Hyperparameter tuning | ml.m5.large | 4 hours | $1.54 |
| **Total** | - | - | **~$2** |

Much cheaper than leaving an endpoint running! ✅

---

## AWS Services Commonly Used

Storage:

* Amazon S3

Machine Learning:

* SageMaker
* SageMaker Experiments
* SageMaker Model Registry

Analytics:

* Athena
* Glue

Monitoring:

* CloudWatch

Security:

* IAM Roles

---

## Preprocessing & Data Automation

Before training on SageMaker, prepare data locally using deterministic preprocessing.

### Preprocessing Workflow

```python
from src.preprocessing import (
    scale_features,
    split_data,
    apply_smote,
    compute_class_weights
)

# Load from S3
from config.aws_config import read_csv_from_s3, S3_DATA_PREFIX
df = read_csv_from_s3(f"{S3_DATA_PREFIX}/creditcard.csv")

# 1. Scale features
df = scale_features(df)  # StandardScaler on Amount, Time; leave V1-V28 as-is (PCA-transformed)

# 2. Create stratified splits
X_train, X_val, X_test, y_train, y_val, y_test = split_data(df)
print(f'Train: {X_train.shape}, fraud={y_train.sum()} ({y_train.mean()*100:.3f}%)')
print(f'Val:   {X_val.shape},   fraud={y_val.sum()} ({y_val.mean()*100:.3f}%)')
print(f'Test:  {X_test.shape},  fraud={y_test.sum()} ({y_test.mean()*100:.3f}%)')

# 3. Handle class imbalance (choose ONE strategy)
# Strategy A: Class weights (simplest, no data changes)
weights = compute_class_weights(y_train)
# Pass to model: LogisticRegression(class_weight=weights)

# Strategy B: SMOTE oversampling
X_train_balanced, y_train_balanced = apply_smote(X_train, y_train)

# 4. Save for SageMaker (XGBoost format: label first, no header)
# SageMaker expects: first column = label, no header
import pandas as pd
train_df = pd.concat([y_train.reset_index(drop=True), X_train.reset_index(drop=True)], axis=1)
train_df.to_csv('../data/splits/train.csv', index=False, header=False)

val_df = pd.concat([y_val.reset_index(drop=True), X_val.reset_index(drop=True)], axis=1)
val_df.to_csv('../data/splits/val.csv', index=False, header=False)

# 5. Upload to S3
import boto3
s3 = boto3.client('s3')
s3.upload_file('../data/splits/train.csv', bucket, 'fraud-detection/data/train/train.csv')
s3.upload_file('../data/splits/val.csv', bucket, 'fraud-detection/data/val/val.csv')
```

### Reproducibility Checklist

Before launching SageMaker jobs:

- ✅ Set random seeds (numpy, sklearn, xgboost)
- ✅ Use stratified splits
- ✅ Document imbalance strategy
- ✅ Version dataset (S3 path in config)
- ✅ Track preprocessing steps
- ✅ Save train/val/test metrics baseline

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

Preprocessing utilities:

* src/preprocessing.py (custom — included in project)
* imblearn (SMOTE, undersampling)

---

## Deliverables

Every ML project should produce:

* Architecture diagram
* README.md
* Jupyter notebooks
* Evaluation report
* Model comparison
* GitHub repository

Projects must be reproducible end-to-end.
