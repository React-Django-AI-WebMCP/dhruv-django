"""
URL configuration for django_mcp_workshop project. Include app URLs here.
"""
from django.contrib import admin
from django.urls import path

from core.views import HealthCheckView, ReadinessCheckView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="health"),
    path("ready/", ReadinessCheckView.as_view(), name="ready"),
]
