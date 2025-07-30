# Sanctify [![codecov](https://codecov.io/gh/skit-ai/sanctify/branch/main/graph/badge.svg?token=WZHSY8T8SC)](https://codecov.io/gh/skit-ai/sanctify)

Sanctify is a Python package designed to facilitate data cleansing and validation operations on pandas DataFrames. It provides a set of predefined transformations and validations that can be applied to different columns of a DataFrame based on a column mapping. The package allows you to define data types, transformations, and validations for each column, making it easy to clean and validate your data.

## Features

- Cleansing and validation of data in pandas DataFrames.
- Support for custom transformations and validations.
- Configurable column mapping to define data types and operations for each column.
- Built-in transformations for common data cleaning tasks.
- Validation functions for common data validation checks.
- Flexibility to handle various data types and formats.
- Ability to handle missing or malformed data gracefully.

## Installation

You can install Sanctify using pip:

```shell
pip install sanctify
```

## Basic Usage

```python
import pandas as pd

from sanctify import Cleanser, Transformer, Validator, process_cleansed_df

###
# The package provides a few built in enums for ease of use
# You can always choose to opt of the below import and use hardcoded strings
from sanctify.constants import Constants, DateOrderTuples

###
from sanctify.processor import process_cleansed_df
from sanctify.transformer import Transformer
from sanctify.validator import Validator

# Suppose You have the List of the standard sheet/csv column headers
# NOTE: By default every cell value is treated as string data type
# Eg. ['Account', 'State', 'Phone', 'First Name', 'Last Name', 'Zip Code', 'DOB', 'Latest Due Date', 'Latest Due Amount', 'SSN']
# The below dictionary represents the mapping of the Input Column Vs the Standard Column in your system
COLUMN_MAPPING = {  # NOTE: Make sure that this  doesn't change during processing
    "DOB": {
        Constants.STANDARD_COLUMN.value: "Date of Birth",
        Constants.VALIDATIONS.value: [
            (
                Validator.validate_date_of_birth,
                {
                    "date_order_tuple": (
                        "year",
                        "month",
                        "day",
                    )  # Date Validations Require Date order tuples | See sanctify.constants.DateOrderTuples
                },
            )
        ],
    },
    "Cell Phone": {
        Constants.STANDARD_COLUMN.value: "Dial Number",
        Constants.VALIDATIONS.value: [
            (
                Validator.validate_phone_number_with_optional_country_code_check,
                {"country_code_equals": 1},
            )
        ],
    },
    "Zip": {
        Constants.STANDARD_COLUMN.value: "Zip Code",
        Constants.VALIDATIONS.value: [Validator.validate_us_zip_code],
    },
    "State": {
        Constants.STANDARD_COLUMN.value: "State",
        Constants.TRANSFORMATIONS.value: [Transformer.remove_punctuations],
    },
    "SSN#": {
        Constants.STANDARD_COLUMN.value: "SSN",
        Constants.VALIDATIONS.value: [Validator.validate_ssn],
    },
    "Account Due Date": {
        Constants.STANDARD_COLUMN.value: "Due Date",
        Constants.VALIDATIONS.value: [
            (
                Validator.validate_due_date,
                {
                    Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value  # Can be changed with strings
                },
            )
        ],
    },
    "Due Amount": {
        Constants.STANDARD_COLUMN.value: "Amount",
        Constants.TRANSFORMATIONS.value: [
            Transformer.remove_currency_from_amount,
        ],
    },
    "Customer Number": {
        Constants.STANDARD_COLUMN.value: "Account",
        Constants.TRANSFORMATIONS.value: [
            Transformer.remove_punctuations,
        ],
    },
}


def cleanse_and_validate_df_with_column_mapping_only(
    input_file_path: str,
    cleansed_output_file_path: str,
    processed_output_file_path: str,
    cleansed_processed_output_file_path: str,
) -> None | Exception:
    # Step 2: Read the CSV data
    input_df = pd.read_csv(input_file_path, dtype=str)

    # Step 3: Perform cleansing operations
    cleanser = Cleanser(df=input_df, column_mapping_schema=COLUMN_MAPPING)
    _ = cleanser.remove_trailing_spaces_from_column_headers()
    _ = cleanser.drop_unmapped_columns()
    _ = cleanser.drop_fully_empty_rows()
    _ = cleanser.remove_trailing_spaces_from_each_cell_value()
    _, updated_column_mapping_schema = cleanser.replace_column_headers()

    # Step 3.1: Extract the cleansed df as csv
    cleanser.df.to_csv(cleansed_output_file_path, index=False)

    # Step 4: Run Transformations and Validations as defined in the column mapping above
    # NOTE: This step adds the column 'Error' into the df
    processed_df = process_cleansed_df(
        df=cleanser.df,
        column_mapping_schema=updated_column_mapping_schema,
        ignore_optional_columns=False,
    )
    # Step 4.1: Extract the processed df as csv
    processed_df.to_csv(processed_output_file_path, index=False)

    # Optional Step 5: Mark duplicate rows via a subset of columns
    cleanser = Cleanser(df=processed_df, column_mapping_=COLUMN_MAPPING)
    # Mark rows with duplicate values while keeping first occurence
    _ = cleanser.mark_all_duplicates(
        columns=["Dial Number"],
    )

    # Optional Step 6: Drop all rows that have the Error column populated or in essence which failed validations
    _ = cleanser.modify_error_column_to_set_all_except_mandatory_to_blank()
    _ = cleanser.drop_rows_with_errors(inplace=True)

    # Alternatively
    # ignore_columns_list = cleanser.get_optional_column_names_from_column_mapping()
    # cleanser.drop_rows_with_errors(inplace=True, ignore_columns_list=ignore_columns_list)

    # Optional Step 7: Extract the final df as csv
    cleanser.df.to_csv(cleansed_processed_output_file_path, index=False)


if __name__ == "__main__":
    # Step 1: Define file paths
    input_file_path = "<path to>/input.csv"
    cleansed_output_file_path = "<path to>/CLEANSED_input.csv"
    processed_output_file_path = "<path to>/PROCESSED_input.csv"
    cleansed_processed_output_file_path = "<path to>/CLEANSED_PROCESSED_input.csv"

    # Trigger
    cleanse_and_validate_df_with_column_mapping_only(
        input_file_path=input_file_path,
        cleansed_output_file_path=cleansed_output_file_path,
        processed_output_file_path=processed_output_file_path,
        cleansed_processed_output_file_path=cleansed_processed_output_file_path,
    )
```

