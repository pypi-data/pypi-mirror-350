import pytest

from graph_reader.indexers.search_expression import (
    SearchCondition,
    SearchExpression,
    SearchOperator,
    parse_search_query,
)


def test_simple_search_queries():
    """Test simple search queries."""
    # Basic equality
    expr = parse_search_query("name:alice")
    assert isinstance(expr, SearchCondition)
    assert expr.key == "name"
    assert expr.operator == SearchOperator.EQUALS
    assert expr.value == "alice"
    assert expr.case_sensitive is True

    # Case insensitive
    expr = parse_search_query("name:alice/i")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is False

    # Numeric comparison
    expr = parse_search_query("age:>25")
    assert isinstance(expr, SearchCondition)
    assert expr.operator == SearchOperator.GREATER_THAN
    assert expr.value == 25

    # Text contains
    expr = parse_search_query("description:~python")
    assert isinstance(expr, SearchCondition)
    assert expr.operator == SearchOperator.CONTAINS_TEXT


def test_complex_search_queries():
    """Test complex search queries with multiple conditions."""
    # AND condition
    expr = parse_search_query("name:alice AND age:>25")
    assert isinstance(expr, SearchExpression)
    assert expr.operator == SearchOperator.AND
    assert len(expr.conditions) == 2

    # OR condition
    expr = parse_search_query("name:alice OR name:bob")
    assert isinstance(expr, SearchExpression)
    assert expr.operator == SearchOperator.OR
    assert len(expr.conditions) == 2

    # Complex nested conditions
    expr = parse_search_query("(name:alice OR name:bob) AND age:>25")
    assert isinstance(expr, SearchExpression)
    assert expr.operator == SearchOperator.AND
    assert len(expr.conditions) == 2
    assert isinstance(expr.conditions[0], SearchExpression)
    assert expr.conditions[0].operator == SearchOperator.OR


def test_web_search_scenarios():
    """Test real-world web search scenarios."""
    # User search with multiple criteria
    expr = parse_search_query("type:user AND (name:~john OR email:~john) AND age:>25")
    assert isinstance(expr, SearchExpression)
    assert expr.operator == SearchOperator.AND

    # Product search with filters
    expr = parse_search_query(
        "category:electronics AND price:<1000 AND (brand:apple OR brand:samsung)"
    )
    assert isinstance(expr, SearchExpression)
    assert expr.operator == SearchOperator.AND

    # Content search with tags
    expr = parse_search_query(
        "type:article AND (tags:python OR tags:programming) AND status:published"
    )
    assert isinstance(expr, SearchExpression)
    assert expr.operator == SearchOperator.AND

    # Location-based search
    expr = parse_search_query(
        "type:restaurant AND (cuisine:italian OR cuisine:japanese) AND rating:>4"
    )
    assert isinstance(expr, SearchExpression)
    assert expr.operator == SearchOperator.AND

    # Job search
    expr = parse_search_query(
        "type:job AND (title:~developer OR title:~engineer) AND location:~remote"
    )
    assert isinstance(expr, SearchExpression)
    assert expr.operator == SearchOperator.AND


def test_special_characters():
    """Test search queries with special characters."""
    # Quoted strings
    expr = parse_search_query('name:"John Doe"')
    assert isinstance(expr, SearchCondition)
    assert expr.value == "John Doe"

    # Escaped quotes
    expr = parse_search_query('description:"O\'Connor"')
    assert isinstance(expr, SearchCondition)
    assert expr.value == "O'Connor"

    # Special characters in values
    expr = parse_search_query("email:user.name@domain.com")
    assert isinstance(expr, SearchCondition)
    assert expr.value == "user.name@domain.com"


def test_invalid_queries():
    """Test handling of invalid search queries."""
    with pytest.raises(ValueError):
        parse_search_query("invalid:")  # Missing value

    with pytest.raises(ValueError):
        parse_search_query(":value")  # Missing key

    with pytest.raises(ValueError):
        parse_search_query("key:value AND")  # Incomplete AND

    with pytest.raises(ValueError):
        parse_search_query("(key:value")  # Unclosed parenthesis


