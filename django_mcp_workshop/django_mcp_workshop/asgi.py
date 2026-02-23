"""
ASGI config for django_mcp_workshop project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_mcp_workshop.settings.local")

application = get_asgi_application()
