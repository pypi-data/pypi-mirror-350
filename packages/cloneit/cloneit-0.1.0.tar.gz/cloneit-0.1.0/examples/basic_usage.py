"""
Basic usage examples for the cloneit package.

This file demonstrates the fundamental concepts and usage patterns
of cloneit for field template registration and cloning.
"""

from cloneit import FieldTemplate, Field, TemplateNotFoundError


def basic_registration_example():
    """Demonstrate basic template registration and usage."""

    print("=== Basic Template Registration ===")

    # Clear any existing templates
    FieldTemplate.clear()

    # Register a simple email template
    FieldTemplate.register(
        "email",
        {"type": str, "required": True, "max_length": 255, "validation": "email"},
    )

    # Register a name template
    FieldTemplate.register(
        "name", {"type": str, "required": True, "max_length": 100, "min_length": 2}
    )

    print("Registered templates:")
    for template_name in FieldTemplate.list():
        print(f"  - {template_name}")

    # Clone templates
    user_email = Field.like("email")
    admin_email = Field.like("email", required=False, default="admin@company.com")
    first_name = Field.like("name")
    last_name = Field.like("name", max_length=150)

    print(f"\nuser_email: {user_email}")
    print(f"admin_email: {admin_email}")
    print(f"first_name: {first_name}")
    print(f"last_name: {last_name}")


def field_override_example():
    """Demonstrate field attribute overriding."""

    print("\n=== Field Override Examples ===")

    # Register a base text field template
    FieldTemplate.register(
        "text_field",
        {"type": str, "required": True, "max_length": 500, "strip_whitespace": True},
    )

    # Create variations with overrides
    title_field = Field.like("text_field", max_length=200, title_case=True)
    description_field = Field.like("text_field", required=False, max_length=1000)
    comment_field = Field.like("text_field", required=False, multiline=True)

    print(f"title_field max_length: {title_field.max_length}")
    print(f"title_field title_case: {title_field.title_case}")
    print(f"description_field required: {description_field.required}")
    print(f"comment_field multiline: {comment_field.multiline}")

    # Show that original template is unchanged
    original = FieldTemplate.get("text_field")
    print(f"Original template max_length: {original['max_length']}")


def error_handling_example():
    """Demonstrate error handling scenarios."""

    print("\n=== Error Handling Examples ===")

    # Try to clone a non-existent template
    try:
        Field.like("nonexistent_template")
    except TemplateNotFoundError as e:
        print(f"Caught expected error: {e}")

    # Try to register invalid template
    try:
        FieldTemplate.register(123, {"type": str})
    except TypeError as e:
        print(f"Caught type error: {e}")

    try:
        FieldTemplate.register("test", "invalid_attributes")
    except TypeError as e:
        print(f"Caught type error: {e}")


def template_management_example():
    """Demonstrate template management operations."""

    print("\n=== Template Management Examples ===")

    # Register several templates
    FieldTemplate.register("temp1", {"type": str})
    FieldTemplate.register("temp2", {"type": int})
    FieldTemplate.register("temp3", {"type": bool})

    print(f"Templates before: {FieldTemplate.list()}")

    # Check if templates exist
    print(f"temp1 exists: {FieldTemplate.exists('temp1')}")
    print(f"temp4 exists: {FieldTemplate.exists('temp4')}")

    # Remove a template
    removed = FieldTemplate.unregister("temp2")
    print(f"Removed temp2: {removed}")
    print(f"Templates after removal: {FieldTemplate.list()}")

    # Try to remove non-existent template
    removed = FieldTemplate.unregister("temp4")
    print(f"Tried to remove temp4: {removed}")

    # Clear all templates
    FieldTemplate.clear()
    print(f"Templates after clear: {FieldTemplate.list()}")


def field_definition_example():
    """Demonstrate FieldDefinition class usage."""

    print("\n=== FieldDefinition Examples ===")

    # Register a template
    FieldTemplate.register(
        "demo_field",
        {"type": str, "required": True, "max_length": 100, "validation": "custom"},
    )

    # Clone to get a FieldDefinition
    field = Field.like("demo_field", default="test_value")

    print(f"Field type: {field.type}")
    print(f"Field required: {field.required}")
    print(f"Field default: {field.default}")

    # Access attributes using methods
    max_len = field.get_attribute("max_length")
    print(f"Max length: {max_len}")

    missing_attr = field.get_attribute("missing", "default_value")
    print(f"Missing attribute with default: {missing_attr}")

    # Set new attributes
    field.set_attribute("placeholder", "Enter text here")
    print(f"New placeholder: {field.placeholder}")

    # Convert to dictionary
    field_dict = field.to_dict()
    print(f"Field as dict: {field_dict}")

    # Test equality
    field2 = Field.like("demo_field", default="test_value")
    print(f"Fields are equal: {field == field2}")

    field3 = Field.like("demo_field", default="different_value")
    print(f"Fields with different defaults are equal: {field == field3}")


