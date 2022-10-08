# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../.'))
sys.setrecursionlimit(1500)

# -- Project information -----------------------------------------------------

project = 'acequia'
copyright = '2022, Thomas de Meij'
author = 'Thomas de Meij'

# The full version, including alpha/beta/rc tags
release = '0.03'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
   'sphinx.ext.autodoc', 
   'sphinx.ext.coverage',
   ##'nbsphinx',
   'sphinx.ext.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'nature'
#html_theme = 'alabaster'
#html_theme = 'bizstyle'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

"""
#import sphinx_rtd_theme
html_theme = 'sphinxdoc'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}
"""

#autodoc_mock_imports = [
#    'math','numpy','pandas','csv','errno','requests','pkgutil','io',
#    'matplotlib','matplotlib.pyplot','matplotlib.dates',
#    'warnings','scipy','scipy.stats','statsmodels.api',
#    'statsmodels.graphics.tsaplots','statsmodels.tsa.stattools',
#    'collections','os','os.path','json','shapefile','time',
#    'datetime','logging','seaborn','simplekml',]
autoclass_content = "class" #"both"
autodoc_member_order = 'bysource'