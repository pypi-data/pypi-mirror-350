"""Tests for schema validation."""
from datetime import datetime
from uuid import UUID, uuid4

import pytest

from graph_reader.schema import AdjacencyRecord, Entity, EntityProperties, Relation


def test_entity_properties_validation():
    """Test validation of entity properties."""
    # Valid properties
    props = EntityProperties(
        name="John Doe",
        type="user",
        email="john@example.com",
        age=30,
        tags=["python", "developer"],
        status="active",
        community_id=1,
    )
    assert props.name == "John Doe"
    assert props.age == 30

    # Invalid age
    with pytest.raises(ValueError, match="Age must be between 0 and 150"):
        EntityProperties(age=-1)

    # Invalid email
    with pytest.raises(ValueError, match="Invalid email format"):
        EntityProperties(email="invalid-email")

    # Valid nullable fields
    props = EntityProperties()
    assert props.name is None
    assert props.email is None
    assert props.age is None
    assert props.tags is None
    assert props.status is None
    assert props.community_id is None
    assert props.description is None


def test_entity_validation():
    """Test validation of entity records."""
    # Valid entity with different ID types
    entity = Entity(
        entity_id=1,
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == 1

    # Valid entity with string ID
    entity = Entity(
        entity_id="user_123",
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == "user_123"

    # Valid entity with zero ID
    entity = Entity(
        entity_id=0,
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == 0

    # Missing required fields
    with pytest.raises(ValueError):
        Entity(entity_id=1)  # Missing properties

    # Test datetime parsing
    # ISO format without Z
    entity = Entity(
        entity_id=1,
        properties=EntityProperties(name="John Doe"),
        last_update_time="2024-03-20T10:30:00",
    )
    assert isinstance(entity.last_update_time, datetime)
    assert entity.last_update_time.year == 2024
    assert entity.last_update_time.month == 3
    assert entity.last_update_time.day == 20

    # ISO format with Z
    entity = Entity(
        entity_id=1,
        properties=EntityProperties(name="John Doe"),
        last_update_time="2024-03-20T10:30:00Z",
    )
    assert isinstance(entity.last_update_time, datetime)
    assert entity.last_update_time.year == 2024
    assert entity.last_update_time.month == 3
    assert entity.last_update_time.day == 20

    # None datetime
    entity = Entity(
        entity_id=1, properties=EntityProperties(name="John Doe"), last_update_time=None
    )
    assert entity.last_update_time is None

    # Already datetime object
    now = datetime.now()
    entity = Entity(
        entity_id=1, properties=EntityProperties(name="John Doe"), last_update_time=now
    )
    assert entity.last_update_time == now


def test_relation_validation():
    """Test validation of relation records."""
    # Valid relation with different ID types
    relation = Relation(
        relation_id=1,
        source_id=1,
        target_id=2,
        type="follows",
        last_update_time=datetime.now(),
    )
    assert relation.relation_id == 1
    assert relation.type == "follows"

    # Valid relation with string IDs
    relation = Relation(
        relation_id="rel_123",
        source_id="user_1",
        target_id="user_2",
        type="follows",
        last_update_time=datetime.now(),
    )
    assert relation.relation_id == "rel_123"
    assert relation.source_id == "user_1"
    assert relation.target_id == "user_2"

    # Valid relation with zero IDs
    relation = Relation(
        relation_id=0,
        source_id=0,
        target_id=0,
        type="follows",
        last_update_time=datetime.now(),
    )
    assert relation.relation_id == 0
    assert relation.source_id == 0
    assert relation.target_id == 0

    # Default type when not provided
    relation = Relation(
        relation_id=1, source_id=1, target_id=2, last_update_time=datetime.now()
    )
    assert relation.type == "default"

    # Test datetime parsing
    # ISO format without Z
    relation = Relation(
        relation_id=1, source_id=1, target_id=2, last_update_time="2024-03-20T10:30:00"
    )
    assert isinstance(relation.last_update_time, datetime)
    assert relation.last_update_time.year == 2024
    assert relation.last_update_time.month == 3
    assert relation.last_update_time.day == 20

    # ISO format with Z
    relation = Relation(
        relation_id=1, source_id=1, target_id=2, last_update_time="2024-03-20T10:30:00Z"
    )
    assert isinstance(relation.last_update_time, datetime)
    assert relation.last_update_time.year == 2024
    assert relation.last_update_time.month == 3
    assert relation.last_update_time.day == 20

    # None datetime
    relation = Relation(relation_id=1, source_id=1, target_id=2, last_update_time=None)
    assert relation.last_update_time is None

    # Already datetime object
    now = datetime.now()
    relation = Relation(relation_id=1, source_id=1, target_id=2, last_update_time=now)
    assert relation.last_update_time == now


def test_adjacency_record_validation():
    """Test validation of adjacency records."""
    # Valid adjacency record with different ID types
    adj = AdjacencyRecord(entity_id=1, relations=[1, 2, 3])
    assert adj.entity_id == 1
    assert adj.relations == [1, 2, 3]

    # Valid adjacency record with string IDs
    adj = AdjacencyRecord(entity_id="user_123", relations=["rel_1", "rel_2", "rel_3"])
    assert adj.entity_id == "user_123"
    assert adj.relations == ["rel_1", "rel_2", "rel_3"]

    # Valid adjacency record with zero IDs
    adj = AdjacencyRecord(entity_id=0, relations=[0, 1, 2])
    assert adj.entity_id == 0
    assert adj.relations == [0, 1, 2]


def test_id_types_entity():
    """Test various ID types for Entity class."""
    # Integer IDs
    entity = Entity(
        entity_id=1,
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == 1

    entity = Entity(
        entity_id=0,
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == 0

    entity = Entity(
        entity_id=-1,
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == -1

    # String IDs
    entity = Entity(
        entity_id="user_123",
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == "user_123"

    entity = Entity(
        entity_id="user:123:active",
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == "user:123:active"

    entity = Entity(
        entity_id="http://dbpedia.org/resource/Paris",
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == "http://dbpedia.org/resource/Paris"

    # UUID
    uuid = uuid4()
    entity = Entity(
        entity_id=uuid,
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == uuid

    # Composite keys
    entity = Entity(
        entity_id=("user", 123, "active"),
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == ("user", 123, "active")

    # Dictionary/object IDs
    entity = Entity(
        entity_id={"system": "salesforce", "id": "001xx000003DIloAAG"},
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == {"system": "salesforce", "id": "001xx000003DIloAAG"}

    # Special cases
    entity = Entity(
        entity_id="",  # Empty string
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == ""

    entity = Entity(
        entity_id="   ",  # Whitespace-only
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == "   "

    entity = Entity(
        entity_id="a" * 1000,  # Very long string
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == "a" * 1000

    entity = Entity(
        entity_id="user_123_测试",  # Unicode
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == "user_123_测试"

    entity = Entity(
        entity_id="user@123#test",  # Special chars
        properties=EntityProperties(name="John Doe"),
        last_update_time=datetime.now(),
    )
    assert entity.entity_id == "user@123#test"


def test_id_types_relation():
    """Test various ID types for Relation class."""
    # Integer IDs
    relation = Relation(
        relation_id=1,
        source_id=1,
        target_id=2,
        type="follows",
        last_update_time=datetime.now(),
    )
    assert relation.relation_id == 1
    assert relation.source_id == 1
    assert relation.target_id == 2

    # String IDs
    relation = Relation(
        relation_id="rel_123",
        source_id="user_1",
        target_id="user_2",
        type="follows",
        last_update_time=datetime.now(),
    )
    assert relation.relation_id == "rel_123"
    assert relation.source_id == "user_1"
    assert relation.target_id == "user_2"

    # Mixed ID types
    relation = Relation(
        relation_id="rel_123",
        source_id=1,
        target_id="user_2",
        type="follows",
        last_update_time=datetime.now(),
    )
    assert relation.relation_id == "rel_123"
    assert relation.source_id == 1
    assert relation.target_id == "user_2"

    # UUID
    uuid1, uuid2, uuid3 = uuid4(), uuid4(), uuid4()
    relation = Relation(
        relation_id=uuid1,
        source_id=uuid2,
        target_id=uuid3,
        type="follows",
        last_update_time=datetime.now(),
    )
    assert relation.relation_id == uuid1
    assert relation.source_id == uuid2
    assert relation.target_id == uuid3

    # Composite keys
    relation = Relation(
        relation_id=("rel", 123),
        source_id=("user", 1),
        target_id=("user", 2),
        type="follows",
        last_update_time=datetime.now(),
    )
    assert relation.relation_id == ("rel", 123)
    assert relation.source_id == ("user", 1)
    assert relation.target_id == ("user", 2)


def test_id_types_adjacency():
    """Test various ID types for AdjacencyRecord class."""
    # Integer IDs
    adj = AdjacencyRecord(entity_id=1, relations=[1, 2, 3])
    assert adj.entity_id == 1
    assert adj.relations == [1, 2, 3]

    # String IDs
    adj = AdjacencyRecord(entity_id="user_123", relations=["rel_1", "rel_2", "rel_3"])
    assert adj.entity_id == "user_123"
    assert adj.relations == ["rel_1", "rel_2", "rel_3"]

    # Mixed ID types in relations list
    adj = AdjacencyRecord(entity_id="user_123", relations=[1, "rel_2", 3])
    assert adj.entity_id == "user_123"
    assert adj.relations == [1, "rel_2", 3]

    # UUID
    uuid = uuid4()
    adj = AdjacencyRecord(entity_id=uuid, relations=[uuid4(), uuid4()])
    assert adj.entity_id == uuid
    assert len(adj.relations) == 2
    assert all(isinstance(r, UUID) for r in adj.relations)

    # Composite keys
    adj = AdjacencyRecord(entity_id=("user", 123), relations=[("rel", 1), ("rel", 2)])
    assert adj.entity_id == ("user", 123)
    assert adj.relations == [("rel", 1), ("rel", 2)]

    # Empty relations list
    adj = AdjacencyRecord(entity_id=1, relations=[])
    assert adj.entity_id == 1
    assert adj.relations == []

    # Special cases in relations list
    adj = AdjacencyRecord(
        entity_id=1, relations=["", "   ", "a" * 1000, "user_123_测试", "user@123#test"]
    )
    assert adj.entity_id == 1
    assert adj.relations == ["", "   ", "a" * 1000, "user_123_测试", "user@123#test"]
