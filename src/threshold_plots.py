# name=Monitoring threshold plots
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import plot
import toolbox as tb
from voluptuous import Schema, All, Any, Range, Datetime, Required, Optional, Lower


class PlotTool(tb.Tool):
    rgb = [
        All(int, Range(min=0, max=255)),
        All(int, Range(min=0, max=255)),
        All(int, Range(min=0, max=255))
    ]
    defaultColour = [166, 206, 227]
    defaultLineWidth = 1.25
    
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
        Optional('thresholds'): {
            unicode: {
                unicode: Any(float, int, None)
            }
        },
        'params': {
            unicode: Any({
                Optional('scale'): All(Lower, Any('lin', 'log'))
            }, None)
        },
        Required('width', default=1200): All(int, Range(min=100, max=3000)),
        Required('height', default=300): All(int, Range(min=100, max=3000)),
        Required('line', default={'width': defaultLineWidth, 
                                  'colour': defaultColour}): {
            Required('width', default=defaultLineWidth): 
                All(float, Range(min=0.5, max=2.0)),
            Required('colour', default=defaultColour): rgb
        }
    }, required=True)
    
    def main(self):
        plotted, messages = plot.paramPerPage(self.config, self.dssFilePath)
        messages.insert(0, "{} Timeseries plots exported.".format(plotted))
        self.message += "\n".join(messages)


tool = PlotTool()
tool.run()
