# name=Monitoring plots
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
    defaultColours = [
        [166, 206, 227],
        [ 31, 120, 180],
        [178, 223, 138],
        [ 51, 160,  44],
        [251, 154, 153],
        [227,  26,  28],
        [253, 191, 111],
        [255, 127,   0],
        [202, 178, 214],
        [106,  61, 154]
    ]
    defaultLineWidth = 2
    
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
            unicode: Any({
                Optional('scale'): All(Lower, Any('lin', 'log'))
            }, None)
        },
        Required('width', default=1200): All(int, Range(min=100, max=3000)),
        Required('height', default=800): All(int, Range(min=100, max=3000)),
        Required('line', default={'width': defaultLineWidth, 
                                  'colours': defaultColours,
                                  'markers': True}): {
            Required('width', default=defaultLineWidth): 
                All(float, Range(min=0.5, max=5.0)),
            Required('colours', default=defaultColours): [
                rgb
            ],
            Required('markers', default=True): bool
        }
    }, required=True)
    
    def main(self):
        plotted, messages = plot.onePerParam(self.config, self.dssFilePath)
        messages.insert(0, "{} Timeseries plots exported.".format(plotted))
        self.message += "\n".join(messages)


tool = PlotTool()
tool.run()
