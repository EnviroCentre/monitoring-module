# name=Import field data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import importdata
import toolbox as tb
import toolbox.util as tbu
from voluptuous import Schema, Optional


class ImportTool(tb.Tool):
    schema = Schema({
        'folder': unicode,
        'files': [
            unicode
        ],
        'site': unicode,
        'version': unicode,
        'columns': {
            'date': {
                'title': unicode,
                'format': unicode
            },
            Optional('time'): {
                'title': unicode
            },
            'location': {
                'title': unicode
            }
        },
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
        records = importdata.locationsDown(self.config)
        imported = tbu.saveRecords(records, self.dssFilePath)
        self.message = "{} Records imported.".format(imported)


tool = ImportTool()
tool.run()
