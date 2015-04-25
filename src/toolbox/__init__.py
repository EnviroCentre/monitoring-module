import codecs
from hec.script import MessageBox
from os import path
from toolbox.util import ValidationError
import yaml

class Tool(object):
    """
    A tool for undertaking tasks in HEC-DSSVue.
    """
    
    #: List of parameters/keys required in the config file.
    requiredParams = []
    #: Whether to refresh the HEC-DSSVue catalogue after completing the task.
    refreshCatalogue = 0
    
    def __init__(self, configFileName, dssFilePath=None):
        """
        A tool is defined by providing a `yaml` configuration file ``configFileName`` and a HEC-DSS database
        ``dssFilePath`` to operate on. If ``dssFilePath`` is not set, the active DSS-file in the HEC-DSSVue
        window will be used.
        
        The attribute :attr:`.config` will be set containing the parsed yaml config file.
        """
        
        if dssFilePath:
            self.dssFilePath = dssFilePath
            self.mainWindow = None
        else:
            from hec.dssgui import ListSelection
            self.mainWindow = ListSelection.getMainWindow()
            self.dssFilePath = self.mainWindow.getDSSFilename()
        
        #: Message to be displayed in HEC-DSSVue after running the tool. This attribute is typically set in the 
        #: :meth:`main`.
        self.message = ""
        
        self.configFilePath = path.join(path.dirname(self.dssFilePath), configFileName)
        
        if self._toolIsValid():
            configFile = codecs.open(self.configFilePath, encoding='utf-8')
            self.config = yaml.load(configFile.read()).next()
            configFile.close()
            self._configIsValid()
        
    def _toolIsValid(self):
        """
        Check if the tool is configured correctly with a valid config file and HEC-DSS database.
        """
        
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
        """
        Validate config file content.
        
        Currently checks for existence of required top-level config parameters/keys only as specified in 
        :attr:`.requiredParams`.
        """
        
        errors = [ValidationError("The parameter '%s' does not exist." % param) 
            for param in self.requiredParams if not param in self.config]

        if errors:
            self._displayConfigErrors(errors)
            raise ValidationError(errors)
        else:
            return 1
    
    def _displayConfigErrors(self, errors):
        """
        Display configuration errors in the HEC-DSSVue window.
        """
        
        message = "The configuration file %s is not valid.\nPlease check the content and try again." % self.configFilePath
        message += "\n"
        for error in errors:
            message += "\n - %s" % error.message
        MessageBox.showError(message, "HEC-DSSVue")

    def run(self):
        """
        Main tool execution method.
        
        This method should be called after instantiating the tool to run it. The method executes :meth:`.main` followed
        by :meth:`postRun`.
        """
        
        self.main()
        self.postRun()
        
    def main(self):
        """
        Run core tool tasks.
        
        Must be implemented in sub-class.
        """
        
        raise NotImplementedError()
    
    def postRun(self):
        """
        Run additional tasks at the end of the core run.
        
        By default this method refreshes the HEC-DSSVue catalogue (if :attr:`.refreshCatalogue` is true) and displays
        any string in :attr:`.message`.
        """
        
        if self.refreshCatalogue and self.mainWindow:
            self.mainWindow.updateCatalog()
    
        if self.message:
            MessageBox.showInformation(self.message, "HEC-DSSVue")
