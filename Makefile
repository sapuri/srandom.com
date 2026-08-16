.PHONY: test serve format lint docker/up docker/down

test:
	uv run python manage.py test

serve:
	uv run python main.py

format:
	uv run autopep8 -ivr .

lint:
	uv run flake8 --show-source .

docker/up:
	docker compose up -d --build

docker/down:
	docker compose down
