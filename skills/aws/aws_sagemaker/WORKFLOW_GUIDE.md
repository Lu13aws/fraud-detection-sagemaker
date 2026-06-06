# SageMaker ML Workflow Guide

## Overview

This guide shows how to use the SageMaker skills in the correct sequence to build a complete machine learning project from raw data to optimized models.

The workflow is designed for **fraud detection and other imbalanced classification problems** using AWS SageMaker, but is generalizable to other ML tasks.

---

## Complete Workflow

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                    CREDIT CARD FRAUD DETECTION WORKFLOW                        ║
╚════════════════════════════════════════════════════════════════════════════════╝

PHASE 1: DATA ASSESSMENT & CLEANING
═════════════════════════════════════════════════════════════════════════════════

  ↓
  SKILL1: Initial Data Assessment
  ├─ Dataset shape analysis
  ├─ Missing value detection
  ├─ Duplicate detection
  ├─ Basic statistics
  └─ Output: Understand data quality

  ↓
  SKILL2: Duplicate Assessment & Cleaning
  ├─ Identify duplicate records
  ├─ Assess impact on modeling
  ├─ Remove duplicates if needed
  └─ Output: Clean, deduplicated dataset

  ↓
  SKILL3: Missing Values Assessment
  ├─ Analyze missing data patterns
  ├─ Determine treatment strategy
  ├─ Apply imputation (if needed)
  └─ Output: Complete dataset, ready for feature engineering

═════════════════════════════════════════════════════════════════════════════════

PHASE 2: FEATURE ENGINEERING & PREPARATION
═════════════════════════════════════════════════════════════════════════════════

  ↓
  SKILL4: Feature Engineering & Scaling ⭐ NEW
  ├─ Select relevant features
  ├─ Apply transformations (log, sqrt, etc.)
  ├─ Scale features (RobustScaler, StandardScaler)
  ├─ Create stratified train/val/test splits
  └─ Output: Scaled features, proper data splits, scaler object

═════════════════════════════════════════════════════════════════════════════════

PHASE 3: EXPLORATION & VISUALIZATION (Optional)
═════════════════════════════════════════════════════════════════════════════════

  ↓
  SKILL5: Visualization & Exploratory Data Analysis
  ├─ Class distribution analysis
  ├─ Feature correlation analysis
  ├─ Outlier visualization
  ├─ Predictive feature identification
  └─ Output: Visualizations, insights, feature recommendations

═════════════════════════════════════════════════════════════════════════════════

PHASE 4: BASELINE MODELING
═════════════════════════════════════════════════════════════════════════════════

  ↓
  SKILL6: ML Baseline Modeling
  ├─ Train initial models (Logistic Regression, Decision Tree)
  ├─ Evaluate with appropriate metrics (Precision, Recall, F1, AUC-PR)
  ├─ Compare different imbalance strategies (class weights, SMOTE, undersampling)
  └─ Output: Baseline model performance, best approach selection

═════════════════════════════════════════════════════════════════════════════════

PHASE 5: THRESHOLD OPTIMIZATION & PRODUCTION READINESS
═════════════════════════════════════════════════════════════════════════════════

  ↓
  SKILL7: Threshold Optimization
  ├─ Evaluate thresholds 0.01 to 0.99
  ├─ Calculate metrics for each threshold
  ├─ Identify optimal thresholds (F1, Recall, Precision)
  ├─ Trade-off analysis (precision vs recall)
  └─ Output: Recommended decision threshold, business trade-off analysis

═════════════════════════════════════════════════════════════════════════════════

