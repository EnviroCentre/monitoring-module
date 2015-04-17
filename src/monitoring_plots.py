# name=Monitoring plots
# displayinmenu=true
# displaytouser=true
# displayinselector=true

from monitoring import plot
import toolbox

CONFIG_FILE = 'plots.yml'

class PlotTool(toolbox.Tool):
    requiredParams = ['site', 'locations', 'interval', 'version', 'period', 
        'params', 'width', 'height', 'colours']
    
    def run(self):
        plot.exportImages(self.config, self.dssFilePath)


tool = PlotTool(CONFIG_FILE)
tool.run()
