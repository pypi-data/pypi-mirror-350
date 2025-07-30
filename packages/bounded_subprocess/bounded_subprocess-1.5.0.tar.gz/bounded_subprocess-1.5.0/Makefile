.PHONY: test

build:
	uv build

publish:
	 python3 -m twine upload dist/*

test:
	uv run python -m pytest
