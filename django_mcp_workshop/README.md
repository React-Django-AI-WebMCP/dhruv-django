# Django MCP Workshop

Django REST API project with a production-ready skeleton: split settings, core app, health checks, and Docker.

## Features

- **Split settings**: `django_mcp_workshop.settings.base`, `django_mcp_workshop.settings.local`, `django_mcp_workshop.settings.production`
- **Core app**: Shared logic, unified responses, custom exception handler, health/ready endpoints
- **Health checks**: `GET /health/` (liveness), `GET /ready/` (readiness, DB check)
- **Requirements**: `requirements/base.txt`, `local.txt`, `production.txt`
- **Docker**: Dockerfile and docker-compose (web + PostgreSQL)

## Quick start

```bash
# Create venv and install
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements/local.txt

# Copy env and run
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

- **Health**: http://127.0.0.1:8000/health/
- **Ready**: http://127.0.0.1:8000/ready/
- **Admin**: http://127.0.0.1:8000/admin/

## Settings

- Default for runserver: `django_mcp_workshop.settings.local` (set in `manage.py` and `django_mcp_workshop/wsgi.py`).
- Production: set `DJANGO_SETTINGS_MODULE=django_mcp_workshop.settings.production` and configure `.env` (SECRET_KEY, ALLOWED_HOSTS, DB, etc.).

## Project structure

```
├── django_mcp_workshop/   # Project package (original)
│   ├── settings/         # base.py, local.py, production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                 # Shared app (responses, exceptions, health, models)
├── requirements/
├── logs/
├── manage.py
├── Dockerfile
└── docker-compose.yml
```

## Adding new apps

```bash
python manage.py startapp myapp
```

Add to `INSTALLED_APPS` in `django_mcp_workshop/settings/base.py`, then add `serializers.py`, `services.py`, `urls.py`, and include app URLs in `django_mcp_workshop/urls.py`.

## Code quality

- Format: `make format` or `black . && isort .`
- Lint: `make lint` or `flake8 .`
- Tests: `make test` or `pytest`

See `CONTRIBUTING.md` for git workflow and commit conventions.
