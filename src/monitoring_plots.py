# name=Monitoring plots
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import plot
import toolbox as tb
from voluptuous import Schema, All, Any, Range, Datetime


class PlotTool(tb.Tool):
    schema = Schema({
        'site': unicode,
        'locations': [
            unicode
        ],
        'interval': unicode,
        'version': unicode,
        'output_folder': unicode,
        'period': {
            'start': Datetime("%d%b%Y %H:%M", msg="Start date must be formatted like this: 01JAN2000 00:00"),
            'end':   Datetime("%d%b%Y %H:%M", msg="End date must be formatted like this: 01JAN2000 00:00")
        },
        'params': {
            unicode: {
                'scale': Any('lin', 'log')
            }
        },
        'width':  All(int, Range(min=100, max=3000)),
        'height': All(int, Range(min=100, max=3000)),
        'line': {
            'width': All(float, Range(min=0.5, max=2.0)),
            'colours': [
                [All(int, Range(min=0, max=255)),
                 All(int, Range(min=0, max=255)),
                 All(int, Range(min=0, max=255))]
            ]
        }
    }, required=True)
    
    def main(self):
        plotted, messages = plot.onePerParam(self.config, self.dssFilePath)
        messages.insert(0, "%s Timeseries plots exported." % plotted)
        self.message += "\n".join(messages)


tool = PlotTool()
tool.run()