def test_array_operations():
    """Test array-related search operations."""
    # Array contains
    expr = parse_search_query("tags:python")
    assert isinstance(expr, SearchCondition)
    assert expr.operator == SearchOperator.EQUALS

    # Array membership
    expr = parse_search_query('role:@["admin", "user"]')
    assert isinstance(expr, SearchCondition)
    assert expr.operator == SearchOperator.IN


def test_regex_operations():
    """Test regex pattern matching."""
    expr = parse_search_query('name:*"^J.*n$"')
    assert isinstance(expr, SearchCondition)
    assert expr.operator == SearchOperator.MATCHES
    assert expr.value == "^J.*n$"


def test_case_sensitivity():
    """Test case sensitivity behavior for different search operations."""

    # Test exact match
    expr = parse_search_query('name:"John Doe"')
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is True
    assert expr.operator == SearchOperator.EQUALS
    assert expr.value == "John Doe"

    # Test case insensitive exact match
    expr = parse_search_query("name:john/i")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is False
    assert expr.operator == SearchOperator.EQUALS
    assert expr.value == "john"

    # Test starts with
    expr = parse_search_query("name:^J")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is True
    assert expr.operator == SearchOperator.STARTS_WITH
    assert expr.value == "J"

    # Test case insensitive starts with
    expr = parse_search_query("name:^j/i")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is False
    assert expr.operator == SearchOperator.STARTS_WITH
    assert expr.value == "j"

    # Test ends with
    expr = parse_search_query("name:$e")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is True
    assert expr.operator == SearchOperator.ENDS_WITH
    assert expr.value == "e"

    # Test case insensitive ends with
    expr = parse_search_query("name:$E/i")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is False
    assert expr.operator == SearchOperator.ENDS_WITH
    assert expr.value == "E"

    # Test contains text
    expr = parse_search_query("email:~example")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is True
    assert expr.operator == SearchOperator.CONTAINS_TEXT
    assert expr.value == "example"

    # Test case insensitive contains text
    expr = parse_search_query("email:~EXAMPLE/i")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is False
    assert expr.operator == SearchOperator.CONTAINS_TEXT
    assert expr.value == "EXAMPLE"

    # Test array contains
    expr = parse_search_query("tags:python")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is True
    assert expr.operator == SearchOperator.EQUALS
    assert expr.value == "python"

    # Test case insensitive array contains
    expr = parse_search_query("tags:PYTHON/i")
    assert isinstance(expr, SearchCondition)
    assert expr.case_sensitive is False
    assert expr.operator == SearchOperator.EQUALS
    assert expr.value == "PYTHON"


