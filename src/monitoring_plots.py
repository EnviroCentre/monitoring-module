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
        plotted = plot.onePerParam(self.config, self.dssFilePath)
        self.message = "%s Timeseries plots exported." % plotted


tool = PlotTool()
tool.run()
