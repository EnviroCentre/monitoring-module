# name=Import field data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import importdata
import toolbox

CONFIG_FILE = 'field_import.yml'

class ImportTool(toolbox.Tool):
    requiredParams = ['folder', 'files', 'site', 'version', 'params']
    
    def run(self):
        importdata.locationsAcross(self.config, self.dssFilePath)


tool = ImportTool(CONFIG_FILE)
tool.run()
