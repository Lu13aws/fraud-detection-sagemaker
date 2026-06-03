"""
SageMaker training script for Random Forest fraud detection.

Expects the same CSV convention as train_xgboost.py:
  - label in column 0, no header
  - /opt/ml/input/data/train/ and /opt/ml/input/data/validation/
  - model saved to /opt/ml/model/
"""
import argparse
import json
import os
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-estimators", type=int, default=200)
    parser.add_argument("--max-depth", type=int, default=None)
    parser.add_argument("--min-samples-leaf", type=int, default=1)
    parser.add_argument("--class-weight", type=str, default="balanced",
                        help="'balanced', 'balanced_subsample', or 'none'")
    parser.add_argument("--n-jobs", type=int, default=-1)
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train"))
    parser.add_argument("--validation", type=str, default=os.environ.get("SM_CHANNEL_VALIDATION", "/opt/ml/input/data/validation"))
    return parser.parse_args()


def load_csv(channel_dir: str) -> tuple:
    files = [f for f in os.listdir(channel_dir) if f.endswith(".csv")]
    df = pd.concat([pd.read_csv(os.path.join(channel_dir, f), header=None) for f in files])
    y = df.iloc[:, 0].values
    X = df.iloc[:, 1:].values
    return X, y


def main():
    args = parse_args()

    X_train, y_train = load_csv(args.train)
    X_val, y_val = load_csv(args.validation)

    class_weight = None if args.class_weight == "none" else args.class_weight

    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        min_samples_leaf=args.min_samples_leaf,
        class_weight=class_weight,
        n_jobs=args.n_jobs,
        random_state=42,
    )

    print(f"Training Random Forest: n_estimators={args.n_estimators}, "
          f"max_depth={args.max_depth}, class_weight={class_weight}")
    model.fit(X_train, y_train)

    y_prob_val = model.predict_proba(X_val)[:, 1]
    auc_roc = roc_auc_score(y_val, y_prob_val)
    auc_pr = average_precision_score(y_val, y_prob_val)

    print(f"[validation] auc_roc={auc_roc:.4f}")
    print(f"[validation] auc_pr={auc_pr:.4f}")

    metrics = {"auc_roc": auc_roc, "auc_pr": auc_pr}
    with open(os.path.join(args.model_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f)

    with open(os.path.join(args.model_dir, "rf_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    print("Model saved.")


if __name__ == "__main__":
    main()
