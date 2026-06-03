# OpenSearch Index Mapping Skill

## Purpose

This skill is responsible for generating, reviewing, and validating
OpenSearch index mappings used in analytics and streaming architectures.

The skill should help create efficient, searchable,
and visualization-friendly index structures.

---

# Responsibilities

The skill should assist with:

* index mapping generation
* field type selection
* geo_point configuration
* timestamp handling
* keyword vs text decisions
* nested object handling
* numeric field optimization
* index naming conventions
* mapping validation
* OpenSearch compatibility checks
* visualization-oriented field preparation

---

# Preferred Outputs

Outputs should include:

* valid JSON mappings
* maintainable field structures
* analytics-friendly schemas
* visualization-ready geo fields
* optimized searchable structures
* operational explanations where useful

---

# Engineering Principles

The skill should:

* prioritize search efficiency
* support real-time analytics
* minimize mapping conflicts
* avoid unnecessary field duplication
* ensure compatibility with dashboards and visualizations
* encourage scalable index design

---

# Common Use Cases

Examples include:

* vessel tracking indexes
* geo_point field mappings
* AIS event indexing
* real-time analytics indexes
* OpenSearch dashboard integrations
* Firehose indexing targets
* timestamp normalization
* streaming document indexing

---

# Index Mapping JSON Code Example
```text
{
  "properties": {
    "ingest_timestamp": {
      "type": "date"
    },
    "ship_name": {
      "type": "keyword"
    },
    "mmsi": {
      "type": "keyword"
    },
    "lat": {
      "type": "float"
    },
    "lon": {
      "type": "float"
    },
    "speed_knots": {
      "type": "float"
    },
    "location": {
      "type": "geo_point"
    }
  }
}
```