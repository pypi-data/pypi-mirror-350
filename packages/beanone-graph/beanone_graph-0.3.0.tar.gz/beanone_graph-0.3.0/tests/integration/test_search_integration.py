import json

import pytest

from graph_reader import GraphReader, GraphReaderConfig


@pytest.fixture
def search_test_data(tmp_path):
    """Create test data for search integration tests."""
    # Create test entities
    entities = [
        {
            "entity_id": 1,
            "properties": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "age": 30,
                "type": "user",
                "tags": ["python", "developer"],
                "status": "active",
            },
        },
        {
            "entity_id": 2,
            "properties": {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "age": 25,
                "type": "user",
                "tags": ["python", "designer"],
                "status": "active",
            },
        },
        {
            "entity_id": 3,
            "properties": {
                "name": "Bob Wilson",
                "email": "bob.j@example.com",
                "age": 35,
                "type": "admin",
                "tags": ["admin", "manager"],
                "status": "inactive",
            },
        },
        {
            "entity_id": 4,
            "properties": {
                "name": "Alice Blue",
                "email": "alice.b@example.com",
                "age": 28,
                "type": "user",
                "tags": ["python", "developer"],
                "status": "active",
            },
        },
    ]

    # Create test directory structure
    base_dir = tmp_path / "test_search"
    base_dir.mkdir()
    entities_dir = base_dir / "entities"
    entities_dir.mkdir()

    # Write test data
    with open(entities_dir / "shard_0.jsonl", "w") as f:
        for entity in entities:
            f.write(f"{json.dumps(entity)}\n")

    return str(base_dir)


def test_simple_search(search_test_data):
    """Test simple search queries."""
    reader = GraphReader(GraphReaderConfig(base_dir=search_test_data))

    # Test exact match
    results = reader.search_query('name:"John Doe"')
    assert len(results) == 1
    assert results[0] == 1

    # Test case insensitive
    results = reader.search_query("name:~john/i")
    assert len(results) == 1
    assert results[0] == 1

    # Test numeric comparison
    results = reader.search_query("age:>30")
    assert len(results) == 1
    assert results[0] == 3


def test_complex_search(search_test_data):
    """Test complex search queries."""
    reader = GraphReader(GraphReaderConfig(base_dir=search_test_data))

    # Test AND condition
    results = reader.search_query("type:user AND age:>25")
    assert len(results) == 2
    assert set(results) == {1, 4}

    # Test OR condition
    results = reader.search_query("name:~john/i OR name:~jane/i")
    assert len(results) == 2
    assert set(results) == {1, 2}

    # Test nested conditions
    results = reader.search_query("(type:user OR type:admin) AND status:active")
    assert len(results) == 3
    assert set(results) == {1, 2, 4}


def test_array_search(search_test_data):
    """Test array-related search operations."""
    reader = GraphReader(GraphReaderConfig(base_dir=search_test_data))

    # Test array contains
    results = reader.search_query("tags:python")
    assert len(results) == 3
    assert set(results) == {1, 2, 4}

    # Test array membership
    results = reader.search_query('type:@["user", "admin"]')
    assert len(results) == 4


def test_text_search(search_test_data):
    """Test text search operations."""
    reader = GraphReader(GraphReaderConfig(base_dir=search_test_data))

    # Test contains text
    results = reader.search_query("email:~example.com")
    assert len(results) == 4

    # Test starts with
    results = reader.search_query("name:^J")
    assert len(results) == 2
    assert set(results) == {1, 2}

    # Test ends with
    results = reader.search_query("name:$n/i")
    print("--------------------------------")
    print(results)
    print("--------------------------------")
    assert len(results) == 1
    assert results[0] == 3


def test_web_search_scenarios(search_test_data):
    """Test real-world web search scenarios."""
    reader = GraphReader(GraphReaderConfig(base_dir=search_test_data))

    # User search with multiple criteria
    results = reader.search_query(
        "type:user AND (name:~john OR email:~john) AND age:>25"
    )
    assert len(results) == 1
    assert results[0] == 1

    # Content search with tags
    results = reader.search_query("type:user AND tags:python AND status:active")
    assert len(results) == 3
    assert set(results) == {1, 2, 4}

    # Complex user search
    results = reader.search_query(
        "(type:user OR type:admin) AND status:active AND (tags:python OR tags:admin)"
    )
    assert len(results) == 3
    assert set(results) == {1, 2, 4}


def test_search_with_both_indexers(search_test_data):
    """Test search functionality with both memory and SQLite indexers."""
    # Test with memory indexer
    memory_reader = GraphReader(
        GraphReaderConfig(base_dir=search_test_data, indexer_type="memory")
    )
    memory_results = memory_reader.search_query("type:user AND tags:python")

    # Test with SQLite indexer
    sqlite_reader = GraphReader(
        GraphReaderConfig(base_dir=search_test_data, indexer_type="sqlite")
    )
    sqlite_results = sqlite_reader.search_query("type:user AND tags:python")

    # Results should be the same regardless of indexer
    assert set(memory_results) == set(sqlite_results)
    assert len(memory_results) == 3
    assert set(memory_results) == {1, 2, 4}