## Advanced Usage

```python
import pandas as pd

from sanctify import Cleanser, Transformer, Validator, process_cleansed_df

###
# The package provides a few built in enums for ease of use
# You can always choose to opt of the below import and use hardcoded strings
from sanctify.constants import ComparisonOperations, Constants, DateOrderTuples

###
from sanctify.processor import process_cleansed_df
from sanctify.transformer import Transformer
from sanctify.validator import Validator

# Suppose You have the List of the standard sheet/csv column headers
# Eg. ['Account', 'State', 'Phone', 'First Name', 'Last Name', 'Zip Code', 'DOB', 'Latest Due Date', 'Latest Due Amount', 'SSN']
# You can define your own Custom Data Types as shown in below examples
# Dictionary representing data type
DATA_TYPE_SCHEMA = {
    "ACCOUNT": {
        Constants.TRANSFORMATIONS.value: [
            Transformer.remove_punctuations,
        ],
    },
    "NAME": {
        Constants.TRANSFORMATIONS.value: [
            Transformer.convert_to_lowercase,
            Transformer.replace_ii_with_II,
            Transformer.convert_jr_to_Junior,
            Transformer.convert_sr_to_Senior,
            Transformer.remove_dot_from_string,
        ],
    },
    "DOB": {
        Constants.VALIDATIONS.value: [
            (
                Validator.validate_age,
                {
                    Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value,
                    Constants.COMPARISON_OPERATIONS.value: {
                        ComparisonOperations.GREATER_THAN_EQUALS.value: 18
                    },
                },
            )
        ],
    },
    "DUE_DATE": {
        Constants.VALIDATIONS.value: [
            (
                Validator.validate_due_date,
                {
                    Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value,
                    "comparison_operations": {"<=": 20, ">": 1},
                },
            )
        ],
    },
    "DATE": {
        Constants.TRANSFORMATIONS.value: [
            (
                Transformer.parse_date_from_string,
                {
                    Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value
                },
            )
        ],
    },
    "PHONE": {
        Constants.TRANSFORMATIONS.value: [Transformer.extract_phone_number],
    },
    "AMOUNT": {
        Constants.TRANSFORMATIONS.value: [
            Transformer.remove_currency_from_amount,
        ],
    },
    "SSN": {Constants.TRANSFORMATIONS.value: [Transformer.remove_punctuations]},
    "ZIP_CODE": {Constants.VALIDATIONS.value: [Validator.validate_us_zip_code]},
    "STATE": {Constants.TRANSFORMATIONS.value: [Transformer.remove_punctuations]},
}

# AND use the Data Types Defined above in your column mapping
# The below dictionary represents the mapping of the Input Column Vs the Standard Column in your system with its Data type
COLUMN_MAPPING = {  # NOTE: Make sure that this  doesn't change during processing
    "DOB": {
        Constants.STANDARD_COLUMN.value: "Date of Birth",
        Constants.DATA_TYPE.value: "DOB",
    },
    "Cell Phone": {"standard_column": "Dial Number", "data_type": "PHONE"},
    "Zip": {Constants.STANDARD_COLUMN.value: "Zip Code", "data_type": "ZIP_CODE"},
    "State": {Constants.STANDARD_COLUMN.value: "State", "data_type": "STATE"},
    "SSN#": {Constants.STANDARD_COLUMN.value: "SSN", "data_type": "SSN"},
    "Account Due Date": {
        Constants.STANDARD_COLUMN.value: "Due Date",
        Constants.DATA_TYPE.value: "DUE_DATE",
    },
    "Due Amount": {
        Constants.STANDARD_COLUMN.value: "Amount",
        Constants.DATA_TYPE.value: "AMOUNT",
    },
    "Customer Number": {
        Constants.STANDARD_COLUMN.value: "Account",
        Constants.DATA_TYPE.value: "ACCOUNT",
    },
}


def cleanse_and_validate(
    input_file_path: str,
    cleansed_output_file_path: str,
    processed_output_file_path: str,
    cleansed_processed_output_file_path: str,
) -> None | Exception:
    # Step 2: Read the CSV data
    input_df = pd.read_csv(input_file_path, dtype=str)

    # Step 3: Perform cleansing operations
    cleanser = Cleanser(df=input_df, column_mapping_schema=COLUMN_MAPPING)
    _ = cleanser.remove_trailing_spaces_from_column_headers()
    _ = cleanser.drop_unmapped_columns()
    _ = cleanser.drop_fully_empty_rows()
    _ = cleanser.remove_trailing_spaces_from_each_cell_value()
    _, updated_column_mapping_schema = cleanser.replace_column_headers()

    # Step 3.1: Extract the cleansed df as csv
    cleanser.df.to_csv(cleansed_output_file_path, index=False)

    # Step 4: Run Transformations and Validations as defined in the column mapping above
    # NOTE: This step adds the column 'Error' into the df
    processed_df = process_cleansed_df(
        df=cleanser.df,
        column_mapping_schema=updated_column_mapping_schema,
        data_type_=DATA_TYPE_SCHEMA,
        ignore_optional_columns=False,
    )
    # Step 4.1: Extract the processed df as csv
    processed_df.to_csv(processed_output_file_path, index=False)

    # Optional Step 5: Mark duplicate rows via a subset of columns
    cleanser = Cleanser(df=processed_df, column_mapping_=COLUMN_MAPPING)
    # Mark rows with duplicate values while keeping first occurence
    _ = cleanser.mark_all_duplicates(
        columns=["Dial Number"],
    )

    # Optional Step 6: Drop all rows that have the Error column populated or in essence which failed validations
    _ = cleanser.modify_error_column_to_set_all_except_mandatory_to_blank()
    _ = cleanser.drop_rows_with_errors(inplace=True)

    # Alternatively
    # ignore_columns_list = cleanser.get_optional_column_names_from_column_mapping()
    # cleanser.drop_rows_with_errors(inplace=True, ignore_columns_list=ignore_columns_list)

    # Optional Step 7: Extract the final df as csv
    cleanser.df.to_csv(cleansed_processed_output_file_path, index=False)


if __name__ == "__main__":
    # Step 1: Define file paths
    input_file_path = "<path to>/input.csv"
    cleansed_output_file_path = "<path to>/CLEANSED_input.csv"
    processed_output_file_path = "<path to>/PROCESSED_input.csv"
    cleansed_processed_output_file_path = "<path to>/CLEANSED_PROCESSED_input.csv"

    cleanse_and_validate(
        input_file_path=input_file_path,
        cleansed_output_file_path=cleansed_output_file_path,
        processed_output_file_path=processed_output_file_path,
        cleansed_processed_output_file_path=cleansed_processed_output_file_path,
    )
```

