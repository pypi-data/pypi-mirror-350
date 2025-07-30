# External Imports
import inspect
import json
from typing import Any

# Internal Imports
from sanctify.exception import SerializationError
from sanctify.transformer import Transformer
from sanctify.validator import Validator


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON Encoder class to handle serialization of custom objects and built-in types."""

    def default(self, obj) -> dict | Any:
        """
        Override the default method of JSONEncoder to handle custom object serialization.

        Args:
            obj (Any): The object to be serialized.

        Returns:
            dict | Any: A JSON-serializable representation of the object.
        """
        # Handle built-in types (int, str, float, bool) separately
        if isinstance(obj, type) and obj in {int, str, float, bool}:
            return {
                "builtin_module_name": obj.__name__,
            }

        # Handle callable objects (methods/functions) like Transformer and Validator
        if callable(obj):
            class_name, _, static_method_name = obj.__qualname__.partition(".")
            if class_name in {Transformer.__name__, Validator.__name__}:
                return {
                    "class_name": class_name,
                    "static_method_name": static_method_name,
                    "static_method_args": list(inspect.signature(obj).parameters.keys()),
                }
        return super().default(obj)


class CustomJSONDecoder(json.JSONDecoder):
    """Custom JSON Decoder class to handle deserialization of custom objects and built-in types."""

    def __init__(self, *args, **kwargs):
        """
        Initialize the CustomJSONDecoder object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        """
        Custom object hook to handle deserialization of custom objects.

        Args:
            dct (dict): The JSON dictionary.

        Returns:
            Any: The deserialized object.
        """
        # Handle built-in types (int, str, float, bool) separately
        if "builtin_module_name" in dct:
            return __builtins__[dct["builtin_module_name"]]

        # Handle callable objects (methods/functions) like Transformer and Validator
        if "static_method_name" in dct and "class_name" in dct:
            static_method_name: str = dct["static_method_name"]
            class_name: str = dct["class_name"]

            if class_name == Transformer.__name__:
                return getattr(Transformer, static_method_name)
            elif class_name == Validator.__name__:
                return getattr(Validator, static_method_name)

        return dct


class SchemaSerializer:
    """Serializer class to serialize the data into JSON format."""

    def __init__(self, data) -> None:
        """
        Initialize the SchemaSerializer object.

        Args:
            data (Any): The data to be serialized.
        """
        self.__data = data

    @property
    def data(self):
        """
        Property to get the serialized JSON data.

        Returns:
            str: The serialized JSON data.
        """
        try:
            return json.dumps(self.__data, cls=CustomJSONEncoder)
        except Exception as err:
            raise SerializationError(f"Failed to Serialize | Error: {str(err)}")


class SchemaDeSerializer:
    """Deserializer class to deserialize the JSON data."""

    def __init__(self, data) -> None:
        """
        Initialize the SchemaDeSerializer object.

        Args:
            data (str): The JSON data to be deserialized.
        """
        self.__data = data

    @property
    def data(self):
        """
        Property to get the deserialized data.

        Returns:
            Any: The deserialized data.
        """
        try:
            return json.loads(self.__data, cls=CustomJSONDecoder)
        except Exception as err:
            raise SerializationError(f"Failed to DeSerialize | Error: {str(err)}")
