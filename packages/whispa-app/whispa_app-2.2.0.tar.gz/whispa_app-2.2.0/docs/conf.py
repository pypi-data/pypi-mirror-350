"""Sphinx configuration for Whispa App documentation."""

import os
import sys
from datetime import datetime

# Add source directory to path
sys.path.insert(0, os.path.abspath("../src"))

# Project information
project = "Whispa App"
copyright = "2025, Your Organization"
author = "Your Organization"

# The full version, including alpha/beta/rc tags
release = "2.2.0"
version = ".".join(release.split(".")[:2])

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints"
]

# Add mappings to Python documentation
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
}

# Add any paths that contain templates
templates_path = ["_templates"]

# List of patterns to exclude
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The theme to use
html_theme = "sphinx_rtd_theme"

# Theme options
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
}

# Add any paths that contain custom static files
html_static_path = ["_static"]

# Custom sidebar templates
html_sidebars = {
    "**": [
        "relations.html",
        "searchbox.html",
        "navigation.html",
    ]
}

# Output options
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# Extension settings
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_format = "short"

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

html_title = f'Whispa App {version} Documentation' 