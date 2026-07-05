import? 'adamghill.justfile'
import? '../dotfiles/just/justfile'

src := "src/dj_angles"

# List commands
_default:
    just --list --unsorted --justfile {{ justfile() }} --list-heading $'Available commands:\n'

# Grab default `adamghill.justfile` from GitHub
fetch:
  curl https://raw.githubusercontent.com/adamghill/dotfiles/master/just/justfile > adamghill.justfile

# Run coverage on the code
coverage *ARGS='':
  -uv run --all-extras pytest --cov=. --ignore=benchmarks {{ ARGS }}

serve:
  uv run python3 example/manage.py runserver 0:8789

# Check the types in the project
type *ARGS='.':
  -uv run --all-extras ty check {{ ARGS }}
