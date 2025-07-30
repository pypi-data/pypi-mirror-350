# External Imports
import ast
from datetime import date

from dateutil.relativedelta import relativedelta
from loguru import logger

# Internal Imports
from sanctify.constants import ComparisonOperations

COMPARISON_OPERATIONS_VS_FUNCTIONS_MAP = {
    ComparisonOperations.LESS_THAN.value: lambda x, y: x < y,
    ComparisonOperations.LESS_THAN_OPERATOR.value: lambda x, y: x < y,
    ComparisonOperations.LESS_THAN_EQUALS.value: lambda x, y: x <= y,
    ComparisonOperations.LESS_THAN_EQUALS_OPERATOR.value: lambda x, y: x <= y,
    ComparisonOperations.GREATER_THAN.value: lambda x, y: x > y,
    ComparisonOperations.GREATER_THAN_OPERATOR.value: lambda x, y: x > y,
    ComparisonOperations.GREATER_THAN_EQUALS.value: lambda x, y: x >= y,
    ComparisonOperations.GREATER_THAN_EQUALS_OPERATOR.value: lambda x, y: x >= y,
    ComparisonOperations.EQUALS.value: lambda x, y: x == y,
    ComparisonOperations.EQUALS_OPERATOR.value: lambda x, y: x == y,
    ComparisonOperations.NOT_EQUALS.value: lambda x, y: x != y,
    ComparisonOperations.NOT_EQUALS_OPERATOR.value: lambda x, y: x != y,
}


def replace_dict_keys(original_dict: dict, key_mapping: dict) -> dict:
    """
    Replace keys in a dictionary with the corresponding values from a key mapping dictionary.

    Args:
        original_dict (dict): Original dictionary.
        key_mapping (dict): Dictionary mapping old keys to new keys.

    Returns:
        dict: Dictionary with replaced keys.
    """
    return {key_mapping.get(key, key): value for key, value in original_dict.items()}


def match_comparision_operation(
    value, operation: str, operand: str | int
) -> bool | NotImplementedError | Exception | ValueError:
    """
    Perform a comparison operation between a value and an operand based on the specified operation.

    Args:
        value: Value to compare.
        operation (str): Comparison operation.
        operand (str|int): Operand for comparison.

    Returns:
        bool: Result of the comparison.

    Raises:
        NotImplementedError: If the operation is not supported.
        TypeError: If the comparison fails due to a type mismatch.
        Exception: If an unexpected exception occurs.
        ValueError: If the operation or operand is invalid.
    """
    err_message = f"{operation = } with {operand = } | DEBUG: {type(value) = }, {value = }"
    try:
        # Perform the comparison operation based on the provided operation

        if operation in COMPARISON_OPERATIONS_VS_FUNCTIONS_MAP:
            return COMPARISON_OPERATIONS_VS_FUNCTIONS_MAP[operation](value, operand)
        else:
            raise NotImplementedError(f"Unsupported Comparision: {err_message}")

    except TypeError as err:
        err = TypeError(f"System Error: {err_message}")
        logger.error(f"{str(err) = }")
        raise err


def calculate_age(date_of_birth: date, current_date: date = date.today()) -> int:
    """
    Calculate the age based on the date of birth.

    Args:
        date_of_birth (date): Date of birth.

    Returns:
        int: Calculated age.

    Notes:
        The age is calculated by subtracting the birth year from the current year,
        and adjusting for the birth month and day.

    Example:
        If the date of birth is '1990-05-15', and the current date is '2022-08-10',
        the calculated age will be 32.
    """
    return relativedelta(current_date, date_of_birth).years


def convert_tuples_to_lists(input_data):
    """
    Recursively converts tuples to lists in a nested dictionary.

    This function takes a nested data structure (dictionary, list, or tuple) as input
    and traverses through it recursively to find tuples. Whenever a tuple is found,
    it converts it into a list. The function handles nested dictionaries, lists, and tuples.

    Parameters:
        input_data (dict, list, tuple, or any): The nested data structure to process.

    Returns:
        The input data structure with tuples converted to lists.
    """
    if isinstance(input_data, dict):
        # If the input is a dictionary, process its key-value pairs recursively.
        return {key: convert_tuples_to_lists(value) for key, value in input_data.items()}
    elif isinstance(input_data, (tuple, list)):
        # If the input is a tuple or list, process its elements recursively.
        return [convert_tuples_to_lists(item) for item in input_data]
    else:
        # If the input is not a dictionary, tuple, or list, return it unchanged.
        return input_data


@staticmethod
def convert_stringified_list_to_list(value: str) -> list | str:
    """
    Converts a stringified list to a list.

    Args:
        value (str): The input string representing a list.

    Returns:
        list | str: The converted list if successful, otherwise the original string.

    """
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
