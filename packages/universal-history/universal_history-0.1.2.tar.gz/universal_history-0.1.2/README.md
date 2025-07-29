# Universal History

A library for creating, maintaining, and utilizing Universal Histories across multiple domains.

## Overview

The Universal History library provides a standardized framework for recording, analyzing, and retrieving historical information about any subject across various domains. Whether you're tracking educational progress, medical history, employment records, or any other domain-specific information, this library offers a unified approach to managing that data.

## Key Features

- **Multi-domain support**: Track histories across education, health, work, finance, and other domains
- **Event recording**: Capture individual events with rich context and metadata
- **Trajectory synthesis**: Generate summaries and analyses from sequences of events
- **State document**: Maintain an up-to-date representation of the subject's current state
- **Domain catalogs**: Define and standardize domain-specific terminology and metrics
- **LLM integration**: Optimize historical data for use as context with language models
- **Multiple storage backends**: Store data in memory, files, or MongoDB

## Installation

```bash
pip install universal-history
```

For MongoDB support:

```bash
pip install universal-history[mongodb]
```

For LLM integration:

```bash
pip install universal-history[llm]
```

## Quick Start

```python
from universal_history import UniversalHistoryClient

# Initialize a client with file storage
client = UniversalHistoryClient(storage_dir="./data")

# Create an event
event = client.create_event(
    subject_id="student123",
    domain_type="education",
    event_type="exam",
    content="Student scored 92/100 on Algebra final exam.",
    source_type="institution",
    source_id="school001",
    source_name="Springfield High School",
    metrics={"score": 92, "max_score": 100},
    tags=["math", "algebra", "exam"]
)

# Update the state document with information from events
client.update_state_from_events(
    subject_id="student123",
    domain_type="education"
)

# Get LLM-optimized context
context = client.get_llm_context("student123")
print(context)
```

## Architecture

The Universal History system consists of several key components:

- **Event Record (RE)**: The basic unit of information, capturing specific events or observations
- **Trajectory Synthesis (ST)**: Analysis and summary of multiple events over a period of time
- **State Document (DE)**: Real-time representation of the current state of a subject
- **Domain Catalog (CDD)**: Semantic framework for interpreting information in a specific domain
- **Universal History (HU)**: Container for all components related to a specific subject

## Documentation

For detailed documentation, visit [https://universal-history.readthedocs.io/](https://universal-history.readthedocs.io/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
