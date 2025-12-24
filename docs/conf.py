import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "TorHost"
author = "ByteBreach"
release = "0.0.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_title = "TorHost Documentation"
