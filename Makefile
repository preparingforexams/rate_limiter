.PHONY: check
check: lint test

.PHONY: lint
lint:
	poetry run ruff format src/
	poetry run ruff check --fix --show-fixes src/
	poetry run mypy src/

.PHONY: pre-commit
pre-commit:
	pre-commit install --hook-type commit-msg

.PHONY: test
test:
	poetry run pytest src/

.PHONY: migrations-postgres
migrations-postgres:
	cd migrations/postgres && flyway migrate

.PHONY: migrations-sqlite
migrations-sqlite:
	cd migrations/sqlite &&	flyway migrate

.PHONY: migrations
migrations: migrations-postgres migrations-sqlite
