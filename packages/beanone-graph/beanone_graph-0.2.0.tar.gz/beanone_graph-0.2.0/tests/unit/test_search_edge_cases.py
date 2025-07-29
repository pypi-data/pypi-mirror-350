import re

import pytest

from graph_reader.indexers.search_expression import (
    SearchCondition,
    SearchExpression,
    SearchExpressionEvaluator,
    SearchOperator,
    parse_search_query,
)


def test_base_indexer_error_handling():
    """Test error handling in base indexer."""
    from graph_reader.indexers.base_indexer import BaseIndexer

    class TestIndexer(BaseIndexer):
        pass

    indexer = TestIndexer()

    # Test NotImplementedError for search_by_property
    with pytest.raises(NotImplementedError):
        indexer.search_by_property("name", "test")

    # Test NotImplementedError for search
    with pytest.raises(NotImplementedError):
        indexer.search(SearchCondition("name", SearchOperator.EQUALS, "test"))

    # Test search_query with invalid query
    with pytest.raises(ValueError):
        indexer.search_query("invalid:query:format")


def test_search_expression_edge_cases():
    """Test edge cases in search expression evaluation."""
    evaluator = SearchExpressionEvaluator()

    # Test empty array handling
    assert not evaluator.evaluate_condition(
        SearchCondition("tags", SearchOperator.EQUALS, "python"), {"tags": []}
    )

    # Test None value handling
    assert not evaluator.evaluate_condition(
        SearchCondition("name", SearchOperator.EQUALS, "test"), {"name": None}
    )

    # Test invalid operator
    with pytest.raises(ValueError):
        evaluator.evaluate_expression(
            SearchExpression(SearchOperator.NOT, []), {"name": "test"}
        )

    # Test empty expression conditions (AND returns True for all([]))
    assert evaluator.evaluate_expression(
        SearchExpression(SearchOperator.AND, []), {"name": "test"}
    )


def test_search_parser_edge_cases():
    """Test edge cases in search query parsing."""
    # Test array value with one empty string
    expr = parse_search_query('tags:@[""]')
    assert isinstance(expr, SearchCondition)
    assert expr.operator == SearchOperator.IN
    assert expr.value == [""]

    # Test invalid condition format
    with pytest.raises(ValueError):
        parse_search_query("invalid")

    # Test empty query
    with pytest.raises(ValueError):
        parse_search_query("")

    # Test unbalanced parentheses
    with pytest.raises(ValueError):
        parse_search_query("(name:test")

    # Test array value with special characters
    expr = parse_search_query('tags:@["test@domain.com", "file/path"]')
    assert isinstance(expr, SearchCondition)
    assert expr.operator == SearchOperator.IN
    assert expr.value == ["test@domain.com", "file/path"]


def test_search_expression_operators():
    """Test all search operators with edge cases."""
    evaluator = SearchExpressionEvaluator()

    # Test MATCHES operator with invalid regex
    with pytest.raises(re.error):
        evaluator.evaluate_condition(
            SearchCondition("name", SearchOperator.MATCHES, "[invalid"),
            {"name": "test"},
        )

    # Test GREATER_THAN with non-numeric values
    assert not evaluator.evaluate_condition(
        SearchCondition("name", SearchOperator.GREATER_THAN, "test"), {"name": "test"}
    )

    # Test LESS_THAN with non-numeric values
    assert not evaluator.evaluate_condition(
        SearchCondition("name", SearchOperator.LESS_THAN, "test"), {"name": "test"}
    )

    # Test CONTAINS_TEXT with non-string values
    assert not evaluator.evaluate_condition(
        SearchCondition("count", SearchOperator.CONTAINS_TEXT, "test"), {"count": 123}
    )

    # Test STARTS_WITH with non-string values
    assert not evaluator.evaluate_condition(
        SearchCondition("count", SearchOperator.STARTS_WITH, "test"), {"count": 123}
    )

    # Test ENDS_WITH with non-string values
    assert not evaluator.evaluate_condition(
        SearchCondition("count", SearchOperator.ENDS_WITH, "test"), {"count": 123}
    )
