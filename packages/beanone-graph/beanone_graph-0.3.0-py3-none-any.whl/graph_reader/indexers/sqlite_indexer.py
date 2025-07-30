import glob
import json
import os
import sqlite3
from typing import Any

from .base_indexer import BaseIndexer
from .search_expression import (
    SearchCondition,
    SearchExpression,
    SearchExpressionEvaluator,
    SearchOperator,
)


class SQLiteIndexer(BaseIndexer):
    def __init__(self, base_dir):
        self.db_path = os.path.join(base_dir, "index.db")
        self.conn = sqlite3.connect(self.db_path)
        self.evaluator = SearchExpressionEvaluator()
        self._create_table()
        self._build_index_from_entities(base_dir)

    def _create_table(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS entity_index (
                    entity_id INTEGER PRIMARY KEY,
                    properties TEXT NOT NULL
                )
            """
            )

    def _build_index_from_entities(self, base_dir):
        entity_dir = os.path.join(base_dir, "entities")
        for file in glob.glob(os.path.join(entity_dir, "shard_*.jsonl")):
            with open(file, encoding="utf-8") as f:
                for line in f:
                    entity = json.loads(line)
                    eid = entity["entity_id"]
                    props = entity["properties"]
                    self._insert(eid, props)

    def _insert(self, entity_id, props):
        with self.conn:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO entity_index
                (entity_id, properties)
                VALUES (?, ?)
                """,
                (entity_id, json.dumps(props)),
            )

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
        """Search for entities using a search expression."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT entity_id, properties FROM entity_index")
        results = []
        for entity_id, props_json in cursor.fetchall():
            props = json.loads(props_json)
            if self.evaluator.evaluate_expression(expression, props):
                results.append(entity_id)
        return results

    def __del__(self):
        if hasattr(self, "conn"):
            self.conn.close()
