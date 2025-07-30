from typing import Any

from .search_expression import SearchCondition, SearchExpression


class BaseIndexer:
    def search_by_property(
        self,
        key: str,
        value: Any,
        operation: str = "equals",
        case_sensitive: bool = True,
    ) -> list[int]:
        """Search for entities by property value with various operations.

        Args:
            key: The property key to search for
            value: The value to compare against
            operation: The comparison operation to use. One of:
                - "equals": Exact match (default)
                - "contains": Value is in array property
                - "starts_with": String starts with value
                - "ends_with": String ends with value
                - "contains_text": String contains value
                - "greater_than": Numeric greater than
                - "less_than": Numeric less than
            case_sensitive: Whether string comparisons should be case sensitive

        Returns:
            List of entity IDs matching the search criteria
        """
        raise NotImplementedError

    def search(self, expression: SearchExpression | SearchCondition) -> list[int]:
        """Search for entities using a search expression.

        Args:
            expression: A search expression or condition to evaluate

        Returns:
            List of entity IDs matching the search criteria

        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError

    def search_query(self, query: str) -> list[int]:
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
        from .search_expression import parse_search_query

        expression = parse_search_query(query)
        return self.search(expression)
