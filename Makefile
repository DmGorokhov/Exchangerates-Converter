install:
	 poetry install

migrations:
	 docker exec -it app alembic revision --autogenerate

build:
	docker compose build

setup: install build

start-dev:
	docker compose up

start-server:
	poetry run uvicorn src.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

test:
	poetry run pytest

lint:
	poetry run flake8 .

