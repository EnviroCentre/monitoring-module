# name=Import lab data
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
        'files': [
            unicode
        ],
        'site': unicode,
        'version': unicode,
        'rows': {
            'location': {
                'title': unicode
            },
            'date': {
                'title': unicode,
                'format': unicode
            },
        },
        'columns': {
            'parameter': {
                'title': unicode
            },
            'unit': {
                'title': unicode
            },
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
        records = importdata.locationsAcross(self.config)
        imported = tbu.saveRecords(records, self.dssFilePath)
        self.message = "{} Records imported.".format(imported)


tool = ImportTool()
tool.run()
