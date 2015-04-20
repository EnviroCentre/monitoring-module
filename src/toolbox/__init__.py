import codecs
from hec.dssgui import ListSelection
from hec.script import MessageBox
from os import path
from toolbox.util import ValidationError
import yaml

class Tool(object):
    requiredParams = []
    
    def __init__(self, configFileName, dssFilePath=None):
        if dssFilePath:
            self.dssFilePath = dssFilePath
        else:
            self.dssFilePath = ListSelection.getMainWindow().getDSSFilename()
            
        self.configFilePath = path.join(path.dirname(self.dssFilePath), configFileName)
        
        if self._toolIsValid():
            configFile = codecs.open(self.configFilePath, encoding='utf-8')
            self.config = yaml.load(configFile.read()).next()
            configFile.close()
            self._configIsValid()
        
    def _toolIsValid(self):
        # Check if HEC-DSS db exists
        if not path.isfile(self.dssFilePath):
            error = ValidationError("Please open a HEC-DSS database first.")
            MessageBox.showError(error.message, "HEC-DSSVue")
            raise error
        
        # Check if config file exists
        if not path.isfile(self.configFilePath):
            error = ValidationError("The configuration file %s does not exist.\n\nPlease create this file and try again." % self.configFilePath)
            MessageBox.showError(error.message, "HEC-DSSVue")
            raise error
        
        return 1
    
    def _configIsValid(self):
        errors = [ValidationError("The parameter '%s' does not exist." % param) 
            for param in self.requiredParams if not param in self.config]

        if errors:
            self._displayConfigErrors(errors)
            raise ValidationError(errors)
        else:
            return 1
    
    def _displayConfigErrors(self, errors):
        message = "The configuration file %s is not valid.\nPlease check the content and try again." % self.configFilePath
        message += "\n"
        for error in errors:
            message += "\n - %s" % error.message
        MessageBox.showError(message, "HEC-DSSVue")

    def run(self):
        raise NotImplementedError()
    