def test_pyparsing_basic():
    """Test basic pyparsing behavior to understand how it handles values and case sensitivity."""
    from pyparsing import Literal, QuotedString, Word, ZeroOrMore, printables

    # Test 1: Basic value parsing with Word
    value = Word(printables, excludeChars=":()/")
    result = value.parseString("john/i")
    print("\nTest 1 - Basic value parse with Word:")
    print("Input: john/i")
    print("Result:", result.asList())

    # Test 2: Value with case sensitivity using Word
    value = Word(printables, excludeChars=":()/")
    case_sensitive = Literal("/i")
    result = (value + case_sensitive).parseString("john/i")
    print("\nTest 2 - Value with case sensitivity using Word:")
    print("Input: john/i")
    print("Result:", result.asList())

    # Test 3: Value with spaces using Word + ZeroOrMore
    value = Word(printables, excludeChars=":()/") + ZeroOrMore(
        Word(printables, excludeChars=":()/")
    )
    result = value.parseString("john doe")
    print("\nTest 3 - Value with spaces using Word + ZeroOrMore:")
    print("Input: john doe")
    print("Result:", result.asList())

    # Test 4: Value with spaces and case sensitivity using Word + ZeroOrMore
    value = Word(printables, excludeChars=":()/") + ZeroOrMore(
        Word(printables, excludeChars=":()/")
    )
    case_sensitive = Literal("/i")
    result = (value + case_sensitive).parseString("john doe/i")
    print("\nTest 4 - Value with spaces and case sensitivity using Word + ZeroOrMore:")
    print("Input: john doe/i")
    print("Result:", result.asList())

    # Test 5: Value with spaces using Word + ZeroOrMore with parse action
    value = (
        Word(printables, excludeChars=":()/")
        + ZeroOrMore(Word(printables, excludeChars=":()/"))
    ).setParseAction(lambda t: " ".join(t))
    result = value.parseString("john doe")
    print("\nTest 5 - Value with spaces using Word + ZeroOrMore with parse action:")
    print("Input: john doe")
    print("Result:", result.asList())

    # Test 6: Value with spaces and case sensitivity using Word + ZeroOrMore with parse action
    value = (
        Word(printables, excludeChars=":()/")
        + ZeroOrMore(Word(printables, excludeChars=":()/"))
    ).setParseAction(lambda t: " ".join(t))
    case_sensitive = Literal("/i")
    result = (value + case_sensitive).parseString("john doe/i")
    print(
        "\nTest 6 - Value with spaces and case sensitivity using Word + ZeroOrMore with parse action:"
    )
    print("Input: john doe/i")
    print("Result:", result.asList())

    # Test 7: Quoted string
    value = QuotedString('"', escChar="\\")
    result = value.parseString('"John Doe"')
    print("\nTest 7 - Quoted string:")
    print('Input: "John Doe"')
    print("Result:", result.asList())

    # Test 8: Quoted string with case sensitivity
    value = QuotedString('"', escChar="\\")
    case_sensitive = Literal("/i")
    result = (value + case_sensitive).parseString('"John Doe"/i')
    print("\nTest 8 - Quoted string with case sensitivity:")
    print('Input: "John Doe"/i')
    print("Result:", result.asList())

    # Test 9: Special characters in value
    value = Word(printables, excludeChars=":()/")
    result = value.parseString("user.name@domain.com")
    print("\nTest 9 - Special characters:")
    print("Input: user.name@domain.com")
    print("Result:", result.asList())

    # Test 10: Special characters with case sensitivity
    value = Word(printables, excludeChars=":()/")
    case_sensitive = Literal("/i")
    result = (value + case_sensitive).parseString("user.name@domain.com/i")
    print("\nTest 10 - Special characters with case sensitivity:")
    print("Input: user.name@domain.com/i")
    print("Result:", result.asList())


def test_pyparsing_logical_operators():
    """Test pyparsing behavior with logical operators and grouping."""
    from pyparsing import (
        CaselessKeyword,
        Forward,
        Group,
        Literal,
        ParseException,
        QuotedString,
        StringEnd,
        Suppress,
        Word,
        alphanums,
        infixNotation,
        opAssoc,
        printables,
    )

    # Basic tokens
    key = Word(alphanums + "_")
    value = (
        QuotedString('"', escChar="\\")
        | QuotedString("'", escChar="\\")
        | Word(printables, excludeChars=":()/")
    )
    operator = Literal(":")

    # Build the condition parser
    condition = Group(key + operator + value)

    # Build the expression parser
    expr = Forward()
    term = condition | Group(Suppress("(") + expr + Suppress(")"))
    expr <<= infixNotation(
        term,
        [
            (CaselessKeyword("NOT"), 1, opAssoc.RIGHT),
            (CaselessKeyword("AND"), 2, opAssoc.LEFT),
            (CaselessKeyword("OR"), 2, opAssoc.LEFT),
        ],
    )

    # Test simple condition
    print("\nTest 1: Simple condition")
    result = expr.parseString("name:john")
    print("Input: name:john")
    print(f"Result: {result}")

    # Test AND condition
    print("\nTest 2: AND condition")
    result = expr.parseString("name:john AND age:25")
    print("Input: name:john AND age:25")
    print(f"Result: {result}")

    # Test OR condition
    print("\nTest 3: OR condition")
    result = expr.parseString("name:john OR name:jane")
    print("Input: name:john OR name:jane")
    print(f"Result: {result}")

    # Test grouped condition
    print("\nTest 4: Grouped condition")
    result = expr.parseString("(name:john OR name:jane) AND age:25")
    print("Input: (name:john OR name:jane) AND age:25")
    print(f"Result: {result}")

    # Test with StringEnd
    print("\nTest 5: With StringEnd")
    expr_with_end = expr + StringEnd()
    result = expr_with_end.parseString("name:john AND age:25")
    print("Input: name:john AND age:25")
    print(f"Result: {result}")

    # Test invalid query
    print("\nTest 6: Invalid query")
    try:
        result = expr_with_end.parseString("name:john AND")
        print("Input: name:john AND")
        print(f"Result: {result}")
    except ParseException as e:
        print(f"Expected error: {e!s}")

    # Test invalid query with StringEnd
    print("\nTest 7: Invalid query with StringEnd")
    try:
        result = expr_with_end.parseString("name:john AND")
        print("Input: name:john AND")
        print(f"Result: {result}")
    except ParseException as e:
        print(f"Expected error: {e!s}")


