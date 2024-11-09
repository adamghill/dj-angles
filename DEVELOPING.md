# Developing

1. Install `uv`
1. `uv sync --all-extras`

# Publishing

1. `just dev`
1. Update version in `pyproject.toml`
1. Update `CHANGELOG.md`
1. `just docs-build`
1. Commit and tag with a version
1. `git push --tags origin main`
1. Go to https://github.com/adamghill/dj-angles/releases and create a new release with the same version
1. This will kick off the https://github.com/adamghill/dj-angles/actions/workflows/publish.yml GitHub Action
