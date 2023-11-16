.DEFAULT_GOAL := fetch

.PHONY: fetch
fetch:
	poetry run python fireflies.py fetch

.PHONY: format
format:
	poetry run black .
	poetry run isort .
	poetry run ruff --fix .

.PHONY: lint
lint:
	poetry run black --check .
	poetry run isort -c .
	poetry run ruff check .
