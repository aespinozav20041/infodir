.PHONY: lint test run

lint:
	pre-commit run --all-files

test:
	pytest

run:
	uvicorn api.app:app --reload
