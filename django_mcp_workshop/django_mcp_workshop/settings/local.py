"""
Local/development settings. Load with DJANGO_SETTINGS_MODULE=django_mcp_workshop.settings.local
"""
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# Use default SECRET_KEY in local; set in .env for production
SECRET_KEY = "django-insecure-dev-key-change-in-production"

# Optional: django-debug-toolbar, CORS for local frontend, etc. can be added here
