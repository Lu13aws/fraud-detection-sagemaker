"""
SageMaker training script for XGBoost fraud detection.

SageMaker passes hyperparameters as CLI args and expects:
  - training data at /opt/ml/input/data/train/train.csv  (label in col 0, no header)
  - validation data at /opt/ml/input/data/validation/val.csv
  - model saved to /opt/ml/model/
"""
import argparse
import json
import os

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import average_precision_score, roc_auc_score


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-estimators", type=int, default=200)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--learning-rate", type=float, default=0.1)
    parser.add_argument("--scale-pos-weight", type=float, default=None,
                        help="Weight of positive class. If None, computed from data.")
    parser.add_argument("--subsample", type=float, default=0.8)
    parser.add_argument("--colsample-bytree", type=float, default=0.8)
    # SageMaker injects these automatically
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

    scale_pos_weight = args.scale_pos_weight
    if scale_pos_weight is None:
        neg = (y_train == 0).sum()
        pos = (y_train == 1).sum()
        scale_pos_weight = neg / pos
        print(f"Computed scale_pos_weight={scale_pos_weight:.2f} (neg={neg}, pos={pos})")

    model = xgb.XGBClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
        scale_pos_weight=scale_pos_weight,
        subsample=args.subsample,
        colsample_bytree=args.colsample_bytree,
        use_label_encoder=False,
        eval_metric="aucpr",
        random_state=42,
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=50,
    )

    y_prob_val = model.predict_proba(X_val)[:, 1]
    auc_roc = roc_auc_score(y_val, y_prob_val)
    auc_pr = average_precision_score(y_val, y_prob_val)

    # SageMaker Experiments picks up metrics from stdout with this format
    print(f"[validation] auc_roc={auc_roc:.4f}")
    print(f"[validation] auc_pr={auc_pr:.4f}")

    metrics = {"auc_roc": auc_roc, "auc_pr": auc_pr}
    with open(os.path.join(args.model_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f)

    model.save_model(os.path.join(args.model_dir, "xgboost_model.json"))
    print("Model saved.")


if __name__ == "__main__":
    main()