def test_pyparsing_value_parsing():
    """Test pyparsing behavior specifically for value parsing with spaces."""
    from pyparsing import (
        Group,
        Literal,
        ParseException,
        QuotedString,
        Word,
        ZeroOrMore,
        printables,
    )

    # Test 1: Basic value parsing with Word
    print("\nTest 1: Basic value parsing")
    value = Word(printables, excludeChars=":()/")
    result = value.parseString("john")
    print("Input: john")
    print(f"Result: {result.asList()}")

    # Test 2: Value with spaces using Word + ZeroOrMore
    print("\nTest 2: Value with spaces")
    value = Word(printables, excludeChars=":()/") + ZeroOrMore(
        Word(printables, excludeChars=":()/")
    )
    result = value.parseString("john doe")
    print("Input: john doe")
    print(f"Result: {result.asList()}")

    # Test 3: Value with spaces and parse action
    print("\nTest 3: Value with spaces and parse action")
    value = (
        Word(printables, excludeChars=":()/")
        + ZeroOrMore(Word(printables, excludeChars=":()/"))
    ).setParseAction(lambda t: " ".join(t))
    result = value.parseString("john doe")
    print("Input: john doe")
    print(f"Result: {result.asList()}")

    # Test 4: Value with spaces in a condition
    print("\nTest 4: Value with spaces in condition")
    key = Word(printables, excludeChars=":()/")
    operator = Literal(":")
    value = (
        Word(printables, excludeChars=":()/")
        + ZeroOrMore(Word(printables, excludeChars=":()/"))
    ).setParseAction(lambda t: " ".join(t))
    condition = Group(key + operator + value)
    result = condition.parseString("name:john doe")
    print("Input: name:john doe")
    print(f"Result: {result.asList()}")

    # Test 5: Value with spaces and case sensitivity
    print("\nTest 5: Value with spaces and case sensitivity")
    key = Word(printables, excludeChars=":()/")
    operator = Literal(":")
    value = (
        Word(printables, excludeChars=":()/")
        + ZeroOrMore(Word(printables, excludeChars=":()/"))
    ).setParseAction(lambda t: " ".join(t))
    case_sensitive = Literal("/i")
    condition = Group(key + operator + value + case_sensitive)
    result = condition.parseString("name:john doe/i")
    print("Input: name:john doe/i")
    print(f"Result: {result.asList()}")

    # Test 6: Quoted string with spaces
    print("\nTest 6: Quoted string with spaces")
    value = QuotedString('"', escChar="\\")
    result = value.parseString('"John Doe"')
    print('Input: "John Doe"')
    print(f"Result: {result.asList()}")

    # Test 7: Invalid value (should raise ParseException)
    print("\nTest 7: Invalid value")
    try:
        value = (
            Word(printables, excludeChars=":()/")
            + ZeroOrMore(Word(printables, excludeChars=":()/"))
        ).setParseAction(lambda t: " ".join(t))
        result = value.parseString("john:doe")  # Contains invalid character
        print("Input: john:doe")
        print(f"Result: {result.asList()}")
    except ParseException as e:
        print(f"Expected error: {e!s}")


