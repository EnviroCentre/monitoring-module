# name=Monitoring plots
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import plot
import toolbox as tb
from voluptuous import Schema, All, Any, Range, Datetime, Required, Lower


class PlotTool(tb.Tool):
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
    defaultLineWidth = 1.25
    
    schema = Schema({
        'site': unicode,
        'locations': [
            unicode
        ],
        'interval': unicode,
        'version': unicode,
        Required('output_folder', default="Output"): unicode,
        'period': {
            'start': Datetime("%d%b%Y %H:%M", msg="Start date must be formatted like this: 01JAN2000 00:00"),
            'end':   Datetime("%d%b%Y %H:%M", msg="End date must be formatted like this: 01JAN2000 00:00")
        },
        'params': {
            unicode: {
                'scale': All(Lower, Any('lin', 'log'))
            }
        },
        'width':  All(int, Range(min=100, max=3000)),
        'height': All(int, Range(min=100, max=3000)),
        Required('line', default={'width': defaultLineWidth, 
                                  'colours': defaultColours}): {
            Required('width', default=defaultLineWidth): 
                All(float, Range(min=0.5, max=2.0)),
            Required('colours', default=defaultColours): [
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
