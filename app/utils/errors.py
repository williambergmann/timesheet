"""
API Error Handling Module (REQ-035)

Provides standardized error responses and exception handling.

Error response format:
{
    "error": "Human-readable error message",
    "code": "ERROR_CODE",
    "details": { ... optional details ... },
    "request_id": "uuid"  // if available
}
"""

import uuid
import traceback
from functools import wraps
from flask import request, g, current_app


# ============================================================================
# Error Codes
# ============================================================================
class ErrorCode:
    """Standardized error codes for API responses."""
    
    # Validation errors (400)
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_DATE = "INVALID_DATE"
    INVALID_UUID = "INVALID_UUID"
    INVALID_TYPE = "INVALID_TYPE"
    MISSING_FIELD = "MISSING_FIELD"
    FIELD_TOO_LONG = "FIELD_TOO_LONG"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    INVALID_ENUM = "INVALID_ENUM"
    
    # Authentication errors (401)
    UNAUTHORIZED = "UNAUTHORIZED"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    
    # Authorization errors (403)
    FORBIDDEN = "FORBIDDEN"
    CSRF_ERROR = "CSRF_ERROR"
    RATE_LIMITED = "RATE_LIMITED"
    
    # Not found errors (404)
    NOT_FOUND = "NOT_FOUND"
    TIMESHEET_NOT_FOUND = "TIMESHEET_NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    ATTACHMENT_NOT_FOUND = "ATTACHMENT_NOT_FOUND"
    
    # Conflict errors (409)
    ALREADY_EXISTS = "ALREADY_EXISTS"
    INVALID_STATUS = "INVALID_STATUS"
    
    # Server errors (500)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"


# ============================================================================
# Custom Exceptions
# ============================================================================
class APIError(Exception):
    """Base API exception with standardized format."""
    
    def __init__(
        self,
        message: str,
        code: str = ErrorCode.INTERNAL_ERROR,
        status_code: int = 500,
        details: dict = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
    
    def to_dict(self):
        """Convert to standardized error response format."""
        response = {
            "error": self.message,
            "code": self.code,
        }
        
        if self.details:
            response["details"] = self.details
        
        # Include request ID if available
        if hasattr(g, 'request_id'):
            response["request_id"] = g.request_id
        
        return response


class ValidationError(APIError):
    """Raised when request validation fails."""
    
    def __init__(self, message: str, field: str = None, details: dict = None):
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            status_code=400,
            details={"field": field, **(details or {})} if field else details
        )


class NotFoundError(APIError):
    """Raised when a resource is not found."""
    
    def __init__(self, resource: str, resource_id: str = None):
        message = f"{resource} not found"
        code_map = {
            "Timesheet": ErrorCode.TIMESHEET_NOT_FOUND,
            "User": ErrorCode.USER_NOT_FOUND,
            "Attachment": ErrorCode.ATTACHMENT_NOT_FOUND,
        }
        super().__init__(
            message=message,
            code=code_map.get(resource, ErrorCode.NOT_FOUND),
            status_code=404,
            details={"resource": resource, "id": resource_id} if resource_id else None
        )


class ForbiddenError(APIError):
    """Raised when access is denied."""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            code=ErrorCode.FORBIDDEN,
            status_code=403
        )


