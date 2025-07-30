import glob
import json
import os
from typing import Any

from .base_indexer import BaseIndexer
from .search_expression import (
    SearchCondition,
    SearchExpression,
    SearchExpressionEvaluator,
    SearchOperator,
)


class MemoryIndexer(BaseIndexer):
    def __init__(self, base_dir):
        self.map = {}
        self.evaluator = SearchExpressionEvaluator()
        # Read all entity files and build the index
        entity_dir = os.path.join(base_dir, "entities")
        if os.path.exists(entity_dir):
            for file in glob.glob(os.path.join(entity_dir, "shard_*.jsonl")):
                with open(file, encoding="utf-8") as f:
                    for line in f:
                        entity = json.loads(line)
                        entity_id = entity["entity_id"]
                        self.map[entity_id] = entity["properties"]

    def search_by_property(
        self,
        key: str,
        value: Any,
        operation: str = "equals",
        case_sensitive: bool = True,
    ) -> list[int]:
        """Search for entities by property value with various operations."""
        operator = SearchOperator(operation)
        condition = SearchCondition(key, operator, value, case_sensitive)
        return self.search(condition)

    def search(self, expression: SearchExpression | SearchCondition) -> list[int]:
        """Search for entities using a search expression.

        Args:
            expression: A search expression or condition to evaluate

        Returns:
            List of entity IDs matching the search criteria
        """
        evaluator = SearchExpressionEvaluator()
        return [
            entity_id
            for entity_id, props in self.map.items()
            if evaluator.evaluate_expression(expression, props)
        ]
