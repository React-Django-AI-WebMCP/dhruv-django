"""
Custom exception classes and DRF exception handler for consistent error responses.
"""
import logging

from rest_framework.views import exception_handler

from core.responses import error_response

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "API_ERROR",
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(APIError):
    """Resource not found."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, error_code="NOT_FOUND", status_code=404)


class ValidationError(APIError):
    """Request validation failed."""

    def __init__(
        self,
        message: str = "Validation failed",
        *,
        errors: dict | None = None,
    ) -> None:
        super().__init__(message, error_code="VALIDATION_ERROR", status_code=400)
        self.errors = errors or {}


def custom_exception_handler(exc, context):
    """
    DRF exception handler that returns consistent JSON and handles APIError.
    """
    if isinstance(exc, APIError):
        return error_response(
            message=exc.message,
            errors=getattr(exc, "errors", None),
            error_code=exc.error_code,
            status_code=exc.status_code,
        )

    # Let DRF handle known exceptions (e.g. ValidationError from serializers)
    response = exception_handler(exc, context)
    if response is not None:
        # Optionally normalize response body to our format
        return error_response(
            message=str(exc) or "Request failed",
            errors=response.data if isinstance(response.data, dict) else None,
            status_code=response.status_code,
        )

    # Unexpected error: log and return 500
    logger.exception("Unhandled exception", exc_info=exc)
    return error_response(
        message="An internal error occurred",
        error_code="INTERNAL_ERROR",
        status_code=500,
    )