## Additional Classes: SchemaSerializer and SchemaDeSerializer

Sanctify provides two additional classes to facilitate data serialization and deserialization to/from JSON format. These classes are **SchemaSerializer** and **SchemaDeSerializer**.

### SchemaSerializer

The **SchemaSerializer** class is used to serialize data into JSON format. It takes the data to be serialized as input and provides the serialized JSON data as output.

#### Usage

```python
from sanctify.serializer import SchemaSerializer
from sanctify.transformer import Transformer

data_to_serialize = {
    "first_name": {
        "standard_column": "First Name",
        "transformations": [
            Transformer.convert_to_lowercase,
            Transformer.replace_ii_with_II,
            Transformer.convert_jr_to_Junior,
            Transformer.convert_sr_to_Senior,
            Transformer.remove_dot_from_string,
        ],
    },
}

# Serialize the data
serializer = SchemaSerializer(data_to_serialize)
serialized_data = serializer.data

print(serialized_data)
# Output:
"""
{
    "first_name": {
        "standard_column": "First Name",
        "transformations": [
            {
                "class_name": "Transformer",
                "static_method_name": "convert_to_lowercase",
                "static_method_args": [
                    "value"
                ]
            },
            {
                "class_name": "Transformer",
                "static_method_name": "replace_ii_with_II",
                "static_method_args": [
                    "value"
                ]
            },
            {
                "class_name": "Transformer",
                "static_method_name": "convert_jr_to_Junior",
                "static_method_args": [
                    "value"
                ]
            },
            {
                "class_name": "Transformer",
                "static_method_name": "convert_sr_to_Senior",
                "static_method_args": [
                    "value"
                ]
            },
            {
                "class_name": "Transformer",
                "static_method_name": "remove_dot_from_string",
                "static_method_args": [
                    "value"
                ]
            }
        ]
    }
}
"""
```

