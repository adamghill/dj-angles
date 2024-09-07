def get_wrapping_element_name(template_name: str) -> str:
    wrapping_element_name = (
        template_name.replace("/", "-")
        .replace("'", "")
        .replace('"', "")
        .replace("--", "-")
        .replace(" ", "-")
        .replace(":", "-")
    ).lower()
    wrapping_element_name = f"dj-{wrapping_element_name}"

    # Remove extensions
    if "." in wrapping_element_name:
        extension_idx = wrapping_element_name.index(".")
        wrapping_element_name = wrapping_element_name[0:extension_idx]

    # Remove shadow bang
    if wrapping_element_name.endswith("!"):
        wrapping_element_name = wrapping_element_name[:-1]

    return wrapping_element_name
