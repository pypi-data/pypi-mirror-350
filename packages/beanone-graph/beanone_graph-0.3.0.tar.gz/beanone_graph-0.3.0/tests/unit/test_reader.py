"""Tests for GraphReader ID type handling."""
import json
import os
import tempfile
from datetime import datetime
from uuid import UUID, uuid4

import pytest

from graph_reader.config import GraphReaderConfig as Config
from graph_reader.reader import GraphReader
from graph_reader.schema import AdjacencyRecord, Entity, EntityProperties, Relation


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


@pytest.fixture
def temp_dir():
    """Create a temporary directory with test data."""
    with tempfile.TemporaryDirectory() as temp_dir_path:
        # Create directory structure
        os.makedirs(os.path.join(temp_dir_path, "entities"))
        os.makedirs(os.path.join(temp_dir_path, "relations"))
        os.makedirs(os.path.join(temp_dir_path, "adjacency"))

        # Create test data
        entity_file = os.path.join(temp_dir_path, "entities", "shard_0.jsonl")
        relation_file = os.path.join(temp_dir_path, "relations", "shard_0.jsonl")
        adjacency_file = os.path.join(temp_dir_path, "adjacency", "adjacency.jsonl")

        # Generate fixed UUIDs to be used by tests
        entity_uuid = uuid4()
        relation_uuid = uuid4()  # Assuming relation can also have UUID as ID

        # Write test entities
        with open(entity_file, "w", encoding="utf-8") as f:
            # Integer ID
            entity1 = Entity(
                entity_id=1,
                properties=EntityProperties(name="Alice", community_id=1),
                last_update_time=datetime.now(),
            )
            f.write(json.dumps(entity1.model_dump(), cls=DateTimeEncoder) + "\n")

            # String ID
            entity2 = Entity(
                entity_id="user_123",
                properties=EntityProperties(name="Bob", community_id="group_a"),
                last_update_time=datetime.now(),
            )
            f.write(json.dumps(entity2.model_dump(), cls=DateTimeEncoder) + "\n")

            # UUID
            entity3 = Entity(
                entity_id=entity_uuid,  # Use pre-generated UUID
                properties=EntityProperties(name="Charlie", community_id=entity_uuid),
                last_update_time=datetime.now(),
            )
            f.write(json.dumps(entity3.model_dump(), cls=DateTimeEncoder) + "\n")

            # Composite ID (as string)
            entity4 = Entity(
                entity_id="user:123:active",
                properties=EntityProperties(name="Dave", community_id="group:b"),
                last_update_time=datetime.now(),
            )
            f.write(json.dumps(entity4.model_dump(), cls=DateTimeEncoder) + "\n")

            # External system ID (as string)
            entity5 = Entity(
                entity_id="salesforce:001xx000003DIloAAG",
                properties=EntityProperties(name="Eve", community_id="acme:sales"),
                last_update_time=datetime.now(),
            )
            f.write(json.dumps(entity5.model_dump(), cls=DateTimeEncoder) + "\n")

        # Write test relations
        with open(relation_file, "w", encoding="utf-8") as f:
            # Integer IDs
            relation1 = Relation(
                relation_id=1,  # Assuming relation_id can be int
                source_id=1,
                target_id="user_123",  # Changed from 2 for consistency with adj data
                type="follows",
                last_update_time=datetime.now(),
            )
            f.write(json.dumps(relation1.model_dump(), cls=DateTimeEncoder) + "\n")

            # Mixed ID types
            relation2 = Relation(
                relation_id="rel_123",
                source_id="user_123",
                target_id=1,
                type="follows",
                last_update_time=datetime.now(),
            )
            f.write(json.dumps(relation2.model_dump(), cls=DateTimeEncoder) + "\n")

            # UUID IDs
            relation3 = Relation(
                relation_id=relation_uuid,  # Use pre-generated UUID for relation
                source_id=entity_uuid,
                target_id="user_123",
                type="knows",  # Changed type for variety
                last_update_time=datetime.now(),
            )
            f.write(json.dumps(relation3.model_dump(), cls=DateTimeEncoder) + "\n")

        # Write test adjacency records
        with open(adjacency_file, "w", encoding="utf-8") as f:
            # Integer IDs for entity 1
            adj1 = AdjacencyRecord(
                entity_id=1,
                relations=[
                    1,
                    "rel_123",
                ],  # Entity 1 is source for rel 1 and target for rel_123
            )
            f.write(json.dumps(adj1.model_dump(), cls=DateTimeEncoder) + "\n")

            # String IDs for entity "user_123"
            adj2 = AdjacencyRecord(
                entity_id="user_123",
                relations=[
                    1,
                    "rel_123",
                    relation_uuid,
                ],  # user_123 is target for rel 1, source for rel_123, target for relation_uuid
            )
            f.write(json.dumps(adj2.model_dump(), cls=DateTimeEncoder) + "\n")

            # UUID IDs for entity_uuid
            adj3 = AdjacencyRecord(
                entity_id=entity_uuid,
                relations=[relation_uuid],  # entity_uuid is source for relation_uuid
            )
            f.write(json.dumps(adj3.model_dump(), cls=DateTimeEncoder) + "\n")

        yield (
            temp_dir_path,
            entity_uuid,
            relation_uuid,
        )  # Return path and generated UUIDs


