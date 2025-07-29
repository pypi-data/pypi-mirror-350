#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import importlib.metadata

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.graphviz',
    'sphinx_autodoc_typehints',
    'sphinx_sitemap',
    'nbsphinx']

graphviz_output_format = 'svg'
templates_path = ['_templates']
default_role = 'code'
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
todo_include_todos = True

# Collect basic information from main module
metadata = importlib.metadata.metadata('calorine')
version = metadata['version']
release = ''
copyright = '2025'
project = metadata['name']
author = metadata['maintainer']

site_url = 'https://calorine.materialsmodeling.org/'
html_css_files = ['custom.css']
html_logo = '_static/logo.png'
html_favicon = '_static/logo.ico'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_context = {
    'current_version': version,
    'versions':
        [('latest stable release',
          '{}'.format(site_url)),
         ('development version',
          '{}/dev'.format(site_url))]}
htmlhelp_basename = 'calorinedoc'
intersphinx_mapping = \
    {'ase':     ('https://wiki.fysik.dtu.dk/ase', None),
     'numpy':   ('https://numpy.org/doc/stable/', None),
     'h5py':    ('http://docs.h5py.org/en/latest/', None),
     'scipy':   ('https://scipy.github.io/devdocs/', None),
     'sklearn': ('https://scikit-learn.org/stable', None)}

# Settings for nbsphinx
nbsphinx_execute = 'never'

# Options for LaTeX output
_PREAMBLE = r"""
\usepackage{amsmath,amssymb}
\renewcommand{\vec}[1]{\boldsymbol{#1}}
\DeclareMathOperator*{\argmin}{\arg\!\min}
\DeclareMathOperator{\argmin}{\arg\!\min}
"""

latex_elements = {
    'preamble': _PREAMBLE,
}
latex_documents = [
    (master_doc, 'calorine.tex', 'calorine Documentation',
     'The calorine developer team', 'manual'),
]


# Options for manual page output
man_pages = [
    (master_doc, 'calorine', 'calorine Documentation',
     [author], 1)
]


# Options for Texinfo output
texinfo_documents = [
    (master_doc, 'calorine', 'calorine Documentation',
     author, 'calorine', 'Strong coupling calculator',
     'Miscellaneous'),
]
