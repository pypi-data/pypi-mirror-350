# Internal Imports
from sanctify.constants import ComparisonOperations, Constants, DateOrderTuples
from sanctify.transformer import Transformer
from sanctify.validator import Validator

EXAMPLE_DATA_TYPE_SCHEMA = {
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
            Transformer.remove_punctuations,
            Transformer.remove_all_digits,
        ],
    },
    "DOB": {
        Constants.VALIDATIONS.value: [
            (
                Validator.validate_age,
                {
                    Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value,
                    Constants.COMPARISON_OPERATIONS.value: {ComparisonOperations.GREATER_THAN_EQUALS.value: 18},
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
                {Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value},
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
EXAMPLE_COLUMN_MAPPING_USING_DATA_TYPE = {  # NOTE: Make sure that this  doesn't change during processing
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