@pytest.fixture
def reader(temp_dir):
    """Create a GraphReader instance with test data."""
    (
        temp_dir_path,
        entity_uuid,
        relation_uuid,
    ) = temp_dir  # Unpack, we only need the path here
    config = Config(base_dir=temp_dir_path, indexer_type="memory", cache_size=100)
    return GraphReader(config)


def test_get_entity_with_different_id_types(reader, temp_dir):
    """Test getting entities with different ID types."""
    _, entity_uuid, _ = temp_dir  # Get the fixed entity_uuid

    # Integer ID
    entity = reader.get_entity(1)
    assert entity is not None
    assert entity["properties"]["name"] == "Alice"

    # String ID
    entity = reader.get_entity("user_123")
    assert entity is not None
    assert entity["properties"]["name"] == "Bob"

    # UUID
    entity = reader.get_entity(entity_uuid)  # Use the fixed UUID
    assert entity is not None
    assert entity["properties"]["name"] == "Charlie"

    # Composite ID
    entity = reader.get_entity("user:123:active")
    assert entity is not None
    assert entity["properties"]["name"] == "Dave"

    # External system ID
    entity = reader.get_entity("salesforce:001xx000003DIloAAG")
    assert entity is not None
    assert entity["properties"]["name"] == "Eve"


def test_get_neighbors_with_different_id_types(reader, temp_dir):
    """Test getting neighbors with different ID types."""
    _, entity_uuid, relation_uuid = temp_dir  # Get fixed UUIDs

    # Integer ID (Entity 1)
    # Expected relations: 1 (source_id=1), "rel_123" (target_id=1)
    neighbors = reader.get_neighbors(1)
    assert len(neighbors) == 2
    neighbor_ids = {r["relation_id"] for r in neighbors}
    assert 1 in neighbor_ids
    assert "rel_123" in neighbor_ids

    # String ID (Entity "user_123")
    # Expected relations: 1 (target_id="user_123"), "rel_123" (source_id="user_123"), relation_uuid (target_id="user_123")
    neighbors = reader.get_neighbors("user_123")
    assert len(neighbors) == 3
    neighbor_ids = {r["relation_id"] for r in neighbors}
    assert 1 in neighbor_ids
    assert "rel_123" in neighbor_ids
    assert str(relation_uuid) in neighbor_ids

    # UUID (Entity entity_uuid)
    # Expected relations: relation_uuid (source_id=entity_uuid)
    neighbors = reader.get_neighbors(entity_uuid)  # Use fixed UUID
    assert len(neighbors) == 1
    assert neighbors[0]["relation_id"] == str(relation_uuid)


