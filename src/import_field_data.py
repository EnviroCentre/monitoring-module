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
        records = importdata.locationsAcross(self.config)
        imported = importdata.saveIrregularRecords(records, self.dssFilePath)
        self.message = "%s Records imported." % imported


tool = ImportTool(CONFIG_FILE)
tool.run()
