set quiet
set dotenv-load
set export

# List commands
_default:
    just --list --unsorted --justfile {{justfile()}} --list-heading $'Available commands:\n'
  
# Install dependencies
bootstrap:
  uv install

# Set up the project
setup:
  curl -LsSf https://astral.sh/uv/install.sh | sh
  uv tool install ruff
  uv tool install build
  uv tool install twine

# Update the project
update:
  uv sync

# Lock the dependencies
lock:
  uv sync

# Lint the project
lint *ARGS='.':
  -uvx ruff check {{ ARGS }}

# Check the types in the project
type *ARGS='.':
  -uv run mypy {{ ARGS }}  # need to run through uv to see installed dependencies

# Benchmark the project
benchmark:
  -uv run pytest tests/benchmarks/ --benchmark-only --benchmark-compare

# Run the tests
test *ARGS='':
  -uv run pytest {{ ARGS }}

alias t := test

# Run coverage on the code
coverage:
  -uv run pytest --cov=src/dj_angles

# Run all the dev things
dev:
  just lint
  just type
  just coverage

serve:
  uv run python3 example/manage.py migrate
  uv run python3 example/manage.py runserver 0:8789

# Build the package
build:
  just test
  just build-docs
  rm -f dist/*
  uvx --from build pyproject-build --installer uv

# Build and publish the package to test PyPI and prod PyPI
publish:
  just build
  uvx twine check dist/*
  uvx twine upload -r testpypi dist/*
  uvx twine upload -r pypi dist/*

# Run documentation site
serve-docs:
  uv run sphinx-autobuild -W docs/source docs/build

# Build documentation site
build-docs:
  cp CHANGELOG.md docs/source/changelog.md
  uv run sphinx-build -W docs/source docs/build
