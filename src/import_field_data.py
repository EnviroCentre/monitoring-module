# name=Import field data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import importdata
import toolbox

CONFIG_FILE = 'field_import.yml'


class ImportTool(toolbox.Tool):
    requiredParams = ['folder', 'files', 'site', 'version', 'params', 'columns']
    refreshCatalogue = 1
    
    def main(self):
        print self.config['columns']
        imported = importdata.locationsAcross(self.config, self.dssFilePath)
        self.message = "%s Records imported." % imported


tool = ImportTool(CONFIG_FILE)
tool.run()
