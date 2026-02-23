"""
Unified API response structure for success and error responses.
"""
from rest_framework.response import Response


def success_response(data=None, message: str = "OK", status_code: int = 200) -> Response:
    """Return a consistent success JSON: status, message, data."""
    payload = {"status": status_code, "message": message, "data": data}
    return Response(payload, status=status_code)


def error_response(
    message: str = "Error",
    *,
    errors: dict | None = None,
    error_code: str | None = None,
    status_code: int = 400,
) -> Response:
    """Return a consistent error JSON: status, message, optional errors and error_code."""
    payload: dict = {"status": status_code, "message": message}
    if errors is not None:
        payload["errors"] = errors
    if error_code is not None:
        payload["error_code"] = error_code
    return Response(payload, status=status_code)
