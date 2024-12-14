.PHONY: check
check: lint test

.PHONY: lint
lint:
	uv run ruff format src/
	uv run ruff check --fix --show-fixes src/
	uv run mypy src/

.PHONY: pre-commit
pre-commit:
	pre-commit install --hook-type commit-msg

.PHONY: test
test:
	uv run pytest src/

.PHONY: migrations-postgres
migrations-postgres:
	cd migrations/postgres && flyway migrate

.PHONY: migrations-sqlite
migrations-sqlite:
	cd migrations/sqlite &&	flyway migrate

.PHONY: migrations
migrations: migrations-postgres migrations-sqlite

.PHONY: release
release:
	uv run cz bump
	git push
	git push --tags
