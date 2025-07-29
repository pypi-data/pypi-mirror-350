from __future__ import annotations

import datetime
import importlib.metadata

project = "isqtools"
author = "Yusheng Yang, Guolong Cui"
copyright = f"{datetime.date.today().year}, Arclight Quantum"
version = release = importlib.metadata.version("isqtools")
# version = release = "0.1.13"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "nbsphinx",
]

myst_enable_extensions = [
    "amsmath",
    "dollarmath",
    "deflist",
    "colon_fence",
]

todo_include_todos = True
napoleon_google_docstring = True
napoleon_numpy_docstring = True
copybutton_prompt_text = r">>> |\$ "
copybutton_prompt_is_regexp = True

nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]
nbsphinx_prompt_width = "0"

source_suffix = [".rst", ".md"]
exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    ".venv",
]


pygments_style = "colorful"
add_module_names = False
numfig = True
numfig_format = {"table": "Table %s"}
language = "en"


autoclass_content = "both"
always_document_param_types = True

html_theme = "furo"
html_title = f"{project} {version}"
html_theme_options = {}
html_context = {"copyright": copyright}
html_last_updated_fmt = datetime.datetime.now().strftime("%b %d, %Y")
html_static_path = ["_static"]
html_css_files = ["custom.css"]

pygments_style = "default"  # Light mode friendly style
pygments_dark_style = "monokai"  # Optional dark mode style


nitpick_ignore = [
    ("py:class", "_io.StringIO"),
    ("py:class", "_io.BytesIO"),
]

# inter sphinx examples
# intersphinx_mapping = {
#     "python": ("https://docs.python.org/3", None),
# }
