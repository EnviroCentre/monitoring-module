# name=Import lab data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import importdata
import toolbox

CONFIG_FILE = 'lab_import.yml'

class ImportTool(toolbox.Tool):
    requiredParams = ['folder', 'files', 'site', 'version', 'mapping', 'params']
    
    def run(self):
        importdata.locationsDown(self.config, self.dssFilePath)


tool = ImportTool(CONFIG_FILE)
tool.run()
