# Apache Flink Skill

## Purpose

This skill is responsible for generating, reviewing, and optimizing
Apache Flink SQL workflows for streaming data pipelines.

The skill should assist with real-time stream processing,
data transformation, and analytical stream operations.

---

# Responsibilities

The skill should assist with:

* Flink SQL generation
* Source table creation
* Sink table creation
* JSON stream parsing
* Stream transformations
* Window aggregations
* Watermark strategies
* Event-time processing
* Stream enrichment
* Filtering logic
* Real-time aggregation
* OpenSearch sink preparation
* Streaming analytics workflows

---

# Preferred Outputs

Outputs should include:

* readable Flink SQL
* modular stream definitions
* maintainable SQL structures
* reusable transformation patterns
* production-oriented naming conventions
* operational comments where useful

---

# Engineering Principles

The skill should:

* prefer simple streaming architectures
* minimize unnecessary complexity
* avoid deeply coupled stream logic
* encourage reusable SQL patterns
* separate raw ingestion from transformed streams
* prioritize maintainability and observability

---

# Common Use Cases

Examples include:

* Kinesis source streams
* AIS vessel stream processing
* JSON parsing
* Window-based aggregations
* Streaming KPIs
* Vessel traffic analytics
* OpenSearch sink pipelines
* Real-time event filtering
* Event enrichment workflows

---

# SQL Queries Examples

## Create Table

%flink.ssql(type=update)

CREATE TABLE ais_stream (
  raw_data STRING
)
WITH (
  'connector' = 'kinesis',
  'stream' = 'ais-stream-v1',
  'aws.region' = 'eu-central-1',
  'scan.stream.initpos' = 'LATEST',
  'format' = 'raw'
);

---

## Create a Parsed View

%flink.ssql(type=update)

CREATE VIEW ais_parsed AS
SELECT
  JSON_VALUE(raw_data, '$.MetaData.ShipName') AS ship_name,
  CAST(JSON_VALUE(raw_data, '$.Message.PositionReport.Latitude') AS DOUBLE) AS lat,
  CAST(JSON_VALUE(raw_data, '$.Message.PositionReport.Longitude') AS DOUBLE) AS lon,
  CAST(JSON_VALUE(raw_data, '$.Message.PositionReport.Sog') AS DOUBLE) AS speed_knots
FROM ais_stream;

---

## Create Table

%flink.ssql(type=update)

CREATE TABLE opensearch_sink (
  ship_name STRING,
  lat DOUBLE,
  lon DOUBLE,
  speed_knots DOUBLE
)
WITH (
  'connector' = 'elasticsearch-7',
  'hosts' = 'https://search-ais-opensearch-v1-6dto23e5kxe2dlr3nfau5bsc7i.aos.eu-central-1.on.aws:443',
  'index' = 'ais-index-vessel-data-v1',
  'username' = 'admin',
  'password' = 'DEIN_PASSWORT'
);

---

## Insert Fields into Table

%flink.ssql(type=update)

INSERT INTO opensearch_sink
SELECT
  ship_name,
  lat,
  lon,
  speed_knots
FROM ais_parsed;

---
## Drop Table

%flink.ssql(type=update)

DROP TABLE IF EXISTS opensearch_sink;

---