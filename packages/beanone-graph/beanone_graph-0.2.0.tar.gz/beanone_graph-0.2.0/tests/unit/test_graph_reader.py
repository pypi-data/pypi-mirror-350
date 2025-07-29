import json
import os

import pytest
from fixture_generator import create_test_graph_fixture

from graph_reader.config import GraphReaderConfig
from graph_reader.reader import GraphReader


@pytest.fixture(scope="session")
def setup_graph_fixture(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test_graph")
    create_test_graph_fixture(base_dir=temp_dir)
    return str(temp_dir)


@pytest.fixture(scope="module")
def reader(setup_graph_fixture):
    config = GraphReaderConfig(base_dir=setup_graph_fixture)
    return GraphReader(config)


def test_get_entity(reader):
    entity = reader.get_entity(1)
    assert entity is not None
    assert entity["entity_id"] == 1
    assert entity["properties"]["name"] == "John Doe"


def test_entity_cache_hit(setup_graph_fixture):
    """Test that subsequent calls to get_entity use cached values."""
    reader = GraphReader(GraphReaderConfig(base_dir=setup_graph_fixture))

    # First call should read from file
    entity1 = reader.get_entity(1)
    assert entity1 is not None
    assert entity1["properties"]["name"] == "John Doe"

    # Modify the entity file to change the name
    entity_file = os.path.join(setup_graph_fixture, "entities", "shard_0.jsonl")
    with open(entity_file, encoding="utf-8") as f:
        lines = f.readlines()

    modified_lines = []
    for line in lines:
        entity = json.loads(line)
        if entity["entity_id"] == 1:
            entity["properties"]["name"] = "Modified John"
        modified_lines.append(json.dumps(entity) + "\n")

    with open(entity_file, "w", encoding="utf-8") as f:
        f.writelines(modified_lines)

    # Second call should use cached value
    entity2 = reader.get_entity(1)
    assert entity2 is not None
    assert (
        entity2["properties"]["name"] == "John Doe"
    )  # Should be original name, not "Modified John"
    assert entity1 == entity2  # Should be exactly the same object

    # Cleanup - restore original content
    with open(entity_file, "w", encoding="utf-8") as f:
        f.writelines(lines)


def test_get_neighbors(reader):
    neighbors = reader.get_neighbors(1)
    assert isinstance(neighbors, list)
    assert len(neighbors) == 1
    assert neighbors[0]["target_id"] == 2


def test_search_by_property(reader):
    results = reader.search_by_property("name", "John Doe")
    assert isinstance(results, list)
    assert 1 in results


def test_get_entity_community(reader):
    community = reader.get_entity_community(1)
    assert community is None  # No community_id in new test data


def test_get_community_members(reader):
    members = reader.get_community_members("team_alpha")
    assert members == []  # No community_id in new test data


def test_entity_cache_eviction(setup_graph_fixture):
    """Test that entity cache evicts entries when size limit is reached."""
    config = GraphReaderConfig(base_dir=setup_graph_fixture, cache_size=1)
    reader = GraphReader(config)

    # Load first entity
    entity1 = reader.get_entity(1)
    assert entity1 is not None
    assert 1 in reader.entity_cache

    # Load second entity, should evict first
    entity2 = reader.get_entity(2)
    assert entity2 is not None
    assert 2 in reader.entity_cache
    assert 1 not in reader.entity_cache


def test_entity_not_found(setup_graph_fixture):
    """Test behavior when entity is not found."""
    reader = GraphReader(GraphReaderConfig(base_dir=setup_graph_fixture))
    entity = reader.get_entity(999)  # Non-existent entity
    assert entity is None


def test_empty_adjacency_file(setup_graph_fixture, tmp_path):
    """Test behavior with empty adjacency file."""
    # Create a reader with empty adjacency file
    empty_dir = tmp_path / "empty_graph"
    empty_dir.mkdir()
    (empty_dir / "adjacency").mkdir()
    (empty_dir / "adjacency" / "adjacency.jsonl").touch()

    config = GraphReaderConfig(base_dir=str(empty_dir))
    reader = GraphReader(config)

    # Should return empty list for any entity
    neighbors = reader.get_neighbors(1)
    assert neighbors == []


def test_empty_adjacency_map(setup_graph_fixture):
    """Test behavior with empty adjacency map."""
    reader = GraphReader(GraphReaderConfig(base_dir=setup_graph_fixture))
    # Use an entity that exists but has no relations
    neighbors = reader.get_neighbors(4)  # Alice has no relations
    assert neighbors == []


def test_get_entity_community_entity_not_found(setup_graph_fixture):
    """Test behavior when entity is not found."""
    reader = GraphReader(GraphReaderConfig(base_dir=setup_graph_fixture))
    community = reader.get_entity_community(999)
    assert community is None


def test_community_members_not_found(setup_graph_fixture):
    """Test behavior when community has no members."""
    reader = GraphReader(GraphReaderConfig(base_dir=setup_graph_fixture))
    members = reader.get_community_members("non_existent_community")
    assert members == []


def test_entity_community_not_found(setup_graph_fixture, tmp_path):
    """Test behavior when entity has no community."""
    reader = GraphReader(GraphReaderConfig(base_dir=setup_graph_fixture))
    # Create a temporary entity file with an entity that has no community
    temp_dir = tmp_path / "temp_graph"
    temp_dir.mkdir()
    (temp_dir / "entities").mkdir()
    with open(temp_dir / "entities" / "shard_0.jsonl", "w") as f:
        json.dump(
            {
                "entity_id": 999,
                "properties": {"name": "NoCommunity"},
                "update_time": "2025-04-28T12:00:00Z",
            },
            f,
        )

    config = GraphReaderConfig(base_dir=str(temp_dir))
    reader = GraphReader(config)
    community = reader.get_entity_community(999)
    assert community is None
