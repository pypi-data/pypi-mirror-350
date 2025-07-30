"""
Core functionality for cloneit package.

This module provides the main classes for field template registration
and cloning functionality.
"""

import copy
from typing import Any, Dict, List

from .exceptions import TemplateNotFoundError


class FieldTemplate:
    """
    A registry for field templates that can be cloned and reused.

    Inspired by the RPGLE LIKE keyword, this class allows you to register
    field definitions once and reuse them throughout your codebase.
    """

    _registry: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register(cls, name: str, attributes: Dict[str, Any]) -> None:
        """
        Register a field template with the given name and attributes.

        Args:
            name: The name of the template to register
            attributes: A dictionary of field attributes/properties

        Example:
            >>> FieldTemplate.register('email', {
            ...     'type': str,
            ...     'required': True,
            ...     'max_length': 255,
            ...     'validation': 'email'
            ... })
        """
        if not isinstance(name, str):
            raise TypeError("Template name must be a string")

        if not isinstance(attributes, dict):
            raise TypeError("Template attributes must be a dictionary")

        cls._registry[name] = copy.deepcopy(attributes)

    @classmethod
    def get(cls, name: str) -> Dict[str, Any]:
        """
        Get a registered field template by name.

        Args:
            name: The name of the template to retrieve

        Returns:
            A copy of the template attributes

        Raises:
            TemplateNotFoundError: If the template doesn't exist
        """
        if name not in cls._registry:
            raise TemplateNotFoundError(f"Template '{name}' not found")

        return copy.deepcopy(cls._registry[name])

    @classmethod
    def exists(cls, name: str) -> bool:
        """
        Check if a field template exists.

        Args:
            name: The name of the template to check

        Returns:
            True if the template exists, False otherwise
        """
        return name in cls._registry

    @classmethod
    def list(cls) -> List[str]:
        """
        List all registered field template names.

        Returns:
            A list of all registered template names
        """
        return list(cls._registry.keys())

    @classmethod
    def clear(cls) -> None:
        """
        Clear all registered templates.

        This is primarily useful for testing purposes.
        """
        cls._registry.clear()

    @classmethod
    def unregister(cls, name: str) -> bool:
        """
        Unregister a field template.

        Args:
            name: The name of the template to unregister

        Returns:
            True if the template was removed, False if it didn't exist
        """
        if name in cls._registry:
            del cls._registry[name]
            return True
        return False


class Field:
    """
    A utility class for cloning field templates with optional overrides.

    This class provides the main interface for creating fields based on
    registered templates, similar to using the LIKE keyword in RPGLE.
    """

    @staticmethod
    def like(template_name: str, **overrides: Any) -> Any:
        """
        Clone a field template with optional attribute overrides.

        This method retrieves a registered template and applies any provided
        overrides to create a customized field definition.

        Args:
            template_name: The name of the template to clone
            **overrides: Keyword arguments to override template attributes

        Returns:
            A field definition with the template attributes and overrides applied

        Raises:
            TemplateNotFoundError: If the template doesn't exist

        Example:
            >>> # Register a template
            >>> FieldTemplate.register('email', {
            ...     'type': str,
            ...     'required': True,
            ...     'max_length': 255
            ... })
            >>>
            >>> # Clone with overrides
            >>> user_email = Field.like('email')
            >>> optional_email = Field.like('email', required=False, default='')
        """
        # Get the base template
        template_attrs = FieldTemplate.get(template_name)

        # Apply overrides
        for key, value in overrides.items():
            template_attrs[key] = value

        # Handle different field creation patterns
        field_class = template_attrs.pop("field_class", None)

        if field_class is not None:
            # For framework-specific fields (Django, Marshmallow, etc.)
            return field_class(**template_attrs)
        else:
            # For generic field definitions or Pydantic-style fields
            return FieldDefinition(**template_attrs)


class FieldDefinition:
    """
    A generic field definition that holds field attributes.

    This class is used when no specific field_class is provided in the template,
    and serves as a container for field attributes that can be used with various
    frameworks or for general field definitions.
    """

    def __init__(self, **attributes: Any) -> None:
        """
        Initialize a field definition with the given attributes.

        Args:
            **attributes: Field attributes/properties
        """
        self.attributes = attributes

        # Set common attributes as direct properties for convenience
        for key, value in attributes.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        """Return a string representation of the field definition."""
        attrs_str = ", ".join(f"{k}={v!r}" for k, v in self.attributes.items())
        return f"FieldDefinition({attrs_str})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another FieldDefinition."""
        if not isinstance(other, FieldDefinition):
            return NotImplemented
        return self.attributes == other.attributes

    def get_attribute(self, name: str, default: Any = None) -> Any:
        """
        Get a field attribute by name.

        Args:
            name: The attribute name
            default: Default value if attribute doesn't exist

        Returns:
            The attribute value or default
        """
        return self.attributes.get(name, default)

    def set_attribute(self, name: str, value: Any) -> None:
        """
        Set a field attribute.

        Args:
            name: The attribute name
            value: The attribute value
        """
        self.attributes[name] = value
        setattr(self, name, value)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the field definition to a dictionary.

        Returns:
            A dictionary of field attributes
        """
        return copy.deepcopy(self.attributes)
