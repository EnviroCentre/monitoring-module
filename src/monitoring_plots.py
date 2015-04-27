# name=Monitoring plots
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import plot
import toolbox


class PlotTool(toolbox.Tool):
    requiredParams = ['site', 'locations', 'interval', 'version', 'period', 
        'params', 'width', 'height', 'line', 'output_folder']
    
    def run(self):
        plot.exportImages(self.config, self.dssFilePath)


tool = PlotTool()
tool.run()
