""" 
Query builder for ANT API queries. 

Creates query strings or JSON objects for querying.

created by: Dervis van Leersum

"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode
from datetime import datetime, date
import json


from ant_connect.utils import QueryOperator


__all__ = ['QueryBuilder', 'QueryValidationError']

defaultlistindict = defaultdict(list)
reserved_keys = ['filters', 'fields', 'page', 'per_page', 'include', 'sort']


class QueryValidationError(Exception):
    """Raised when query validation fails"""
    pass


@dataclass
class QueryBuilder:
    """
    Enhanced builder for constructing ANT API queries with validation
    and support for all operators.

    **NOTE**
    It is not yet possible to create nested conditions with AND/OR in the filters.

    """
    
    _filters: Dict[str, Any] = field(default_factory=dict)
    _fields: defaultdict[list] = field(default_factory=lambda: defaultdict(list))
    _page: Optional[int] = None
    _per_page: Optional[int] = None
    _include: List[str] = field(default_factory=list)
    _sort: List[str] = field(default_factory=list)

    def _validate_operator_value(self, operator: str, value: Any) -> None:
        """Validate that the value matches the operator requirements."""
        if QueryOperator.requires_array_value(operator):
            if not isinstance(value, (list, tuple)):
                raise QueryValidationError(
                    f"Operator {operator} requires an array value, got {type(value)}"
                )
        elif QueryOperator.requires_string_value(operator):
            if not isinstance(value, str):
                raise QueryValidationError(
                    f"Operator {operator} requires a string value, got {type(value)}"
                )
        elif QueryOperator.requires_no_value(operator):
            if value != "":
                raise QueryValidationError(
                    f"Operator {operator} should be an empty string, got {value}"
                )

    def _format_value(self, value: Any) -> Any:
        """Format value for query string based on its type."""
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, (list, tuple)):
            return [self._format_value(v) for v in value]
        elif isinstance(value, bool):
            return str(value).lower()
        return value

    def _and_or(self, query_operator: QueryOperator, conditions: Tuple[Tuple[str, str, Optional[Any]]]) -> None:
        """
        Add AND or OR conditions.
        
        Args:
            operator: QueryOperator.AND or QueryOperator.OR
            *conditions: Tuples of (field, operator, value)
        """
        filters = []
        for condition in conditions:
            if len(condition) == 3:
                field, operator, value = condition
            elif len(condition) == 2:
                field, operator = condition
                value = ""
            else:
                raise QueryValidationError("Invalid number of arguments")

            self._validate_operator_value(operator, value)
            filters.append({
                field: {operator: self._format_value(value)}
            })

        path = query_operator
        if path not in self._filters:
            self._filters[path] = []
        self._filters[path].extend(filters)

    def _create_unique_list(self, fields: List[str]) -> List[str]:
        """Create a unique list of fields for a model."""
        if isinstance(fields, list):
            fields_unique = list(set(fields))
        else: 
            raise ValueError("Fields must be a list")
        return fields_unique

    def filter(self, field: str, operator: str, value: Any = "", nested_path: Optional[List[str]] = None) -> QueryBuilder:
        """
        Add a filter condition.
        
        Args:
            field: Field name to filter on
            operator: Operator from QueryOperator class
            value: Filter value (optional for some operators)
            nested_path: Optional list parent fields for nesting

        Examples:
            Equal: .filter('status', QueryOperator.EQ, 'open')
            Included in an array: .filter('priority', QueryOperator.IN, ['high', 'urgent'])
            Is null: .filter('deleted_at', QueryOperator.NULL)
            Nesting: .filter('type_one.type_nested', QueryOperator.EQ, 'workflow-blueprint')
            Nesting: .filter('type_one', QueryOperator.EQ, 'workflow-blueprint', nested_path=['type_nested', 'type_double_nested'])
        """
        self._validate_operator_value(operator, value)
        formatted_value = self._format_value(value)

        # Handle dot notation nesting
        if '.' in field and nested_path is None:
            parts = field.split('.')
            field = parts[0]
            nested_path = parts[1:]

        # Building the filter path
        path = f"filters[{field}]"
        if nested_path:
            nested = ']['.join(nested_path)
            path += f"[{nested}]"

        path += f"[{operator}]"
        
        if QueryOperator.requires_array_value(operator):
            if operator in [QueryOperator.BETWEEN, QueryOperator.NOT_BETWEEN]:
                if len(formatted_value) != 2:
                    raise QueryValidationError(
                        f"Operator {operator} requires exactly 2 values, got {len(formatted_value)}"
                    )
                self._filters[path] = ",".join(str(v) for v in formatted_value)
            else:
                self._filters[path] = ",".join(str(v) for v in formatted_value)
        elif QueryOperator.requires_no_value(operator):
            self._filters[path] = ""
        else:
            self._filters[path] = formatted_value

        return self

    def or_where(self, *conditions: Tuple[str, str, Optional[Any]]) -> QueryBuilder:
        """
        Add OR conditions.
        
        Args:
            *conditions: Tuples of (field, operator, value)
            
        Example:
            .or_where(
                ('status', QueryOperator.EQ, 'open'),
                ('priority', QueryOperator.IN, ['high', 'urgent']),
                ('deleted_at', QueryOperator.NULL)
            )
        """
        self._and_or(QueryOperator.OR, conditions)
        return self

    def and_where(self, *conditions: Tuple[str, str, Optional[Any]]) -> QueryBuilder:
        """
        Add AND conditions.
        
        Args:
            *conditions: Tuples of (field, operator, value)
            
        Example:
            .and_where(
                ('status', QueryOperator.NE, 'closed'),
                ('due_date', QueryOperator.LT, datetime.now()),
                ('deleted_at', QueryOperator.NULL)
            )
        """
        self._and_or(QueryOperator.AND, conditions)
        return self

    def where_null(self, field: str) -> QueryBuilder:
        """Shorthand for NULL check."""
        return self.filter(field=field, operator=QueryOperator.NULL, value="")

    def where_not_null(self, field: str) -> QueryBuilder:
        """Shorthand for NOT NULL check."""
        return self.filter(field=field, operator=QueryOperator.NOT_NULL, value="")

    def where_between(self, field: str, min_value: Any, max_value: Any) -> QueryBuilder:
        """Shorthand for BETWEEN check."""
        return self.filter(field=field, operator=QueryOperator.BETWEEN, value=[min_value, max_value])

    def where_contains(self, field: str, value: str, case_sensitive: bool = False) -> QueryBuilder:
        """Shorthand for CONTAINS check."""
        operator = QueryOperator.CONTAINSC if case_sensitive else QueryOperator.CONTAINS
        return self.filter(field=field, operator=operator, value=value)

    def fields(self, model: str, fields: List[str]) -> QueryBuilder:
        """
        Select specific fields to return.
        
        Example:
            .fields('tasks', ['id', 'title', 'status'])
        """
        self._fields[model].extend(fields)

        fields_all = self._fields.get(model, [])
        fields_unique = self._create_unique_list(fields_all)
        self._fields[model] = fields_unique

        return self

    def include(self, *relations: str) -> QueryBuilder:
        """
        Include related data.
        
        Example:
            .include('project', 'assignedTo')
        """
        self._include.extend(relations)
        fields_unique = self._create_unique_list(self._include)
        self._include = fields_unique
        return self

    def sort(self, *fields: str) -> QueryBuilder:
        """
        Add sort criteria. Use '-' prefix for descending order.
        
        Example:
            .sort('title', '-created_at')
        """
        self._sort.extend(fields)
        fields_unique = self._create_unique_list(self._sort)
        self._sort = fields_unique
        return self

    def paginate(self, page: Optional[int] = None, per_page: Optional[int] = None) -> QueryBuilder:
        """
        Add pagination parameters.
        
        Example:
            .paginate(page=2, per_page=15)
        """
        if page is not None and page < 1:
                raise QueryValidationError("Page number must be greater than 0")
        if per_page is not None and per_page < 1:
            raise QueryValidationError("Items per page must be greater than 0")
        if page is None and per_page is None:
            raise QueryValidationError("Page number or items per page must be provided")
        
        if page:
            self._page = page
        if per_page:
            self._per_page = per_page
        return self

    def add_parameter(self, key: str, value: Any) -> QueryBuilder:
        """
        Add a custom query parameter tot he QueryBuilder object.
        
        Args:
            key: Parameter name
            value: Parameter value (must be JSON serializable)

        Example:
            QueryBuilder.add_parameter('is_task', True)
            QueryBuilder.add_parameter('custom_field', 'value')
            QueryBuilder.add_parameter('limit', 100)

        Returns:
            QueryBuilder object

        Raises:
            TypeError: If value is not JSON serializable
            ValueError: If key conflicts with existing query builder properties
        """
        formatted_value = self._format_value(value)

        if key in reserved_keys:
            raise ValueError(
                f"Key '{key}' is a reserved for query builder propertie. Use the approriate method instead:"
                f"filter(), fields(), paginate(), include(), sort()"
            )

        # verify if value is JSON serializable
        try:
            json.dumps(formatted_value)
        except (TypeError, OverflowError) as e:
            raise TypeError(f"Value for parameter '{key}' must be JSON serializable.") from e

        # store custom parameter
        if not hasattr(self, '_custom_parameters'):
            self._custom_parameters = {}

        self._custom_parameters[key] = formatted_value
        return self

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the query to the frontend JSON format.
        
        Returns:
            Dict matching the frontend query structure
            
        Example output:
        {
            "filters": {
                "parent": {
                    "$eq": "123"
                }
            },
            "fields": {
                "tasks": "id,title,status",
                "assignedTo": "id,firstname,lastname"
            },
            "include": "assignedTo,relations",
            "sort": ["title"]
        }
        """
        result = {}
        
        # Handle filters
        if self._filters:
            # Convert URL-style filters to nested structure
            filters = {}
            for key, value in self._filters.items():
                if key.startswith('filters[') and ']' in key:
                    # Extract the nested path from key like "filters[type][type][type]"
                    path_str = key[8:key.rindex('[')]
                    operator = key[key.rindex('[') + 1:-1]

                    # split path into parts: ['type', 'type', 'type'] from "[type][type][type]"
                    part_paths = [p[:-1] for p in path_str.split('[')]

                    # build nested structure
                    current = filters
                    for i, part in enumerate(part_paths):
                        if i == len(part_paths) - 1:
                            if part not in current:
                                current[part] = {}
                            current[part][operator] = value
                        else:
                            if part not in current:
                                current[part] = {}
                            current = current[part]
                elif key in ['$or', '$and']:
                    filters[key] = value

            if filters:
                result['filters'] = filters

        # Add fields
        if self._fields:
            result['fields'] = {
                model: fields if isinstance(fields, str) else ','.join(fields)
                for model, fields in self._fields.items()
            }

        # Add includes
        if self._include:
            result['include'] = ','.join(self._include)

        # Add sorting
        if self._sort:
            result['sort'] = self._sort

        # Add pagination
        if self._page:
            result['page'] = self._page
        if self._per_page:
            result['per_page'] = self._per_page

        # add custom parameters
        if hasattr(self, '_custom_parameters'):
            result.update(self._custom_parameters)

        return result

    # TODO: refactor this method; could be simplified by flattening with flatten-dict first then parsing to standard
    def _flatten_dict(self, d: dict) -> Dict[str, Any]:
        """ Flatten a nested dictionary to a single level. """
        flattened = {}

        def flatten_filters(filters: dict, prefix: str = 'filters') -> None:
            for key, value in filters.items():
                if key in ['$or', '$and']:
                    # Handle OR/AND conditions (unchanged)
                    for i, condition in enumerate(value):
                        for field, operations in condition.items():
                            for op, val in operations.items():
                                if isinstance(val, list):
                                    for j, v in enumerate(val):
                                        flattened[f"{prefix}[{key}][{i}][{field}][{op}][{j}]"] = v
                                else:
                                    if op in ['$null', '$notNull']:
                                        flattened[f"{prefix}[{key}][{i}][{field}][{op}]"] = ''
                                    else:
                                        flattened[f"{prefix}[{key}][{i}][{field}][{op}]"] = val
                else:
                    current_prefix = f"{prefix}[{key}]"
                    if isinstance(value, dict):
                        # Check if the dict contains operators
                        if any(k.startswith('$') for k in value.keys()):
                            for op, val in value.items():
                                if isinstance(val, list):
                                    for j, v in enumerate(val):
                                        flattened[f"{current_prefix}[{op}][{j}]"] = v
                                else:
                                    if op in ['$null', '$notNull']:
                                        flattened[f"{current_prefix}[{op}]"] = ''
                                    else:
                                        flattened[f"{current_prefix}[{op}]"] = val
                        else:
                            # This is a nested structure, recurse
                            flatten_filters(value, current_prefix)

        # handle filters
        if 'filters' in d:
            flatten_filters(d['filters'])

        # Handle fields
        if 'fields' in d:
            for model, fields in d['fields'].items():
                if isinstance(fields, str):
                    fields = fields.split(',')
                flattened[f"fields[{model}]"] = ','.join(fields)

        # Handle include
        if 'include' in d:
            flattened['include'] = d['include'] if isinstance(d['include'], str) else ','.join(d['include'])

        # Handle sort
        if 'sort' in d:
            sort_values = d['sort']
            if isinstance(sort_values, list):
                for i, value in enumerate(sort_values):
                    flattened[f"sort[{i}]"] = value
            else:
                flattened['sort'] = sort_values

        # Handle pagination
        if 'page' in d:
            flattened['page'] = d['page']
        if 'per_page' in d:
            flattened['per_page'] = d['per_page']

        # handle custom parameters
        for key, value in d.items():
            if key not in reserved_keys:
                flattened[key] = value

        return flattened

    def to_query_string(self) -> str:
        """Convert the query to a URL-encoded string."""
        json_query = self.to_json()
        print(f"\njson_query: {json_query}")
        flattened_query = self._flatten_dict(json_query)

        return urlencode(flattened_query, doseq=True).replace('None', '')