def test_pyparsing_case_sensitivity():
    """Test pyparsing behavior specifically for case sensitivity handling."""
    from pyparsing import (
        Group,
        Literal,
        QuotedString,
        Word,
        ZeroOrMore,
        printables,
    )

    # Test 1: Basic case sensitivity flag
    print("\nTest 1: Basic case sensitivity flag")
    case_sensitive = Literal("/i")
    result = case_sensitive.parseString("/i")
    print("Input: /i")
    print(f"Result: {result.asList()}")

    # Test 2: Case sensitivity with value
    print("\nTest 2: Case sensitivity with value")
    value = Word(printables, excludeChars=":()/")
    case_sensitive = Literal("/i")
    result = (value + case_sensitive).parseString("john/i")
    print("Input: john/i")
    print(f"Result: {result.asList()}")

    # Test 3: Case sensitivity with spaces in value
    print("\nTest 3: Case sensitivity with spaces in value")
    value = (
        Word(printables, excludeChars=":()/")
        + ZeroOrMore(Word(printables, excludeChars=":()/"))
    ).setParseAction(lambda t: " ".join(t))
    case_sensitive = Literal("/i")
    result = (value + case_sensitive).parseString("john doe/i")
    print("Input: john doe/i")
    print(f"Result: {result.asList()}")

    # Test 4: Case sensitivity in condition
    print("\nTest 4: Case sensitivity in condition")
    key = Word(printables, excludeChars=":()/")
    operator = Literal(":")
    value = (
        Word(printables, excludeChars=":()/")
        + ZeroOrMore(Word(printables, excludeChars=":()/"))
    ).setParseAction(lambda t: " ".join(t))
    case_sensitive = Literal("/i")
    condition = Group(key + operator + value + case_sensitive)
    result = condition.parseString("name:john doe/i")
    print("Input: name:john doe/i")
    print(f"Result: {result.asList()}")

    # Test 5: Case sensitivity with quoted string
    print("\nTest 5: Case sensitivity with quoted string")
    value = QuotedString('"', escChar="\\")
    case_sensitive = Literal("/i")
    result = (value + case_sensitive).parseString('"John Doe"/i')
    print('Input: "John Doe"/i')
    print(f"Result: {result.asList()}")

    # Test 6: Case sensitivity with parse action
    print("\nTest 6: Case sensitivity with parse action")

    def case_sensitive_action(tokens):
        return not tokens or tokens[0] != "/i"

    case_sensitive = (Literal("/i") | Literal("")).setParseAction(case_sensitive_action)
    result = case_sensitive.parseString("/i")
    print("Input: /i")
    print(f"Result: {result.asList()}")

    # Test 7: Case sensitivity with parse action in condition
    print("\nTest 7: Case sensitivity with parse action in condition")
    key = Word(printables, excludeChars=":()/")
    operator = Literal(":")
    value = (
        Word(printables, excludeChars=":()/")
        + ZeroOrMore(Word(printables, excludeChars=":()/"))
    ).setParseAction(lambda t: " ".join(t))

    def case_sensitive_action(tokens):
        return not tokens or tokens[0] != "/i"

    case_sensitive = (Literal("/i") | Literal("")).setParseAction(case_sensitive_action)
    condition = Group(key + operator + value + case_sensitive)
    result = condition.parseString("name:john doe/i")
    print("Input: name:john doe/i")
    print(f"Result: {result.asList()}")

    # Test 8: Case sensitivity with parse action in condition (no /i)
    print("\nTest 8: Case sensitivity with parse action in condition (no /i)")
    result = condition.parseString("name:john doe")
    print("Input: name:john doe")
    print(f"Result: {result.asList()}")


