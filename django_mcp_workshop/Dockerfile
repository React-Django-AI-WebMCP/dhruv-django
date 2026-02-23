# Multi-stage production Dockerfile
FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Non-root user
RUN addgroup --system app && adduser --system --group app

# Dependencies
COPY requirements/production.txt requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

COPY --chown=app:app . .

USER app

EXPOSE 8000

# Default: run gunicorn; override CMD for migrations etc.
CMD ["gunicorn", "django_mcp_workshop.wsgi:application", "-b", "0.0.0.0:8000", "-w", "2", "-k", "sync"]
