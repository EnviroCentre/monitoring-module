# name=Import logger data
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import importdata
import toolbox as tb
from voluptuous import Schema


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
            'time': {
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
        timeseries = importdata.timeseries(self.config)
        imported = len(timeseries)  # TODO
        self.message = "{} Timeseries imported.".format(imported)


tool = ImportTool()
tool.run()
