from hec.heclib.dss import HecDss
from hec.heclib.util import HecTime
from hec.script import Plot
import os
from os import path

def exportImages(config, dssFilePath):
    
    if path.isabs(config['output_folder']):
        outputFolder = config['output_folder']
        # assume folder exists if absolute path
    else:
        outputFolder = path.join(path.dirname(dssFilePath), config['output_folder'])
        if not path.isdir(outputFolder):
            # create relative folder if required
            os.mkdir(outputFolder)
    
    dssFile = HecDss.open(dssFilePath)
    
    minDate = HecTime(config['period']['start'])
    maxDate = HecTime(config['period']['end'])           

    for param in config['params']:
        thePlot = Plot.newPlot()
        dataPaths = [
            "/%s/%s/%s//%s/%s/" % (config['site'].upper(), 
                                   location.upper(), 
                                   param['name'], 
                                   config['interval'].upper(), 
                                   config['version'].upper())
            for location in config['locations']
        ]
        units = []
        for dataPath in dataPaths:
            timeseries = dssFile.get(dataPath, 1)
            if timeseries.numberValues > 0:
                thePlot.addData(timeseries)

                # Collect unique units
                if not timeseries.units in units:
                    units.append(timeseries.units)

        thePlot.showPlot()
        thePlot.setPlotTitleText(param['name'])
        thePlot.setPlotTitleVisible(1)
        thePlot.setSize(int(config['width']), int(config['height']))

        # We can only access labels at this point
        for dataIndex, dataPath in enumerate(dataPaths):
            timeseries = dssFile.get(dataPath, 1)
            if timeseries.numberValues > 0:
                label = thePlot.getLegendLabel(timeseries)
                label.setText(timeseries.location)

                curve = thePlot.getCurve(dataPath)
                colourIndex = dataIndex % len(config['colours'])
                curve.setLineColor("%s, %s, %s" % tuple(config['colours'][colourIndex]))

        for vp_index in range(len(units)):  # We have one viewport per distinct unit
            viewport = thePlot.getViewport(vp_index)

            viewport.getAxis("X1").setScaleLimits(minDate.value(), maxDate.value())
            viewport.getAxis("Y1").setLabel(units[vp_index])

            viewport.setMinorGridXVisible(1)
            viewport.setMinorGridYVisible(1)

            if param['scale'].lower() == 'log':
                viewport.setLogarithmic('Y1')  # This throws a warning message if y-values <= 0. We can't catch this as an exception. 

        thePlot.saveToPng(os.path.join(outputFolder, config['version'] + "_" + param['name']))
        thePlot.close()

    dssFile.done()
