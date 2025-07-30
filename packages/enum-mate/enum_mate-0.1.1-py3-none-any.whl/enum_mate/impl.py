# -*- coding: utf-8 -*-

"""
Enhanced Python Enum implementation with explicit API for validation and retrieval.

This module provides improved enum classes that extend Python's built-in enum functionality
with convenient methods for getting enum members by name or value, along with validation
utilities. The classes are designed to be drop-in replacements for standard int and str
enums while providing additional safety and convenience methods.
"""

import typing as T
import enum


class EnumMixin:
    """
    Base mixin class providing common utility methods for enhanced enum classes.

    This mixin provides name-based operations that are common to all enum types,
    including retrieval by name, name validation, and name listing functionality.

    .. important::

        Both enum member names and values must be unique within the same enum class.
    """

    @classmethod
    def get_by_name(cls, name: str):
        """
        Get the enum member by its name.

        :param name: The name of the enum member to retrieve

        :return: The enum member object

        :raises KeyError: If the name is not a valid enum member name

        Example:
        >>> class MyEnum(BetterIntEnum):
        ...     VALUE_ONE = 1
        >>> MyEnum.get_by_name("VALUE_ONE")
        <MyEnum.VALUE_ONE: 1>
        """
        try:
            return cls[name]
        except KeyError as e:
            raise KeyError(
                f"Invalid `class {cls.__module__}.{cls.__name__}` member name: {name!r}"
            ) from e

    @classmethod
    def is_valid_name(cls, name: str) -> bool:
        """
        Check if the given name is a valid enum member name.

        :param name: The name to validate

        :return: True if the name is valid, False otherwise

        Example:
        >>> class MyEnum(BetterIntEnum):
        ...     VALUE_ONE = 1
        >>> MyEnum.is_valid_name("VALUE_ONE")
        True
        >>> MyEnum.is_valid_name("INVALID")
        False
        """
        try:
            _ = cls[name]
            return True
        except KeyError:
            return False

    @classmethod
    def get_names(cls) -> T.List[str]:
        """
        Get a list of all enum member names.

        :return: List of all enum member names

        Example:
            >>> class MyEnum(BetterIntEnum):
            ...     VALUE_ONE = 1
            ...     VALUE_TWO = 2
            >>> MyEnum.get_names()
            ['VALUE_ONE', 'VALUE_TWO']
        """
        return [i.name for i in cls]


class BetterIntEnum(EnumMixin, int, enum.Enum):
    """
    Enhanced integer enum with explicit API for validation and retrieval operations.

    Example:

    .. code-block:: python

        >>> class CodeEnum(BetterIntEnum):
        ...     succeeded = 1
        ...     failed = 0
        >>> CodeEnum.get_by_name("succeeded")
        <CodeEnum.succeeded: 1>
        >>> CodeEnum.get_by_value(1)
        <CodeEnum.succeeded: 1>
        >>> CodeEnum.is_valid_name("succeeded")
        True
        >>> CodeEnum.is_valid_name("SUCCEEDED")
        False
        >>> CodeEnum.is_valid_name(1)
        False
        >>> CodeEnum.is_valid_value("succeeded")
        False
        >>> CodeEnum.is_valid_value("SUCCEEDED")
        False
        >>> CodeEnum.is_valid_value(1)
        True
        >>> CodeEnum.ensure_is_valid_value(1)
        >>> CodeEnum.ensure_is_valid_value("succeeded")
        Traceback (most recent call last):
        ...
        ValueError: Invalid CodeEnum: 'succeeded'
        >>> CodeEnum.ensure_int(1)
        1
        >>> CodeEnum.ensure_int(CodeEnum.succeeded)
        1
        >>> isinstance(CodeEnum.ensure_int(1), int)
        True

    .. important::

        Both enum member names and values must be unique within the same enum class.
    """

    @classmethod
    def get_by_value(cls, value: int):
        """
        Get the enum member by its integer value.

        :param value: The integer value of the enum member to retrieve

        :return: The enum member object

        :raises ValueError: If the value is not a valid enum member value

        Example:
        >>> class StatusCode(BetterIntEnum):
        ...     SUCCESS = 200
        >>> StatusCode.get_by_value(200)
        <StatusCode.SUCCESS: 200>
        """
        return cls(value)

    @classmethod
    def is_valid_value(cls, value: int) -> bool:
        """
        Check if the given integer value is a valid enum member value.

        :param value: The integer value to validate

        :return: True if the value is valid, False otherwise

        Example:
        >>> class StatusCode(BetterIntEnum):
        ...     SUCCESS = 200
        >>> StatusCode.is_valid_value(200)
        True
        >>> StatusCode.is_valid_value(999)
        False
        """
        try:
            _ = cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def ensure_is_valid_value(cls, value):
        """
        Ensure the given value is a valid enum member value.

        This method performs validation and raises an exception if the value
        is not valid, making it useful for input validation scenarios.

        :param value: The value to validate

        :raises ValueError: If the value is not a valid enum member value

        Example:
        >>> class StatusCode(BetterIntEnum):
        ...     SUCCESS = 200
        >>> StatusCode.ensure_is_valid_value(200)  # No exception
        >>> StatusCode.ensure_is_valid_value(999)  # Raises ValueError
        Traceback (most recent call last):
        ...
        ValueError: Invalid StatusCode: 999
        """
        if cls.is_valid_value(value) is False:
            raise ValueError(
                f"Invalid `class {cls.__module__}.{cls.__name__}`: {value!r}"
            )

    @classmethod
    def ensure_int(cls, value: T.Union[int, "BetterIntEnum"]) -> int:
        """
        Ensure the value is converted to its integer representation.

        This method accepts either an integer value or an enum object and returns
        the corresponding integer value, with validation to ensure it's a valid
        enum member value.

        :param value: Either an integer value or an enum object

        :return: The integer value of the enum member

        :raises ValueError: If the value is not a valid enum member value

        Example:
        >>> class StatusCode(BetterIntEnum):
        ...     SUCCESS = 200
        >>> StatusCode.ensure_int(200)
        200
        >>> StatusCode.ensure_int(StatusCode.SUCCESS)
        200
        >>> isinstance(StatusCode.ensure_int(StatusCode.SUCCESS), int)
        True
        """
        if isinstance(value, cls):
            return value.value
        else:
            return cls(value).value

    @classmethod
    def get_values(cls) -> T.List[int]:
        """
        Get a list of all enum member integer values.

        :return: List of all enum member integer values

        Example:
        >>> class StatusCode(BetterIntEnum):
        ...     SUCCESS = 200
        ...     NOT_FOUND = 404
        >>> StatusCode.get_values()
        [200, 404]
        """
        return [i.value for i in cls]


