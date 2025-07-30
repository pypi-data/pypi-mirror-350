"""
Test suite for the cloneit package.

This module contains comprehensive tests for all functionality
in the cloneit package.
"""

import pytest
from cloneit import FieldTemplate, Field, TemplateNotFoundError, CloneItError
from cloneit.core import FieldDefinition


class TestFieldTemplate:
    """Test cases for FieldTemplate class."""

    def setup_method(self):
        """Clear registry before each test."""
        FieldTemplate.clear()

    def test_register_template(self):
        """Test registering a field template."""
        template_attrs = {"type": str, "required": True, "max_length": 255}

        FieldTemplate.register("email", template_attrs)

        assert FieldTemplate.exists("email")
        assert "email" in FieldTemplate.list()

    def test_register_template_invalid_name(self):
        """Test registering template with invalid name type."""
        with pytest.raises(TypeError, match="Template name must be a string"):
            FieldTemplate.register(123, {"type": str})

    def test_register_template_invalid_attributes(self):
        """Test registering template with invalid attributes type."""
        with pytest.raises(TypeError, match="Template attributes must be a dictionary"):
            FieldTemplate.register("test", "invalid")

    def test_get_existing_template(self):
        """Test retrieving an existing template."""
        template_attrs = {
            "type": str,
            "required": True,
            "max_length": 255,
            "validation": "email",
        }

        FieldTemplate.register("email", template_attrs)
        retrieved = FieldTemplate.get("email")

        assert retrieved == template_attrs
        # Ensure it's a deep copy
        retrieved["new_key"] = "new_value"
        original = FieldTemplate.get("email")
        assert "new_key" not in original

    def test_get_nonexistent_template(self):
        """Test retrieving a template that doesn't exist."""
        with pytest.raises(
            TemplateNotFoundError, match="Template 'nonexistent' not found"
        ):
            FieldTemplate.get("nonexistent")

    def test_exists_method(self):
        """Test the exists method."""
        assert not FieldTemplate.exists("test")

        FieldTemplate.register("test", {"type": str})
        assert FieldTemplate.exists("test")

    def test_list_templates(self):
        """Test listing all registered templates."""
        assert FieldTemplate.list() == []

        FieldTemplate.register("email", {"type": str})
        FieldTemplate.register("name", {"type": str})

        templates = FieldTemplate.list()
        assert len(templates) == 2
        assert "email" in templates
        assert "name" in templates

    def test_unregister_template(self):
        """Test unregistering a template."""
        FieldTemplate.register("test", {"type": str})
        assert FieldTemplate.exists("test")

        result = FieldTemplate.unregister("test")
        assert result is True
        assert not FieldTemplate.exists("test")

        # Try to unregister non-existent template
        result = FieldTemplate.unregister("nonexistent")
        assert result is False

    def test_clear_templates(self):
        """Test clearing all templates."""
        FieldTemplate.register("test1", {"type": str})
        FieldTemplate.register("test2", {"type": int})

        assert len(FieldTemplate.list()) == 2

        FieldTemplate.clear()
        assert FieldTemplate.list() == []


class TestField:
    """Test cases for Field class."""

    def setup_method(self):
        """Clear registry and set up test templates before each test."""
        FieldTemplate.clear()

        # Register test templates
        FieldTemplate.register(
            "email",
            {"type": str, "required": True, "max_length": 255, "validation": "email"},
        )

        FieldTemplate.register(
            "name", {"type": str, "required": True, "max_length": 100, "min_length": 2}
        )

        FieldTemplate.register("id_field", {"type": int, "required": True, "gt": 0})

    def test_clone_template_basic(self):
        """Test basic template cloning without overrides."""
        field = Field.like("email")

        assert isinstance(field, FieldDefinition)
        assert field.type == str
        assert field.required is True
        assert field.max_length == 255
        assert field.validation == "email"

    def test_clone_template_with_overrides(self):
        """Test template cloning with attribute overrides."""
        field = Field.like("email", required=False, default="test@example.com")

        assert field.type == str
        assert field.required is False
        assert field.default == "test@example.com"
        assert field.max_length == 255  # Original attribute preserved
        assert field.validation == "email"  # Original attribute preserved

    def test_clone_nonexistent_template(self):
        """Test cloning a template that doesn't exist."""
        with pytest.raises(
            TemplateNotFoundError, match="Template 'nonexistent' not found"
        ):
            Field.like("nonexistent")

    def test_clone_with_field_class(self):
        """Test cloning template with field_class attribute."""

        # Mock field class
        class MockField:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        FieldTemplate.register(
            "django_email",
            {"field_class": MockField, "max_length": 255, "unique": True},
        )

        field = Field.like("django_email", blank=False)

        assert isinstance(field, MockField)
        assert field.kwargs == {"max_length": 255, "unique": True, "blank": False}

    def test_multiple_clones_independence(self):
        """Test that multiple clones of the same template are independent."""
        field1 = Field.like("name")
        field2 = Field.like("name", max_length=150)

        assert field1.max_length == 100
        assert field2.max_length == 150

        # Modifying one shouldn't affect the other
        field1.set_attribute("new_attr", "value1")
        assert field2.get_attribute("new_attr") is None


