# Examples

This directory contains practical examples demonstrating how to use cloneit with various frameworks and scenarios.

## Files

### basic_usage.py
Demonstrates fundamental cloneit concepts:
- Template registration and cloning
- Field attribute overrides
- Error handling
- Template management
- FieldDefinition usage
- Real-world scenarios

### framework_examples.py  
Shows integration with popular Python frameworks:
- Pydantic models
- Django models (pseudo-code)
- Marshmallow schemas
- SQLAlchemy models (pseudo-code)
- WTForms (pseudo-code)
- Advanced template patterns

## Running the Examples

```bash
# Run basic usage examples
python examples/basic_usage.py

# Run framework integration examples
python examples/framework_examples.py
```

## Installation Requirements

Some examples require optional dependencies:

```bash
# For Pydantic examples
pip install pydantic

# For Marshmallow examples  
pip install marshmallow

# For Django examples (full Django installation)
pip install django

# For SQLAlchemy examples
pip install sqlalchemy

# For WTForms examples
pip install wtforms flask-wtf
```

The examples will gracefully handle missing dependencies and show pseudo-code alternatives.
