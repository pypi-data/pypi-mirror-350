# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from omicron_gap._version import __version__

sys.path.insert(0, os.path.abspath('../'))

project = 'omicron-gap'
copyright = '2023, Joseph Areeda'
author = 'Joseph Areeda'
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_rtd_theme",
              'sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.mathjax',
              'numpydoc',
              'sphinx_tabs.tabs',
              "sphinx.ext.viewcode",
              'sphinx.ext.napoleon',
              'sphinxcontrib.programoutput',
              'sphinx.ext.intersphinx',
              ]
autodoc_default_options = {'autosummary': True,
                           "members": True,
                           "inherited-members": True,
                           "private-members": True,
                           "show-inheritance": True,
                           }
autoclass_content = "both"
autosummary_generate = True
napoleon_numpy_docstring = False
napoleon_use_rtype = False

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
numfig = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'display_version': True,
    # TOC options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False

}

