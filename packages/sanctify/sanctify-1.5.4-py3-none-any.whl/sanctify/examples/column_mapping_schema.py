# Internal Imports
from sanctify.constants import Constants, DateOrderTuples
from sanctify.transformer import Transformer
from sanctify.validator import Validator

EXAMPLE_COLUMN_MAPPING = {  # NOTE: Make sure that this  doesn't change during processing
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
                {Constants.DATE_ORDER_TUPLE.value: DateOrderTuples.YEAR_MONTH_DAY.value},  # Can be changed with strings
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
