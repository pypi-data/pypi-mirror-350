import re
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Union

from pyparsing import (
    CaselessKeyword,
    Forward,
    Group,
    Literal,
    Optional,
    ParseException,
    ParseResults,
    QuotedString,
    StringEnd,
    Suppress,
    Word,
    alphanums,
    delimitedList,
    infixNotation,
    opAssoc,
    printables,
)


class SearchOperator(Enum):
    """Supported search operators."""

    EQUALS = "equals"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    CONTAINS_TEXT = "contains_text"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    MATCHES = "matches"  # For regex pattern matching
    IN = "in"  # For array membership
    NOT = "not"  # For negation
    AND = "and"  # For combining conditions
    OR = "or"  # For combining conditions


@dataclass
class SearchCondition:
    """A single search condition."""

    key: str
    operator: SearchOperator
    value: Any
    case_sensitive: bool = True


@dataclass
class SearchExpression:
    """A search expression that can combine multiple conditions."""

    operator: SearchOperator
    conditions: list[Union["SearchExpression", SearchCondition]]


class SearchExpressionEvaluator:
    """Evaluates search expressions against entity properties."""

    def __init__(self):
        self._operations: dict[SearchOperator, Callable[[Any, Any], bool]] = {
            SearchOperator.EQUALS: lambda x, y: x == y,
            SearchOperator.CONTAINS: lambda x, y: isinstance(x, list) and y in x,
            SearchOperator.STARTS_WITH: lambda x, y: isinstance(x, str)
            and x.startswith(y),
            SearchOperator.ENDS_WITH: lambda x, y: isinstance(x, str) and x.endswith(y),
            SearchOperator.CONTAINS_TEXT: lambda x, y: isinstance(x, str) and y in x,
            SearchOperator.GREATER_THAN: lambda x, y: isinstance(x, int | float)
            and x > y,
            SearchOperator.LESS_THAN: lambda x, y: isinstance(x, int | float) and x < y,
            SearchOperator.MATCHES: lambda x, y: isinstance(x, str)
            and bool(re.match(y, x)),
            SearchOperator.IN: lambda x, y: isinstance(y, list) and x in y,
        }

    def normalize_value(self, val: Any, case_sensitive: bool = True) -> Any:
        """Normalize a value for comparison."""
        if not case_sensitive:
            # Convert to string and lowercase for case-insensitive comparison
            return str(val).lower()
        return val

    def evaluate_condition(
        self, condition: SearchCondition, props: dict[str, Any]
    ) -> bool:
        """Evaluate a single search condition against entity properties."""
        if condition.key not in props:
            return False

        prop_value = props[condition.key]
        search_value = condition.value

        if condition.operator == SearchOperator.NOT:
            return not self.evaluate_condition(condition.value, props)

        # For array values, we need to handle them differently
        if condition.operator == SearchOperator.IN:
            # For array membership, we want to check if the property value is in the search value list
            return isinstance(search_value, list) and prop_value in search_value
        elif (
            isinstance(prop_value, list) and condition.operator == SearchOperator.EQUALS
        ):
            # For array contains, we want to check if the search value is in the property value list
            return search_value in prop_value

        # For text operations, we need to ensure both values are strings
        if condition.operator in {
            SearchOperator.CONTAINS_TEXT,
            SearchOperator.STARTS_WITH,
            SearchOperator.ENDS_WITH,
            SearchOperator.MATCHES,
        }:
            prop_value = str(prop_value)
            search_value = str(search_value)

        # Normalize values for comparison
        prop_value = self.normalize_value(prop_value, condition.case_sensitive)
        search_value = self.normalize_value(search_value, condition.case_sensitive)

        # Special handling for text operations
        if condition.operator == SearchOperator.CONTAINS_TEXT:
            print(
                f"[DEBUG] CONTAINS_TEXT: prop_value='{prop_value}', search_value='{search_value}'"
            )
            return search_value in prop_value
        elif condition.operator == SearchOperator.STARTS_WITH:
            return prop_value.startswith(search_value)
        elif condition.operator == SearchOperator.ENDS_WITH:
            return prop_value.endswith(search_value)
        elif condition.operator == SearchOperator.MATCHES:
            return bool(re.match(search_value, prop_value))
        elif condition.operator == SearchOperator.GREATER_THAN:
            print(
                f"[DEBUG] GREATER_THAN: prop_value={prop_value} ({type(prop_value)}), search_value={search_value} ({type(search_value)})"
            )
            return prop_value > search_value

        # For other operations, use the standard comparison
        compare = self._operations[condition.operator]
        return compare(prop_value, search_value)

    def evaluate_expression(
        self, expression: SearchExpression | SearchCondition, props: dict[str, Any]
    ) -> bool:
        """Evaluate a search expression against entity properties."""
        if isinstance(expression, SearchCondition):
            return self.evaluate_condition(expression, props)

        if expression.operator == SearchOperator.AND:
            results = [
                self.evaluate_expression(cond, props) for cond in expression.conditions
            ]
            print(f"[DEBUG] AND: conditions={results}, props={props}")
            return all(results)
        elif expression.operator == SearchOperator.OR:
            return any(
                self.evaluate_expression(cond, props) for cond in expression.conditions
            )
        else:
            print("DEBUG: Unsupported expression operator branch hit")
            raise ValueError(f"Unsupported expression operator: {expression.operator}")


