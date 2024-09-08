.PHONY: all install clean test

clean:
	rm -rf docs/build
	rm -rf dist
	rm -f .coverage

build-requirements:
	pip install pip-tools
	pip-compile -o requirements.txt pyproject.toml
	pip-compile --extra dev -o dev-requirements.txt pyproject.toml

build: clean
	pip-sync requirements.txt dev-requirements.txt\

tag-release:
	commit-and-tag-version

tag-prerelease:
	commit-and-tag-version --prerelease alpha

upload: clean test
	python -m build
	twine upload dist/*

docs: clean
	cd docs && make html

test: clean
	pytest --cov=traffic_weaver --cov-report term-missing --cov-report html
	mkdir -p _images
	coverage-badge -f -o badges/coverage.svg
