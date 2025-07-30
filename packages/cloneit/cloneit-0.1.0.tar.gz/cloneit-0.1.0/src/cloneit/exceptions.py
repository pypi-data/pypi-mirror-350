"""
Custom exceptions for the cloneit package.

This module defines specific exceptions that can be raised during
field template operations.
"""


class CloneItError(Exception):
    """
    Base exception class for all cloneit-related errors.

    This serves as the parent class for all custom exceptions
    in the cloneit package.
    """

    pass


class TemplateNotFoundError(CloneItError):
    """
    Raised when attempting to access a template that doesn't exist.

    This exception is raised when trying to clone a field template
    that hasn't been registered or has been removed from the registry.
    """

    pass


class InvalidTemplateError(CloneItError):
    """
    Raised when a template definition is invalid.

    This exception is raised when trying to register a template
    with invalid attributes or structure.
    """

    pass


class TemplateAlreadyExistsError(CloneItError):
    """
    Raised when attempting to register a template with a name that already exists.

    This exception can be used to prevent accidental overwriting of templates.
    """

    pass
