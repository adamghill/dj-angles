# Configuration file for the Sphinx documentation builder.

import toml

# -- Project information

project = "dj-angles"
copyright = "2024, Adam Hill"  # noqa: A001
author = "Adam Hill"

pyproject = toml.load("../../pyproject.toml")
version = pyproject["project"]["version"]
release = version


# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx_inline_tabs",
    "autoapi.extension",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "furo"

# -- Options for EPUB output
epub_show_urls = "footnote"

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 3

myst_heading_anchors = 3
myst_enable_extensions = ["linkify", "colon_fence"]


autoapi_dirs = [
    "../../src/dj_angles",
]
autoapi_root = "api"
autoapi_add_toctree_entry = False
autoapi_generate_api_docs = True
# autoapi_keep_files = True  # useful for debugging generated errors
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
]
autoapi_type = "python"
autodoc_typehints = "signature"
