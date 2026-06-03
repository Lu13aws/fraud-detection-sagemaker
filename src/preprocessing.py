"""
Shared preprocessing utilities for the fraud detection project.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def scale_features(df: pd.DataFrame) -> pd.DataFrame:
    """Scale Amount and Time; V1-V28 are already PCA-normalized."""
    df = df.copy()
    scaler = StandardScaler()
    df[["Amount_scaled", "Time_scaled"]] = scaler.fit_transform(df[["Amount", "Time"]])
    df = df.drop(columns=["Amount", "Time"])
    return df


def split_data(
    df: pd.DataFrame,
    target_col: str = "Class",
    train_size: float = 0.70,
    val_size: float = 0.15,
    random_state: int = 42,
):
    """Stratified split into train / validation / test."""
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, train_size=train_size, stratify=y, random_state=random_state
    )
    # val_size and test_size are equal halves of the remaining data
    val_ratio = val_size / (1.0 - train_size)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, train_size=val_ratio, stratify=y_temp, random_state=random_state
    )
    return X_train, X_val, X_test, y_train, y_val, y_test


def apply_smote(X_train, y_train, random_state: int = 42):
    """Oversample minority class with SMOTE."""
    from imblearn.over_sampling import SMOTE

    sm = SMOTE(random_state=random_state)
    X_res, y_res = sm.fit_resample(X_train, y_train)
    return X_res, y_res


def undersample_majority(X_train, y_train, ratio: float = 0.1, random_state: int = 42):
    """Random undersample majority class to achieve fraud_count / total = ratio."""
    from imblearn.under_sampling import RandomUnderSampler

    rus = RandomUnderSampler(sampling_strategy=ratio, random_state=random_state)
    X_res, y_res = rus.fit_resample(X_train, y_train)
    return X_res, y_res


def compute_class_weight(y_train) -> dict:
    """Return {0: w0, 1: w1} with weights inversely proportional to class frequency."""
    from sklearn.utils.class_weight import compute_class_weight

    classes = np.unique(y_train)
    weights = compute_class_weight("balanced", classes=classes, y=y_train)
    return dict(zip(classes, weights))


def save_splits_csv(X_train, y_train, X_val, y_val, X_test, y_test, output_dir: str):
    """Write train/val/test CSVs (label first column — SageMaker XGBoost convention)."""
    import os

    os.makedirs(output_dir, exist_ok=True)
    for split, X, y in [("train", X_train, y_train), ("val", X_val, y_val), ("test", X_test, y_test)]:
        df_out = pd.concat([y.reset_index(drop=True), X.reset_index(drop=True)], axis=1)
        df_out.to_csv(f"{output_dir}/{split}.csv", index=False, header=False)