RESULT: Production-ready fraud detection model ✨
```

---

## When to Use Each Skill

### SKILL1: Initial Data Assessment

**Use when:**
- Starting a new project with raw data
- You need to understand dataset structure and quality
- You want to identify initial data issues

**Do NOT skip:**
- Establishes baseline understanding
- Identifies critical issues early

**Time: 10-15 minutes**

---

### SKILL2: Duplicate Assessment & Cleaning

**Use when:**
- SKILL1 revealed duplicate records
- You need to assess impact on modeling
- You want to remove duplicates safely

**Common findings:**
- Exact duplicates (data entry errors)
- Duplicate transactions (legitimate repeat behavior)

**Decision point:** Keep or remove duplicates based on impact analysis

**Time: 15-20 minutes**

---

### SKILL3: Missing Values Assessment

**Use when:**
- SKILL1 revealed missing data
- You need to determine imputation strategy
- You want to evaluate treatment options

**Outcomes:**
- No missing data → proceed to SKILL4
- Few missing values → apply simple imputation
- Many missing values → remove features or advanced imputation

**Time: 15-20 minutes**

---

### SKILL4: Feature Engineering & Scaling ⭐ NEW

**Use when:**
- Data is clean (after SKILL1-3)
- You need to prepare features for modeling
- You must create proper train/val/test splits

**Critical operations:**
- Scale features with RobustScaler
- Create stratified splits (preserve class distribution)
- Fit scaler ONLY on training data (prevents data leakage)

**Outputs needed for SKILL6:**
- X_train_scaled, X_val_scaled, X_test_scaled
- y_train, y_val, y_test
- Scaler object

**Time: 20-30 minutes**

---

### SKILL5: Visualization & EDA (Optional)

**Use when:**
- You want to explore patterns visually
- You need to understand feature relationships
- You want to identify outliers or anomalies

**Is this optional?**
- **For Kaggle/Learning:** Recommended (builds intuition)
- **For Production:** Can skip (data is already assessed)

**Best time to run:** After SKILL4, before SKILL6

**Time: 15-25 minutes**

---

### SKILL6: ML Baseline Modeling

**Use when:**
- Features are scaled and splits are created (SKILL4 complete)
- You need initial model performance
- You want to compare imbalance-handling strategies

**What happens here:**
- Train logistic regression and decision tree
- Test class weights, SMOTE, undersampling
- Establish baseline for comparison
- Identify best approach

**Key decision:** Which imbalance strategy works best?

**Time: 20-30 minutes**

---

### SKILL7: Threshold Optimization

**Use when:**
- Baseline models are trained (SKILL6 complete)
- Default 0.5 threshold produces poor precision/recall trade-off
- You need to find business-optimal threshold

**Business questions answered:**
- How many false alarms can we accept?
- How much fraud do we need to catch?
- What's the cost of missing fraud vs. false alarms?

**Outputs:**
- Recommended decision threshold (0.01 - 0.99)
- Precision/recall at each threshold
- Business trade-off analysis

**Time: 15-20 minutes**

---

## Workflow Decision Points

### After SKILL1: Data Assessment
```
Is the dataset suitable for modeling?
├─ YES → Continue to SKILL2
└─ NO  → Address issues (missing documentation, data quality, etc.)
```

### After SKILL2: Duplicates
```
Should we remove duplicates?
├─ YES (impacting model) → Remove, proceed to SKILL3
└─ NO  (legitimate data)  → Keep, proceed to SKILL3
```

### After SKILL3: Missing Values
```
How to handle missing values?
├─ None found        → Skip imputation, proceed to SKILL4
├─ Few (<5%)         → Simple imputation (mean/median)
├─ Some (5-20%)      → KNN imputation or feature removal
└─ Many (>20%)       → Remove feature or advanced strategy
```

### After SKILL4: Feature Engineering
```
Ready for baseline modeling?
├─ YES → Proceed to SKILL5 or SKILL6
└─ NO  → Review feature scaling and splits
```

### After SKILL5: EDA (Optional)
```
Any new insights about features?
├─ YES → Adjust feature engineering, re-run SKILL4
└─ NO  → Proceed to SKILL6
```

### After SKILL6: Baseline Modeling
```
Which approach performed best?
├─ Class weights         → Use for SKILL7
├─ SMOTE               → Use for SKILL7
├─ Undersampling       → Use for SKILL7
└─ None of the above   → Investigate further
```

### After SKILL7: Threshold Optimization
```
Is the model production-ready?
├─ YES → Deploy with recommended threshold
└─ NO  → Try advanced models (XGBoost, Random Forest)
```

---

## Quick Reference: Skill Dependencies

```
SKILL1 (Initial Assessment)
    ↓
    └─→ SKILL2 (Duplicate Cleaning) 
        ↓
        └─→ SKILL3 (Missing Values)
            ↓
            └─→ SKILL4 (Feature Engineering & Scaling)
                ↓
                ├─→ SKILL5 (EDA) ← Optional
                │   ↓
                └─→ SKILL6 (Baseline Modeling)
                    ↓
                    └─→ SKILL7 (Threshold Optimization)