def test_pyparsing_array_values():
    """Test pyparsing behavior specifically for array value handling."""
    from pyparsing import (
        Group,
        Literal,
        Optional,
        ParseException,
        QuotedString,
        Suppress,
        Word,
        delimitedList,
        printables,
    )

    # Test 1: Basic array value parsing
    print("\nTest 1: Basic array value parsing")
    array_value = (
        Suppress("[")
        + Optional(
            delimitedList(
                QuotedString('"', escChar="\\") | Word(printables, excludeChars='[],"/')
            ).setParseAction(lambda t: list(t))
        )
        + Suppress("]")
    )
    result = array_value.parseString('["python", "java", "c++"]')
    print('Input: ["python", "java", "c++"]')
    print(f"Result: {result.asList()}")

    # Test 2: Array value with spaces
    print("\nTest 2: Array value with spaces")
    result = array_value.parseString(
        '["python programming", "java development", "c++ coding"]'
    )
    print('Input: ["python programming", "java development", "c++ coding"]')
    print(f"Result: {result.asList()}")

    # Test 3: Array value with mixed types
    print("\nTest 3: Array value with mixed types")
    result = array_value.parseString('["python", 123, "c++"]')
    print('Input: ["python", 123, "c++"]')
    print(f"Result: {result.asList()}")

    # Test 4: Array value in condition
    print("\nTest 4: Array value in condition")
    key = Word(printables, excludeChars=":()/")
    operator = Literal(":@")
    array_value = (
        Suppress("[")
        + Optional(
            delimitedList(
                QuotedString('"', escChar="\\") | Word(printables, excludeChars='[],"/')
            ).setParseAction(lambda t: list(t))
        )
        + Suppress("]")
    )
    condition = Group(key + operator + array_value)
    result = condition.parseString('tags:@["python", "java", "c++"]')
    print('Input: tags:@["python", "java", "c++"]')
    print(f"Result: {result.asList()}")

    # Test 5: Array value with case sensitivity
    print("\nTest 5: Array value with case sensitivity")
    key = Word(printables, excludeChars=":()/")
    operator = Literal(":@")
    array_value = (
        Suppress("[")
        + Optional(
            delimitedList(
                QuotedString('"', escChar="\\") | Word(printables, excludeChars='[],"/')
            ).setParseAction(lambda t: list(t))
        )
        + Suppress("]")
    )
    case_sensitive = Literal("/i")
    condition = Group(key + operator + array_value + case_sensitive)
    result = condition.parseString('tags:@["python", "java", "c++"]/i')
    print('Input: tags:@["python", "java", "c++"]/i')
    print(f"Result: {result.asList()}")

    # Test 6: Empty array
    print("\nTest 6: Empty array")
    result = array_value.parseString("[]")
    print("Input: []")
    print(f"Result: {result.asList()}")

    # Test 7: Single value array
    print("\nTest 7: Single value array")
    result = array_value.parseString('["python"]')
    print('Input: ["python"]')
    print(f"Result: {result.asList()}")

    # Test 8: Invalid array (should raise ParseException)
    print("\nTest 8: Invalid array")
    try:
        result = array_value.parseString('["python", "java"')  # Missing closing bracket
        print('Input: ["python", "java"')
        print(f"Result: {result.asList()}")
    except ParseException as e:
        print(f"Expected error: {e!s}")

    # Test 9: Array with special characters
    print("\nTest 9: Array with special characters")
    result = array_value.parseString(
        '["user@domain.com", "file/path", "name-with-dashes"]'
    )
    print('Input: ["user@domain.com", "file/path", "name-with-dashes"]')
    print(f"Result: {result.asList()}")


