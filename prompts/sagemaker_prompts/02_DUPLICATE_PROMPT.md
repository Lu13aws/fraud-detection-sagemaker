Act as a Senior Data Scientist.

Analyze duplicate records in the dataset.

FILE_NAME: creditcard.csv
SOURCE_NAME: s3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv

Tasks:

* Count duplicate rows
* Calculate duplicate percentage
* Compare duplicate and non-duplicate records
* Assess potential impact on modeling
* Recommend whether duplicates should be removed

Only remove duplicates if they are exact duplicates and likely to bias analysis or model training.

If duplicates are removed:

* Report number removed
* Show dataset shape before and after cleaning
* Explain the impact

Do not perform any other data cleaning or modeling.
