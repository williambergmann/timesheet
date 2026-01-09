"""
API Validation Module (REQ-035)

Provides request validation utilities and schema validation.

Usage:
    from app.utils.validation import validate_request, Schema, Field

    @timesheets_bp.route("/<timesheet_id>/entries", methods=["POST"])
    @login_required
    def update_entries(timesheet_id):
        # Validate path parameter
        validate_uuid(timesheet_id, "timesheet_id")
        
        # Validate request body
        data = validate_request({
            "entries": Field(required=True, field_type=list),
        })
        
        # Continue with validated data...
"""

import re
import uuid
from datetime import datetime, date
from functools import wraps
from flask import request, g

from .errors import ValidationError, ErrorCode, error_response


# ============================================================================
# Field Types for Schema Validation
# ============================================================================
class Field:
    """Field definition for schema validation."""
    
    def __init__(
        self,
        required: bool = False,
        field_type: type = None,
        min_length: int = None,
        max_length: int = None,
        min_value: float = None,
        max_value: float = None,
        choices: list = None,
        default=None,
        nullable: bool = True,
        pattern: str = None,
        custom_validator=None,
    ):
        self.required = required
        self.field_type = field_type
        self.min_length = min_length
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value
        self.choices = choices
        self.default = default
        self.nullable = nullable
        self.pattern = pattern
        self.custom_validator = custom_validator
    
    def validate(self, value, field_name: str):
        """Validate a value against this field's constraints.
        
        Args:
            value: The value to validate
            field_name: Name of the field (for error messages)
            
        Returns:
            The validated (and possibly coerced) value
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if required
        if value is None:
            if self.required:
                raise ValidationError(f"{field_name} is required", field_name)
            if not self.nullable:
                raise ValidationError(f"{field_name} cannot be null", field_name)
            return self.default
        
        # Check type
        if self.field_type:
            value = self._validate_type(value, field_name)
        
        # Check string constraints
        if isinstance(value, str):
            if self.min_length and len(value) < self.min_length:
                raise ValidationError(
                    f"{field_name} must be at least {self.min_length} characters",
                    field_name
                )
            if self.max_length and len(value) > self.max_length:
                raise ValidationError(
                    f"{field_name} must be at most {self.max_length} characters",
                    field_name
                )
            if self.pattern and not re.match(self.pattern, value):
                raise ValidationError(f"{field_name} has invalid format", field_name)
        
        # Check numeric constraints
        if isinstance(value, (int, float)):
            if self.min_value is not None and value < self.min_value:
                raise ValidationError(
                    f"{field_name} must be at least {self.min_value}",
                    field_name
                )
            if self.max_value is not None and value > self.max_value:
                raise ValidationError(
                    f"{field_name} must be at most {self.max_value}",
                    field_name
                )
        
        # Check choices
        if self.choices and value not in self.choices:
            raise ValidationError(
                f"{field_name} must be one of: {', '.join(str(c) for c in self.choices)}",
                field_name
            )
        
        # Custom validation
        if self.custom_validator:
            try:
                value = self.custom_validator(value, field_name)
            except ValidationError:
                raise
            except Exception as e:
                raise ValidationError(str(e), field_name)
        
        return value
    
    def _validate_type(self, value, field_name: str):
        """Validate and coerce value to the expected type."""
        if self.field_type == str:
            if not isinstance(value, str):
                try:
                    value = str(value)
                except Exception:
                    raise ValidationError(f"{field_name} must be a string", field_name)
        
        elif self.field_type == int:
            if not isinstance(value, int) or isinstance(value, bool):
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    raise ValidationError(f"{field_name} must be an integer", field_name)
        
        elif self.field_type == float:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    raise ValidationError(f"{field_name} must be a number", field_name)
        
        elif self.field_type == bool:
            if not isinstance(value, bool):
                if value in (0, 1, '0', '1', 'true', 'false', 'True', 'False'):
                    value = value in (1, '1', 'true', 'True')
                else:
                    raise ValidationError(f"{field_name} must be a boolean", field_name)
        
        elif self.field_type == list:
            if not isinstance(value, list):
                raise ValidationError(f"{field_name} must be a list", field_name)
        
        elif self.field_type == dict:
            if not isinstance(value, dict):
                raise ValidationError(f"{field_name} must be an object", field_name)
        
        elif self.field_type == date:
            value = validate_date(value, field_name)
        
        elif self.field_type == datetime:
            value = validate_datetime(value, field_name)
        
        return value


# ============================================================================
# Schema Validation
# ============================================================================
def validate_request(schema: dict, data: dict = None):
    """Validate request body against a schema.
    
    Args:
        schema: Dict mapping field names to Field instances
        data: Optional data dict (defaults to request.get_json())
        
    Returns:
        Dict of validated data
        
    Raises:
        ValidationError: If validation fails
    """
    if data is None:
        data = request.get_json() or {}
    
    validated = {}
    errors = []
    
    for field_name, field in schema.items():
        value = data.get(field_name)
        try:
            validated[field_name] = field.validate(value, field_name)
        except ValidationError as e:
            errors.append({
                "field": field_name,
                "message": e.message
            })
    
    if errors:
        raise ValidationError(
            "Validation failed",
            details={"errors": errors}
        )
    
    return validated


# ============================================================================
# Common Validators
# ============================================================================
def validate_uuid(value: str, field_name: str = "id") -> str:
    """Validate a UUID string.
    
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        
    Returns:
        The validated UUID string
        
    Raises:
        ValidationError: If the value is not a valid UUID
    """
    if not value:
        raise ValidationError(f"{field_name} is required", field_name)
    
    try:
        # Validate and normalize UUID
        uuid.UUID(str(value))
        return str(value)
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} must be a valid UUID", field_name)


def validate_date(value, field_name: str = "date") -> date:
    """Validate and parse a date.
    
    Accepts:
        - date objects
        - ISO format strings (YYYY-MM-DD)
        
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        
    Returns:
        date object
        
    Raises:
        ValidationError: If the value is not a valid date
    """
    if value is None:
        return None
    
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    
    if isinstance(value, datetime):
        return value.date()
    
    if isinstance(value, str):
        try:
            # Handle ISO format YYYY-MM-DD
            return datetime.fromisoformat(value.split('T')[0]).date()
        except ValueError:
            pass
    
    raise ValidationError(
        f"{field_name} must be a valid date (YYYY-MM-DD format)",
        field_name
    )


def validate_datetime(value, field_name: str = "datetime") -> datetime:
    """Validate and parse a datetime.
    
    Accepts:
        - datetime objects
        - ISO format strings
        
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        
    Returns:
        datetime object
        
    Raises:
        ValidationError: If the value is not a valid datetime
    """
    if value is None:
        return None
    
    if isinstance(value, datetime):
        return value
    
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            pass
    
    raise ValidationError(
        f"{field_name} must be a valid datetime (ISO format)",
        field_name
    )


def validate_positive_number(
    value,
    field_name: str = "value",
    max_value: float = None,
    allow_zero: bool = True
) -> float:
    """Validate a positive number.
    
    Args:
        value: The value to validate
        field_name: Name of the field (for error messages)
        max_value: Optional maximum value
        allow_zero: Whether to allow zero (default True)
        
    Returns:
        float
        
    Raises:
        ValidationError: If validation fails
    """
    if value is None or value == "" or value == "null":
        return 0.0 if allow_zero else None
    
    try:
        num = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} must be a valid number", field_name)
    
    if not allow_zero and num == 0:
        raise ValidationError(f"{field_name} cannot be zero", field_name)
    
    if num < 0:
        raise ValidationError(f"{field_name} must be positive", field_name)
    
    if max_value is not None and num > max_value:
        raise ValidationError(f"{field_name} must be at most {max_value}", field_name)
    
    return num


def validate_string_length(
    value: str,
    field_name: str = "value",
    min_length: int = None,
    max_length: int = None,
    required: bool = False
) -> str:
    """Validate string length constraints.
    
    Args:
        value: The string to validate
        field_name: Name of the field (for error messages)
        min_length: Minimum length (optional)
        max_length: Maximum length (optional)
        required: Whether the field is required
        
    Returns:
        The (possibly truncated) string
        
    Raises:
        ValidationError: If validation fails
    """
    if value is None or value == "":
        if required:
            raise ValidationError(f"{field_name} is required", field_name)
        return None
    
    value = str(value).strip()
    
    if min_length and len(value) < min_length:
        raise ValidationError(
            f"{field_name} must be at least {min_length} characters",
            field_name
        )
    
    # Truncate if needed (soft enforcement)
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    return value


def validate_enum(value, choices: list, field_name: str = "value") -> str:
    """Validate that a value is in a list of choices.
    
    Args:
        value: The value to validate
        choices: List of valid choices
        field_name: Name of the field (for error messages)
        
    Returns:
        The validated value
        
    Raises:
        ValidationError: If the value is not in choices
    """
    if value is None:
        return None
    
    if value not in choices:
        raise ValidationError(
            f"{field_name} must be one of: {', '.join(str(c) for c in choices)}",
            field_name
        )
    
    return value


# ============================================================================
# Decorator for Route Validation
# ============================================================================
def validate_json_body(required_fields: list = None):
    """Decorator to ensure request has valid JSON body.
    
    Usage:
        @route.route("/example", methods=["POST"])
        @validate_json_body(["name", "email"])
        def example():
            data = request.get_json()
            # data is guaranteed to have "name" and "email" keys
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.is_json:
                return error_response(
                    "Request must be JSON",
                    ErrorCode.VALIDATION_ERROR,
                    400
                )
            
            data = request.get_json()
            if data is None:
                return error_response(
                    "Invalid JSON body",
                    ErrorCode.VALIDATION_ERROR,
                    400
                )
            
            if required_fields:
                missing = [f for f in required_fields if f not in data]
                if missing:
                    return error_response(
                        f"Missing required fields: {', '.join(missing)}",
                        ErrorCode.MISSING_FIELD,
                        400,
                        {"missing_fields": missing}
                    )
            
            return f(*args, **kwargs)
        return decorated
    return decorator
