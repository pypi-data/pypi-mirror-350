class QueryOperator:
    """
    Query operators for filtering data in ANT API queries.
    These operators match the Laravel-style query filtering system:
    https://abbasudo.github.io/laravel-purity/js-examples/available-methods.html

    Operators:
        EQ ("$eq"): Equal (case-insensitive)
        EQC ("$eqc"): Equal (case-sensitive)
        NE ("$ne"): Not equal
        LT ("$lt"): Less than
        LTE ("$lte"): Less than or equal to
        GT ("$gt"): Greater than
        GTE ("$gte"): Greater than or equal to
        IN ("$in"): Included in an array
        NOT_IN ("$notIn"): Not included in an array
        CONTAINS ("$contains"): Contains text (case-insensitive)
        NOT_CONTAINS ("$notContains"): Does not contain text (case-insensitive)
        CONTAINSC ("$containsc"): Contains text (case-sensitive)
        NOT_CONTAINSC ("$notContainsc"): Does not contain text (case-sensitive)
        NULL ("$null"): Is null
        NOT_NULL ("$notNull"): Is not null
        BETWEEN ("$between"): Value is between two numbers
        NOT_BETWEEN ("$notBetween"): Value is not between two numbers
        STARTS_WITH ("$startsWith"): Starts with text (case-insensitive)
        STARTS_WITHC ("$startsWithc"): Starts with text (case-sensitive)
        ENDS_WITH ("$endsWith"): Ends with text (case-insensitive)
        ENDS_WITHC ("$endsWithc"): Ends with text (case-sensitive)
        OR ("$or"): Logical OR for combining multiple conditions
        AND ("$and"): Logical AND for combining multiple conditions
    """
    
    # Basic comparison operators
    EQ = "$eq"              # Equal (case-insensitive)
    EQC = "$eqc"           # Equal (case-sensitive)
    NE = "$ne"             # Not equal
    LT = "$lt"             # Less than
    LTE = "$lte"           # Less than or equal to
    GT = "$gt"             # Greater than
    GTE = "$gte"           # Greater than or equal to
    
    # Array operators
    IN = "$in"             # Included in an array
    NOT_IN = "$notIn"      # Not included in an array
    
    # Text search operators
    CONTAINS = "$contains"         # Contains text (case-insensitive)
    NOT_CONTAINS = "$notContains"  # Does not contain text (case-insensitive)
    CONTAINSC = "$containsc"       # Contains text (case-sensitive)
    NOT_CONTAINSC = "$notContainsc"  # Does not contain text (case-sensitive)
    
    # Null checking operators
    NULL = "$null"         # Is null
    NOT_NULL = "$notNull"  # Is not null
    
    # Range operators
    BETWEEN = "$between"       # Value is between two numbers
    NOT_BETWEEN = "$notBetween"  # Value is not between two numbers
    
    # String pattern matching operators
    STARTS_WITH = "$startsWith"     # Starts with text (case-insensitive)
    STARTS_WITHC = "$startsWithc"   # Starts with text (case-sensitive)
    ENDS_WITH = "$endsWith"         # Ends with text (case-insensitive)
    ENDS_WITHC = "$endsWithc"       # Ends with text (case-sensitive)
    
    # Logical operators
    OR = "$or"     # Logical OR for combining multiple conditions
    AND = "$and"   # Logical AND for combining multiple conditions

    @classmethod
    def requires_array_value(cls, operator: str) -> bool:
        """
        Check if an operator requires an array value.
        
        Args:
            operator: The operator to check
            
        Returns:
            bool: True if the operator requires an array value
        """
        return operator in {cls.IN, cls.NOT_IN, cls.BETWEEN, cls.NOT_BETWEEN, cls.OR, cls.AND}

    @classmethod
    def requires_string_value(cls, operator: str) -> bool:
        """
        Check if an operator requires a string value.
        
        Args:
            operator: The operator to check
            
        Returns:
            bool: True if the operator requires a string value
        """
        return operator in {
            cls.CONTAINS, cls.NOT_CONTAINS, cls.CONTAINSC, cls.NOT_CONTAINSC,
            cls.STARTS_WITH, cls.STARTS_WITHC, cls.ENDS_WITH, cls.ENDS_WITHC
        }

    @classmethod
    def requires_no_value(cls, operator: str) -> bool:
        """
        Check if an operator requires no value.
        
        Args:
            operator: The operator to check
            
        Returns:
            bool: True if the operator requires no value
        """
        return operator in {cls.NULL, cls.NOT_NULL}
