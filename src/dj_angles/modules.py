from importlib.util import find_spec


def is_module_available(module_name):
    """Helper method to check if a module is available."""

    return find_spec(module_name) is not None
