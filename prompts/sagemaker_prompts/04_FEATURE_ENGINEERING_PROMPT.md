Act as a Senior Machine Learning Engineer specializing in data preparation.

Using the cleaned dataset (duplicates removed, missing values handled), 
prepare features and data for machine learning modeling.

## Primary Tasks

1. **Feature Selection & Transformation**
   - Select relevant features for modeling
   - Identify and apply feature transformations:
     - Log transformation for right-skewed numerical features (e.g., monetary values, transaction amounts)
     - Square root transformation for moderate skewness
     - Power transformations for non-normal distributions
   - Document all transformations applied

2. **Feature Scaling**
   - Choose appropriate scaler:
     - **RobustScaler** (RECOMMENDED): Robust to outliers, ideal for imbalanced classification
     - StandardScaler: For normally distributed features
     - MinMaxScaler: When bounded ranges are important
   - Justify your scaler choice based on feature distributions
   - **CRITICAL:** Fit scaler ONLY on training data to prevent data leakage

3. **Data Splitting**
   - Create stratified train/validation/test splits:
     - 70% Training (model fitting)
     - 15% Validation (hyperparameter tuning, early stopping)
     - 15% Testing (final evaluation, unseen data)
   - **CRITICAL:** Use stratified splitting to preserve class distribution
   - For imbalanced classification:
     - Ensure each split maintains the original minority class percentage
     - Example: If your dataset has 1% minority class, maintain ~1% in each split
   - Document split sizes and class percentages

4. **Data Leakage Prevention**
   - Verify scaler is fit ONLY on training data
   - Confirm no row overlap between train/validation/test sets
   - Check that validation and test sets are truly unseen
   - Provide explicit verification results

5. **Class Imbalance Preparation**
   - Analyze target variable distribution across splits
   - Document imbalance ratio (majority:minority class)
   - Prepare context for baseline modeling (which handles imbalance via strategies)
   - No imbalance handling here—just document and prepare context

## Required Outputs

**Data Matrices:**
- X_train_scaled, X_val_scaled, X_test_scaled (scaled feature matrices)
- y_train, y_val, y_test (target variables)
- Fitted scaler object (for applying to future predictions)

**Documentation:**
- Feature transformations applied (which columns, which transformations, why)
- Scaler selection and justification
- Dataset split summary:
  - Number of rows in each set
  - Minority class count and percentage per set
  - Proof that class distribution is preserved
- Data leakage verification:
  - No row overlap between sets
  - Scaler fit verification
  - Index overlap check results

**Statistics:**
- Feature summary statistics BEFORE scaling:
  - Min, max, mean, std for each numerical feature
- Feature summary statistics AFTER scaling:
  - Confirm appropriate ranges
  - Verify centering/normalization

**Validation Checklist:**
- ✓ Stratified splits created (class distribution preserved)
- ✓ No data leakage detected
- ✓ Scaler fit on training data only
- ✓ All sets properly transformed
- ✓ Ready for baseline modeling

## Best Practices to Follow

**Data Integrity:**
- Always fit scaler ONLY on training data (prevents future data from influencing the scaler)
- Use stratified splits for classification (preserves class distribution)
- Never modify original data unexpectedly
- Verify no row overlap between sets

**Reproducibility:**
- Set random_state=42 for train_test_split
- Document all transformations applied
- Save the fitted scaler object (needed for production predictions)
- Log class distribution percentages

**Safety Checks:**
- Confirm stratified split by checking minority class % in each set
- Verify scaler statistics make sense (centered at 0, standard scaled)
- Check for NaN values after scaling
- Validate that all data points were processed

## Important Notes for Imbalanced Classification

- **Class Imbalance Expected:** Rare classes may represent 1% or less of your data
- **Stratification is Critical:** Without stratified splits, you risk train/val/test having different class percentages
- **Outliers are Important:** Minority class samples often have unusual feature values—RobustScaler preserves these signals
- **No Imbalance Handling Here:** This step prepares data. Imbalance handling (SMOTE, class weights, undersampling) happens in baseline modeling

## Proceed to Next Step

Once data is prepared and verified:
→ Move to **SKILL5/Visualization** for exploratory analysis (optional but recommended)
→ Move to **SKILL6/Baseline Modeling** for training and comparing models with different imbalance strategies
