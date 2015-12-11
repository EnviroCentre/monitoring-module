# -*- coding: utf-8 -*-
import copy
import math
import numbers
import os
import toolbox.util as tbu
from hec.heclib.dss import HecDss
from hec.heclib.util import HecTime
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
    outputFolder = tbu.relativeFolder(config['output_folder'], 
                                      config['config_file'])
    minDate = HecTime(config['period']['start'])
    maxDate = HecTime(config['period']['end'])           
    dssFile = HecDss.open(dssFilePath, str(minDate), str(maxDate))
    colours = _coloursByLocation(config)

    for param, paramConfig in config['params'].iteritems():
        plot = Plot.newPlot()
        dataPaths = [
            "/%s/%s/%s//%s/%s/" % (config['site'].upper(), 
                                   location.upper(), 
                                   param.upper(), 
                                   config['interval'].upper(), 
                                   config['version'].upper())
            for location in config['locations']
        ]
        datasets = [dssFile.get(p) for p in dataPaths]
        datasets = [d for d in datasets if d.numberValues > 0]
        if not datasets:
            messages.append("No data for parameter '%s'." % param)
            continue
        map(plot.addData, datasets)

        plot.showPlot()
        plot.setPlotTitleText(param)
        plot.setPlotTitleVisible(1)
        plot.setSize(int(config['width']), int(config['height']))

        # We can only access labels and curves at this point
        map(lambda d: plot.getLegendLabel(d).setText(d.location), datasets)

        # Style curves
        for dataset in datasets:
            curve = plot.getCurve(dataset)
            curve.setLineColor('{}, {}, {}'.format(*colours[dataset.location]))
            curve.setLineWidth(config['line']['width'])
            if config['line']['markers']:
                curve.setSymbolsVisible(1)
                curve.setSymbolType('Circle')
                curve.setSymbolLineColor('{}, {}, {}'
                                         .format(*colours[dataset.location]))
                curve.setSymbolFillColor('{}, {}, {}'
                                         .format(*colours[dataset.location]))
             
        # Axes scales
        units = set(ds.units for ds in datasets)
        for vp_index, unit in enumerate(units):  # 1 viewport per distinct unit
            viewport = plot.getViewport(vp_index)
            viewport.getAxis("X1").setScaleLimits(minDate.value(), 
                                                  maxDate.value())
            viewport.getAxis("Y1").setLabel(unit)
            viewport.setMinorGridXVisible(1)
            viewport.setMinorGridYVisible(1)
            if paramConfig:
                if paramConfig['scale'].lower() == 'log':
                    viewport.setLogarithmic('Y1')  # This throws a warning message if y-values <= 0. We can't catch this as an exception. 
            # Horizontal threshold lines
            thresholds = _get_thresholds(datasets[0], dssFilePath, config)
            for marker in _thresholdMarkers(thresholds):
                viewport.addAxisMarker(marker)
            
        # Export plot
        plot.saveToJpeg(os.path.join(outputFolder, 
                        config['version'] + "_" + param),
                        95)
        plot.close()
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
    
    outputFolder = tbu.relativeFolder(config['output_folder'], 
                                      config['config_file'])
    
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
        datasets = [dssFile.get(dp) for dp in dataPaths]
        datasets = [d for d in datasets if d.numberValues > 0]
        if not datasets:
            messages.append("No data for parameter '{}'.".format(param))
            continue
        
        for dataset in datasets:
            plot = Plot.newPlot(param)
            layout = Plot.newPlotLayout()
            layout.setHasLegend(0)
            vp = layout.addViewport()
            vp.addCurve('Y1', dataset)
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
            if config['line']['markers']:
                curve.setSymbolsVisible(1)
                curve.setSymbolType('Circle')
                curve.setSymbolLineColor('{}, {}, {}'.format(*config['line']['colour']))
                curve.setSymbolFillColor('{}, {}, {}'.format(*config['line']['colour']))
            vp = plot.getViewport(dataset.fullName)
            vp.setMinorGridXVisible(1)
            vp.getAxis('Y1').setLabel(dataset.units)
            if _paramScale(param, config) == 'log':
                vp.setLogarithmic('Y1')  # This throws a warning message if y-values <= 0. We can't catch this as an exception. 
            # Horizontal lines
            thresholds = _get_thresholds(dataset, dssFilePath, config)
            for marker in _thresholdMarkers(thresholds):
                vp.addAxisMarker(marker)
            # Vertical lines
            if _baselinePeriod(dataset.location, config):
                vp.addAxisMarker(_baselineMarker(dataset.location, config))
            ymin = min(ymin, vp.getAxis('Y1').getScaleMin())
            ymax = max(ymax, vp.getAxis('Y1').getScaleMax())
        
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


def _get_thresholds(parentTsc, dssFilePath, config):
    """
    Return all tresholds associated with ``parentTsc`` as a dict of 
    threshold value/label pairs.
    """
    try:
        # parameter- and location-specific thresholds
        thresholds = config['thresholds'][parentTsc.parameter][parentTsc.location]
        if thresholds is None:
            return []
    except KeyError:
        try:
            # parameter-specific, for all locations, thresholds
            thresholds = config['thresholds'][parentTsc.parameter]['all']
            if thresholds is None:
                return []
        except KeyError:
            return []
    
    calc_thresholds = {}
    # If there is any threshold like `mean` or `+2sd`, calculate baseline stats
    if any(isinstance(value, unicode) for value in thresholds):
        period = _baselinePeriod(parentTsc.location, config)
        baselineHmc = _baselineHmc(parentTsc, dssFilePath, *period)
        scale = _paramScale(parentTsc.parameter, config)
        mean, sd = _tscStats(baselineHmc, scale=scale)

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
        calc_thresholds[thValue] = label
    return calc_thresholds


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

def _thresholdMarkers(thresholds):
    """
    Return list of :class:`AxisMarker` objects for given `thresholds`.
    
    :param thresholds: dict of {treshold value: treshold label}
    :type thresholds: dict
    """
    markers = []
    for value, label in thresholds.iteritems():
        marker = AxisMarker()
        marker.axis = 'Y'
        marker.value = str(value)
        marker.labelText = label.upper()
        marker.lineStyle = 'Dash'
        marker.lineColor = '50, 50, 50'
        markers.append(marker)
    return markers
