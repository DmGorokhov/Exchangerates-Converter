install:
	 poetry install

migrations:
	 docker exec -it app alembic revision --autogenerate

build:
	docker compose build

setup: install build

start:
	docker compose up

start-d:
	docker compose up -d

stop:
	docker compose stop

lint:
	poetry run flake8 .

