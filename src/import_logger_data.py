# name=Import logger data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import importdata
import toolbox as tb
import toolbox.util as tbu
from voluptuous import Schema


class ImportTool(tb.Tool):
    schema = Schema({
        'folder': unicode,
        'files': {
            unicode: unicode
        },
        'site': unicode,
        'version': unicode,
        'date_format': unicode,
        'mapping': {
            unicode: unicode
        },
        'params': {
            unicode: {
                'unit': unicode
            }
        }
    }, required=True)
    
    refreshCatalogue = 1
    
    def main(self):
        records = importdata.timeseries(self.config)
        imported = tbu.saveRecords(records, self.dssFilePath)
        self.message = "{} Timeseries imported.".format(imported)


tool = ImportTool()
tool.run()
