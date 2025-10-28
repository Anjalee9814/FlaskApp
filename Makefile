# Makefile for common tasks
.PHONY: build up down logs test-unit test-integration initdb

build:
	docker-compose build --no-cache

up:
	docker-compose up --build -d

down:
	docker-compose down

logs:
	docker-compose logs -f

initdb:
	docker-compose run --rm initdb

test-unit:
	# Run unit tests using the venv python
	if [ -f app/.venv/bin/python ]; then \
		app/.venv/bin/python -m pytest -q app/tests/test_app.py; \
	else \
		python -m pytest -q app/tests/test_app.py; \
	fi

test-integration:
	# Bring up the stack, run integration test, tear down
	docker-compose up --build -d
	python -m pytest -q app/tests/test_integration.py
	docker-compose down