class ConflictError(APIError):
    """Raised when there's a conflict (e.g., duplicate entry)."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            code=ErrorCode.ALREADY_EXISTS,
            status_code=409,
            details=details
        )


class InvalidStatusError(APIError):
    """Raised when an operation is invalid for the current status."""
    
    def __init__(self, message: str, current_status: str = None):
        super().__init__(
            message=message,
            code=ErrorCode.INVALID_STATUS,
            status_code=400,
            details={"current_status": current_status} if current_status else None
        )


# ============================================================================
# Request ID Middleware
# ============================================================================
def init_request_id():
    """Initialize request ID for the current request.
    
    Should be called at the start of each request.
    Uses X-Request-ID header if provided, otherwise generates a new UUID.
    """
    request_id = request.headers.get('X-Request-ID')
    if not request_id:
        request_id = str(uuid.uuid4())[:8]  # Short request ID
    g.request_id = request_id


def get_request_id():
    """Get the current request ID."""
    return getattr(g, 'request_id', None)


# ============================================================================
# Error Response Helpers
# ============================================================================
def error_response(
    message: str,
    code: str = ErrorCode.VALIDATION_ERROR,
    status_code: int = 400,
    details: dict = None
):
    """Create a standardized error response tuple.
    
    Usage:
        return error_response("Invalid date format", code=ErrorCode.INVALID_DATE)
    """
    response = {
        "error": message,
        "code": code,
    }
    
    if details:
        response["details"] = details
    
    if hasattr(g, 'request_id'):
        response["request_id"] = g.request_id
    
    return response, status_code


def validation_error(message: str, field: str = None):
    """Shortcut for validation error response."""
    details = {"field": field} if field else None
    return error_response(message, ErrorCode.VALIDATION_ERROR, 400, details)


def not_found(resource: str = "Resource"):
    """Shortcut for not found error response."""
    code_map = {
        "Timesheet": ErrorCode.TIMESHEET_NOT_FOUND,
        "User": ErrorCode.USER_NOT_FOUND,
        "Attachment": ErrorCode.ATTACHMENT_NOT_FOUND,
    }
    return error_response(
        f"{resource} not found",
        code_map.get(resource, ErrorCode.NOT_FOUND),
        404
    )


# ============================================================================
# Global Exception Handlers
# ============================================================================
def register_error_handlers(app):
    """Register global error handlers with the Flask app.
    
    Call this in your app factory after creating the Flask app.
    """
    
    @app.before_request
    def before_request():
        """Initialize request ID for each request."""
        init_request_id()
    
    @app.after_request
    def after_request(response):
        """Add request ID to response headers."""
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        return response
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors."""
        current_app.logger.warning(
            f"API Error [{error.code}]: {error.message}",
            extra={
                "request_id": get_request_id(),
                "code": error.code,
                "status_code": error.status_code,
                "path": request.path,
                "method": request.method,
            }
        )
        return error.to_dict(), error.status_code
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 Bad Request errors."""
        return error_response(
            str(error.description) if error.description else "Bad request",
            ErrorCode.VALIDATION_ERROR,
            400
        )
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle 401 Unauthorized errors."""
        return error_response(
            "Authentication required",
            ErrorCode.UNAUTHORIZED,
            401
        )
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle 403 Forbidden errors."""
        return error_response(
            str(error.description) if error.description else "Access denied",
            ErrorCode.FORBIDDEN,
            403
        )
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found errors."""
        return error_response(
            "Resource not found",
            ErrorCode.NOT_FOUND,
            404
        )
    
    @app.errorhandler(429)
    def handle_rate_limit(error):
        """Handle 429 Too Many Requests errors."""
        return error_response(
            "Too many requests. Please try again later.",
            ErrorCode.RATE_LIMITED,
            429
        )
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 Internal Server errors."""
        # Log the full traceback for debugging
        current_app.logger.error(
            f"Internal Server Error: {str(error)}",
            extra={
                "request_id": get_request_id(),
                "path": request.path,
                "method": request.method,
                "traceback": traceback.format_exc(),
            }
        )
        return error_response(
            "An unexpected error occurred",
            ErrorCode.INTERNAL_ERROR,
            500
        )
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unhandled exceptions."""
        # Don't hide HTTP exceptions
        if hasattr(error, 'code'):
            raise error
        
        # Log the full traceback
        current_app.logger.error(
            f"Unhandled Exception: {type(error).__name__}: {str(error)}",
            extra={
                "request_id": get_request_id(),
                "path": request.path,
                "method": request.method,
                "traceback": traceback.format_exc(),
            }
        )
        
        # In debug mode, re-raise to show full traceback
        if current_app.debug:
            raise error
        
        return error_response(
            "An unexpected error occurred",
            ErrorCode.INTERNAL_ERROR,
            500
        )
