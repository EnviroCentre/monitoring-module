import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))

needs_sphinx = '1.3'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
]

autodoc_mock_imports = ['hec', 'hec.dssgui', 'hec.heclib', 'hec.heclib.util', 'hec.io', 'hec.script']
autodoc_member_order = 'bysource'
autoclass_content = 'both'

source_suffix = '.rst'
master_doc = 'index'

project = 'HEC-DSS Monitoring Module'
copyright = '2015, EnviroCentre'
version = '0.1'
release = '0.1.0'
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
#html_theme = 'classic'
html_static_path = ['_static']
html_last_updated_fmt = '%d/%m/%Y'
html_show_sourcelink = False
html_show_sphinx = False
htmlhelp_basename = 'doc'
