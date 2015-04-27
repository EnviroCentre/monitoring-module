# name=Import field data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import importdata
import toolbox
import toolbox.util


class ImportTool(toolbox.Tool):
    requiredParams = ['folder', 'files', 'site', 'version', 'params', 'columns']
    refreshCatalogue = 1
    
    def main(self):
        records = importdata.locationsAcross(self.config)
        imported = toolbox.util.saveIrregularRecords(records, self.dssFilePath)
        self.message = "%s Records imported." % imported


tool = ImportTool()
tool.run()
