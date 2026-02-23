"""
Production settings. Load with DJANGO_SETTINGS_MODULE=django_mcp_workshop.settings.production
Use environment variables for SECRET_KEY, ALLOWED_HOSTS, DATABASES, etc.
"""
from .base import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = []  # Set via env, e.g. ALLOWED_HOSTS=example.com,api.example.com

# SECRET_KEY must be set via environment in production
# SECURITY: Ensure SECRET_KEY, DB credentials, and other secrets come from env

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# HTTPS (enable when behind TLS)
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
