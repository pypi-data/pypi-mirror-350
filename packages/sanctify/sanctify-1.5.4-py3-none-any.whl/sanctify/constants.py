# External Imports
import string
from enum import Enum, StrEnum, auto

import pandas as pd
from frozendict import frozendict


class PrimitiveDataTypes(StrEnum):
    """
    Enum representing primitive data types.
    """

    BOOLEAN = auto()
    FLOAT = auto()
    INTEGER = auto()
    STRING = auto()


class AbstractDataTypes(StrEnum):
    """
    Enum representing abstract data types.
    """

    TEXT = auto()
    DECIMAL = auto()
    EMAIL = auto()


class Constants(StrEnum):
    """
    Enum representing various constants.
    """

    STANDARD_COLUMN = auto()
    DATA_TYPE = auto()
    DATE_ORDER_TUPLE = auto()
    TRANSFORMATIONS = auto()
    VALIDATIONS = auto()
    POST_PROCESSING_DATA_TYPE = auto()
    COMPARISON_OPERATIONS = auto()
    IS_OPTIONAL = auto()
    COALESCE_CHILD_REQUIRED = auto()


class ComparisonOperations(StrEnum):
    """
    Enum representing comparison operations and their corresponding operators.
    """

    LESS_THAN = auto()
    LESS_THAN_OPERATOR = "<"
    LESS_THAN_EQUALS = auto()
    LESS_THAN_EQUALS_OPERATOR = "<="
    GREATER_THAN = auto()
    GREATER_THAN_OPERATOR = ">"
    GREATER_THAN_EQUALS = auto()
    GREATER_THAN_EQUALS_OPERATOR = ">="
    EQUALS = auto()
    EQUALS_OPERATOR = "=="
    NOT_EQUALS = auto()
    NOT_EQUALS_OPERATOR = "!="


class CalendarDateComponents(StrEnum):
    """
    Enum representing calendar date components.
    """

    DAY = auto()
    MONTH = auto()
    YEAR = auto()


class DateOrderTuples(Enum):
    """
    Enum representing different date orders.
    """

    DAY_MONTH_YEAR = (
        CalendarDateComponents.DAY.value,
        CalendarDateComponents.MONTH.value,
        CalendarDateComponents.YEAR.value,
    )
    MONTH_DAY_YEAR = (
        CalendarDateComponents.MONTH.value,
        CalendarDateComponents.DAY.value,
        CalendarDateComponents.YEAR.value,
    )
    YEAR_DAY_MONTH = (
        CalendarDateComponents.YEAR.value,
        CalendarDateComponents.DAY.value,
        CalendarDateComponents.MONTH.value,
    )
    YEAR_MONTH_DAY = (
        CalendarDateComponents.YEAR.value,
        CalendarDateComponents.MONTH.value,
        CalendarDateComponents.DAY.value,
    )


class DefaultColumns(StrEnum):
    """
    Enum representing default column names.
    """

    VALUE_PLACEHOLDER = "Value_Placeholder"
    ERROR = "Error"
    IS_ALLOWED = "Is_Allowed"
    REASON = "Reason"


# Create a translation table with all punctuation characters mapped to ''
STRING_TRANSLATION_TABLE = str.maketrans("", "", string.punctuation)

# Create a translation table with all digits characters mapped to ''
DIGIT_TRANSLATION_TABLE = str.maketrans("", "", string.digits)

PRIMITIVE_TO_NULLABLE_DATA_TYPE_MAP = frozendict(
    {
        int: pd.Int64Dtype(),
        float: pd.Float64Dtype(),
    }
)
