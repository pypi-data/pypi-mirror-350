"""
Tests for framework integration examples.

This module contains tests that demonstrate how cloneit works
with popular Python frameworks like Django, Pydantic, and Marshmallow.
"""

from cloneit import FieldTemplate, Field


class TestFrameworkIntegration:
    """Test framework integration scenarios."""

    def setup_method(self):
        """Set up test templates before each test."""
        FieldTemplate.clear()

    def test_pydantic_style_fields(self):
        """Test Pydantic-style field definitions."""
        # Register Pydantic-style templates
        FieldTemplate.register(
            "pydantic_email",
            {
                "type": str,
                "min_length": 5,
                "max_length": 255,
                "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            },
        )

        FieldTemplate.register(
            "pydantic_age",
            {"type": int, "ge": 0, "le": 150, "description": "Age in years"},
        )

        # Clone fields
        email_field = Field.like("pydantic_email")
        age_field = Field.like("pydantic_age", le=120)  # Override max age

        assert email_field.type == str
        assert email_field.min_length == 5
        assert email_field.max_length == 255
        assert email_field.regex == r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        assert age_field.type == int
        assert age_field.ge == 0
        assert age_field.le == 120  # Overridden value
        assert age_field.description == "Age in years"

    def test_django_style_fields(self):
        """Test Django-style field definitions."""

        # Mock Django field classes
        class CharField:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        class EmailField:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        class IntegerField:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        # Register Django-style templates
        FieldTemplate.register(
            "django_email",
            {
                "field_class": EmailField,
                "max_length": 255,
                "unique": True,
                "blank": False,
            },
        )

        FieldTemplate.register(
            "django_name",
            {
                "field_class": CharField,
                "max_length": 100,
                "blank": False,
                "null": False,
            },
        )

        FieldTemplate.register(
            "django_id",
            {"field_class": IntegerField, "primary_key": True, "auto_created": True},
        )

        # Clone fields
        email_field = Field.like("django_email")
        name_field = Field.like("django_name", max_length=150)
        id_field = Field.like("django_id")

        # Verify field classes and attributes
        assert isinstance(email_field, EmailField)
        assert email_field.kwargs == {"max_length": 255, "unique": True, "blank": False}

        assert isinstance(name_field, CharField)
        assert name_field.kwargs == {
            "max_length": 150,  # Overridden
            "blank": False,
            "null": False,
        }

        assert isinstance(id_field, IntegerField)
        assert id_field.kwargs == {"primary_key": True, "auto_created": True}

    def test_marshmallow_style_fields(self):
        """Test Marshmallow-style field definitions."""

        # Mock Marshmallow field classes
        class String:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        class Email:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        class Integer:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        # Register Marshmallow-style templates
        FieldTemplate.register(
            "marshmallow_email",
            {
                "field_class": Email,
                "required": True,
                "validate": lambda x: "@" in x,
                "error_messages": {"invalid": "Not a valid email address."},
            },
        )

        FieldTemplate.register(
            "marshmallow_name",
            {
                "field_class": String,
                "required": True,
                "validate": lambda x: len(x) >= 2,
                "allow_none": False,
            },
        )

        # Clone fields
        email_field = Field.like("marshmallow_email", required=False)
        name_field = Field.like("marshmallow_name")

        assert isinstance(email_field, Email)
        assert email_field.kwargs["required"] is False  # Overridden
        assert email_field.kwargs["validate"] is not None
        assert "invalid" in email_field.kwargs["error_messages"]

        assert isinstance(name_field, String)
        assert name_field.kwargs["required"] is True
        assert name_field.kwargs["validate"] is not None
        assert name_field.kwargs["allow_none"] is False

    def test_sqlalchemy_style_fields(self):
        """Test SQLAlchemy-style field definitions."""

        # Mock SQLAlchemy field classes
        class Column:
            def __init__(self, type_, **kwargs):
                self.type_ = type_
                self.kwargs = kwargs

        class String:
            def __init__(self, length=None):
                self.length = length

        class Integer:
            pass

        # Register SQLAlchemy-style templates
        FieldTemplate.register(
            "sqlalchemy_email",
            {
                "field_class": Column,
                "type_": String(255),
                "unique": True,
                "nullable": False,
                "index": True,
            },
        )

        FieldTemplate.register(
            "sqlalchemy_id",
            {
                "field_class": Column,
                "type_": Integer(),
                "primary_key": True,
                "autoincrement": True,
            },
        )

        # Clone fields
        email_field = Field.like("sqlalchemy_email", index=False)
        id_field = Field.like("sqlalchemy_id")

        assert isinstance(email_field, Column)
        assert isinstance(email_field.type_, String)
        assert email_field.type_.length == 255
        assert email_field.kwargs["unique"] is True
        assert email_field.kwargs["nullable"] is False
        assert email_field.kwargs["index"] is False  # Overridden

        assert isinstance(id_field, Column)
        assert isinstance(id_field.type_, Integer)
        assert id_field.kwargs["primary_key"] is True
        assert id_field.kwargs["autoincrement"] is True

    def test_wtforms_style_fields(self):
        """Test WTForms-style field definitions."""

        # Mock WTForms field classes
        class StringField:
            def __init__(self, label=None, validators=None, **kwargs):
                self.label = label
                self.validators = validators or []
                self.kwargs = kwargs

        class EmailField:
            def __init__(self, label=None, validators=None, **kwargs):
                self.label = label
                self.validators = validators or []
                self.kwargs = kwargs

        # Mock validators
        class DataRequired:
            pass

        class Length:
            def __init__(self, min=-1, max=-1):
                self.min = min
                self.max = max

        # Register WTForms-style templates
        FieldTemplate.register(
            "wtforms_email",
            {
                "field_class": EmailField,
                "label": "Email Address",
                "validators": [DataRequired(), Length(min=5, max=255)],
                "render_kw": {"placeholder": "Enter your email"},
            },
        )

        FieldTemplate.register(
            "wtforms_name",
            {
                "field_class": StringField,
                "label": "Full Name",
                "validators": [DataRequired(), Length(min=2, max=100)],
                "render_kw": {"placeholder": "Enter your name"},
            },
        )

        # Clone fields
        email_field = Field.like(
            "wtforms_email",
            label="Work Email",
            render_kw={"placeholder": "Enter work email"},
        )
        name_field = Field.like("wtforms_name")

        assert isinstance(email_field, EmailField)
        assert email_field.label == "Work Email"  # Overridden
        assert len(email_field.validators) == 2
        assert email_field.kwargs["render_kw"]["placeholder"] == "Enter work email"

        assert isinstance(name_field, StringField)
        assert name_field.label == "Full Name"
        assert len(name_field.validators) == 2
        assert name_field.kwargs["render_kw"]["placeholder"] == "Enter your name"


class TestComplexScenarios:
    """Test complex real-world scenarios."""

    def setup_method(self):
        """Set up complex test scenarios."""
        FieldTemplate.clear()

        # Register common templates for a user management system
        FieldTemplate.register(
            "base_string", {"type": str, "required": True, "strip_whitespace": True}
        )

        FieldTemplate.register(
            "email_field",
            {
                "type": str,
                "required": True,
                "max_length": 255,
                "validation": "email",
                "unique": True,
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
                "title_case": True,
            },
        )

        FieldTemplate.register(
            "phone_field",
            {
                "type": str,
                "required": False,
                "max_length": 20,
                "validation": "phone",
                "format": "international",
            },
        )

        FieldTemplate.register(
            "address_field",
            {"type": str, "required": False, "max_length": 500, "multiline": True},
        )

        FieldTemplate.register(
            "id_field",
            {
                "type": int,
                "required": True,
                "primary_key": True,
                "auto_increment": True,
            },
        )

        FieldTemplate.register(
            "timestamp_field",
            {
                "type": "datetime",
                "required": True,
                "auto_now_add": True,
                "timezone_aware": True,
            },
        )

    def test_user_profile_model(self):
        """Test creating a complete user profile model."""
        # User profile fields
        user_id = Field.like("id_field")
        email = Field.like("email_field")
        first_name = Field.like("name_field")
        last_name = Field.like("name_field")
        phone = Field.like("phone_field")
        address = Field.like("address_field")
        created_at = Field.like("timestamp_field")
        updated_at = Field.like("timestamp_field", auto_now=True, auto_now_add=False)

        # Verify all fields have correct properties
        assert user_id.primary_key is True
        assert user_id.auto_increment is True

        assert email.unique is True
        assert email.index is True
        assert email.validation == "email"

        assert first_name.title_case is True
        assert first_name.min_length == 2
        assert last_name.title_case is True

        assert phone.required is False
        assert phone.validation == "phone"

        assert address.multiline is True
        assert address.required is False

        assert created_at.auto_now_add is True
        assert created_at.timezone_aware is True

        assert updated_at.auto_now is True
        assert updated_at.auto_now_add is False

    def test_admin_user_extensions(self):
        """Test extending user model for admin users."""
        # Admin user with additional fields
        admin_email = Field.like("email_field", default="admin@company.com")
        admin_role = Field.like("base_string", max_length=50, default="administrator")
        permissions = Field.like("base_string", max_length=1000, required=False)
        last_login = Field.like("timestamp_field", required=False, auto_now_add=False)

        assert admin_email.default == "admin@company.com"
        assert admin_email.unique is True  # Inherited from template

        assert admin_role.default == "administrator"
        assert admin_role.max_length == 50
        assert admin_role.strip_whitespace is True  # Inherited from base_string

        assert permissions.required is False
        assert permissions.max_length == 1000

        assert last_login.required is False
        assert last_login.auto_now_add is False

    def test_form_field_variations(self):
        """Test creating form field variations."""
        # Registration form fields
        reg_email = Field.like(
            "email_field",
            placeholder="Enter your email address",
            help_text="We will send verification to this email",
            css_class="form-control",
        )

        reg_password = Field.like(
            "base_string",
            input_type="password",
            min_length=8,
            max_length=128,
            placeholder="Choose a strong password",
            validation="password_strength",
        )

        # Login form fields (simplified versions)
        login_email = Field.like(
            "email_field",
            required=True,
            unique=False,  # Override for form use
            placeholder="Email",
            css_class="form-control-sm",
        )

        login_password = Field.like(
            "base_string",
            input_type="password",
            required=True,
            placeholder="Password",
            css_class="form-control-sm",
        )

        # Verify form-specific properties
        assert reg_email.placeholder == "Enter your email address"
        assert reg_email.help_text == "We will send verification to this email"
        assert reg_email.css_class == "form-control"
        assert reg_email.validation == "email"  # Inherited

        assert reg_password.input_type == "password"
        assert reg_password.min_length == 8
        assert reg_password.validation == "password_strength"

        assert login_email.unique is False  # Overridden for form use
        assert login_email.css_class == "form-control-sm"
        assert login_email.validation == "email"  # Still inherited

        assert login_password.input_type == "password"
        assert login_password.css_class == "form-control-sm"
