# Jupyter Notebook Workflow Skill

## Purpose

This skill guides best practices for writing reproducible, maintainable Jupyter notebooks.

Use this skill whenever:

* Creating exploratory data analysis (EDA) notebooks
* Building machine learning training notebooks
* Developing data transformation workflows
* Working in interactive development environments
* Need to ensure notebook reproducibility and collaboration

---

## Core Principles

1. **Reproducibility First** — Same code run twice produces identical results
2. **Clarity Over Cleverness** — Write for humans to read, machines to execute
3. **Modular Cells** — Each cell does one logical thing
4. **No Hidden State** — Avoid running cells out of order
5. **Self-Documenting** — Code is clear; markdown explains why

---

## Notebook Structure

### File Naming Convention

```
01_eda.ipynb                    ← 2-digit prefix, descriptive name
02_feature_engineering.ipynb
03_baseline_models.ipynb
04_advanced_models.ipynb
05_threshold_tuning.ipynb
```

**Why 2-digit prefix:** Forces execution order and prevents sorting confusion.

### Notebook Metadata

Every notebook should start with a title cell:

```markdown
# Phase 1: Exploratory Data Analysis

**Goal:** Understand dataset structure, class imbalance, feature relationships

**Dataset:** Kaggle Credit Card Fraud Detection (284,807 transactions, 0.17% fraud)

**Outputs:** EDA visualizations, distribution plots, correlation heatmap

**Time estimate:** 10-15 minutes
```

---

## Cell Organization

### Cell 1: Imports & Configuration

**ALWAYS put imports first and in one cell.**

```python
import sys
sys.path.insert(0, '..')  # Add parent to path for src/ imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure matplotlib
sns.set_theme(style='whitegrid')
%matplotlib inline
%config InlineBackend.figure_format = 'png'  # Crisp images

# Reproducibility
np.random.seed(42)
import random
random.seed(42)
```

**Why this matters:**
- All imports visible upfront
- Reproducibility via fixed seeds
- Path configuration explicit
- Jupyter magic commands documented

### Cell 2: Load Data

**Load from S3 (or local fallback for development):**

```python
from config.aws_config import read_csv_from_s3, S3_BUCKET, S3_DATA_PREFIX

# Load from S3
s3_key = f"{S3_DATA_PREFIX}/creditcard.csv"
df = read_csv_from_s3(s3_key)

print(f'Loaded from S3: s3://{S3_BUCKET}/{s3_key}')
print(f'Shape: {df.shape}')
df.head()
```

**Why S3:**
- Same code works on any machine
- No local data copies
- Scalable to large files

### Cells 3+: Analysis

**Structure: Markdown title + Code + Output**

```markdown
## 2. Class Imbalance Analysis

Class imbalance is critical for fraud detection. 
Rare fraud events need special handling.
```

```python
class_counts = df['Class'].value_counts()
fraud_rate = class_counts[1] / len(df) * 100

print(f'Legitimate: {class_counts[0]:,} ({100-fraud_rate:.2f}%)')
print(f'Fraudulent: {class_counts[1]:,} ({fraud_rate:.4f}%)')
print(f'Imbalance ratio: 1:{class_counts[0]/class_counts[1]:.0f}')
```

**Output shows insight, not just numbers.**

---

## Cell Best Practices

### Do

✅ **One concern per cell**
```python
# Good: Each cell does one thing
# Cell A: Load data
df = read_csv_from_s3(...)

# Cell B: Inspect data
print(f'Shape: {df.shape}')
df.info()

# Cell C: Check nulls
print(df.isnull().sum())
```

✅ **Explicit variable names**
```python
# Good
fraud_rate = (y == 1).sum() / len(y)
legitimate_count = (y == 0).sum()

# Avoid
fr = (y == 1).sum() / len(y)
lc = (y == 0).sum()
```

✅ **Use functions for repeated logic**
```python
def evaluate_model(model, X, y, name='Model'):
    """Evaluate classification model."""
    y_pred = model.predict(X)
    acc = (y_pred == y).mean()
    print(f'{name}: Accuracy = {acc:.4f}')

evaluate_model(model_1, X_val, y_val, 'LR no weight')
evaluate_model(model_2, X_val, y_val, 'LR balanced')
```

✅ **Document assumptions**
```python
# Assumption: V1-V28 are PCA-transformed (already normalized)
# Only Amount and Time need scaling
df['Amount'] = StandardScaler().fit_transform(df[['Amount']])
df['Time'] = StandardScaler().fit_transform(df[['Time']])
```

### Don't

❌ **Run cells out of order**
```python
# BAD: Depends on previous cells
y_pred = model.predict(X_val)  # model defined 3 cells up

# GOOD: Redefine if needed, or restart kernel and run from top
```

❌ **Modify global state unexpectedly**
```python
# BAD: Changes dataframe in place
df.drop(columns=['temp'], inplace=True)

# GOOD: Create new variable
df_clean = df.drop(columns=['temp'])
```

❌ **Magic numbers without explanation**
```python
# BAD: Why 0.5?
threshold = 0.5
y_pred = (y_proba > threshold).astype(int)

# GOOD: Explain
# Choose threshold = 0.5 for balanced precision-recall tradeoff
threshold = 0.5
y_pred = (y_proba > threshold).astype(int)
```

❌ **Extremely long cells**
```python
# BAD: 100 lines in one cell
# If it fails, can't debug easily

# GOOD: Break into logical chunks
# Cell A: Load and inspect
# Cell B: Clean data
# Cell C: Visualize
```

