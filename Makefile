.DEFAULT_GOAL := all

.PHONY: all
all: fetch delete

.PHONY: fetch
fetch:
	poetry run python src/fireflies.py fetch

.PHONY: delete
delete:
	poetry run python src/fireflies.py delete

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
