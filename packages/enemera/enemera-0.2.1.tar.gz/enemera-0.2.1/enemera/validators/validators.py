"""
Validation functions for the Enemera API client.

This module provides utility functions for validating input parameters
and enforcing type safety throughout the API client. It includes support
for validating enum values, date formats, and file paths.
"""
import enum
import pathlib
from typing import Union, TypeVar, Type

from enemera.core.exceptions import ValidationError
from enemera.models.enums import Market, Area, Purpose

# Type variable for enum validation
T = TypeVar('T', bound=enum.Enum)


class MarketValidationError(ValidationError):
    """Exception raised when a market identifier is invalid.

    This exception is raised when an invalid market identifier is provided to
    functions that expect a valid Market enum value or string representation.

    Attributes:
        value: The invalid market value that was provided
        supported_markets: List of valid market identifiers
    """

    def __init__(self, value, supported_markets=None):
        """Initialize a new MarketValidationError.

        Args:
            value: The invalid value that was provided
            supported_markets: Optional list of valid market identifiers.
                If not provided, all values from the Market enum are used.
        """
        self.value = value
        self.supported_markets = supported_markets or [m.value for m in Market]
        message = f"Invalid market identifier: '{value}'. Supported markets are: {', '.join(self.supported_markets)}"
        super().__init__(message)


class AreaValidationError(ValidationError):
    """Exception raised when an area identifier is invalid.

    This exception is raised when an invalid area identifier is provided to
    functions that expect a valid Area enum value or string representation.

    Attributes:
        value: The invalid area value that was provided
        supported_areas: List of valid area identifiers
    """

    def __init__(self, value, supported_areas=None):
        """Initialize a new AreaValidationError.

        Args:
            value: The invalid value that was provided
            supported_areas: Optional list of valid area identifiers.
                If not provided, all values from the Area enum are used.
        """
        self.value = value
        self.supported_areas = supported_areas or [a.value for a in Area]
        message = f"Invalid area identifier: '{value}'. Supported areas are: {', '.join(self.supported_areas)}"
        super().__init__(message)


def validate_market(value: Union[str, Market]) -> Market:
    """
    Validate a market identifier and convert it to a Market enum.

    Args:
        value: Market identifier as string or Market enum

    Returns:
        Market: The validated Market enum

    Raises:
        MarketValidationError: If the market identifier is invalid
    """
    # If already a Market enum, return it
    if isinstance(value, Market):
        return value

    # If string, try to convert to Market enum
    if isinstance(value, str):

        # Try case-insensitive match
        for market in Market:
            if value.upper() == market.value.upper():
                return market

        # No match found
        raise MarketValidationError(value)

    # Not a valid type
    raise MarketValidationError(
        str(value),
        f"Market must be a string or Market enum, got {type(value).__name__}"
    )


def validate_area(value: Union[str, Area]) -> Area:
    """
    Validate an area identifier and convert it to an Area enum.

    Args:
        value: Area identifier as string or Area enum

    Returns:
        Area: The validated Area enum

    Raises:
        AreaValidationError: If the area identifier is invalid
    """
    # If already an Area enum, return it
    if isinstance(value, Area):
        return value

    # If string, try to convert to Area enum
    if isinstance(value, str):

        # Try case-insensitive match
        for area in Area:
            if value.upper() == area.value.upper():
                return area

        # No match found
        raise AreaValidationError(value)

    # Not a valid type
    raise AreaValidationError(
        str(value),
        f"Area must be a string or Area enum, got {type(value).__name__}"
    )


def validate_purpose(value: Union[str, Purpose]) -> Purpose:
    """
    Validate a purpose identifier and convert it to a Purpose enum.

    Args:
        value: Purpose identifier as string or Purpose enum
    Returns:
        Purpose: The validated Purpose enum
    Raises:
        ValidationError: If the purpose identifier is invalid
    """
    # If already a Purpose enum, return it
    if isinstance(value, Purpose):
        return value

    # If string, try to convert to Purpose enum
    if isinstance(value, str):
        # Try match with enum value
        for purpose in Purpose:
            if value.upper().strip() == purpose.value:
                return purpose

        # No match found
        raise ValidationError(
            f"Invalid Purpose value: '{value}'. "
            f"Supported values are: {', '.join([p.value for p in Purpose])}"
        )

    # Not a valid type
    raise ValidationError(
        f"Purpose must be a string or Purpose enum, got {type(value).__name__}"
    )


def validate_enum(value: Union[str, T], enum_class: Type[T]) -> T:
    """
    Generic function to validate an enum value.

    Args:
        value: Enum value as string or enum
        enum_class: The enum class to validate against

    Returns:
        T: The validated enum value

    Raises:
        ValidationError: If the value is invalid
    """
    # If already the correct enum type, return it
    if isinstance(value, enum_class):
        return value

    # If string, try to convert to enum
    if isinstance(value, str):
        # Try direct match with enum value
        for enum_value in enum_class:
            if value == enum_value.value:
                return enum_value

        # Try case-insensitive match
        for enum_value in enum_class:
            if value.upper() == enum_value.value.upper():
                return enum_value

        # No match found
        raise ValidationError(
            f"Invalid {enum_class.__name__} value: '{value}'. "
            f"Supported values are: {', '.join([e.value for e in enum_class])}"
        )

    # Not a valid type
    raise ValidationError(
        f"{enum_class.__name__} must be a string or {enum_class.__name__} enum, "
        f"got {type(value).__name__}"
    )


def validate_and_transform_areas(area: Union[str, Area, list[str], list[Area], None]) -> str:
    """
    Validate and transform area identifiers into a comma-separated string.
    :param area: area identifier(s) as string, Area enum, or list of strings/Area enums
    :return: string of comma-separated area identifiers
    """

    if area is not None:
        if isinstance(area, list):
            # Handle list of areas
            validated_areas = [validate_area(a) for a in area]
        elif isinstance(area, str):
            # Handle single area or comma-separated list
            if ',' in area:
                area_parts = str(area).split(',')
                validated_areas = [validate_area(
                    a.strip()) for a in area_parts]
            else:
                validated_areas = [validate_area(area)]
        elif isinstance(area, Area):
            # Handle Area enum
            validated_areas = [validate_area(area)]
        else:
            raise ValueError("Areas must be string or Area enum")

        # area_param
        area_param = ','.join([a.value for a in validated_areas])

        return area_param
    return None


def validate_filepath(filepath: Union[str, pathlib.Path], extension: str) -> pathlib.Path:
    """
    Validate filepath and ensure it has the correct extension.

    Args:
        filepath: Path to the output file
        extension: Expected file extension (e.g., '.csv', '.xlsx')

    Returns:
        Validated Path object

    Raises:
        ValueError: If filepath is invalid or has wrong extension
    """
    # Convert to Path object if string
    path = pathlib.Path(filepath)

    # Check if parent directory exists
    if not path.parent.exists():
        raise ValueError(f"Directory {path.parent} does not exist")

    # Check file extension
    if not path.name.lower().endswith(extension.lower()):
        raise ValueError(f"Filepath must have {extension} extension")

    return path