def test_pyparsing_logical_operators_handling():
    """Test pyparsing behavior specifically for logical operator handling."""
    from pyparsing import (
        CaselessKeyword,
        Forward,
        Group,
        Literal,
        ParseException,
        QuotedString,
        StringEnd,
        Suppress,
        Word,
        alphanums,
        infixNotation,
        opAssoc,
        printables,
    )

    # Basic tokens
    key = Word(alphanums + "_")
    value = (
        QuotedString('"', escChar="\\")
        | QuotedString("'", escChar="\\")
        | Word(printables, excludeChars=":()/")
    )
    operator = Literal(":")

    # Build the condition parser
    condition = Group(key + operator + value)

    # Build the expression parser
    expr = Forward()
    term = condition | Group(Suppress("(") + expr + Suppress(")"))
    expr <<= (
        infixNotation(
            term,
            [
                (CaselessKeyword("NOT"), 1, opAssoc.RIGHT),
                (CaselessKeyword("AND"), 2, opAssoc.LEFT),
                (CaselessKeyword("OR"), 2, opAssoc.LEFT),
            ],
        )
        + StringEnd()
    )

    # Test 1: Simple AND condition
    print("\nTest 1: Simple AND condition")
    result = expr.parseString("name:john AND age:25")
    print("Input: name:john AND age:25")
    print(f"Result: {result}")

    # Test 2: Simple OR condition
    print("\nTest 2: Simple OR condition")
    result = expr.parseString("name:john OR name:jane")
    print("Input: name:john OR name:jane")
    print(f"Result: {result}")

    # Test 3: NOT condition
    print("\nTest 3: NOT condition")
    result = expr.parseString("NOT name:john")
    print("Input: NOT name:john")
    print(f"Result: {result}")

    # Test 4: Complex AND/OR condition
    print("\nTest 4: Complex AND/OR condition")
    result = expr.parseString("name:john AND (age:25 OR age:30)")
    print("Input: name:john AND (age:25 OR age:30)")
    print(f"Result: {result}")

    # Test 5: Multiple AND conditions
    print("\nTest 5: Multiple AND conditions")
    result = expr.parseString("name:john AND age:25 AND city:london")
    print("Input: name:john AND age:25 AND city:london")
    print(f"Result: {result}")

    # Test 6: Multiple OR conditions
    print("\nTest 6: Multiple OR conditions")
    result = expr.parseString("name:john OR name:jane OR name:bob")
    print("Input: name:john OR name:jane OR name:bob")
    print(f"Result: {result}")

    # Test 7: NOT with AND
    print("\nTest 7: NOT with AND")
    result = expr.parseString("NOT (name:john AND age:25)")
    print("Input: NOT (name:john AND age:25)")
    print(f"Result: {result}")

    # Test 8: NOT with OR
    print("\nTest 8: NOT with OR")
    result = expr.parseString("NOT (name:john OR name:jane)")
    print("Input: NOT (name:john OR name:jane)")
    print(f"Result: {result}")

    # Test 9: Complex nested conditions
    print("\nTest 9: Complex nested conditions")
    result = expr.parseString("(name:john OR name:jane) AND (age:25 OR age:30)")
    print("Input: (name:john OR name:jane) AND (age:25 OR age:30)")
    print(f"Result: {result}")

    # Test 10: Invalid logical operator (should raise ParseException)
    print("\nTest 10: Invalid logical operator")
    try:
        result = expr.parseString("name:john XOR age:25")
        print("Input: name:john XOR age:25")
        print(f"Result: {result}")
    except ParseException as e:
        print(f"Expected error: {e!s}")

    # Test 11: Invalid grouping (should raise ParseException)
    print("\nTest 11: Invalid grouping")
    try:
        result = expr.parseString("(name:john AND age:25")
        print("Input: (name:john AND age:25")
        print(f"Result: {result}")
    except ParseException as e:
        print(f"Expected error: {e!s}")

    # Test 12: Invalid operator placement (should raise ParseException)
    print("\nTest 12: Invalid operator placement")
    try:
        result = expr.parseString("name:john AND")
        print("Input: name:john AND")
        print(f"Result: {result}")
    except ParseException as e:
        print(f"Expected error: {e!s}")


