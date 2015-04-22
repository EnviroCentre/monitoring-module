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
        records = importdata.locationsDown(self.config)
        imported = importdata.saveIrregularRecords(records, self.dssFilePath)
        self.message = "%s Records imported." % imported


tool = ImportTool(CONFIG_FILE)
tool.run()
