import glob
import json
import os
from typing import Any

from .indexers import get_indexer
from .indexers.search_expression import parse_search_query
from .schema import AdjacencyRecord, Entity, Relation


class GraphReader:
    def __init__(self, config):
        self.config = config
        self.indexer = get_indexer(config.indexer_type, config.base_dir)
        self.entity_files = sorted(
            glob.glob(os.path.join(config.base_dir, "entities", "shard_*.jsonl"))
        )
        self.relation_files = sorted(
            glob.glob(os.path.join(config.base_dir, "relations", "shard_*.jsonl"))
        )
        self.adjacency_file = os.path.join(
            config.base_dir, "adjacency", "adjacency.jsonl"
        )
        self.entity_cache = {}
        self.adjacency_map = self._load_adjacency()

    def _make_hashable(self, value: Any) -> str:
        """Convert any value to a string for consistent dictionary keys and comparisons.

        This method ensures consistent string representation for:
        - Basic types (int, str, float, bool, None)
        - UUID objects (converted to string)
        - Any other type (converted to string)
        """
        return str(value)

    def _load_adjacency(self):
        """Load adjacency records from file.

        Returns:
            dict: Dictionary mapping entity IDs to their relation IDs.
        """
        adjacency = {}
        if os.path.exists(self.adjacency_file):
            with open(self.adjacency_file, encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    # Validate adjacency record
                    adj_record = AdjacencyRecord(**record)
                    # Convert entity_id to string for dictionary key
                    key = self._make_hashable(adj_record.entity_id)
                    adjacency[key] = adj_record.relations
        return adjacency

    def get_entity(self, entity_id: Any) -> dict | None:
        """Get an entity by its ID.

        Args:
            entity_id: Unique identifier for the entity. Can be any type that uniquely identifies an entity.

        Returns:
            dict | None: Entity data if found, None otherwise.
        """
        # Convert entity_id to string for dictionary lookup
        key = self._make_hashable(entity_id)
        if key in self.entity_cache:
            return self.entity_cache[key]

        for file in self.entity_files:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    # Validate entity record
                    entity = Entity(**record)
                    if self._make_hashable(entity.entity_id) == key:
                        self._cache_entity(key, entity.model_dump())
                        return entity.model_dump()
        return None

    def _cache_entity(self, entity_id: str, record: dict) -> None:
        """Cache an entity record.

        Args:
            entity_id: String representation of the entity ID.
            record: Entity data to cache.
        """
        self.entity_cache[entity_id] = record
        if len(self.entity_cache) > self.config.cache_size:
            self.entity_cache.pop(next(iter(self.entity_cache)))

    def get_neighbors(self, entity_id: Any) -> list[dict]:
        """Get all relations where the given entity is either source or target.

        Args:
            entity_id: Unique identifier for the entity.

        Returns:
            list[dict]: List of relation records.
        """
        neighbors: list[dict] = []
        # Convert entity_id to string for dictionary lookup
        key = self._make_hashable(entity_id)
        rel_ids = self.adjacency_map.get(key, [])
        if not rel_ids:
            return neighbors

        # Convert rel_ids to set of strings for O(1) lookup
        rel_ids = {self._make_hashable(rel_id) for rel_id in rel_ids}

        for file in self.relation_files:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    # Validate relation record
                    relation = Relation(**record)
                    # Convert relation_id to string for set lookup
                    rel_key = self._make_hashable(relation.relation_id)
                    if rel_key in rel_ids:
                        neighbors.append(relation.model_dump())
        return neighbors

    def search_by_property(self, key, value):
        return self.indexer.search_by_property(key, value)

    def search_query(self, query: str):
        """Search for entities using a search query string.

        Args:
            query: A search query string in the format:
                - Simple: "name:alice"
                - Multiple conditions: "name:alice AND age:>25"
                - Complex: "(name:alice OR name:bob) AND age:>25"
                - Array search: "tags:python"
                - Text search: "description:~python"
                - Case insensitive: "name:alice/i"

        Returns:
            List of entity IDs matching the search criteria
        """
        expression = parse_search_query(query)
        return self.indexer.search(expression)

    def get_entity_community(self, entity_id: Any) -> Any | None:
        """Get the community ID for an entity.

        Args:
            entity_id: Unique identifier for the entity.

        Returns:
            Any | None: Community ID if found, None otherwise.
        """
        entity = self.get_entity(entity_id)
        if not entity:
            return None
        return entity["properties"].get("community_id")

    def get_community_members(self, community_id: Any) -> list[Any]:
        """Retrieve all entity IDs belonging to a given community.

        Args:
            community_id: Unique identifier for the community.

        Returns:
            list[Any]: List of entity IDs in the specified community.
        """
        members = []
        community_key = self._make_hashable(community_id)
        for file in self.entity_files:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    # Validate entity record
                    entity = Entity(**record)
                    if (
                        self._make_hashable(entity.properties.community_id)
                        == community_key
                    ):
                        members.append(entity.entity_id)
        return members
