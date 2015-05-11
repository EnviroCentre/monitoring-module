import codecs
from hec.script import MessageBox
from os import path
from toolbox.util import CancelledError, ValidationError
import yaml
from voluptuous import MultipleInvalid

def construct_yaml_str(self, node):
    # Override the default string handling function to always return unicode 
    return self.construct_scalar(node)

yaml.Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


class Tool(object):
    """
    A tool for undertaking tasks in HEC-DSSVue.
    """
    #: Configuaration schema (uses ``voluptuous`` library)
    schema = None
    #: Whether to refresh the HEC-DSSVue catalogue after completing the task.
    refreshCatalogue = 0
    
    def __init__(self, configFileName=None, dssFilePath=None):
        """
        A tool is defined by providing a `yaml` configuration file 
        ``configFileName`` and a HEC-DSS database ``dssFilePath`` to operate on.
        If ``dssFilePath`` is not set, the active DSS-file in the HEC-DSSVue
        window will be used. If ``configFileName`` is not set, a file selection
        dialogue is displayed prompting for a configuration file.
        
        The attribute :attr:`.config` will be set containing the parsed yaml 
        config file.
        """
        
        if dssFilePath:
            self.dssFilePath = dssFilePath
            self.mainWindow = None
        else:
            from hec.dssgui import ListSelection
            self.mainWindow = ListSelection.getMainWindow()
            self.dssFilePath = self.mainWindow.getDSSFilename()
            if not configFileName:
                from javax.swing import JFileChooser
                from javax.swing.filechooser import FileNameExtensionFilter
                fileDialogue = JFileChooser(self.dssFilePath)
                filter = FileNameExtensionFilter("Configuration file (*.yml; *.yaml)", 
                                                 ["yaml", "yml"])
                fileDialogue.setFileFilter(filter)
                ret = fileDialogue.showOpenDialog(self.mainWindow)
                if ret == JFileChooser.APPROVE_OPTION:
                    self.configFilePath = (fileDialogue.getSelectedFile().
                                           getAbsolutePath())
                else:
                    raise CancelledError("Config file selection was cancelled.") 
        
        if configFileName:
            self.configFilePath = path.join(path.dirname(self.dssFilePath), 
                                            configFileName)
        elif dssFilePath:
            raise ValueError("`configFileName` argument must be provided if `dssFilePath` is specified.")
        
        #: Message to be displayed in HEC-DSSVue after running the tool. This 
        #: attribute is typically set in the :meth:`main`.
        self.message = ""
        
        if self._toolIsValid():
            with codecs.open(self.configFilePath, encoding='utf-8') as configFile:
                self.config = yaml.load(configFile.read())
            self._configIsValid()
        
    def _toolIsValid(self):
        """
        Check if the tool is configured correctly with a valid config file and 
        HEC-DSS database.
        """
        
        # Check if HEC-DSS db exists
        if not path.isfile(self.dssFilePath):
            error = ValidationError("Please open a HEC-DSS database first.")
            MessageBox.showError(error.message, "HEC-DSSVue")
            raise error
        
        # Check if config file exists
        if not path.isfile(self.configFilePath):
            error = ValidationError("The configuration file {} does not exist.\n\nPlease create this file and try again.".format(self.configFilePath))
            MessageBox.showError(error.message, "HEC-DSSVue")
            raise error
        
        return 1
    
    def _configIsValid(self):
        """
        Validate config file content.
        
        Currently checks for existence of required top-level config parameters/
        keys only as specified in :attr:`.requiredParams`.
        """
        
        if self.schema:
            try:
                self.schema(self.config) 
            except MultipleInvalid as e:
                self._displayConfigErrors(e.errors)
                raise
        return 1
    
    def _displayConfigErrors(self, errors):
        """
        Display configuration errors in the HEC-DSSVue window.
        """
        
        message = "The configuration file {} is not valid.\nPlease check the content and try again.".format(self.configFilePath)
        message += "\n"
        for error in errors:
            message += "\n - {}".format(error)
        MessageBox.showError(message, "HEC-DSSVue")

    def run(self):
        """
        Main tool execution method.
        
        This method should be called after instantiating the tool to run it. The
        method executes :meth:`.main` followed by :meth:`postRun`.
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
        
        By default this method refreshes the HEC-DSSVue catalogue (if 
        :attr:`.refreshCatalogue` is true) and displays any string in 
        :attr:`.message`.
        """
        
        if self.refreshCatalogue and self.mainWindow:
            self.mainWindow.updateCatalog()
    
        if self.message:
            MessageBox.showInformation(self.message, "HEC-DSSVue")
