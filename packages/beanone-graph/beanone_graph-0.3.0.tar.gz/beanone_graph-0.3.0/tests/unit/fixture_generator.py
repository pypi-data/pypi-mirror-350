import json
from pathlib import Path


def create_test_graph_fixture(base_dir: str) -> None:
    """Create a test graph fixture with the new schema.

    Args:
        base_dir: Base directory for the test graph fixture.
    """
    base_path = Path(base_dir)
    base_path.mkdir(exist_ok=True)

    # Create directories for logs, entities, relations, and adjacency
    logs_dir = base_path / "logs"
    entities_dir = base_path / "entities"
    relations_dir = base_path / "relations"
    adjacency_dir = base_path / "adjacency"

    logs_dir.mkdir(exist_ok=True)
    entities_dir.mkdir(exist_ok=True)
    relations_dir.mkdir(exist_ok=True)
    adjacency_dir.mkdir(exist_ok=True)

    # Create entity logs
    entity_logs = [
        {
            "entity_id": 1,
            "properties": {
                "name": "John Doe",
                "type": "user",
                "email": "john@example.com",
                "age": 30,
                "tags": ["python", "developer"],
                "status": "active",
            },
            "last_update_time": "2025-05-23T06:12:50.515324+00:00Z",
        },
        {
            "entity_id": 2,
            "properties": {
                "name": "Jane Smith",
                "type": "user",
                "email": "jane@example.com",
                "age": 25,
                "tags": ["python", "designer"],
                "status": "active",
            },
            "last_update_time": "2025-05-23T06:12:50.515324+00:00Z",
        },
        {
            "entity_id": 3,
            "properties": {
                "name": "Bob Johnson",
                "type": "admin",
                "email": "bob@example.com",
                "age": 35,
                "tags": ["admin", "manager"],
                "status": "inactive",
            },
            "last_update_time": "2025-05-23T06:12:50.515324+00:00Z",
        },
        {
            "entity_id": 4,
            "properties": {
                "name": "Alice Brown",
                "type": "user",
                "email": "alice@example.com",
                "age": 28,
                "tags": ["python", "tester"],
                "status": "active",
            },
            "last_update_time": "2025-05-23T06:12:50.515324+00:00Z",
        },
    ]

    with open(logs_dir / "entity_updates.jsonl", "w", encoding="utf-8") as f:
        for log in entity_logs:
            f.write(json.dumps(log) + "\n")

    # Create relation logs
    relation_logs = [
        {
            "relation_id": 0,
            "source_id": 1,
            "target_id": 2,
            "properties": {"weight": 8, "z": 6.414269805898186},
            "update_time": "2025-05-23T06:12:51.573800+00:00Z",
        },
        {
            "relation_id": 1,
            "source_id": 2,
            "target_id": 3,
            "properties": {"weight": 6, "z": 5.123456789012345},
            "update_time": "2025-05-23T06:12:51.573800+00:00Z",
        },
    ]

    # Write relation logs
    with open(logs_dir / "relation_updates.jsonl", "w", encoding="utf-8") as f:
        for log in relation_logs:
            f.write(json.dumps(log) + "\n")

    # Create compacted entities
    compacted_entities = entity_logs

    with open(entities_dir / "shard_0.jsonl", "w", encoding="utf-8") as f:
        for entity in compacted_entities:
            f.write(json.dumps(entity) + "\n")

    # Create compacted relations
    compacted_relations = relation_logs

    with open(relations_dir / "shard_0.jsonl", "w", encoding="utf-8") as f:
        for relation in compacted_relations:
            f.write(json.dumps(relation) + "\n")

    # Create adjacency map
    adjacency_map = [
        {"entity_id": 1, "relations": [0]},
        {"entity_id": 2, "relations": [0, 1]},
        {"entity_id": 3, "relations": [1]},
        {"entity_id": 4, "relations": []},
    ]

    with open(adjacency_dir / "adjacency.jsonl", "w", encoding="utf-8") as f:
        for entry in adjacency_map:
            f.write(json.dumps(entry) + "\n")


# Run and return path
create_test_graph_fixture("test_graph_fixture")
