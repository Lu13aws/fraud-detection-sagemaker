# AWS Lambda Skill

## Purpose

This skill is responsible for generating, reviewing, and optimizing
AWS Lambda functions used in data engineering and streaming architectures.

The skill should help automate repetitive Lambda setup tasks
and generate production-oriented Lambda implementations.

---

# Responsibilities

The skill should assist with:

* Lambda function generation
* Event-driven architecture patterns
* Kinesis consumers
* SQS integrations
* Firehose integrations
* OpenSearch ingestion logic
* Environment variable configuration
* IAM permission recommendations
* Logging and monitoring setup
* Error handling
* Retry strategies
* Dead-letter queue recommendations
* Deployment preparation
* Lambda folder structure generation

---

# Preferred Outputs

Outputs should include:

* production-ready Python code
* clear function separation
* reusable helper methods
* structured logging
* environment variable support
* operational comments where useful
* lightweight and maintainable implementations

---

# Engineering Principles

The skill should:

* avoid overengineering
* prioritize operational simplicity
* minimize unnecessary dependencies
* encourage modular reusable code
* separate transformation logic from infrastructure logic
* include validation where appropriate

---

# Common Use Cases

Examples include:

* Kinesis → Lambda consumers
* SQS → Lambda processors
* Lambda → Firehose producers
* Geo-field transformations
* JSON parsing pipelines
* Event enrichment
* OpenSearch document preparation
* Streaming event normalization
