# External Imports
from typing import Any

from email_validator import EmailNotValidError, EmailUndeliverableError, ValidatedEmail, validate_email
from loguru import logger

# Internal Imports
from sanctify.constants import ComparisonOperations
from sanctify.exception import ValidationError
from sanctify.transformer import Transformer
from sanctify.utils import calculate_age, match_comparision_operation


class Validator:
    SSN_VALIDATION_ERROR_MSG = "Should be 4 digits"

    @staticmethod
    def validate_comparison_operations(value: Any, comparison_operations: dict[str: int | None]) -> Any | Exception:
        """
        Validate a value against a set of comparison operations.

        Args:
            value: The value to be validated.
            comparison_operations: A dictionary of comparison operations and their operands.

        Returns:
            The validated value if all comparison operations pass.

        Raises:
            ValidationError: If any comparison operation fails.
        """
        result = True
        for operation, operand in comparison_operations.items():
            result = result and match_comparision_operation(value=value, operation=operation, operand=operand)

        if result is True:
            return value
        else:
            raise ValidationError(f"Comparison Failed for {comparison_operations = }")

    @staticmethod
    def validate_age(
        value: str | int,
        date_order_tuple: tuple,
        comparison_operations: dict[str:int],
    ) -> str | Exception:
        """
        Validate the age based on comparison operations.

        Args:
            value: The value representing a date.
            date_order_tuple: A tuple specifying the order of year, month, and day in the date.
            comparison_operations: A dictionary of comparison operations and their operands.

        Returns:
            The validated date value if all comparison operations pass.

        Raises:
            ValidationError: If any comparison operation fails.
        """
        parsed_datetime = Transformer.parse_date_from_string(
            value=value, date_order_tuple=date_order_tuple, return_datetime=True
        )
        age = calculate_age(date_of_birth=parsed_datetime.date())

        if age < 0:
            raise ValidationError(f"Given date {str(parsed_datetime.date())} is in the future by {abs(age)} years")

        # Raises err on validation failure
        _ = Validator.validate_comparison_operations(value=age, comparison_operations=comparison_operations)

        return str(parsed_datetime.date())

    @staticmethod
    def validate_date_of_birth(
        value: str | int,
        date_order_tuple: tuple,
    ) -> str | Exception:
        """
        Validate the age based on comparison operations.

        Args:
            value: The value representing the date of birth.
            date_order_tuple: A tuple specifying the order of year, month, and day in the date.

        Returns:
            The validated date of birth date if it is valid

        Raises:
            ValidationError: If any comparison operation fails.
        """
        parsed_datetime = Transformer.parse_date_from_string(
            value=value, date_order_tuple=date_order_tuple, return_datetime=True
        )
        age = calculate_age(date_of_birth=parsed_datetime.date())

        if age < 0:
            raise ValidationError("Should not be in the future")

        try:
            # Raises err on validation failure
            _ = Validator.validate_comparison_operations(
                value=age,
                comparison_operations={
                    ComparisonOperations.GREATER_THAN_EQUALS.value: 18,
                    ComparisonOperations.LESS_THAN_EQUALS.value: 100,
                },
            )
        except ValidationError:
            raise ValidationError("Age should be >=18 and <=100")

        return str(parsed_datetime.date())

    @staticmethod
    def validate_due_date(
        value: str | int,
        date_order_tuple: tuple,
        comparison_operations: dict[str: int | None] = None,
    ) -> str | Exception:
        """
        Validate the due date based on comparison operations.

        Args:
            value: The value representing a date.
            date_order_tuple: A tuple specifying the order of year, month, and day in the date.
            comparison_operations: A dictionary of comparison operations and their operands.

        Returns:
            The validated due date if it is valid

        Raises:
            ValidationError: If any comparison operation fails.
        """
        parsed_datetime = Transformer.parse_date_from_string(
            value=value, date_order_tuple=date_order_tuple, return_datetime=True
        )
        age = calculate_age(date_of_birth=parsed_datetime.date())

        if age > 0:
            return str(parsed_datetime.date())
        else:
            age = abs(age)
            if isinstance(comparison_operations, dict):
                # Raises err on validation failure
                _ = Validator.validate_comparison_operations(value=age, comparison_operations=comparison_operations)
            else:
                try:
                    # Raises err on validation failure
                    _ = Validator.validate_comparison_operations(
                        value=age,
                        comparison_operations={
                            ComparisonOperations.LESS_THAN_EQUALS.value: 10,
                        },
                    )

                except ValidationError:
                    raise ValidationError("Should not be greater than 10 years")

            return str(parsed_datetime.date())

    @staticmethod
    def validate_email(
        value: str, check_deliverability: bool = False
    ) -> str | EmailNotValidError | EmailUndeliverableError | Exception:
        """
        Validate an email address.

        Args:
            value: The email address to be validated.
            check_deliverability: Boolean flag indicating whether to check email deliverability.

        Returns:
            The normalized and validated email address.

        Raises:
            ValidationError: If the email is not valid or undeliverable.
            Exception: If an unexpected exception occurs.
        """
        try:
            validated_email: ValidatedEmail = validate_email(email=value, check_deliverability=check_deliverability)
            return validated_email.normalized

        except (EmailNotValidError, EmailUndeliverableError) as err:
            # The email is not valid or undeliverable, handle the exception
            logger.exception(f"{str(err) = }")

            raise ValidationError(f"Invalid Email: {str(err)}")

    @staticmethod
    def validate_length_of_string(value: str, length: int):
        """
        Validate the length of a string.

        Args:
            value: The string to be validated.
            length: The expected length of the string.

        Returns:
            The validated string length.

        Raises:
            ValidationError: If the string length is not equal to the expected length.
        """
        return Validator.validate_comparison_operations(
            value=len(str(value)),
            comparison_operations={ComparisonOperations.EQUALS.value: length},
        )

    @staticmethod
    def validate_ssn(value: str):
        """
        Validate a Social Security Number (SSN).

        Args:
            value: The SSN to be validated.

        Returns:
            The validated SSN.

        Raises:
            ValidationError: If the SSN is not valid.
        """
        # Extract the ssn
        digits_only = Transformer.extract_digits_from_string(value=value)

        # Validate based on the number of digits
        if len(digits_only) < 4:
            raise ValidationError(Validator.SSN_VALIDATION_ERROR_MSG)
        else:
            # Take last 4
            return digits_only[-4:]

    @staticmethod
    def validate_zip_code(value: str):
        """
        **DEPRECATION NOTICE**
        **It is recommended to use the validate_us_zip_code to validate a United States Zip Code**
        **This method will be removed / overridden in the future in case of a different region based requirement**

        Validate a zip code.

        Args:
            value: The zip code to be validated.

        Returns:
            The validated zip code.

        Raises:
            ValidationError: If the zip code does not have 5 digits.
        """
        # Extract the zip code
        digits_only = Transformer.extract_digits_from_string(value=value)

        # Validate based on the number of digits
        if len(digits_only) < 5:
            raise ValidationError(f"ZipCode({digits_only}) does not have 5 digits (Actual: {len(digits_only)})")
        else:
            return digits_only[:5]

    @staticmethod
    def validate_us_zip_code(value: str):
        """
        Validates a United States zip code.

        Args:
            value: The US zip code to be validated.

        Returns:
            The validated US zip code.

        Raises:
            ValidationError: If the US zip code does not have 5 digits.
        """
        # Extract the zip code
        digits_only = Transformer.extract_digits_from_string(value=value)

        # Validate based on the number of digits
        if len(digits_only) < 5:
            raise ValidationError(f"US ZipCode({digits_only}) does not have 5 digits (Actual: {len(digits_only)})")
        else:
            return digits_only[:5]

    @staticmethod
    def validate_country_code(value: str, comparison_operations: dict, region: str | None = "US"):
        """
        Validate a country code in a given phone number.

        Args:
            value: The phone number whose country code to be validated.
            comparison_operations: eg. = 91 or < 10
            region (str | default = "US"): Here are some examples of valid country codes you can use as the region parameter:
                'US': United States
                'GB': United Kingdom
                'CA': Canada
                'AU': Australia
                'JP': Japan
                'DE': Germany
                You can find a comprehensive list of country codes in the ISO 3166-1 standard documentation.

        Returns:
            The validated country code integer.

        Raises:
            ValidationError: If phone number is invalid or comparison_operations fails
        """
        country_code = Transformer.extract_country_code(value=value, region=region)
        return Validator.validate_comparison_operations(value=country_code, comparison_operations=comparison_operations)

    @staticmethod
    def validate_phone_number(value: str, region: str | None = "US") -> str | ValidationError:
        """
        Validate a phone number.

        Args:
            value (str): The phone number to be validated.
            region (str | default = "US"): Here are some examples of valid country codes you can use as the region parameter:
                'US': United States
                'GB': United Kingdom
                'CA': Canada
                'AU': Australia
                'JP': Japan
                'DE': Germany
                You can find a comprehensive list of country codes in the ISO 3166-1 standard documentation.

        Returns:
            str | ValidationError: The validated phone number if it is valid.

        Raises:
            ValidationError: If the phone number is not valid.
        """
        return Transformer.extract_phone_number(value=value, region=region)

    @staticmethod
    def validate_phone_number_with_optional_country_code_check(
        value: str,
        region: str | None = "US",
        country_code_equals: int | str | None = None,
    ) -> str | ValidationError:
        """
        Validate a phone number with an optional country code check.

        Args:
            value (str): The phone number to be validated.
            region (str | default = "US"): Here are some examples of valid country codes you can use as the region parameter:
                'US': United States
                'GB': United Kingdom
                'CA': Canada
                'AU': Australia
                'JP': Japan
                'DE': Germany
                You can find a comprehensive list of country codes in the ISO 3166-1 standard documentation.
            country_code_equals (int | str | None, optional): The expected country code. Defaults to None.

        Returns:
            str | ValidationError: The validated phone number if the country code check passes.

        Raises:
            ValidationError: If the country code check fails.

        """
        parsed_number = Transformer.transform_str_into_phone_number_obj(value=value, region=region)

        if country_code_equals is not None and str(parsed_number.country_code) != str(country_code_equals):
            raise ValidationError(f"Country Code for {value} do not match {country_code_equals}")

        return str(parsed_number.national_number)
