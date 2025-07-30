from _typeshed import Incomplete
from tlc.core.schema import ScalarValue as ScalarValue, Schema as Schema

logger: Incomplete

class SerializationVersionHelper:
    """A class with helper methods for working with Object/Schema versions"""
    @staticmethod
    def compare_versions(input_version: str, current_version: str) -> None:
        """Compare the input version to the current version of the."""
    @staticmethod
    def diff_schema(schema1: Schema, schema2: Schema, verbosity: int = 0) -> list[str]:
        """Returns the difference between two schemas.

        :param schema1: The first schema.
        :param schema2: The second schema.
        :return: The difference between the two schemas.
        """
    @staticmethod
    def diff_value(value1: ScalarValue, value2: ScalarValue, verbosity: int = 0) -> str | None:
        """Returns the difference between two ScalarValues as an optional readable string.

        :param value1: The first value.
        :param value2: The second value.
        :return: The difference between the two values.
        """
