# name=Monitoring plots
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import plot
import toolbox as tb


class PlotTool(tb.Tool):
    requiredParams = ['site', 'locations', 'interval', 'version', 'period', 
        'params', 'width', 'height', 'line', 'output_folder']
    
    def main(self):
        plotted, messages = plot.onePerParam(self.config, self.dssFilePath)
        messages.insert(0, "%s Timeseries plots exported." % plotted)
        self.message += "\n".join(messages)


tool = PlotTool()
tool.run()