```

---

## Common Workflows

### Quick Path (Data is Already Clean)
```
✓ SKILL1 (5 min - verify)
✓ SKILL2 (skip - no duplicates)
✓ SKILL3 (skip - no missing values)
✓ SKILL4 (20 min - feature engineering)
→ SKILL6 (25 min - baseline modeling)
→ SKILL7 (15 min - threshold tuning)
Total: ~65 minutes
```

### Exploratory Path (Learning, Understanding Data)
```
✓ SKILL1 (15 min - initial assessment)
✓ SKILL2 (15 min - duplicate assessment)
✓ SKILL3 (15 min - missing values)
✓ SKILL4 (25 min - feature engineering)
✓ SKILL5 (20 min - visualizations & EDA) ← Exploratory
✓ SKILL6 (25 min - baseline modeling)
✓ SKILL7 (15 min - threshold optimization)
Total: ~130 minutes
```

### Production Path (Automated Pipeline)
```
✓ SKILL1 (5 min - verify)
✓ SKILL2 (10 min - assess only)
✓ SKILL3 (5 min - verify)
✓ SKILL4 (20 min - feature engineering)
→ SKILL6 (25 min - baseline modeling)
→ SKILL7 (15 min - threshold optimization)
Total: ~80 minutes
```

---

## Best Practices Across All Skills

### Data Integrity
- ✓ Always verify no data leakage between train/val/test
- ✓ Fit scalers ONLY on training data
- ✓ Use stratified splits for classification
- ✓ Never modify original data unexpectedly

### Metrics & Evaluation
- ✓ For fraud detection: Use AUC-PR, not accuracy
- ✓ Use Precision and Recall for imbalanced data
- ✓ Compare multiple imbalance-handling strategies
- ✓ Document metric interpretation

### Safety & Reproducibility
- ✓ Set random_state=42 for reproducibility
- ✓ Document all transformations applied
- ✓ Save scaler object for future predictions
- ✓ Preserve class distribution in splits

### Decision Making
- ✓ Recommendations are data-driven, not arbitrary
- ✓ Trade-offs (e.g., precision vs recall) are explicit
- ✓ Business context guides threshold selection
- ✓ Results are validated before proceeding

---

## Troubleshooting Guide

### Problem: Class distribution not preserved in splits
**Solution:** Ensure you're using `stratify=y` in train_test_split

### Problem: Model performance suddenly drops on test set
**Possible causes:**
- Data leakage (scaler fit on entire dataset)
- Non-stratified split (different class distribution)
- Feature scaling mismatch

**Solution:** Verify data leakage checks in SKILL4

### Problem: SKILL7 shows poor precision/recall trade-off
**Possible causes:**
- Imbalance handling strategy not working
- Features not informative for fraud detection
- Baseline model not appropriate

**Solution:** Return to SKILL6 and try different strategies

### Problem: Duplicates are significant but hard to remove
**Solution:** Check SKILL2 analysis - some duplicates may be legitimate

---

## Next Steps After SKILL7

Once you've optimized the threshold with SKILL7, you have options:

### Option 1: Advanced Models
```
If baseline model (Logistic Regression) isn't good enough:
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
→ Track threshold performance over time
```

### Option 3: Explainability
```
For business adoption:
→ Use SHAP for feature importance
→ Explain why model flags specific transactions
→ Build trust with stakeholders
```

---

## Estimated Timeline

| Phase | Time | Steps |
|-------|------|-------|
| **Data Assessment** | 30-40 min | SKILL1-3 |
| **Feature Prep** | 20-30 min | SKILL4 |
| **Exploration** | 15-25 min | SKILL5 (optional) |
| **Baseline Modeling** | 20-30 min | SKILL6 |
| **Optimization** | 15-20 min | SKILL7 |
| **TOTAL** | 100-145 min | All skills |

---

## Success Criteria

You've successfully completed the workflow when:

✓ Data is clean and ready for modeling  
✓ Features are properly scaled and splits are stratified  
✓ Baseline model performance is documented  
✓ Imbalance handling strategy is chosen  
✓ Optimal decision threshold is identified  
✓ Business trade-offs (precision vs recall) are clear  
✓ Model is production-ready with documented threshold  

---

## Support & Next Questions

**Need help?**
- Review the specific SKILL file for detailed guidance
- Check the "Code Example" section in each SKILL
- Verify class distribution is preserved
- Confirm no data leakage in your splits

**Ready for production?**
- Document your chosen threshold
- Save the scaler object for future predictions
- Set up monitoring for threshold performance
- Plan for retraining when drift is detected

---

**Happy modeling! 🚀**
