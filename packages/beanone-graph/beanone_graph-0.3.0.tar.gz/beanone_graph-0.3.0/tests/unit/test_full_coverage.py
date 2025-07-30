import pytest

from graph_reader.config import GraphReaderConfig
from graph_reader.indexers.base_indexer import BaseIndexer
from graph_reader.indexers.search_expression import (
    SearchCondition,
    SearchExpression,
    SearchExpressionEvaluator,
    SearchOperator,
    SearchQueryParser,
)
from graph_reader.reader import GraphReader


class DummyIndexer(BaseIndexer):
    def search(self, expression):
        # Just return a dummy list to cover the return in search_query
        return [42]

    def search_by_property(self, key, value, operation="equals", case_sensitive=True):
        return [1]


def test_base_indexer_search_query():
    indexer = DummyIndexer()
    # This will cover the return in search_query
    result = indexer.search_query("name:test")
    assert result == [42]


def test_search_expression_not_operator():
    evaluator = SearchExpressionEvaluator()
    # Cover the NOT operator branch in evaluate_condition
    cond = SearchCondition("name", SearchOperator.EQUALS, "foo")
    not_cond = SearchCondition("name", SearchOperator.NOT, cond)
    assert evaluator.evaluate_condition(not_cond, {"name": "bar"}) is True
    assert evaluator.evaluate_condition(not_cond, {"name": "foo"}) is False


def test_search_expression_unsupported_operator():
    evaluator = SearchExpressionEvaluator()
    # Cover the unsupported operator branch in evaluate_expression
    # Create a SearchExpression with MATCHES operator and a non-empty conditions list
    cond = SearchCondition("name", SearchOperator.EQUALS, "foo")
    expr = SearchExpression(SearchOperator.MATCHES, [cond])
    with pytest.raises(ValueError, match="Unsupported expression operator"):
        evaluator.evaluate_expression(expr, {"name": "foo"})


def test_search_query_parser_invalid_condition():
    parser = SearchQueryParser()
    # Cover the ValueError for invalid condition format (len < 4)
    with pytest.raises(ValueError):
        parser._parse_condition([["a", ":"]])


def test_search_query_parser_parse_results():
    parser = SearchQueryParser()
    # Cover the ParseResults handling in _parse_not, _parse_and, _parse_or
    # _parse_not
    from pyparsing import ParseResults

    cond = SearchCondition("name", SearchOperator.EQUALS, "foo")
    not_expr = parser._parse_not(ParseResults(["NOT", ParseResults([cond])]))
    assert isinstance(not_expr, SearchExpression)
    # _parse_and
    and_expr = parser._parse_and(ParseResults([[cond, "AND", cond]]))
    assert isinstance(and_expr, SearchExpression)
    # _parse_or
    or_expr = parser._parse_or(ParseResults([[cond, "OR", cond]]))
    assert isinstance(or_expr, SearchExpression)


def test_reader_get_community_members(tmp_path):
    # Create a minimal graph structure
    base_dir = tmp_path / "graph"
    entities_dir = base_dir / "entities"
    entities_dir.mkdir(parents=True)
    # Write a single entity with community_id 1
    with open(entities_dir / "shard_0.jsonl", "w", encoding="utf-8") as f:
        f.write('{"entity_id": 1, "properties": {"community_id": 1}}\n')
    config = GraphReaderConfig(base_dir=str(base_dir))
    reader = GraphReader(config)
    # Should return [1] for community_id 1
    assert reader.get_community_members(1) == [1]
    # Should return [] for a community with no members (covers the return statement)
    assert reader.get_community_members(999) == []


def test_parse_not_grouped_condition():
    from graph_reader.indexers.search_expression import SearchQueryParser

    parser = SearchQueryParser()
    expr = parser.parse("NOT (name:foo)")
    # Assert the structure is as expected
    assert expr.operator.value == "not"
    assert expr.conditions[0].key == "name"
    assert expr.conditions[0].value == "foo"


def test_parse_or_with_grouped_condition():
    from graph_reader.indexers.search_expression import SearchQueryParser

    parser = SearchQueryParser()
    expr = parser.parse("name:foo OR (name:bar)")
    # The first condition is a SearchCondition
    assert expr.operator.value == "or"
    assert expr.conditions[0].key == "name"
    assert expr.conditions[0].value == "foo"
    # The second condition is also a SearchCondition (from the group)
    assert expr.conditions[1].key == "name"
    assert expr.conditions[1].value == "bar"
