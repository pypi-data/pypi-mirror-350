# External Imports
from typing import Callable

import pandas as pd
from frozendict import frozendict
from loguru import logger

# Internal Imports
from sanctify.constants import (
    PRIMITIVE_TO_NULLABLE_DATA_TYPE_MAP,
    AbstractDataTypes,
    Constants,
    DefaultColumns,
    PrimitiveDataTypes,
)
from sanctify.transformer import Transformer
from sanctify.validator import Validator

PRIMITIVE_DATA_TYPE_VS_TRANSFORMATIONS = {
    PrimitiveDataTypes.BOOLEAN.value: [Transformer.parse_boolean],
    PrimitiveDataTypes.FLOAT.value: [float],
    AbstractDataTypes.DECIMAL.value: [float],
    PrimitiveDataTypes.INTEGER.value: [int],
    PrimitiveDataTypes.STRING.value: [str],
    AbstractDataTypes.TEXT.value: [str],
}


def handle_additional_transformations_and_validations(
    data_type_name_for_column: str,
) -> list[Callable]:
    """
    Handles additional transformations and validations based on the data type name for a column.

    Args:
        data_type_name_for_column (str): Data type name for the column.

    Returns:
        list[Callable]: List of transformation functions to apply.
        []: Empty List if data type do not match
    """
    return PRIMITIVE_DATA_TYPE_VS_TRANSFORMATIONS.get(data_type_name_for_column, [])


def handle_data_type(data_type_schema: dict[str:dict], col_config: dict) -> tuple[list[Callable], list[Callable]]:
    """
    Handles data type transformations and validations for a column.

    Args:
        data_type_schema (dict[str: dict]): Data type schema containing data type configurations.
        col_config (dict): Column configuration.

    Returns:
        tuple[list[Callable], list[Callable]]: List of transformation functions and list of validation functions.
    """
    transformations, validations = [], []
    if Constants.DATA_TYPE.value in col_config:
        data_type_name_for_column: str = col_config[Constants.DATA_TYPE.value]
        transformations += handle_additional_transformations_and_validations(
            data_type_name_for_column=data_type_name_for_column
        )
        data_type_config_for_column: dict = data_type_schema.get(data_type_name_for_column, {})
        transformations += data_type_config_for_column.get(Constants.TRANSFORMATIONS, [])
        validations += data_type_config_for_column.get(Constants.VALIDATIONS, [])

    return transformations, validations


def process_nullable_or_post_processing_dtype(series: pd.Series, dtype) -> pd.Series:
    """
    Process a pandas Series by inferring the object data type, filling missing values with 0,
    and converting the data type to the specified dtype.

    Args:
        series (pd.Series): The pandas Series to be processed.
        dtype: The desired data type for the Series.

    Returns:
        pd.Series: The processed pandas Series with the specified data type.
    """
    processed_series = series.infer_objects().fillna(0).astype(dtype, errors="ignore")
    return processed_series


def handle_date_order_tuple(col_config) -> tuple[list[Callable], list[Callable]]:
    """
    Handles date order transformations for a column.

    Args:
        col_config (dict): Column configuration.

    Returns:
        tuple[list[Callable], list[Callable]]: List of transformation functions and list of validation functions.
    """
    transformations, validations = [], []
    if Constants.DATE_ORDER_TUPLE.value in col_config:
        date_order_tuple = col_config[Constants.DATE_ORDER_TUPLE.value]
        transformations = [
            (
                Transformer.parse_date_from_string,
                {Constants.DATE_ORDER_TUPLE.value: date_order_tuple},
            )
        ]

    return transformations, validations


def handle_comparison_operation(col_config) -> tuple[list[Callable], list[Callable]]:
    """
    Handles comparison operation validations for a column.

    Args:
        col_config (dict): Column configuration.

    Returns:
        tuple[list[Callable], list[Callable]]: List of transformation functions and list of validation functions.
    """
    transformations, validations = [], []
    if Constants.COMPARISON_OPERATIONS.value in col_config:
        comparison_operations = col_config[Constants.COMPARISON_OPERATIONS.value]
        validations = [
            (
                Validator.validate_comparison_operations,
                {"comparison_operations": comparison_operations},
            )
        ]

    return transformations, validations


def handle_transformations(col_config) -> tuple[list[Callable], list[Callable]]:
    """
    Handles general transformations for a column.

    Args:
        col_config (dict): Column configuration.

    Returns:
        tuple[list[Callable], list[Callable]]: List of transformation functions and list of validation functions.
    """
    transformations, validations = [], []
    if Constants.TRANSFORMATIONS.value in col_config:
        transformations = col_config[Constants.TRANSFORMATIONS.value]

    return transformations, validations


