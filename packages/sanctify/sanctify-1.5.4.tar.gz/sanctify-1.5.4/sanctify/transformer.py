# External Imports
import re
from datetime import datetime

import phonenumbers
from dateutil import parser
from loguru import logger
from phonenumbers import is_valid_number, parse

# Internal Imports
from sanctify.constants import DIGIT_TRANSLATION_TABLE, STRING_TRANSLATION_TABLE, CalendarDateComponents
from sanctify.exception import ValidationError


class Transformer:
    @staticmethod
    def parse_boolean(value: str):
        """
        Parses a boolean value from a string.

        Args:
            value (str): The input string.

        Returns:
            bool: The parsed boolean value.

        Raises:
            ValidationError: If the input string is not a valid boolean.
        """
        bool_string = str(value).lower()
        if bool_string in {"true", "false"}:
            return str(value).lower() == "true"
        else:
            raise ValidationError(f"Invalid boolean input: {bool_string = }")

    @staticmethod
    def remove_dot_from_string(value: str) -> str:
        """
        Removes all dots from a string except for "jr." and "sr.".

        Args:
            value (str): The input string.

        Returns:
            str: The string with dots removed.
        """
        return str(value).replace(".", "")

    @staticmethod
    def remove_punctuations(value: str) -> str:
        """
        Removes all punctuations from a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with punctuations removed.
        """
        # Remove punctuation using the translation table
        return str(value).translate(STRING_TRANSLATION_TABLE)

    @staticmethod
    def remove_all_digits(value: str) -> str:
        """
        Removes all digits from a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with digits removed.
        """
        # Remove digits using the translation table
        return str(value).translate(DIGIT_TRANSLATION_TABLE)

    @staticmethod
    def remove_punctuations_and_leading_zeroes_except_plus(value: str) -> str:
        """
        Removes all characters from a string except for digits and the plus sign.
        Strips leading zeroes from the resulting string, while preserving the plus sign if it exists.

        Args:
            value (str): The input string from which punctuations and leading zeroes need to be removed.

        Returns:
            str: The resulting string after removing punctuations and leading zeroes, with the plus sign preserved if it exists.
        """
        # Remove all characters except digits and plus sign, then strip leading zeroes
        cleaned_value = re.sub(r"[^\d+]", "", str(value))
        # Check if the string starts with a plus sign
        if cleaned_value.startswith("+"):
            # Preserve the plus sign, remove leading zeroes after the plus sign
            return "+" + cleaned_value[1:].lstrip("0")
        else:
            # If there's no plus sign, simply remove leading zeroes
            return cleaned_value.lstrip("0")

    @staticmethod
    def remove_all_spaces(value: str) -> str:
        """
        Removes all spaces from a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with spaces removed.
        """
        return re.sub(r"\s", "", str(value))

    @staticmethod
    def convert_to_lowercase(value: str) -> str:
        """
        Converts a string to lowercase.

        Args:
            value (str): The input string.

        Returns:
            str: The lowercase string.
        """
        return str(value).lower()

    @staticmethod
    def convert_to_uppercase(value: str) -> str:
        """
        Converts a string to uppercase.

        Args:
            value (str): The input string.

        Returns:
            str: The uppercase string.
        """
        return str(value).upper()

    @staticmethod
    def convert_to_titlecase(value: str) -> str:
        """
        Converts a string to titlecase.

        Args:
            value (str): The input string.

        Returns:
            str: The titlecase string.
        """
        return str(value).title()

    @staticmethod
    def replace_ii_with_II(value: str) -> str:
        """
        Replaces "ii","iI","Ii","II" with "II" in a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with "ii" replaced by "II".
        """
        return re.sub(r"\b[iI]{2}\b", "II", str(value))

    @staticmethod
    def convert_jr_to_Junior(value: str) -> str:
        """
        Replaces "jr., Jr." with "Junior." in a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with "jr." replaced by "Junior.".
        """
        return re.sub(r"\b[Jj]r\.", "Junior ", str(value))

    @staticmethod
    def convert_sr_to_Senior(value: str) -> str:
        """
        Replaces "sr., Sr." with "Senior." in a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string with "sr." replaced by "Senior.".
        """
        return re.sub(r"\b[Ss]r\.", "Senior ", str(value))

    @staticmethod
    def parse_date_from_string(
        value: str, date_order_tuple: tuple, return_datetime: bool = False
    ) -> str | datetime | NotImplementedError | parser.ParserError:
        """
        Parses a date from a string using a specified date order.

        Args:
            value (str): The input string representing the date.
            date_order_tuple (tuple): The tuple specifying the order of date components (day, month, year).
            return_datetime (bool, optional): Whether to return a datetime object instead of a string date.
                Defaults to False.

        Returns:
            str | datetime: The parsed date as a string or datetime object.

        Raises:
            NotImplementedError: If the date order tuple is invalid.
            parser.ParserError: If the input string cannot be parsed as a date.
        """
        logger.debug(f"In parse_date_from_string received: {value = } | {date_order_tuple = }")
        error_message = f"({type(value)}, {value}) | {date_order_tuple = } | {return_datetime = }"

        try:
            value = str(value)
            day_first = date_order_tuple.index(CalendarDateComponents.DAY.value) < date_order_tuple.index(
                CalendarDateComponents.MONTH.value
            )
            year_first = date_order_tuple.index(CalendarDateComponents.YEAR.value) < date_order_tuple.index(
                CalendarDateComponents.MONTH.value
            )
        except ValueError as value_err:
            err = NotImplementedError(f"Invalid `date_order` tuple | {date_order_tuple = } | {value_err = }")
            logger.exception(f"{str(err) = }")
            raise err

        try:
            parsed_datetime = parser.parse(value, dayfirst=day_first, yearfirst=year_first)
        except parser.ParserError as err:
            logger.exception(f"{str(err) = } | DEBUG: {error_message}")
            raise ValidationError(f"Invalid date passed: {str(err)}")
        else:
            if return_datetime is True:
                return parsed_datetime
            else:
                return str(parsed_datetime.date())

    @staticmethod
    def extract_digits_from_string(value: str):
        """
        Extracts only the digits from a string.

        Args:
            value (str): The input string.

        Returns:
            str: The string containing only the digits.
        """
        return re.sub(r"\D", "", str(value))

    @staticmethod
    def extract_currency_from_amount(value: str) -> str:
        """
        Extracts the currency symbol from an amount string.

        Args:
            value (str): The input amount string.

        Returns:
            str: The extracted currency symbol.
        """
        match = re.search(r"[^\d.,\s]+", str(value))
        if match:
            return match.group()
        else:
            return ""

    @staticmethod
    def remove_currency_from_amount(value: str) -> str | ValidationError:
        """
        Removes currency symbols and separators from an amount string.

        Args:
            value (str): The input amount string.

        Returns:
            str: The amount string with currency symbols and separators removed.
            ValidationError: if amount is invalid or negative
        """
        # Use regex to remove everything except digits, decimal point, and minus sign
        _amount = re.sub(r"[^\d.-]", "", str(value))

        try:
            amount = float(_amount)
            if amount > 0:
                return str(amount)
            else:
                raise ValidationError(f"Amount {str(amount)} should not be negative")

        except ValueError:
            raise ValidationError(f"Failed to parse amount {str(_amount)}")

    @staticmethod
    def transform_str_into_phone_number_obj(
        value: str, region: str | None = "US"
    ) -> phonenumbers.PhoneNumber | ValidationError:
        """
        Transforms a phone number string into phone number object.

        Args:
            value (str): The phone number string from which the phone number object needs to be extracted.
            region (str | default = "US"): Here are some examples of valid country codes you can use as the region parameter:
                'US': United States
                'GB': United Kingdom
                'CA': Canada
                'AU': Australia
                'JP': Japan
                'DE': Germany
                You can find a comprehensive list of country codes in the ISO 3166-1 standard documentation.

        Returns:
            phonenumbers.PhoneNumber | ValidationError: The extracted phone number object, or a ValidationError if the phone number is invalid.

        Raises:
            ValidationError: If the phone number is invalid or cannot be parsed.
        """
        try:
            err_msg = f"Invalid/Fake phone_number = '{value}'"
            cleaned_number = Transformer.remove_punctuations_and_leading_zeroes_except_plus(value=value)
            parsed_number = parse(number=cleaned_number, region=region)
            if not is_valid_number(numobj=parsed_number):
                raise ValidationError(err_msg)

            return parsed_number

        except phonenumbers.NumberParseException:
            # Raise an error if the phone number is invalid
            raise ValidationError(err_msg)

        except Exception as err:
            raise ValidationError(f"Failed to Parse Phone Number '{value}' | {str(err)}")

    @staticmethod
    def extract_phone_number(value: str, region: str | None = "US") -> str | ValidationError:
        """
        Extracts the national phone number from a phone number string.

        Args:
            value (str): The phone number string from which the national phone number needs to be extracted.
            region (str | default = "US"): Here are some examples of valid country codes you can use as the region parameter:
                'US': United States
                'GB': United Kingdom
                'CA': Canada
                'AU': Australia
                'JP': Japan
                'DE': Germany
                You can find a comprehensive list of country codes in the ISO 3166-1 standard documentation.

        Returns:
            str | ValidationError: The extracted national phone number as a string, or a ValidationError if the phone number is invalid.
        """
        parsed_number: phonenumbers.PhoneNumber = Transformer.transform_str_into_phone_number_obj(
            value=value, region=region
        )
        return str(parsed_number.national_number)

    @staticmethod
    def extract_country_code(value: str, region: str | None = "US") -> str | ValidationError:
        """
        Extracts the country code from a phone number string.

        Args:
            value (str): The phone number string from which the country code needs to be extracted.
            region (str | default = "US"): Here are some examples of valid country codes you can use as the region parameter:
                'US': United States
                'GB': United Kingdom
                'CA': Canada
                'AU': Australia
                'JP': Japan
                'DE': Germany
                You can find a comprehensive list of country codes in the ISO 3166-1 standard documentation.

        Returns:
            str | ValidationError: The extracted country code as a string, or a ValidationError if the phone number is invalid.
        """
        parsed_number: phonenumbers.PhoneNumber = Transformer.transform_str_into_phone_number_obj(
            value=value, region=region
        )
        return str(parsed_number.country_code)
