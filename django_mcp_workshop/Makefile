.PHONY: install run migrate test lint format shell clean

install:
	pip install -r requirements/local.txt

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	pytest

lint:
	flake8 .
	black --check .
	isort --check-only .

format:
	black .
	isort .

shell:
	python manage.py shell

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov 2>/dev/null || true
