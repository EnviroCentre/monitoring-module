from hec.dssgui import ListSelection
from hec.script import MessageBox
from os import path
import yaml
import codecs

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
            error = ValueError("Please open a HEC-DSS database first.")
            MessageBox.showError(str(error), "HEC-DSSVue")
            raise error
        
        # Check if config file exists
        if not path.isfile(self.configFilePath):
            error = ValueError("The configuration file %s does not exist.\n\nPlease create this file and try again." % self.configFilePath)
            MessageBox.showError(str(error), "HEC-DSSVue")
            raise error
        
        return 1
    
    def _configIsValid(self):
        errors = []

        for param in self.requiredParams:
            if not param in self.config:
                errors.append(ValueError("The parameter '%s' does not exist." % param))

        if errors:
            self._displayConfigErrors(errors)
            raise errors
        else:
            return 1
    
    def _displayConfigErrors(self, errors):
        message = "The configuration file %s is not valid.\nPlease check the content and try again." % self.configFilePath
        message += "\n"
        for error in errors:
            message += "\n - %s" % error
        MessageBox.showError(message, "HEC-DSSVue")

    def run(self):
        raise NotImplementedError()
    