class SearchQueryParser:
    """Parser for search query strings."""

    def __init__(self):
        # Basic tokens
        key = Word(alphanums + "_")
        value = (
            QuotedString('"', escChar="\\")
            | QuotedString("'", escChar="\\")
            | Word(printables, excludeChars=":()/")
        )

        # Case sensitivity: default True, set to False if /i is present
        def case_sensitive_action(tokens):
            # For case insensitive, we want to return False
            # For case sensitive, we want to return True
            return not tokens or tokens[0] != "/i"

        case_sensitive = (Literal("/i") | Literal("")).setParseAction(
            case_sensitive_action
        )

        # Operators - order matters! More specific operators first
        matches = Literal(":*")
        greater_than = Literal(":>")
        less_than = Literal(":<")
        contains_text = Literal(":~")
        starts_with = Literal(":^")
        ends_with = Literal(":$")
        in_array = Literal(":@")
        equals = Literal(":")

        # Build the condition parser
        operator = (
            matches
            | greater_than
            | less_than
            | contains_text
            | starts_with
            | ends_with
            | in_array
            | equals
        )

        # Array value parser
        array_value = (
            Suppress("[")
            + Optional(
                delimitedList(
                    QuotedString('"', escChar="\\")
                    | Word(printables, excludeChars='[],"/')  # Also exclude / here
                ).setParseAction(lambda t: list(t))
            )
            + Suppress("]")
        )

        # Build the condition parser with array support
        condition = Group(
            key + operator + (array_value | value) + case_sensitive
        ).setParseAction(self._parse_condition)

        # Build the expression parser
        self.expr = Forward()
        term = condition | Group(Suppress("(") + self.expr + Suppress(")"))

        # Define the operators with their precedence
        not_op = CaselessKeyword("NOT").setParseAction(lambda: SearchOperator.NOT)
        and_op = CaselessKeyword("AND").setParseAction(lambda: SearchOperator.AND)
        or_op = CaselessKeyword("OR").setParseAction(lambda: SearchOperator.OR)

        # Build the expression parser with operator precedence
        self.expr <<= infixNotation(
            term,
            [
                (not_op, 1, opAssoc.RIGHT, self._parse_not),
                (and_op, 2, opAssoc.LEFT, self._parse_and),
                (or_op, 2, opAssoc.LEFT, self._parse_or),
            ],
        )

        # Create the final parser that requires the entire string to be consumed
        self.parser = self.expr + StringEnd()

    def _parse_condition(self, tokens):
        """Parse a condition token into a SearchCondition."""
        # tokens: [key, op, value, case_sensitive]
        if len(tokens[0]) < 4:
            raise ValueError(f"Invalid condition format: {tokens[0]}")

        key, op = tokens[0][:2]
        case_sensitive = tokens[0][-1]

        # Handle array values
        if op == ":@":
            # For array values, get all values between op and case_sensitive
            values = tokens[0][2:-1]
            # If no values were found (empty array), use an empty list
            value = list(values) if values else []
            return SearchCondition(
                key=key,
                operator=SearchOperator.IN,
                value=value,
                case_sensitive=case_sensitive,
            )

        # For non-array values, use the standard format
        value = tokens[0][2]

        # Map operators to SearchOperator enum
        operator_map = {
            ":": SearchOperator.EQUALS,
            ":*": SearchOperator.MATCHES,
            ":>": SearchOperator.GREATER_THAN,
            ":<": SearchOperator.LESS_THAN,
            ":~": SearchOperator.CONTAINS_TEXT,
            ":^": SearchOperator.STARTS_WITH,
            ":$": SearchOperator.ENDS_WITH,
            ":@": SearchOperator.IN,
        }

        # Convert numeric values
        if isinstance(value, str) and value.isdigit():
            value = int(value)

        # Create the condition with the correct operator and case sensitivity
        return SearchCondition(
            key=key,
            operator=operator_map[op],
            value=value,
            case_sensitive=case_sensitive,
        )

    def _parse_not(self, tokens):
        """Parse a NOT expression."""
        expr = tokens[0][1]
        if isinstance(expr, ParseResults):
            expr = expr[0]
        return SearchExpression(SearchOperator.NOT, [expr])

    def _parse_and(self, tokens):
        """Parse an AND expression."""
        conditions = []
        for token in tokens[0][0::2]:
            if isinstance(token, ParseResults):
                conditions.append(token[0])
            else:
                conditions.append(token)
        return SearchExpression(SearchOperator.AND, conditions)

    def _parse_or(self, tokens):
        """Parse an OR expression."""
        conditions = []
        for token in tokens[0][0::2]:
            if isinstance(token, ParseResults):
                conditions.append(token[0])
            else:
                conditions.append(token)
        return SearchExpression(SearchOperator.OR, conditions)

    def parse(self, query: str) -> SearchExpression:
        """Parse a search query string into a SearchExpression."""
        try:
            result = self.parser.parseString(query, parseAll=True)
            return result[0]
        except ParseException as e:
            raise ValueError(f"Invalid search query: {e!s}") from e


def parse_search_query(query: str) -> SearchExpression:
    """Parse a search query string into a SearchExpression.

    Query syntax examples:
    - Simple: "name:alice"
    - Multiple conditions: "name:alice AND age:>25"
    - Complex: "(name:alice OR name:bob) AND age:>25"
    - Array search: "tags:python"
    - Text search: "description:~python"
    - Case insensitive: "name:alice/i"

    Operators:
    - : (equals)
    - :> (greater than)
    - :< (less than)
    - :~ (contains text)
    - :^ (starts with)
    - :$ (ends with)
    - :* (matches regex)
    - :@ (in array)
    - /i (case insensitive)

    Logical operators:
    - AND
    - OR
    - NOT
    - () (grouping)
    """
    parser = SearchQueryParser()
    return parser.parse(query)
