"""
AWS and S3 Configuration
Centralized configuration for AWS credentials, S3 bucket paths, and boto3 client.
"""

import os
import boto3
import pandas as pd

# AWS Configuration - Read from environment or use defaults
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
S3_BUCKET = os.getenv("S3_BUCKET", "raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an")

# S3 Path Prefixes
S3_DATA_PREFIX = "data/raw"
S3_MODELS_PREFIX = "models"
S3_TRAINING_PREFIX = "training"

# Full S3 URIs
RAW_DATA_URI = f"s3://{S3_BUCKET}/{S3_DATA_PREFIX}"
MODELS_URI = f"s3://{S3_BUCKET}/{S3_MODELS_PREFIX}"
TRAINING_URI = f"s3://{S3_BUCKET}/{S3_TRAINING_PREFIX}"

# Initialize boto3 S3 client
try:
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    # Test credentials
    s3_client.head_bucket(Bucket=S3_BUCKET)
    print(f"✓ AWS S3 configured: {AWS_REGION} / {S3_BUCKET}")
except Exception as e:
    print(f"✗ AWS S3 configuration error: {e}")
    print("  Run: aws configure")
    raise


def read_csv_from_s3(s3_key):
    """
    Read CSV file from S3 bucket using boto3.

    Args:
        s3_key (str): S3 object key (path within bucket), e.g., "data/raw/creditcard.csv"

    Returns:
        pd.DataFrame: Loaded CSV data

    Raises:
        FileNotFoundError: If file not found in S3
        Exception: If S3 access fails
    """
    try:
        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        return pd.read_csv(obj["Body"])
    except s3_client.exceptions.NoSuchKey:
        raise FileNotFoundError(
            f"File not found in S3: s3://{S3_BUCKET}/{s3_key}"
        )
    except Exception as e:
        raise RuntimeError(
            f"AWS S3 error reading {s3_key}: {e}\n"
            f"Check credentials with: aws sts get-caller-identity"
        )


def upload_file_to_s3(file_path, s3_key):
    """
    Upload file to S3 bucket.

    Args:
        file_path (str): Local file path
        s3_key (str): S3 destination key
    """
    try:
        s3_client.upload_file(file_path, S3_BUCKET, s3_key)
        print(f"✓ Uploaded: s3://{S3_BUCKET}/{s3_key}")
    except Exception as e:
        raise RuntimeError(f"AWS S3 error uploading {file_path}: {e}")


def list_s3_objects(prefix):
    """
    List objects in S3 bucket with given prefix.

    Args:
        prefix (str): S3 prefix/folder

    Returns:
        list: List of object keys
    """
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]
    except Exception as e:
        raise RuntimeError(f"AWS S3 error listing {prefix}: {e}")


# Convenience functions for common paths
def get_raw_data_path(filename="creditcard.csv"):
    """Get S3 path for raw data file."""
    return f"{S3_DATA_PREFIX}/{filename}"


def get_training_path(dataset_type, filename):
    """Get S3 path for training data (train/val/test)."""
    return f"{S3_TRAINING_PREFIX}/{dataset_type}/{filename}"


# SageMaker-specific configuration
SAGEMAKER_ROLE_ARN = os.getenv("SAGEMAKER_ROLE_ARN", None)  # Should be set by user
SAGEMAKER_EXECUTION_ROLE = os.getenv("SAGEMAKER_EXECUTION_ROLE", None)
