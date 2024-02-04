# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from traffic_weaver import __version__

project = 'traffic_weaver'
copyright = '2024, Piotr T. Lechowicz'
author = 'Piotr T. Lechowicz'
version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'sphinx_mdinclude',
]

# configuration ----
templates_path = ['_templates']
exclude_patterns = []
numfig = True

# -- Options for HTML output -----------
# --------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "_static/gfx/logo.png"

html_theme_options = {
    'collapse_navigation': False,
    # 'titles_only': False
}

# configuration sphinx.ext.napoleon ----
napoleon_google_docstring = False
napoleon_use_param = True
napoleon_use_ivar = True

# configuration sphinx.ext.autodoc ----
autodoc_member_order = 'bysource'   # do not sort methods from files
autodoc_default_options = {"exclude-members": '_abc_impl'}
autoclass_content = 'both'  # Both the class’ and the __init__ method’s docstring are concatenated and inserted.

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