class BetterStrEnum(EnumMixin, str, enum.Enum):
    """
    Enhanced string enum with explicit API for validation and retrieval operations.

    Example:

    .. code-block:: python

        >>> class StatusEnum(BetterStrEnum):
        ...     succeeded = "SUCCEEDED"
        ...     failed = "FAILED"
        >>> StatusEnum.get_by_name("succeeded")
        <StatusEnum.succeeded: 'SUCCEEDED'>
        >>> StatusEnum.get_by_value("SUCCEEDED")
        <StatusEnum.succeeded: 'SUCCEEDED'>
        >>> StatusEnum.is_valid_name("succeeded")
        True
        >>> StatusEnum.is_valid_name("SUCCEEDED")
        False
        >>> StatusEnum.is_valid_value("succeeded")
        False
        >>> StatusEnum.is_valid_value("SUCCEEDED")
        True
        >>> StatusEnum.ensure_is_valid_value("SUCCEEDED")
        >>> StatusEnum.ensure_is_valid_value("succeeded")
        Traceback (most recent call last):
        ...
        ValueError: Invalid StatusEnum: 'succeeded'
        >>> StatusEnum.ensure_str("SUCCEEDED")
        'SUCCEEDED'
        >>> StatusEnum.ensure_str(StatusEnum.succeeded)
        'SUCCEEDED'
        >>> isinstance(StatusEnum.ensure_str("SUCCEEDED"), str)
        True

    .. important::

        Both enum member names and values must be unique within the same enum class.
    """

    @classmethod
    def get_by_value(cls, value: str):
        """
        Get the enum member by its string value.

        :param value: The string value of the enum member to retrieve

        :return: The enum member object

        :raises ValueError: If the value is not a valid enum member value

        Example:
        >>> class Environment(BetterStrEnum):
        ...     DEVELOPMENT = "dev"
        >>> Environment.get_by_value("dev")
        <Environment.DEVELOPMENT: 'dev'>
        """
        return cls(value)

    @classmethod
    def is_valid_value(cls, value: str) -> bool:
        """
        Check if the given string value is a valid enum member value.

        :param value: The string value to validate

        :return: True if the value is valid, False otherwise

        Example:
        >>> class Environment(BetterStrEnum):
        ...     DEVELOPMENT = "dev"
        >>> Environment.is_valid_value("dev")
        True
        >>> Environment.is_valid_value("invalid")
        False
        """
        try:
            _ = cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def ensure_is_valid_value(cls, value):
        """
        Ensure the given value is a valid enum member value.

        This method performs validation and raises an exception if the value
        is not valid, making it useful for input validation scenarios.

        :param value: The value to validate

        :raises ValueError: If the value is not a valid enum member value

        Example:
        >>> class Environment(BetterStrEnum):
        ...     DEVELOPMENT = "dev"
        >>> Environment.ensure_is_valid_value("dev")  # No exception
        >>> Environment.ensure_is_valid_value("invalid")  # Raises ValueError
        Traceback (most recent call last):
        ...
        ValueError: Invalid Environment: 'invalid'
        """
        if cls.is_valid_value(value) is False:
            raise ValueError(
                f"Invalid `class {cls.__module__}.{cls.__name__}`: {value!r}"
            )

    @classmethod
    def ensure_str(cls, value: T.Union[str, "BetterStrEnum"]) -> str:
        """
        Ensure the value is converted to its string representation.

        This method accepts either a string value or an enum object and returns
        the corresponding string value, with validation to ensure it's a valid
        enum member value.

        :param value: Either a string value or an enum object
        :type value: Union[str, BetterStrEnum]

        :return: The string value of the enum member
        :rtype: str

        :raises ValueError: If the value is not a valid enum member value

        Example:
        >>> class Environment(BetterStrEnum):
        ...     DEVELOPMENT = "dev"
        >>> Environment.ensure_str("dev")
        'dev'
        >>> Environment.ensure_str(Environment.DEVELOPMENT)
        'dev'
        >>> isinstance(Environment.ensure_str(Environment.DEVELOPMENT), str)
        True
        """
        if isinstance(value, cls):
            return value.value
        else:
            return cls(value).value

    @classmethod
    def get_values(cls) -> T.List[str]:
        """
        Get a list of all enum member string values.

        :return: List of all enum member string values

        Example:
        >>> class Environment(BetterStrEnum):
        ...     DEVELOPMENT = "dev"
        ...     PRODUCTION = "prod"
        >>> Environment.get_values()
        ['dev', 'prod']
        """
        return [i.value for i in cls]
