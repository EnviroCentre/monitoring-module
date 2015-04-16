# name=Import field data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from hec.dssgui import ListSelection
from hec.script import MessageBox
from monitoring import dataimport
import os.path
import yaml

CONFIG_FILE = 'field_import.yml'
DSS_FILE = ListSelection.getMainWindow().getDSSFilename()

def validateConfig(config, errors=[]):
    valid = 1
    try:
        pass
    except:
        valid = 0
    return valid

if not DSS_FILE:
    MessageBox.showError("Please open an HEC-DSS database first.", "HEC-DSSVue")
    raise ValueError("No HEC-DSS database file open.")

configFilePath = os.path.join(os.path.dirname(DSS_FILE), CONFIG_FILE)
if not os.path.isfile(configFilePath):
    MessageBox.showError("The configuration file %s does not exist.\n\nPlease create this file and try again." % configFilePath, 
                         "HEC-DSSVue")
    raise ValueError("Cannot find config file %s" % configFilePath)

config = yaml.load(open(configFilePath).read()).next()
errors = []
if validateConfig(config, errors):
    dataimport.locationsAcross(config, DSS_FILE)
else:
    MessageBox.showError("The configuration file %s is not valid. Please check the content and try again." % configFilePath,
                         "HEC-DSSVue")
    raise errors
