# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial implementation of cloneit package
- FieldTemplate class for template registration and management
- Field class for template cloning with overrides
- FieldDefinition class for generic field definitions
- Comprehensive test suite with pytest
- Framework integration examples (Pydantic, Django, Marshmallow, etc.)
- Documentation and usage examples
- MIT license
- PyPI package configuration

### Features
- Template registration with validation
- Field cloning with attribute overrides
- Framework-agnostic design
- Support for field_class attribute for framework-specific fields
- Error handling with custom exceptions
- Template management (list, exists, unregister, clear)
- Deep copying of templates to prevent mutations

## [1.0.0] - 2025-05-25

### Added
- Initial release of cloneit
- Core functionality inspired by RPGLE LIKE keyword
- Basic field template registration and cloning
- Support for Python 3.6+
- Comprehensive documentation and examples
