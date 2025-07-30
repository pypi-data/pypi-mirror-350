from enum import Enum


class HttpMethodType(Enum):
    """possible HTTP methods"""

    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    POST = "POST"


class DataType(Enum):
    """possible column data types
    
    Types:
        TEXT: text
        TEXT_FIELD: text-field
        INTEGER: integer
        BOOLEAN: boolean
        DATE: date
        LINK: link
        EMAIL: email
        DROPDOWN: dropdown
        DOCUMENT: document
        FLOAT: float
        SBSCODE: sbscode
        TABLE: table
    """

    TEXT = "text"
    TEXT_FIELD = "text-field"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DATE = "date"
    LINK = "link"
    EMAIL = "email"
    DROPDOWN = "dropdown"
    DOCUMENT = "document"
    FLOAT = "float"
    SBSCODE = "sbscode"
    TABLE = "table"


class Priority(Enum):
    """possible priority levels"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
