"""
Health check views for /health/ and /ready/.
"""
from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Basic liveness: returns 200 if the app is running."""

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return JsonResponse({"status": "ok", "message": "OK"})


class ReadinessCheckView(APIView):
    """Readiness: checks DB (and optionally cache). Returns 200 if ready to serve traffic."""

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            connection.ensure_connection()
        except Exception:
            return JsonResponse(
                {"status": "error", "message": "Database unavailable"},
                status=503,
            )
        return JsonResponse({"status": "ok", "message": "Ready"})