def test_pyparsing_operator_precedence():
    """Test pyparsing behavior for operator precedence and complex nested conditions."""
    from pyparsing import (
        CaselessKeyword,
        Forward,
        Group,
        Literal,
        ParseException,
        QuotedString,
        StringEnd,
        Suppress,
        Word,
        alphanums,
        infixNotation,
        opAssoc,
        printables,
    )

    # Basic tokens
    key = Word(alphanums + "_")
    value = (
        QuotedString('"', escChar="\\")
        | QuotedString("'", escChar="\\")
        | Word(printables, excludeChars=":()/")
    )
    operator = Literal(":")

    # Build the condition parser
    condition = Group(key + operator + value)

    # Build the expression parser
    expr = Forward()
    term = condition | Group(Suppress("(") + expr + Suppress(")"))
    expr <<= (
        infixNotation(
            term,
            [
                (CaselessKeyword("NOT"), 1, opAssoc.RIGHT),
                (CaselessKeyword("AND"), 2, opAssoc.LEFT),
                (CaselessKeyword("OR"), 2, opAssoc.LEFT),
            ],
        )
        + StringEnd()
    )

    # Test 1: Operator precedence (AND before OR)
    print("\nTest 1: Operator precedence (AND before OR)")
    result = expr.parseString("name:john OR name:jane AND age:25")
    print("Input: name:john OR name:jane AND age:25")
    print(f"Result: {result}")

    # Test 2: Complex nested conditions with multiple levels
    print("\nTest 2: Complex nested conditions with multiple levels")
    result = expr.parseString(
        "(name:john OR (name:jane AND age:25)) AND (city:london OR city:paris)"
    )
    print(
        "Input: (name:john OR (name:jane AND age:25)) AND (city:london OR city:paris)"
    )
    print(f"Result: {result}")

    # Test 3: Multiple NOT operations
    print("\nTest 3: Multiple NOT operations")
    result = expr.parseString("NOT NOT name:john")
    print("Input: NOT NOT name:john")
    print(f"Result: {result}")

    # Test 4: Whitespace handling
    print("\nTest 4: Whitespace handling")
    result = expr.parseString("  name:john   AND   age:25  ")
    print("Input: '  name:john   AND   age:25  '")
    print(f"Result: {result}")

    # Test 5: Complex NOT with nested conditions
    print("\nTest 5: Complex NOT with nested conditions")
    result = expr.parseString("NOT (name:john AND (age:25 OR age:30))")
    print("Input: NOT (name:john AND (age:25 OR age:30))")
    print(f"Result: {result}")

    # Test 6: Deep nesting
    print("\nTest 6: Deep nesting")
    result = expr.parseString(
        "((name:john OR name:jane) AND (age:25 OR age:30)) AND (city:london OR city:paris)"
    )
    print(
        "Input: ((name:john OR name:jane) AND (age:25 OR age:30)) AND (city:london OR city:paris)"
    )
    print(f"Result: {result}")

    # Test 7: Mixed operators with parentheses
    print("\nTest 7: Mixed operators with parentheses")
    result = expr.parseString("(name:john AND age:25) OR (name:jane AND age:30)")
    print("Input: (name:john AND age:25) OR (name:jane AND age:30)")
    print(f"Result: {result}")

    # Test 8: Invalid nested grouping (should raise ParseException)
    print("\nTest 8: Invalid nested grouping")
    try:
        result = expr.parseString("((name:john AND age:25)")
        print("Input: ((name:john AND age:25)")
        print(f"Result: {result}")
    except ParseException as e:
        print(f"Expected error: {e!s}")

    # Test 9: Invalid operator sequence (should raise ParseException)
    print("\nTest 9: Invalid operator sequence")
    try:
        result = expr.parseString("name:john AND OR age:25")
        print("Input: name:john AND OR age:25")
        print(f"Result: {result}")
    except ParseException as e:
        print(f"Expected error: {e!s}")

    # Test 10: Complex whitespace and formatting
    print("\nTest 10: Complex whitespace and formatting")
    result = expr.parseString(
        """
        (name:john OR name:jane) AND
        (age:25 OR age:30) AND
        (city:london OR city:paris)
    """
    )
    print("Input: Complex whitespace and formatting")
    print(f"Result: {result}")


def test_minimal_diagnostic_parser():
    """Minimal diagnostic test to print parsed tokens for failing and passing cases."""
    from graph_reader.indexers.search_expression import parse_search_query

    print("\nMinimal Diagnostic Test: Single condition")
    try:
        expr = parse_search_query("name:alice")
        print("Parsed successfully:", expr)
    except Exception as e:
        print("Failed to parse 'name:alice':", e)

    print("\nMinimal Diagnostic Test: Two conditions with AND")
    try:
        expr = parse_search_query("name:alice AND age:>25")
        print("Parsed successfully:", expr)
    except Exception as e:
        print("Failed to parse 'name:alice AND age:>25':", e)