def test_get_community_members_with_different_id_types(reader, temp_dir):
    """Test getting community members with different ID types."""
    _, entity_uuid, _ = temp_dir  # Get fixed entity_uuid

    # Integer community ID
    members = reader.get_community_members(1)
    assert len(members) == 1
    assert members[0] == 1

    # String community ID
    members = reader.get_community_members("group_a")
    assert len(members) == 1
    assert members[0] == "user_123"

    # UUID community ID
    members = reader.get_community_members(entity_uuid)  # Use fixed UUID
    assert len(members) == 1
    assert members[0] == str(entity_uuid)

    # Composite community ID
    members = reader.get_community_members("group:b")
    assert len(members) == 1
    assert members[0] == "user:123:active"

    # External system community ID
    members = reader.get_community_members("acme:sales")
    assert len(members) == 1
    assert members[0] == "salesforce:001xx000003DIloAAG"


def test_get_entity_community_with_different_id_types(reader, temp_dir):
    """Test getting entity community with different ID types."""
    _, entity_uuid, _ = temp_dir  # Get fixed entity_uuid

    # Integer ID
    community = reader.get_entity_community(1)
    assert community == 1

    # String ID
    community = reader.get_entity_community("user_123")
    assert community == "group_a"

    # UUID
    community = reader.get_entity_community(entity_uuid)  # Use fixed UUID
    assert community == str(entity_uuid)

    # Composite ID
    community = reader.get_entity_community("user:123:active")
    assert community == "group:b"

    # External system ID
    community = reader.get_entity_community("salesforce:001xx000003DIloAAG")
    assert community == "acme:sales"


def test_special_string_ids(reader):
    """Test handling of special string IDs."""
    # Empty string
    entity = Entity(
        entity_id="",
        properties=EntityProperties(name="Empty"),
        last_update_time=datetime.now(),
    )
    with open(
        os.path.join(reader.config.base_dir, "entities", "shard_0.jsonl"), "a"
    ) as f:
        f.write(json.dumps(entity.model_dump(), cls=DateTimeEncoder) + "\n")

    result = reader.get_entity("")
    assert result is not None
    assert result["properties"]["name"] == "Empty"

    # Whitespace-only string
    entity = Entity(
        entity_id="   ",
        properties=EntityProperties(name="Whitespace"),
        last_update_time=datetime.now(),
    )
    with open(
        os.path.join(reader.config.base_dir, "entities", "shard_0.jsonl"), "a"
    ) as f:
        f.write(json.dumps(entity.model_dump(), cls=DateTimeEncoder) + "\n")

    result = reader.get_entity("   ")
    assert result is not None
    assert result["properties"]["name"] == "Whitespace"

    # Unicode string
    entity = Entity(
        entity_id="user_123_测试",
        properties=EntityProperties(name="Unicode"),
        last_update_time=datetime.now(),
    )
    with open(
        os.path.join(reader.config.base_dir, "entities", "shard_0.jsonl"), "a"
    ) as f:
        f.write(json.dumps(entity.model_dump(), cls=DateTimeEncoder) + "\n")

    result = reader.get_entity("user_123_测试")
    assert result is not None
    assert result["properties"]["name"] == "Unicode"

    # Special characters
    entity = Entity(
        entity_id="user@123#test",
        properties=EntityProperties(name="Special"),
        last_update_time=datetime.now(),
    )
    with open(
        os.path.join(reader.config.base_dir, "entities", "shard_0.jsonl"), "a"
    ) as f:
        f.write(json.dumps(entity.model_dump(), cls=DateTimeEncoder) + "\n")

    result = reader.get_entity("user@123#test")
    assert result is not None
    assert result["properties"]["name"] == "Special"
