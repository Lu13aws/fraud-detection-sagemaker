# Prompt 1

Act as a Senior Data Analyst or Data Scientist.

Create visualizations to understand the dataset.

FILE_NAME: creditcard.csv
SOURCE_NAME: s3://raw-creditcard-fraud-data-v1-759302162548-eu-central-1-an/data/raw/creditcard.csv

Include:

* Target variable distribution
* Class imbalance visualization
* Numerical feature distributions
* Amount and Time distributions (if available)
* Correlation analysis
* Outlier visualizations
* Most discriminative feature visualizations

Explain key findings from each visualization.

Highlight:

* Patterns
* Anomalies
* Potential predictive features
* Risks for machine learning

Do not train any models.

Finish with recommendations for feature engineering and modeling preparation.


# Prompt 2

Alternativ Prompt because the Prompt above didn't work in SageMaker. Got an error message. This one worked and I got results.

Act as a Senior Data Analyst or Data Scientist.

Create 5 visualizations to understand the dataset that you have just cleaned.

Explain key findings from each visualization.

Highlight:

* Patterns
* Anomalies
* Potential predictive features
* Risks for machine learning

Do not train any models.

Finish with recommendations for feature engineering and modeling preparation.