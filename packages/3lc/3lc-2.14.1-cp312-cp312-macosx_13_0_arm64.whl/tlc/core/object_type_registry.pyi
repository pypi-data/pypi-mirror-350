from _typeshed import Incomplete
from tlc.core.object import Object as Object
from typing import Any

class NotRegisteredError(Exception):
    """Exception raised when a type or component is not registered."""
    type_name: Incomplete
    message: Incomplete
    def __init__(self, type_name: str) -> None: ...

class MalformedContentError(ValueError):
    """Exception raised when a serialized object does not contain expected attributes."""
    missing_attribute: Incomplete
    message: Incomplete
    def __init__(self, missing_attribute: str) -> None: ...

class ObjectTypeRegistry:
    '''A class which maintains a global list of registered 3LC object types.

    This list is used e.g. when a JSON string containing a \'type\' property needs
    to be mapped to a create_object() method on a particular class.

    Note that the registry also contains abstract types like "Table" in order to
    deduce inheritance and order between types.
    '''
    @staticmethod
    def register_object_type(obj_type: type[Object]) -> None:
        """
        Register a 3LC object type (i.e. a class derived from Object) so that it
        can be mapped to a 'type' property found within a JSON structure.

        This way, instances of the class can be instantiated from JSON strings
        as needed.
        """
    @staticmethod
    def get_object_type_from_type_name(type_name: str) -> type[Object] | None:
        """
        Get 3LC object type from type name.

        :param type_name: The type name to look up
        :return: The object type if found, otherwise None
        :raises NotRegisteredError: If the type name is not registered
        """
    @staticmethod
    def print_object_types(line_prefix: str = '') -> None:
        """
        Print all object types. OlaFixme! Print class hierarchy recursively
        """
    @staticmethod
    def is_type_registered(_type_name: str) -> bool:
        """Reports whether a type name is registered in the system

        Only registered types can be instantiated"""
    @staticmethod
    def is_type_derived_from(_type: str, _base_type: str) -> bool:
        """
        Reports whether an object type is derived from another

        Raises if the type strings are not possible to resolve into registered types
        """
    @staticmethod
    def get_object_type_from_content(content: Any) -> type[Object] | None:
        '''Returns the object type for the given content.

        Tries to look up the type name in the content, and if that fails, tries to infer if the table has the required
        properties set so that it can be served as an "opaque" table. This requires that the table has a row-cache set
        and is fully defined.


        :param content: A dictionary containing the properties of an object.
        :returns: The object type for the given content.
        '''