---

## Output Management

### Save Figures

**Always save visualizations to `data/` folder:**

```python
plt.figure(figsize=(10, 6))
plt.hist(df[df['Class'] == 0]['Amount'], bins=100, alpha=0.7)
plt.title('Transaction Amount Distribution (Legitimate)')
plt.xlabel('Amount (€)')

# Save with descriptive name
plt.savefig('../data/eda_amount_legitimate.png', dpi=120, bbox_inches='tight')
plt.show()
```

**Why:**
- Separate data from code
- Versioned in git (if committed)
- Easy to reference in reports

### Clear Output

**Use `print()` liberally for clarity:**

```python
print('='*50)
print('DATA QUALITY CHECK')
print('='*50)
print(f'Total rows: {len(df):,}')
print(f'Total columns: {len(df.columns)}')
print(f'Duplicate rows: {df.duplicated().sum()}')
print(f'Missing values: {df.isnull().sum().sum()}')
print('✓ Data quality OK')
```

**Why:** Makes notebooks self-documenting, easy to scan.

---

## Reproducibility Checklist

Before sharing/committing a notebook:

- [ ] **Imports cell runs first** — No mysterious undefined variables
- [ ] **Random seeds set** — `np.random.seed(42)`, `tf.random.set_seed(42)`
- [ ] **Data loaded from S3** — Not hardcoded local paths
- [ ] **No cell dependencies** — Can restart kernel and run top-to-bottom
- [ ] **Paths relative** — `../data/file.csv` not `/Users/john/...`
- [ ] **Output saved** — Figures, CSVs go to `data/` folder
- [ ] **Clear markdown** — Explains sections and assumptions
- [ ] **No commented-out code** — Delete or move to separate notebook
- [ ] **Execution time < 30 min** — User can run end-to-end quickly

---

## Common Jupyter Magic Commands

```python
# Display settings
%matplotlib inline           # Show plots in notebook
%config InlineBackend.figure_format = 'png'

# Debugging
%timeit df.sum()            # Time a line
%time result = expensive_operation()

# Development
%load_ext autoreload       # Auto-reload modules
%autoreload 2

# System commands
!pip install package       # Install packages
!ls ../data/               # List files
```

---

## Example Notebook Structure

```python
# ============================================================================
# CELL 1: Imports & Config
# ============================================================================
import sys
sys.path.insert(0, '..')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sns.set_theme(style='whitegrid')
np.random.seed(42)

# ============================================================================
# CELL 2: Load Data
# ============================================================================
from config.aws_config import read_csv_from_s3, S3_DATA_PREFIX, S3_BUCKET

df = read_csv_from_s3(f"{S3_DATA_PREFIX}/creditcard.csv")
print(f'Loaded: {df.shape[0]:,} rows, {df.shape[1]} columns')

# ============================================================================
# CELL 3: Data Inspection
# ============================================================================
# Check for nulls, duplicates, data types
print(f'Nulls: {df.isnull().sum().sum()}')
print(f'Duplicates: {df.duplicated().sum()}')
df.dtypes

# ============================================================================
# CELL 4: Class Distribution (MARKDOWN + CODE)
# ============================================================================
# ## Class Imbalance Analysis
# 
# Fraud is rare (0.17%). Need special handling.

class_counts = df['Class'].value_counts()
fraud_rate = class_counts[1] / len(df) * 100
print(f'Fraud rate: {fraud_rate:.4f}%')

# ============================================================================
# CELL 5: Visualization
# ============================================================================
fig, ax = plt.subplots()
ax.bar(['Legitimate', 'Fraud'], class_counts.values)
plt.savefig('../data/eda_class_distribution.png', dpi=120)
plt.show()
```

---

## Sharing & Collaboration

### Before Committing

1. **Clear all outputs:** `Kernel → Restart & Clear Output`
2. **Run all cells:** `Cell → Run All`
3. **Verify no errors**
4. **Check reproducibility:** Run again, same output?

### For Team Review

Include in commit message:

```
Add 01_eda.ipynb

- Analyzed 284K transactions
- Found 0.17% fraud rate
- Identified 4 key discriminative features (V4, V11, V14, V17)
- Time to run: ~5 min
```

### Notebook-as-Report

Notebooks ARE documentation:

- Clear markdown sections
- Self-explanatory code
- Visualizations embedded
- Findings highlighted

No separate README needed for a well-structured notebook.

---

## Troubleshooting

### "NameError: name 'X' is not defined"

**Cause:** Cell ran out of order.  
**Fix:** Restart kernel (`Kernel → Restart`) and run all cells in order.

### "ModuleNotFoundError: No module named 'src'"

**Cause:** Missing path setup.  
**Fix:** Ensure Cell 1 has:
```python
import sys
sys.path.insert(0, '..')
```

### "FileNotFoundError: ../data/file.csv"

**Cause:** Ran notebook from wrong directory.  
**Fix:** Use S3 paths or check working directory:
```python
import os
print(os.getcwd())
```

### Notebook too slow

**Solution:**
- Reduce dataset size for development
- Add sampling: `df_sample = df.sample(frac=0.1, random_state=42)`
- Cache intermediate results
- Use `%%time` to find bottleneck

---

## Final Principle

**A good notebook reads like a story:**
- Clear beginning (imports, data load)
- Middle (analysis, investigation)
- End (conclusions, next steps)

Anyone should understand what you did, why, and what you found — without running the code.
