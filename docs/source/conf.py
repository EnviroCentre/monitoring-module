# -*- coding: utf-8 -*-

import os
from subprocess import check_output
import sys

git_args = ['git', 'describe', '--tags', '--always']
git_tag = check_output(git_args, universal_newlines=True)

sys.path.insert(0, os.path.abspath('../../src'))

needs_sphinx = '1.3'

extensions = [
    'sphinx.ext.autodoc',
]

autodoc_mock_imports = [
    'hec', 
    'hec.dssgui', 
    'hec.heclib', 'hec.heclib.util', 
    'hec.io', 
    'hec.script'
]
autodoc_member_order = 'bysource'
autoclass_content = 'both'

source_suffix = '.rst'
master_doc = 'index'

project = 'Monitoring Module for HEC-DSSVue'
copyright = '2015, EnviroCentre. All rights reserved.'
version = '.'.join(git_tag.strip('v').split(".")[0:2])
release = git_tag.strip('v')
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']
html_last_updated_fmt = '%d/%m/%Y'
html_show_sourcelink = False
html_copy_source = False
html_show_sphinx = False
htmlhelp_basename = 'doc'