def advanced_template_patterns():
    """Demonstrate advanced template usage patterns."""

    print("\n=== Advanced Template Patterns ===")

    # Hierarchical templates
    FieldTemplate.register("base_field", {"required": True, "strip_whitespace": True})

    # Build on base template
    base_attrs = FieldTemplate.get("base_field")
    email_attrs = {
        **base_attrs,
        "type": str,
        "max_length": 255,
        "validation": "email",
        "unique": True,
    }
    FieldTemplate.register("extended_email", email_attrs)

    # Template with callable defaults
    import datetime

    FieldTemplate.register(
        "timestamp_field",
        {
            "type": datetime.datetime,
            "required": True,
            "default_factory": datetime.datetime.now,
            "timezone_aware": True,
        },
    )

    # Template for different contexts
    FieldTemplate.register(
        "contextual_field", {"type": str, "required": True, "context_dependent": True}
    )

    # Clone with different contexts
    form_field = Field.like(
        "contextual_field", placeholder="Enter value", css_class="form-control"
    )

    api_field = Field.like(
        "contextual_field", serialization="json", validation_level="strict"
    )

    db_field = Field.like("contextual_field", index=True, nullable=False)

    print("Extended email field:")
    extended_email = Field.like("extended_email")
    print(f"  Type: {extended_email.type}")
    print(f"  Unique: {extended_email.unique}")
    print(f"  Strip whitespace: {extended_email.strip_whitespace}")

    print("\nTimestamp field:")
    timestamp = Field.like("timestamp_field")
    print(f"  Type: {timestamp.type}")
    print(f"  Default factory: {timestamp.default_factory}")

    print("\nContextual fields:")
    print(f"  Form field CSS class: {form_field.css_class}")
    print(f"  API field validation: {api_field.validation_level}")
    print(f"  DB field index: {db_field.index}")


def real_world_scenario():
    """Demonstrate a real-world user management scenario."""

    print("\n=== Real-World User Management Scenario ===")

    # Clear and set up templates for user management
    FieldTemplate.clear()

    # Core field templates
    FieldTemplate.register(
        "id_field",
        {"type": int, "required": True, "primary_key": True, "auto_increment": True},
    )

    FieldTemplate.register(
        "email_field",
        {
            "type": str,
            "required": True,
            "max_length": 255,
            "unique": True,
            "validation": "email",
            "index": True,
        },
    )

    FieldTemplate.register(
        "name_field",
        {
            "type": str,
            "required": True,
            "max_length": 100,
            "min_length": 2,
            "strip_whitespace": True,
        },
    )

    FieldTemplate.register(
        "optional_text",
        {"type": str, "required": False, "max_length": 500, "strip_whitespace": True},
    )

    FieldTemplate.register(
        "timestamp", {"type": "datetime", "required": True, "auto_now_add": True}
    )

    # User model fields
    print("Creating User model fields:")
    user_fields = {
        "id": Field.like("id_field"),
        "email": Field.like("email_field"),
        "first_name": Field.like("name_field"),
        "last_name": Field.like("name_field"),
        "bio": Field.like("optional_text"),
        "created_at": Field.like("timestamp"),
        "updated_at": Field.like("timestamp", auto_now=True, auto_now_add=False),
    }

    for name, field in user_fields.items():
        print(f"  {name}: {field}")

    # Admin user with overrides
    print("\nCreating Admin user fields:")
    admin_fields = {
        "id": Field.like("id_field"),
        "email": Field.like("email_field", default="admin@company.com"),
        "first_name": Field.like("name_field", default="Admin"),
        "last_name": Field.like("name_field", default="User"),
        "role": Field.like("name_field", max_length=50, default="administrator"),
        "permissions": Field.like("optional_text", max_length=1000),
        "created_at": Field.like("timestamp"),
        "last_login": Field.like("timestamp", required=False, auto_now_add=False),
    }

    for name, field in admin_fields.items():
        print(f"  {name}: {field}")

    # Registration form fields
    print("\nCreating Registration form fields:")
    form_fields = {
        "email": Field.like(
            "email_field",
            placeholder="Enter your email",
            help_text="We will never share your email",
        ),
        "first_name": Field.like(
            "name_field", placeholder="First name", css_class="form-control"
        ),
        "last_name": Field.like(
            "name_field", placeholder="Last name", css_class="form-control"
        ),
        "bio": Field.like(
            "optional_text",
            placeholder="Tell us about yourself (optional)",
            multiline=True,
            rows=4,
        ),
    }

    for name, field in form_fields.items():
        print(f"  {name}: {field}")


def main():
    """Run all basic examples."""

    print("CLONEIT BASIC USAGE EXAMPLES")
    print("=" * 50)

    basic_registration_example()
    field_override_example()
    error_handling_example()
    template_management_example()
    field_definition_example()
    advanced_template_patterns()
    real_world_scenario()

    print("\n" + "=" * 50)
    print("ALL BASIC EXAMPLES COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()
