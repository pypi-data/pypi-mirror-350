import glob
import json
import os

from .indexers import get_indexer
from .indexers.search_expression import parse_search_query


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

    def _load_adjacency(self):
        adjacency = {}
        if os.path.exists(self.adjacency_file):
            with open(self.adjacency_file, encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    adjacency[record["entity_id"]] = record["relations"]
        return adjacency

    def get_entity(self, entity_id):
        if entity_id in self.entity_cache:
            return self.entity_cache[entity_id]
        for file in self.entity_files:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    if record["entity_id"] == entity_id:
                        self._cache_entity(entity_id, record)
                        return record
        return None

    def _cache_entity(self, entity_id, record):
        self.entity_cache[entity_id] = record
        if len(self.entity_cache) > self.config.cache_size:
            self.entity_cache.pop(next(iter(self.entity_cache)))

    def get_neighbors(self, entity_id):
        neighbors = []
        rel_ids = self.adjacency_map.get(entity_id, [])
        if not rel_ids:
            return neighbors
        rel_ids = set(rel_ids)
        for file in self.relation_files:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    r = json.loads(line)
                    if r["relation_id"] in rel_ids:
                        neighbors.append(r)
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

    def get_entity_community(self, entity_id):
        entity = self.get_entity(entity_id)
        if not entity:
            return None
        return entity["properties"].get("community_id")

    def get_community_members(self, community_id):
        members = []
        for file in self.entity_files:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    record = json.loads(line)
                    if record["properties"].get("community_id") == community_id:
                        members.append(record["entity_id"])
        return members
