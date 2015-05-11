# name=Import field data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import importdata
import toolbox as tb
import toolbox.util as tbu


class ImportTool(tb.Tool):
    requiredParams = ['folder', 'files', 'site', 'version', 'columns', 
        'mapping', 'params']
    refreshCatalogue = 1
    
    def main(self):
        records = importdata.locationsDown(self.config)
        imported = tbu.saveIrregularRecords(records, self.dssFilePath)
        self.message = "{} Records imported.".format(imported)


tool = ImportTool()
tool.run()
