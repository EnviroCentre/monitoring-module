# -*- coding: utf-8 -*-
import copy
import os
import toolbox.util as tbu
from hec.heclib.dss import HecDss
from hec.heclib.util import HecTime
from hec.script import Plot



def _coloursByLocation(config):
    """Assign a fixed colour to each location"""
    
    colours = {}  # {'locationId': [#r, #g, #b]}
    for locationIndex, location in enumerate(config['locations']):
        colourIndex = locationIndex % len(config['line']['colours'])
        colours[location] = config['line']['colours'][colourIndex]
    return colours


def onePerParam(config, dssFilePath):
    plotted = 0  # Number of plots exported
    messages = []
    
    outputFolder = tbu.relativeFolder(config['output_folder'], dssFilePath)
    dssFile = HecDss.open(dssFilePath)
    
    minDate = HecTime(config['period']['start'])
    maxDate = HecTime(config['period']['end'])           

    colours = _coloursByLocation(config)

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
            messages.append("No data for parameter '%s'." % param)
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
        plotted += 1

    dssFile.done()
    return plotted, messages


def paramPerPage(config, dssFilePath):
    """
    Plot timeseries, 1 location per plot, 1 parameter per page.
    
    Also adds specified thresholds.    
    """
    
    plotted = 0  # Number of plots exported
    messages = []
    
    outputFolder = tbu.relativeFolder(config['output_folder'], dssFilePath)
    
    minDate = HecTime(config['period']['start'])
    maxDate = HecTime(config['period']['end'])           

    dssFile = HecDss.open(dssFilePath, str(minDate), str(maxDate))

    for param, paramConfig in config['params'].iteritems():
        plots = []
        dataPaths = [
            '/{}/{}/{}//{}/{}/'.format(config['site'].upper(), 
                                       loc.upper(), 
                                       param.upper(), 
                                       config['interval'].upper(), 
                                       config['version'].upper())
            for loc in config['locations']
        ]
        datasets = [dssFile.get(dp, 1) for dp in dataPaths]
        datasets = [d for d in datasets if d.numberValues > 0]
        if not datasets:
            messages.append("No data for parameter '{}'.".format(param))
            continue
        
        thDatasets = []
        for dataset in datasets:
            plot = Plot.newPlot(param)
            layout = Plot.newPlotLayout()
            layout.setHasLegend(0)
            vp = layout.addViewport()
            vp.addCurve('Y1', dataset)
            try:
                th = config['thresholds'][param][dataset.location]
                if not th is None:
                    thRec = constantTsc(th, minDate, maxDate, templateTsc=dataset)
                    thDatasets.append(thRec)
                    vp.addCurve('Y1', thRec)
            except KeyError:
                pass
                        
            plot.configurePlotLayout(layout)
            plot.setPlotTitleText("{0.parameter} at {0.location}".format(dataset))
            plot.setPlotTitleVisible(1)
            plot.setLocation(-10000, -10000)
            plot.setSize(config['width'], config['height'])
            panel = plot.getPlotpanel()
            prop = panel.getProperties()
            prop.setViewportSpaceSize(0)
            plots.append(plot)
        
        # Format normal data curves
        ymin, ymax = float('+inf'), float('-inf')
        for dataset, plot in zip(datasets, plots):
            curve = plot.getCurve(dataset)
            curve.setLineColor('{}, {}, {}'.format(*config['line']['colour']))
            curve.setLineWidth(config['line']['width'])
            plot.setLegendLabelText(dataset, dataset.location)
            vp = plot.getViewport(dataset.fullName)
            vp.setMinorGridXVisible(1)
            vp.getAxis('Y1').setLabel(dataset.units)
            if paramConfig:
                if paramConfig['scale'].lower() == 'log':
                    vp.setLogarithmic('Y1')  # This throws a warning message if y-values <= 0. We can't catch this as an exception. 
            ymin = min(ymin, vp.getAxis('Y1').getScaleMin())
            ymax = max(ymax, vp.getAxis('Y1').getScaleMax())
        
            # Format threshold curves
            associatedThDatasets = [d for d in thDatasets 
                                    if d.location == dataset.location]
            for thDataset in associatedThDatasets:
                curve = plot.getCurve(thDataset)
                curve.setLabel(thDataset.version)
                curve.setLabelVisible(1)
                curve.setLineColor('50, 50, 50')
                curve.setLineWidth(config['line']['width'])
                curve.setLineStyle('Dash')
        
        for dataset, plot in zip(datasets, plots):
            plot.showPlot()
            plot.setSize(config['width'], config['height'])
            # Set all y-axes same limits
            vp = plot.getViewports()[0]
            vp.getAxis('Y1').setScaleLimits(ymin, ymax)
            vp.getAxis('X1').setScaleLimits(minDate.value(), maxDate.value())
        
            plot.saveToJpeg(os.path.join(outputFolder, 
                            "TH plot-{0.parameter}-{0.version}-{0.location}"
                            .format(dataset)), 95)
            plot.close()
            plotted += 1

    dssFile.done()
    return plotted, messages

def constantTsc(value, startDate, endDate, templateTsc):
    rec = copy.copy(templateTsc)
    rec.values = [value] * 2
    rec.times = [startDate.value(), endDate.value()]
    rec.type = 'INST-VAL'
    rec.interval = -1
    rec.version = 'THRESHOLD'
    rec.numberValues = 2
    rec.fullName = "/{0.watershed}/{0.location}/{0.parameter}//IR-DECADE/{0.version}/".format(rec)
    return rec
