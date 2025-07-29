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
