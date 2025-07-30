"""
Real-world examples demonstrating cloneit usage with popular frameworks.

This file contains practical examples showing how to use cloneit
with Django, Pydantic, Marshmallow, and other frameworks.
"""

from datetime import datetime
from typing import Optional
from cloneit import FieldTemplate, Field


# ============================================================================
# Common Field Templates
# ============================================================================


def setup_common_templates():
    """Set up commonly used field templates."""

    # Basic field types
    FieldTemplate.register(
        "email",
        {"type": str, "required": True, "max_length": 255, "validation": "email"},
    )

    FieldTemplate.register(
        "name", {"type": str, "required": True, "max_length": 100, "min_length": 2}
    )

    FieldTemplate.register(
        "phone",
        {"type": str, "required": False, "max_length": 20, "validation": "phone"},
    )

    FieldTemplate.register("id_field", {"type": int, "required": True, "gt": 0})

    FieldTemplate.register(
        "timestamp",
        {"type": datetime, "required": True, "default_factory": datetime.now},
    )

    FieldTemplate.register(
        "text_field", {"type": str, "required": False, "max_length": 1000}
    )


# ============================================================================
# Pydantic Examples
# ============================================================================


def pydantic_example():
    """Example using cloneit with Pydantic models."""
    try:
        from pydantic import BaseModel, Field as PydanticField
    except ImportError:
        print("Pydantic not installed. Install with: pip install pydantic")
        return

    # Set up Pydantic-specific templates
    FieldTemplate.register(
        "pydantic_email",
        {
            "description": "User email address",
            "example": "user@example.com",
            "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        },
    )

    FieldTemplate.register(
        "pydantic_name",
        {
            "description": "User name",
            "min_length": 2,
            "max_length": 100,
            "example": "John Doe",
        },
    )

    FieldTemplate.register(
        "pydantic_age",
        {"description": "User age in years", "ge": 0, "le": 150, "example": 25},
    )

    class User(BaseModel):
        id: int = Field.like("id_field").get_attribute("default", 1)
        email: str = PydanticField(**Field.like("pydantic_email").to_dict())
        first_name: str = PydanticField(**Field.like("pydantic_name").to_dict())
        last_name: str = PydanticField(**Field.like("pydantic_name").to_dict())
        age: Optional[int] = PydanticField(
            **Field.like("pydantic_age", ge=13, le=120).to_dict()
        )
        phone: Optional[str] = PydanticField(**Field.like("phone").to_dict())

    # Example usage
    user_data = {
        "id": 1,
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "phone": "+1234567890",
    }

    user = User(**user_data)
    print(f"Created user: {user}")
    return user


# ============================================================================
# Django Examples
# ============================================================================


def django_example():
    """Example using cloneit with Django models."""
    print("Django Example (pseudo-code - requires Django installation):")

    # Set up Django-specific templates
    FieldTemplate.register(
        "django_email",
        {
            "field_class": "EmailField",  # Would be models.EmailField in real Django
            "max_length": 255,
            "unique": True,
            "blank": False,
        },
    )

    FieldTemplate.register(
        "django_char",
        {
            "field_class": "CharField",  # Would be models.CharField in real Django
            "max_length": 100,
            "blank": False,
            "null": False,
        },
    )

    FieldTemplate.register(
        "django_text",
        {
            "field_class": "TextField",  # Would be models.TextField in real Django
            "blank": True,
            "null": True,
        },
    )

    FieldTemplate.register(
        "django_datetime",
        {
            "field_class": "DateTimeField",  # Would be models.DateTimeField
            "auto_now_add": True,
        },
    )

    # Example model definition (pseudo-code)
    django_model_code = """    from django.db import models
    from cloneit import Field

    class User(models.Model):
        email = Field.like('django_email')
        first_name = Field.like('django_char', max_length=50)
        last_name = Field.like('django_char', max_length=50)
        bio = Field.like('django_text')
        created_at = Field.like('django_datetime')
        updated_at = Field.like('django_datetime', auto_now=True, auto_now_add=False)
        
        def __str__(self):
            return f"{self.first_name} {self.last_name}"
    """

    print(django_model_code)


# ============================================================================
# Marshmallow Examples
# ============================================================================


def marshmallow_example():
    """Example using cloneit with Marshmallow schemas."""
    try:
        from marshmallow import Schema, fields, validate
    except ImportError:
        print("Marshmallow not installed. Install with: pip install marshmallow")
        return

    # Set up Marshmallow-specific templates
    FieldTemplate.register(
        "marshmallow_email",
        {
            "field_class": fields.Email,
            "required": True,
            "validate": validate.Length(min=5, max=255),
            "error_messages": {"invalid": "Not a valid email address."},
        },
    )

    FieldTemplate.register(
        "marshmallow_string",
        {
            "field_class": fields.String,
            "required": True,
            "validate": validate.Length(min=2, max=100),
            "allow_none": False,
        },
    )

    FieldTemplate.register(
        "marshmallow_integer",
        {
            "field_class": fields.Integer,
            "required": True,
            "validate": validate.Range(min=1),
            "allow_none": False,
        },
    )

    class UserSchema(Schema):
        id = Field.like("marshmallow_integer")
        email = Field.like("marshmallow_email")
        first_name = Field.like("marshmallow_string")
        last_name = Field.like("marshmallow_string")
        age = Field.like(
            "marshmallow_integer",
            required=False,
            validate=validate.Range(min=0, max=150),
        )

    # Example usage
    schema = UserSchema()

    user_data = {
        "id": 1,
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
    }

    try:
        result = schema.load(user_data)
        print(f"Validated user data: {result}")
        return result
    except Exception as e:
        print(f"Validation error: {e}")


# ============================================================================
# SQLAlchemy Examples
# ============================================================================


def sqlalchemy_example():
    """Example using cloneit with SQLAlchemy models."""
    print("SQLAlchemy Example (pseudo-code):")

    # Set up SQLAlchemy-specific templates
    FieldTemplate.register(
        "sqlalchemy_id",
        {
            "field_class": "Column",  # Would be Column in real SQLAlchemy
            "type_": "Integer",  # Would be Integer() in real SQLAlchemy
            "primary_key": True,
            "autoincrement": True,
        },
    )

    FieldTemplate.register(
        "sqlalchemy_string",
        {
            "field_class": "Column",  # Would be Column in real SQLAlchemy
            "type_": "String",  # Would be String(length) in real SQLAlchemy
            "nullable": False,
        },
    )

    FieldTemplate.register(
        "sqlalchemy_email",
        {
            "field_class": "Column",  # Would be Column in real SQLAlchemy
            "type_": "String",  # Would be String(255) in real SQLAlchemy
            "unique": True,
            "nullable": False,
            "index": True,
        },
    )

    sqlalchemy_model_code = """
    from sqlalchemy import Column, Integer, String, DateTime, Text
    from sqlalchemy.ext.declarative import declarative_base
    from cloneit import Field
      Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'

        id = Field.like('sqlalchemy_id')
        email = Field.like('sqlalchemy_email')
        first_name = Field.like('sqlalchemy_string', type_=String(50))
        last_name = Field.like('sqlalchemy_string', type_=String(50))
        created_at = Field.like('sqlalchemy_datetime')
    """

    print(sqlalchemy_model_code)


# ============================================================================
# WTForms Examples
# ============================================================================


def wtforms_example():
    """Example using cloneit with WTForms."""
    print("WTForms Example (pseudo-code):")

    # Set up WTForms-specific templates
    FieldTemplate.register(
        "wtforms_email",
        {
            "field_class": "EmailField",  # Would be EmailField in real WTForms
            "label": "Email Address",
            "validators": [
                "DataRequired",
                "Email",
            ],  # Would be [DataRequired(), Email()] in real WTForms
            "render_kw": {"placeholder": "Enter your email"},
        },
    )

    FieldTemplate.register(
        "wtforms_string",
        {
            "field_class": "StringField",  # Would be StringField in real WTForms
            "validators": [
                "DataRequired",
                "Length",
            ],  # Would be [DataRequired(), Length(min=2, max=100)] in real WTForms
            "render_kw": {"class": "form-control"},
        },
    )

    FieldTemplate.register(
        "wtforms_password",
        {
            "field_class": "PasswordField",  # Would be PasswordField in real WTForms
            "label": "Password",
            "validators": [
                "DataRequired",
                "Length",
            ],  # Would be [DataRequired(), Length(min=8)] in real WTForms
            "render_kw": {"placeholder": "Enter password"},
        },
    )

    wtforms_code = """
    from flask_wtf import FlaskForm
    from wtforms import StringField, EmailField, PasswordField, SubmitField
    from wtforms.validators import DataRequired, Email, Length
    from cloneit import Field
    
    class RegistrationForm(FlaskForm):
        email = Field.like('wtforms_email')        first_name = Field.like(
            'wtforms_string',
            label='First Name',
            render_kw={'placeholder': 'First Name'}
        )
        last_name = Field.like(
            'wtforms_string',
            label='Last Name',
            render_kw={'placeholder': 'Last Name'}
        )
        password = Field.like('wtforms_password')
        submit = SubmitField('Register')
    """

    print(wtforms_code)


# ============================================================================
# Advanced Usage Examples
# ============================================================================


def advanced_template_inheritance():
    """Example of template inheritance and composition."""

    # Base templates
    FieldTemplate.register("base_field", {"required": True, "strip_whitespace": True})

    FieldTemplate.register(
        "string_field",
        {"type": str, "required": True, "strip_whitespace": True, "max_length": 255},
    )

    # Specialized templates building on base templates
    FieldTemplate.register(
        "name_field",
        {
            **Field.like("string_field").to_dict(),
            "max_length": 100,
            "min_length": 2,
            "title_case": True,
        },
    )

    FieldTemplate.register(
        "email_field",
        {
            **Field.like("string_field").to_dict(),
            "validation": "email",
            "unique": True,
            "index": True,
        },
    )

    FieldTemplate.register(
        "username_field",
        {
            **Field.like("string_field").to_dict(),
            "max_length": 50,
            "min_length": 3,
            "validation": "alphanumeric",
            "unique": True,
            "lowercase": True,
        },
    )

    # Usage
    user_email = Field.like("email_field")
    admin_email = Field.like("email_field", required=False, default="admin@company.com")

    first_name = Field.like("name_field")
    last_name = Field.like("name_field", max_length=150)

    username = Field.like("username_field")
    display_name = Field.like("name_field", required=False)

    print("Advanced template inheritance example completed")
    return {
        "user_email": user_email,
        "admin_email": admin_email,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "display_name": display_name,
    }


def conditional_field_generation():
    """Example of conditional field generation based on context."""

    def create_user_fields(user_type="regular", include_admin_fields=False):
        """Create user fields based on user type and context."""

        fields = {}

        # Basic fields for all users
        fields["id"] = Field.like("id_field")
        fields["email"] = Field.like("email")
        fields["first_name"] = Field.like("name")
        fields["last_name"] = Field.like("name")
        fields["created_at"] = Field.like("timestamp")

        if user_type == "admin":
            # Admin-specific field overrides
            fields["email"] = Field.like("email", default="admin@company.com")
            fields["role"] = Field.like("name", max_length=50, default="administrator")
            fields["permissions"] = Field.like("text_field", required=False)

        elif user_type == "customer":
            # Customer-specific fields
            fields["phone"] = Field.like("phone")
            fields["address"] = Field.like("text_field", max_length=500)
            fields["newsletter_opt_in"] = Field.like(
                "id_field", type=bool, default=False, gt=None
            )

        if include_admin_fields and user_type != "admin":
            # Add admin tracking fields for non-admin users
            fields["last_login"] = Field.like("timestamp", required=False)
            fields["is_active"] = Field.like(
                "id_field", type=bool, default=True, gt=None
            )

        return fields

    # Generate different field sets
    regular_user_fields = create_user_fields("regular")
    admin_user_fields = create_user_fields("admin")
    customer_fields = create_user_fields("customer", include_admin_fields=True)

    print(f"Regular user fields: {list(regular_user_fields.keys())}")
    print(f"Admin user fields: {list(admin_user_fields.keys())}")
    print(f"Customer fields: {list(customer_fields.keys())}")

    return {
        "regular": regular_user_fields,
        "admin": admin_user_fields,
        "customer": customer_fields,
    }


# ============================================================================
# Main Demo Function
# ============================================================================


def run_examples():
    """Run all examples to demonstrate cloneit functionality."""

    print("=" * 60)
    print("CLONEIT FRAMEWORK EXAMPLES")
    print("=" * 60)

    # Set up common templates
    setup_common_templates()

    print("\n1. Pydantic Example:")
    print("-" * 40)
    pydantic_example()

    print("\n2. Django Example:")
    print("-" * 40)
    django_example()

    print("\n3. Marshmallow Example:")
    print("-" * 40)
    marshmallow_example()

    print("\n4. SQLAlchemy Example:")
    print("-" * 40)
    sqlalchemy_example()

    print("\n5. WTForms Example:")
    print("-" * 40)
    wtforms_example()

    print("\n6. Advanced Template Inheritance:")
    print("-" * 40)
    advanced_template_inheritance()

    print("\n7. Conditional Field Generation:")
    print("-" * 40)
    conditional_field_generation()

    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_examples()
