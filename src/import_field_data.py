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
        'folder': str,
        'files': [
            str
        ],
        'site': str,
        'version': str,
        'columns': {
            'date': {
                'title': str,
                'format': str
            },
            Optional('time'): {
                'title': str
            },
            'location': {
                'title': str
            }
        },
        'mapping': {
            str: str
        },
        'params': {
            str: {
                'unit': tb.ustr
            }
        }
    }, required=True)
    
    refreshCatalogue = 1
    
    def main(self):
        records = importdata.locationsDown(self.config)
        imported = tbu.saveIrregularRecords(records, self.dssFilePath)
        self.message = "{} Records imported.".format(imported)


tool = ImportTool()
tool.run()