def handle_validations(col_config) -> tuple[list[Callable], list[Callable]]:
    """
    Handles validations for a column.

    Args:
        col_config (dict): Column configuration.

    Returns:
        tuple[list[Callable], list[Callable]]: List of transformation functions and list of validation functions.
    """
    transformations, validations = [], []
    if Constants.VALIDATIONS.value in col_config:
        validations = col_config[Constants.VALIDATIONS.value]

    return transformations, validations


def handle_post_processing_dtype(col_config: dict, data_type_schema: dict) -> Callable or None:
    """
    Handles post-validation transformations for a column.

    Args:
        col_config (dict): Column configuration containing column-specific settings.
        data_type_schema (dict): A schema containing data types and their configurations.

    Returns:
        Callable or None: If post-validation transformation is applicable for int or float,
        it returns the corresponding transformation function. Otherwise, it returns None.
    """

    result = None

    # Check if the column configuration contains a post-processing data type
    if Constants.POST_PROCESSING_DATA_TYPE.value in col_config:
        pp_datatype = col_config.get(Constants.POST_PROCESSING_DATA_TYPE.value)
        # Get the corresponding post-validation transformation function from the mapping
        result = PRIMITIVE_TO_NULLABLE_DATA_TYPE_MAP.get(pp_datatype, None)

    # Check if the column configuration refers to a predefined data type in the schema
    if Constants.DATA_TYPE.value in col_config:
        data_type_name_for_column: str = col_config.get(Constants.DATA_TYPE.value, None)
        if data_type_name_for_column is not None:
            # Retrieve the configuration for the specified data type from the schema
            data_type_config_for_column: dict = data_type_schema.get(data_type_name_for_column, {})
            # Check if the data type configuration contains a post-processing data type
            if Constants.POST_PROCESSING_DATA_TYPE.value in data_type_config_for_column:
                pp_datatype = data_type_config_for_column.get(Constants.POST_PROCESSING_DATA_TYPE.value)
                # Get the corresponding post-validation transformation function from the mapping
                result = PRIMITIVE_TO_NULLABLE_DATA_TYPE_MAP.get(pp_datatype, None)

    return result


def apply_functions(cell_value: str, col_name: str, functions: list[Callable | tuple[Callable, dict]], is_optional: bool = False) -> pd.Series:
    """
    Applies a series of transformation and validation functions to a value.

    Args:
        value: The value to apply the functions to.
        functions (list[Callable]): List of transformation and validation functions.
        functions (tuple[Callable, dict]]): List of tuple of transformation and validation functions and additional kwargs.
        is_optional (bool): Whether this column is optional. If True, no error messages will be generated.

    Returns:
        pd.Series: Series containing the modified value and error message (if any).
    """
    final_cell_value = cell_value
    error_message = None

    if not cell_value or cell_value == "nan":  # All possible absent value cases
        if not is_optional:
            error_message = f"{col_name} is required"

    else:
        for function in functions:
            func = function
            kwargs = {}

            if isinstance(function, (list, tuple)):
                func = function[0]
                kwargs = function[1]

            logger.debug(f"Running {func.__name__ = } on {col_name} containing {cell_value = } with {kwargs = }")

            try:
                final_cell_value = func(final_cell_value, **kwargs)

            except Exception as err:
                logger.error(f"FAILED: {func.__name__ = } on {cell_value = } with {kwargs = } | ERROR: {(str(err)) = }")
                if not is_optional:
                    error_message = f"{col_name} with {cell_value = } got error = {str(err)}"
                # Reset the cell_value on failure
                final_cell_value = cell_value
                break

            if final_cell_value in {"", "nan"}:
                str_err = "Cleansed value is empty"
                logger.error(f"FAILED: {func.__name__ = } on {cell_value = } with {kwargs = } | ERROR: {str_err}")
                if not is_optional:
                    error_message = f"{col_name} with {cell_value = } got error = {str_err}"
                # Reset the cell_value on failure
                final_cell_value = cell_value
                break

            logger.debug(
                f"Result: {func.__name__ = } on {col_name} containing {cell_value = } with {kwargs = } | {final_cell_value = }"
            )

    # Return the modified value and error message (if any)
    return pd.Series(
        [final_cell_value, error_message],
        index=[DefaultColumns.VALUE_PLACEHOLDER.value, DefaultColumns.ERROR.value],
    )