### SchemaDeSerializer

The **SchemaDeSerializer** class is used to deserialize JSON data back into Python data structures. It takes the JSON data as input and provides the deserialized data as output.

#### Usage

```python
from sanctify.serializer import SchemaDeSerializer
from sanctify.transformer import Transformer

serialized_data = """
{
    "first_name": {
        "standard_column": "First Name",
        "transformations": [
            {
                "class_name": "Transformer",
                "static_method_name": "convert_to_lowercase",
                "static_method_args": [
                    "value"
                ]
            },
            {
                "class_name": "Transformer",
                "static_method_name": "replace_ii_with_II",
                "static_method_args": [
                    "value"
                ]
            },
            {
                "class_name": "Transformer",
                "static_method_name": "convert_jr_to_Junior",
                "static_method_args": [
                    "value"
                ]
            },
            {
                "class_name": "Transformer",
                "static_method_name": "convert_sr_to_Senior",
                "static_method_args": [
                    "value"
                ]
            },
            {
                "class_name": "Transformer",
                "static_method_name": "remove_dot_from_string",
                "static_method_args": [
                    "value"
                ]
            }
        ]
    }
}
"""

# Deserialize the data
deserializer = SchemaDeSerializer(serialized_data)
deserialized_data = deserializer.data

print(deserialized_data)
# Output:
"""
{
    "first_name": {
        "standard_column": "First Name",
        "transformations": [
            Transformer.convert_to_lowercase,
            Transformer.replace_ii_with_II,
            Transformer.convert_jr_to_Junior,
            Transformer.convert_sr_to_Senior,
            Transformer.remove_dot_from_string,
        ],
    },
}
"""
```

## Contributing

Contributions to Sanctify are welcome! If you find any bugs, have feature requests, or want to contribute code, please open an issue or submit a pull request on the [GitHub repository](https://github.com/skit-ai/sanctify/).

Before starting: Make sure to create a python3.11 virtual env install the pre-commit hook

```shell
python3.11 -m venv venv && source venv/bin/activate && pip install pre-commit && pre-commit install
```
