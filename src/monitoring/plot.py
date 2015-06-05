# -*- coding: utf-8 -*-
import copy
import math
import numbers
import os
import toolbox.util as tbu
from hec.heclib.dss import HecDss
from hec.heclib.util import HecTime
from hec.hecmath import HecMath
from hec.script import Plot, AxisMarker


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
            # Thresholds
            thTscs = _thresholdTscs(dataset, dssFilePath, config, 
                                    minDate, maxDate)
            thDatasets += thTscs
            for thTsc in thTscs:
                vp.addCurve('Y1', thTsc)

            plot.configurePlotLayout(layout)
            plots.append(plot)
        
        # Format normal data curves
        ymin, ymax = float('+inf'), float('-inf')
        for dataset, plot in zip(datasets, plots):
            plot.setPlotTitleText("{0.parameter} at {0.location}".format(dataset))
            plot.setPlotTitleVisible(1)
            plot.setLocation(-10000, -10000)
            plot.setSize(config['width'], config['height'])
            plot.setLegendLabelText(dataset, dataset.location)
            panelProp = plot.getPlotpanel().getProperties()
            panelProp.setViewportSpaceSize(0)

            curve = plot.getCurve(dataset)
            curve.setLineColor('{}, {}, {}'.format(*config['line']['colour']))
            curve.setLineWidth(config['line']['width'])
            vp = plot.getViewport(dataset.fullName)
            vp.setMinorGridXVisible(1)
            vp.getAxis('Y1').setLabel(dataset.units)
            if _paramScale(param, config) == 'log':
                vp.setLogarithmic('Y1')  # This throws a warning message if y-values <= 0. We can't catch this as an exception. 
            # Vertical lines
            if _baselinePeriod(dataset.location, config):
                vp.addAxisMarker(_baselineMarker(dataset.location, config))
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


def constantTsc(value, version, startDate, endDate, templateTsc):
    """
    Return a :class:`TimeSeriesContainer` with a constant value and specified 
    ``version`` (F-part) between ``startDate`` and ``endDate``. All other
    parameters are taken from ``templateTsc``.
    """
    rec = copy.copy(templateTsc)
    rec.values = [value] * 2
    rec.times = [startDate.value(), endDate.value()]
    rec.type = 'INST-VAL'
    rec.interval = -1
    rec.version = version.upper()
    rec.numberValues = 2
    rec.fullName = "/{0.watershed}/{0.location}/{0.parameter}//IR-DECADE/{0.version}/".format(rec)
    return rec


def _tscStats(hmc, scale='lin'):
    """
    Return mean and standard deviation of a dataset.
    
    :param hmc: Input timeseries
    :type hmc: :class:`HecMath`
    :param scale: If set to ``log``, the stats will be taken from the 
                  log-transformed timeseries.
    :type sale: str
    :return: mean and standard deviation
    :rtype: (float, float)
    """
    if scale == 'log':
        hmc = hmc.log()
    return hmc.mean(), hmc.standardDeviation()


def _baselineHmc(parentTsc, dssFilePath, startDate, endDate):
    """
    Return the baseline timeseries between two dates.
    
    Note: ``parentTsc`` does not necessarily need to contain the baseline 
    period. It's just used for the metadata.
    
    :param parentTsc: The timeseries for which the baseline period should be
                      extracted
    :type parentTsc: :class:`TimeSeriesContainer`
    :param dssFilePath: File path to HEC-DSS file to load data from
    :type dssFilePath: str
    :param startDate: Start of baseline period
    :type startDate: str
    :param endDate: End of baseline period
    :type endDate: str
    :return: Baseline timeseries
    :rtype: :class:`HecMath`
    """
    dssFile = HecDss.open(dssFilePath)
    return dssFile.read(parentTsc.fullName, str(startDate), str(endDate))


def _thresholdTscs(parentTsc, dssFilePath, config, startDate, endDate):
    """
    Return all tresholds associated with ``parentTsc`` as a list of 
    :class:`TimeSeriesContainers` between ``startDate`` and ``endDate``.
    """
    try:
        thresholds = config['thresholds'][parentTsc.parameter][parentTsc.location]
        if thresholds is None:
            return []
    except KeyError:
        return []
    
    # If there is any threshold like `mean` or `+2sd`, calculate baseline stats
    if any(isinstance(value, unicode) for value in thresholds):
        period = _baselinePeriod(parentTsc.location, config)
        baselineHmc = _baselineHmc(parentTsc, dssFilePath, *period)
        scale = _paramScale(parentTsc.parameter, config)
        mean, sd = _tscStats(baselineHmc, scale=scale)

    tscs = []
    for value, label in thresholds.iteritems():
        if isinstance(value, numbers.Real):
            # Simple numeric threshold
            thValue = value
        else:
            # Baseline stats thresholds
            if value == 'mean':
                thValue = mean
                if scale == 'log':
                    thValue = math.exp(thValue)
            elif value[-2:] == 'sd':  # e.g. +2sd, -1sd
                mult = int(value[:2])
                thValue = mean + sd * mult
                if scale == 'log':
                    thValue = math.exp(thValue)
            else:
                continue
        tscs.append(constantTsc(thValue, label, startDate, endDate, 
                    templateTsc=parentTsc))
    return tscs


def _baselinePeriod(location, config):
    try:
        # Try if there is a location-specific baseline period
        baseline = config['baseline'][location]
    except KeyError:
        try:
            # Otherwise use site-wide period
            baseline = config['baseline']['all']
        except KeyError:
            return None
    return HecTime(baseline['start']), HecTime(baseline['end'])


def _paramScale(param, config):
    scale = None
    paramConfig = config['params'][param]
    if paramConfig:
        try:
            scale = paramConfig['scale'].lower() 
        except KeyError:
            pass

    if scale in ['lin', 'log']:
        return scale
    else:
        return 'lin'

def _baselineMarker(location, config):
    baselineEnd = _baselinePeriod(location, config)[1]
    marker = AxisMarker()
    marker.axis = 'X'
    marker.value = str(baselineEnd)
    marker.labelText = "BASELINE"
    marker.fillPattern = 'Diagonal Cross'
    marker.fillStyle = 'Below'
    marker.fillColor = 'lightgray'
    marker.lineColor = 'lightgray'
    marker.labelColor = 'gray'
    
    return marker
