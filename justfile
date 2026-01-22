import? 'adamghill.justfile'
import? '../dotfiles/just/justfile'

src := "src/dj_angles"

# List commands
_default:
    just --list --unsorted --justfile {{ justfile() }} --list-heading $'Available commands:\n'

# Grab default `adamghill.justfile` from GitHub
fetch:
  curl https://raw.githubusercontent.com/adamghill/dotfiles/master/just/justfile > adamghill.justfile

serve:
  uv run python3 example/manage.py runserver 0:8789

# Run all the dev things
dev:
  just lint
  just type
  just coverage
