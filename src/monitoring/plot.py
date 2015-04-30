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

    # Assign a fixed colour to each location
    colours = {}  # {'locationId': [#r, #g, #b]}
    for locationIndex, location in enumerate(config['locations']):
        colourIndex = locationIndex % len(config['line']['colours'])
        colours[location] = config['line']['colours'][colourIndex]

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
        datasets = [dssFile.get(p, 1) for p in dataPaths]
        datasets = [d for d in datasets if d.numberValues > 0]
        if not datasets:
            print "No data for parameter %s. Plot skipped." % param
            continue
        
        map(thePlot.addData, datasets)

        thePlot.showPlot()
        thePlot.setPlotTitleText(param)
        thePlot.setPlotTitleVisible(1)
        thePlot.setSize(int(config['width']), int(config['height']))

        # We can only access labels and curves at this point
        map(lambda d: thePlot.getLegendLabel(d).setText(d.location), datasets)

        for dataset in datasets:
            curve = thePlot.getCurve(dataset)
            curve.setLineColor("%s, %s, %s" % tuple(colours[dataset.location]))
            curve.setLineWidth(config['line']['width'])

        units = set(ds.units for ds in datasets)
        for vp_index, unit in enumerate(units):  # 1 viewport per distinct unit
            viewport = thePlot.getViewport(vp_index)
            viewport.getAxis("X1").setScaleLimits(minDate.value(), 
                                                  maxDate.value())
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