def process_cleansed_df(
    df: pd.DataFrame,
    column_mapping_schema: frozendict = {},
    data_type_schema: frozendict = {},
    ignore_optional_columns: bool = False,
) -> pd.DataFrame:
    """
    Processes the cleansed DataFrame by applying transformations and validations based on the column mapping and data type schema.

    Args:
        df (pd.DataFrame): The cleansed DataFrame.
        column_mapping_schema (frozendict): Column mapping schema.
        data_type_schema (frozendict): Data type schema.
        ignore_optional_columns (bool): Flag indicating whether to ignore optional columns when applying transformations and validations.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    if column_mapping_schema == {}:
        return df

    # Create an "Error" column in the DataFrame to track errors, if it does not exists
    if DefaultColumns.ERROR.value not in df.columns:
        df[DefaultColumns.ERROR.value] = ""

    # Iterate over each column in column_mapping_schema
    for col_name, col_config in column_mapping_schema.items():
        logger.debug(f"{col_name = } | {col_config = }")

        # If a column is marked optional and ignore_optional_columns is True,
        # then ignore any transformation or validation on that column
        is_optional_column = col_config.get(Constants.IS_OPTIONAL.value, False)
        if ignore_optional_columns is True and is_optional_column is True:
            continue

        # Check if col_name in column mapping schema exists in df
        col_name_in_df_columns = col_name in df.columns
        if col_name_in_df_columns is False:
            logger.error(f"Column({col_name}) with doesn't exist in the input dataframe | {col_config = }")
            # Continue to next column in the column mapping schema
            continue

        if col_config == {}:
            logger.error(f"Column({col_name})'s column config not provided in the input dataframe | {col_config = }")
            # Continue to next column in the column mapping schema
            continue  # Skip empty config items
        else:
            logger.debug(f"Parsing Column({col_name}) as str dtype | {col_config = }")
            # Convert column rows to string data type
            df[col_name] = df[col_name].astype(str)

        transformations, validations = [], []

        d_type_transformations, d_type_validations = handle_data_type(data_type_schema, col_config)
        d_order_transformations, d_order_validations = handle_date_order_tuple(col_config)
        (
            comparison_op_transformations,
            comparison_op_validations,
        ) = handle_comparison_operation(col_config)
        col_transformations, _ = handle_transformations(col_config)
        _, col_validations = handle_validations(col_config)
        post_processing_dtype = handle_post_processing_dtype(col_config=col_config, data_type_schema=data_type_schema)

        transformations += (
            d_type_transformations + d_order_transformations + comparison_op_transformations + col_transformations
        )
        validations += d_type_validations + d_order_validations + comparison_op_validations + col_validations

        # Apply transformations and validations on the column
        logger.debug(f"Running {col_name}: {transformations = }")
        logger.debug(f"Running {col_name}: {validations = }")

        data_type_name_for_column: str = col_config.get(Constants.DATA_TYPE.value)
        primitive_data_type_classes = handle_additional_transformations_and_validations(
            data_type_name_for_column=data_type_name_for_column
        )
        applied_series: pd.Series = df[col_name].apply(
            apply_functions, col_name=col_name, functions=transformations + validations, is_optional=is_optional_column
        )

        # Update cell values
        successful_rows = applied_series[DefaultColumns.ERROR.value].isnull()
        df.loc[successful_rows, col_name] = applied_series.loc[successful_rows, DefaultColumns.VALUE_PLACEHOLDER.value]

        # Update "Error" column for errored rows
        errored_rows = applied_series[DefaultColumns.ERROR.value].notnull()
        if errored_rows.sum() > 0:
            df.loc[errored_rows, col_name] = applied_series.loc[errored_rows, DefaultColumns.VALUE_PLACEHOLDER.value]
            df.loc[errored_rows, DefaultColumns.ERROR.value] += (
                " | " + applied_series.loc[errored_rows, DefaultColumns.ERROR.value]
            )

        if len(primitive_data_type_classes) == 1:
            primitive_data_type_class = primitive_data_type_classes[0]
            if primitive_data_type_class in PRIMITIVE_TO_NULLABLE_DATA_TYPE_MAP:
                nullable_dtype = PRIMITIVE_TO_NULLABLE_DATA_TYPE_MAP[primitive_data_type_class]
                df[col_name] = process_nullable_or_post_processing_dtype(series=df[col_name], dtype=nullable_dtype)
                logger.debug(f"Converting the column {col_name} back to {nullable_dtype} data type")

        if post_processing_dtype is not None:
            logger.debug(f"Converting the column {col_name} to {post_processing_dtype} data type")
            df[col_name] = process_nullable_or_post_processing_dtype(series=df[col_name], dtype=post_processing_dtype)

    return df
