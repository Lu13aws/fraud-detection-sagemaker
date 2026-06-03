# Athena SQL & Data Quality Skill

## Purpose

This skill is responsible for generating, reviewing, and optimizing
Amazon Athena SQL queries for analytics, validation,
data exploration, and data quality workflows.

The skill should assist with practical SQL operations
commonly used in data engineering projects.

---

# Responsibilities

The skill should assist with:

* Athena SQL query generation
* Data quality checks
* Null value detection
* Duplicate detection
* Row count analysis
* Schema validation
* Aggregations and summaries
* Partition-aware querying
* Exploratory data analysis
* Filtering and transformation logic
* Cost-aware Athena query patterns
* Query optimization
* Validation workflows
* Data consistency checks

---

# Common Data Quality Checks

The skill should support checks such as:

## Null Value Checks

```sql id="vjjlwm"
SELECT *
FROM table_name
WHERE column_name IS NULL;
```

---

## Duplicate Detection

```sql id="lhnwlo"
SELECT column_name, COUNT(*)
FROM table_name
GROUP BY column_name
HAVING COUNT(*) > 1;
```

---

## Row Counts

```sql id="76hfxw"
SELECT COUNT(*)
FROM table_name;
```

---

## Distinct Value Counts

```sql id="cr3n74"
SELECT COUNT(DISTINCT column_name)
FROM table_name;
```

---

## Missing Value Analysis

```sql id="4spp14"
SELECT
    COUNT(*) AS total_rows,
    COUNT(column_name) AS non_null_rows
FROM table_name;
```

---

## Basic Aggregations

```sql id="jlwm0x"
SELECT
    AVG(column_name),
    MIN(column_name),
    MAX(column_name)
FROM table_name;
```

---

# Preferred Outputs

Outputs should include:

* readable SQL
* maintainable query structures
* practical analytics workflows
* validation-oriented queries
* production-friendly formatting
* operational explanations where useful

---

# Engineering Principles

The skill should:

* prioritize practical SQL workflows
* encourage efficient Athena usage
* minimize unnecessary data scans
* support partition-aware querying
* encourage reusable query patterns
* focus on data quality and observability
* support scalable analytics workflows

---

# Common Use Cases

Examples include:

* S3 data lake analytics
* AIS historical analysis
* Data quality validation
* Duplicate detection
* Partition analysis
* KPI generation
* Trend analysis
* Operational reporting
* Streaming archive analysis
* QuickSight preparation
* Historical traffic analytics
