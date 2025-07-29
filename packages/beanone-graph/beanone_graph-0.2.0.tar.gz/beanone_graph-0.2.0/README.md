<p align="center">
  <img src="https://raw.githubusercontent.com/beanone/graph_reader/refs/heads/main/docs/assets/logos/banner.svg" alt="Graph Context Banner" width="100%">
</p>

This library enables fast graph traversal and lookup from file-based storage with sharded and indexed structure.
Now includes community exploration.

[![Python Versions](https://img.shields.io/pypi/pyversions/beanone_graph)](https://pypi.org/project/beanone_graph)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/beanone/graph_reader/blob/main/LICENSE)
[![Tests](https://github.com/beanone/graph_reader/actions/workflows/tests.yml/badge.svg)](https://github.com/beanone/graph_reader/actions?query=workflow%3Atests)
[![Coverage](https://codecov.io/gh/beanone/graph_reader/branch/main/graph/badge.svg)](https://codecov.io/gh/beanone/graph_reader)
[![Code Quality](https://img.shields.io/badge/code%20style-ruff-000000)](https://github.com/astral-sh/ruff)
[![PyPI version](https://img.shields.io/pypi/v/beanone_graph)](https://pypi.org/project/beanone_graph)


## Features

- Efficient reading of graph data from JSONL files
- Support for multiple indexing strategies (SQLite and Memory)
- Entity caching for improved performance
- Adjacency list-based neighbor lookup
- Property-based entity search
- Community lookup
- Configurable cache size

## Architecture

The library is organized into the following components:

### Core Components

- `GraphReader`: Main class for reading and querying graph data
- `GraphReaderConfig`: Configuration class for customizing reader behavior

### Indexers

The library supports multiple indexing strategies through a plugin architecture:

- `BaseIndexer`: Abstract base class for indexers
- `SQLiteIndexer`: SQLite-based indexing for persistent storage
- `MemoryIndexer`: In-memory indexing for faster access

### Data Structure

The library expects data to be organized in the following directory structure:

```
base_dir/
├── entities/
│   └── shard_*.jsonl
├── relations/
│   └── shard_*.jsonl
└── adjacency/
    └── adjacency.jsonl
```

### Architecture Diagram

```mermaid
graph TD
    GR[GraphReader]
    GC[GraphReaderConfig]
    BI[BaseIndexer]
    SI[SQLiteIndexer]
    MI[MemoryIndexer]
    EF[Entity Files]
    RF[Relation Files]
    AF[Adjacency File]
    DB[(SQLite DB)]

    GR --> GC
    GR --> BI
    SI --> BI
    MI --> BI
    GR --> EF
    GR --> RF
    GR --> AF
    SI --> DB

    style GR fill:#e6f3ff,stroke:#000000,stroke-width:2px,color:#000000
    style GC fill:#e6f3ff,stroke:#000000,stroke-width:2px,color:#000000
    style BI fill:#fff2e6,stroke:#000000,stroke-width:2px,color:#000000
    style SI fill:#fff2e6,stroke:#000000,stroke-width:2px,color:#000000
    style MI fill:#fff2e6,stroke:#000000,stroke-width:2px,color:#000000
    style EF fill:#f0fff0,stroke:#000000,stroke-width:2px,color:#000000
    style RF fill:#f0fff0,stroke:#000000,stroke-width:2px,color:#000000
    style AF fill:#f0fff0,stroke:#000000,stroke-width:2px,color:#000000
    style DB fill:#f0fff0,stroke:#000000,stroke-width:2px,color:#000000
```

## Installation

```bash
pip install beanone-graph
```

## Usage

```python
from graph_reader import GraphReader, GraphReaderConfig

config = GraphReaderConfig(base_dir="graph_output")
reader = GraphReader(config)

# Get an entity
entity = reader.get_entity(1)
print("Entity:", entity)

# Get neighbors
neighbors = reader.get_neighbors(1)
print("Neighbors:", neighbors)

# Search
matches = reader.search_by_property("name", "Alice")
print("Matches:", matches)

# Get entity's community
community = reader.get_entity_community(1)
print("Community:", community)

# Get members of a community
members = reader.get_community_members("team_alpha")
print("Members:", members)
```

## Search Queries

The library supports powerful search queries with various operators and conditions. Here are comprehensive examples based on a real graph structure:

### Basic Property Search

```python
# Simple equality
results = reader.search_by_property("name", "effect")

# Case-insensitive search
results = reader.search_by_property("name", "nuclear", case_sensitive=False)

# Numeric comparison
results = reader.search_by_property("community", 155, operator="==")
```

### Complex Queries

```python
# Multiple conditions with AND
query = "name:effect AND community:155"
results = reader.search(query)

# Multiple conditions with OR
query = "name:effect OR name:nuclear"
results = reader.search(query)

# Combining AND and OR
query = "community:155 AND (levels.0:>=3 OR levels.1:>=17)"
results = reader.search(query)

# Array value search
query = "keywords:protein OR keywords:formula"
results = reader.search(query)

# Multiple properties
query = "community:155 AND keywords:protein AND levels.0:>=3"
results = reader.search(query)
```

### Search Operators

The following operators are supported:

- `:` - Equals (default)
  - For arrays: checks if the value is in the array
  - Example: `keywords:protein` matches if "protein" is in the keywords array
- `:@` - Array membership
  - Checks if the property value is in the specified array
  - Example: `type:@['user', 'admin']` matches if type is either 'user' or 'admin'
- `==` - Equals (explicit)
- `!=` - Not equals
- `>` - Greater than
- `>=` - Greater than or equal
- `<` - Less than
- `<=` - Less than or equal
- `AND` - Logical AND
- `OR` - Logical OR
- `(` and `)` - Grouping

### Search Examples by Use Case

#### Entity Search
```python
# Find entities by community and level
query = "community:155 AND levels.0:>=3"

# Find entities by keywords (array contains)
query = "keywords:protein AND keywords:formula"

# Find entities by name pattern
query = "name:*nuclear*"

# Find entities with multiple keywords
query = "keywords:protein AND keywords:home AND keywords:formula"

# Find entities by type (array membership)
query = "type:@['user', 'admin']"
```

#### Level-based Search
```python
# Find entities with high level 0 values
query = "levels.0:>=50"

# Find entities with specific level combinations
query = "levels.0:>=3 AND levels.1:>=17"

# Find entities with no higher level connections
query = "levels.3:0 AND levels.4:0"
```

#### Community Search
```python
# Find entities in specific communities
query = "community:155 OR community:245"

# Find entities by community and keywords
query = "community:155 AND keywords:protein"

# Find entities by community and level distribution
query = "community:155 AND levels.0:>=3 AND levels.1:>=17"

# Find entities with specific keyword combinations
query = "keywords:protein AND keywords:home AND keywords:formula"
```

### Best Practices

1. Use parentheses to group complex conditions
2. Combine related conditions with AND
3. Use OR for alternative values
4. Use numeric operators for ranges
5. Consider case sensitivity for text searches
6. For array properties:
   - Use `:` to check if a value exists in an array
   - Use `:@` to check if a property value is in a specified array
   - Combine multiple array conditions with AND to find entities with all specified values
7. Use wildcards (*) for pattern matching in text fields
8. Use dot notation for nested properties (e.g., levels.0)
9. Combine community and level information for precise filtering
10. Use keyword arrays for semantic search

## Configuration

The `GraphReaderConfig` class supports the following parameters:

- `base_dir`: Base directory containing the graph data
- `indexer_type`: Type of indexer to use ("sqlite" or "memory")
- `cache_size`: Maximum number of entities to cache in memory

## License

This project is licensed under the MIT License - see the LICENSE file for details.
