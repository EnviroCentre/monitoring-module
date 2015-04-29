# -*- coding: utf-8 -*-
from hec.heclib.dss import HecDss
from hec.heclib.util import HecTime
from hec.script import Plot
import os
import toolbox.util as tbu


def onePerParam(config, dssFilePath):
    
    outputFolder = tbu.relativeFolder(config['output_folder'], dssFilePath)
    dssFile = HecDss.open(dssFilePath)
    
    minDate = HecTime(config['period']['start'])
    maxDate = HecTime(config['period']['end'])           

    for param, paramConfig in config['params'].iteritems():
        thePlot = Plot.newPlot()
        dataPaths = [
            "/%s/%s/%s//%s/%s/" % (config['site'].upper(), 
                                   location.upper(), 
                                   param.upper(), 
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
        thePlot.setPlotTitleText(param)
        thePlot.setPlotTitleVisible(1)
        thePlot.setSize(int(config['width']), int(config['height']))

        # We can only access labels at this point
        for dataIndex, dataPath in enumerate(dataPaths):
            timeseries = dssFile.get(dataPath, 1)
            if timeseries.numberValues > 0:
                label = thePlot.getLegendLabel(timeseries)
                label.setText(timeseries.location)

                curve = thePlot.getCurve(dataPath)
                colourIndex = dataIndex % len(config['line']['colours'])
                curve.setLineColor("%s, %s, %s" % tuple(config['line']['colours'][colourIndex]))
                curve.setLineWidth(config['line']['width'])

        for vp_index, unit in enumerate(units):  # We have one viewport per distinct unit
            viewport = thePlot.getViewport(vp_index)

            viewport.getAxis("X1").setScaleLimits(minDate.value(), maxDate.value())
            viewport.getAxis("Y1").setLabel(unit)

            viewport.setMinorGridXVisible(1)
            viewport.setMinorGridYVisible(1)
            
            if paramConfig:
                if paramConfig['scale'].lower() == 'log':
                    viewport.setLogarithmic('Y1')  # This throws a warning message if y-values <= 0. We can't catch this as an exception. 

        thePlot.saveToJpeg(os.path.join(outputFolder, 
                           config['version'] + "_" + param),
                           95)
        thePlot.close()

    dssFile.done()