class TestFieldDefinition:
    """Test cases for FieldDefinition class."""

    def test_initialization(self):
        """Test FieldDefinition initialization."""
        field = FieldDefinition(type=str, required=True, max_length=100, default="test")

        assert field.type == str
        assert field.required is True
        assert field.max_length == 100
        assert field.default == "test"

        expected_attrs = {
            "type": str,
            "required": True,
            "max_length": 100,
            "default": "test",
        }
        assert field.attributes == expected_attrs

    def test_get_attribute(self):
        """Test getting field attributes."""
        field = FieldDefinition(type=str, required=True)

        assert field.get_attribute("type") == str
        assert field.get_attribute("required") is True
        assert field.get_attribute("nonexistent") is None
        assert field.get_attribute("nonexistent", "default") == "default"

    def test_set_attribute(self):
        """Test setting field attributes."""
        field = FieldDefinition(type=str)

        field.set_attribute("max_length", 100)
        assert field.max_length == 100
        assert field.get_attribute("max_length") == 100
        assert field.attributes["max_length"] == 100

    def test_to_dict(self):
        """Test converting field to dictionary."""
        attrs = {"type": str, "required": True, "max_length": 100}
        field = FieldDefinition(**attrs)

        result = field.to_dict()
        assert result == attrs

        # Ensure it's a deep copy
        result["new_key"] = "new_value"
        assert "new_key" not in field.attributes

    def test_equality(self):
        """Test FieldDefinition equality comparison."""
        field1 = FieldDefinition(type=str, required=True)
        field2 = FieldDefinition(type=str, required=True)
        field3 = FieldDefinition(type=str, required=False)

        assert field1 == field2
        assert field1 != field3
        assert field1 != "not a field"

    def test_repr(self):
        """Test FieldDefinition string representation."""
        field = FieldDefinition(type=str, required=True, max_length=100)
        repr_str = repr(field)

        assert "FieldDefinition(" in repr_str
        assert "type=" in repr_str
        assert "required=" in repr_str
        assert "max_length=" in repr_str


class TestIntegrationScenarios:
    """Integration tests for real-world usage scenarios."""

    def setup_method(self):
        """Set up common templates for integration tests."""
        FieldTemplate.clear()

        # Common field templates
        FieldTemplate.register(
            "email",
            {"type": str, "required": True, "max_length": 255, "validation": "email"},
        )

        FieldTemplate.register(
            "name", {"type": str, "required": True, "max_length": 100, "min_length": 2}
        )

        FieldTemplate.register("id_field", {"type": int, "required": True, "gt": 0})

        FieldTemplate.register(
            "timestamp", {"type": "datetime", "required": True, "auto_now_add": True}
        )

    def test_user_model_scenario(self):
        """Test creating user model fields."""
        # User model fields
        user_id = Field.like("id_field")
        email = Field.like("email")
        first_name = Field.like("name")
        last_name = Field.like("name", max_length=150)
        created_at = Field.like("timestamp")
        updated_at = Field.like("timestamp", auto_now=True, auto_now_add=False)

        # Verify field properties
        assert user_id.type == int
        assert user_id.gt == 0

        assert email.type == str
        assert email.validation == "email"
        assert email.max_length == 255

        assert first_name.max_length == 100
        assert last_name.max_length == 150

        assert created_at.auto_now_add is True
        assert updated_at.auto_now is True
        assert updated_at.auto_now_add is False

    def test_admin_user_scenario(self):
        """Test creating admin user with different defaults."""
        # Admin user with different defaults
        admin_email = Field.like("email", default="admin@company.com")
        admin_first_name = Field.like("name", default="Admin")
        admin_last_name = Field.like("name", default="User", required=False)

        assert admin_email.default == "admin@company.com"
        assert admin_first_name.default == "Admin"
        assert admin_last_name.default == "User"
        assert admin_last_name.required is False

    def test_form_field_scenario(self):
        """Test creating form fields with additional properties."""
        # Form fields with additional UI properties
        email_field = Field.like(
            "email",
            placeholder="Enter your email",
            help_text="We will never share your email",
            css_class="form-control",
        )

        name_field = Field.like(
            "name", placeholder="Enter your full name", css_class="form-control"
        )

        assert email_field.placeholder == "Enter your email"
        assert email_field.help_text == "We will never share your email"
        assert email_field.css_class == "form-control"
        assert email_field.type == str  # Original template property preserved

        assert name_field.placeholder == "Enter your full name"
        assert name_field.css_class == "form-control"
        assert name_field.min_length == 2  # Original template property preserved


class TestExceptionHandling:
    """Test exception handling scenarios."""

    def setup_method(self):
        """Clear registry before each test."""
        FieldTemplate.clear()

    def test_template_not_found_error_message(self):
        """Test that TemplateNotFoundError has a clear message."""
        template_name = "missing_template"

        with pytest.raises(TemplateNotFoundError) as exc_info:
            Field.like(template_name)

        assert template_name in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    def test_template_not_found_inheritance(self):
        """Test that TemplateNotFoundError inherits from CloneItError."""
        with pytest.raises(CloneItError):
            Field.like("nonexistent")

    def test_invalid_template_registration(self):
        """Test various invalid template registration scenarios."""
        # Invalid name types
        invalid_names = [None, 123, [], {}]
        for invalid_name in invalid_names:
            with pytest.raises(TypeError):
                FieldTemplate.register(invalid_name, {"type": str})

        # Invalid attributes types
        invalid_attrs = [None, "string", 123, []]
        for invalid_attr in invalid_attrs:
            with pytest.raises(TypeError):
                FieldTemplate.register("test", invalid_attr)
