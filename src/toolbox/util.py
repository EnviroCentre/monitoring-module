# -*- coding: utf-8 -*-
from datetime import datetime
import hec.heclib
from hec.heclib.util import HecTime
import hec.io
import os
from os import path


def relativeFolder(folder, dssFilePath, createFolder='ifrelative'):
    """
    Return an absolute path to ``folder`` relative to ``dssFilePath``.
    
    If the path ``folder`` is already absolute, it will simply return the path. ``createFolder`` is one of
    'ifrelative', 'ifabsolute' or 'allways'.
    """
    if path.isabs(folder):
        absPath = folder
        if not path.isdir(absPath) and createFolder.lower() in ['allways', 'ifabsolute']:
            os.mkdir(absPath)
    else:
        absPath = path.join(path.dirname(dssFilePath), folder)
        if not path.isdir(absPath) and createFolder.lower() in ['allways', 'ifrelative']:
            os.mkdir(absPath)
    return absPath


class ValidationError(Exception):
    """
    An error while validating data.
    
    Based on :class:`django.core.exceptions.ValidationError`. Copyright © Django Software Foundation and individual 
    contributors. All rights reserved.
    """
    
    def __init__(self, message):
        """
        The ``message`` argument can be a single error, a list of errors. What we define as an "error" can be either 
        a simple string or an instance of ValidationError with its message attribute set, and what we define as
        list can be an actual `list` or an instance of :class:`ValidationError` with its :attr:`.error_list`` attribute
        set.
        """

        if isinstance(message, ValidationError):
            message = message.message
        
        elif isinstance(message, list):
            self.error_list = []
            for message in message:
                if not isinstance(message, ValidationError):
                    message = ValidationError(message)
                self.error_list.extend(message.error_list)
        
        else:
            self.message = message
            self.error_list = [self]
            
    def __getitem__(self, index):
        return self.error_list[index]
            
    def __str__(self):
        return repr(list(self))

    def __repr__(self):
        return "ValidationError(%r)" % self.message
    

class CancelledError(Exception):
    """
    Operation cancellation/interruption by the user.
    """
    pass

    
def saveIrregularRecords(records, dssFilePath):
    saved = 0
    try:
        dssFile = hec.heclib.dss.HecDss.open(dssFilePath)
        for record in records:
            dssFile.put(_timeSeriesContainer(record))
            saved += 1
    finally:
        dssFile.close()
    return saved


def _timeSeriesContainer(record):
    """
    record:
      site:
      location:
      parameter:
      version:
      units:
      sampledate:
      samplevalue:
    """
    tsc = hec.io.TimeSeriesContainer()
    
    tsc.watershed = record['site']
    tsc.location = record['location']
    tsc.parameter = record['parameter']
    tsc.version = record['version']
    tsc.fullName = "/%s/%s/%s//IR-YEAR/%s/" % (tsc.watershed, tsc.location, tsc.parameter, tsc.version)
    tsc.interval = -1  # irregular
    tsc.values = [record['samplevalue']]
    tsc.times = [record['sampledate'].value()]
    tsc.startTime = tsc.times[0]
    tsc.endTime = tsc.times[-1]
    tsc.numberValues = 1
    tsc.units = record['units']
    tsc.type = "INST-VAL"
    
    return tsc


def _tscFromRecord(record):
    """
    Convert simple records object to HEC timeseries container
    
    :param record: Record object
    :type record: :class:`monitoring.Record`
    """   
    
    tsc = hec.io.TimeSeriesContainer()
    tsc.watershed = record.site
    tsc.location = record.location
    tsc.parameter = record.parameter
    tsc.version = record.version
    tsc.interval = record.interval
    tsc.fullName = record.fullName
    tsc.values = record.values
    tsc.times = record.times
    tsc.startTime = record.startTime
    tsc.endTime = record.endTime
    tsc.numberValues = len(record)
    tsc.units = record.units
    tsc.type = record.type
    return tsc


def saveRecords(records, dssFilePath):
    """
    Save simple record objects to DSS file
    
    :param record: Record object
    :type record: :class:`monitoring.Record`
    :param dssFilePath: HEC-DSS database to save record to
    :param dssFilePath: str
    :return: Number of records saved
    :rtype: int
    """   

    saved = 0
    try:
        dssFile = hec.heclib.dss.HecDss.open(dssFilePath)
        for record in records:
            dssFile.put(_tscFromRecord(record))
            saved += 1
    finally:
        dssFile.close()
    return saved


def parseMeasurement(valueStr):
    """
    Return numeric value of measurement string.
    
    If ``valueStr`` starts with ``<`` (i.e. below limit of detection), the 
    returned value is 50% of the value after the ``<``.
    """
    try:
        return float(valueStr)
    except ValueError:
        if valueStr.strip().startswith('<'):
            return float(valueStr.strip(' <')) * 0.5
        else:
            return None

def parseDateTime(dateStr, timeStr, dateFmt='%Y/%m/%d'):
    """
    Return HecTime from date and time strings.
    
    Time format is always `%H:%M:%S`.
    """

    pyDate = datetime.strptime(dateStr + timeStr, dateFmt + "%H:%M:%S")
    # Create HecTime from USA date format
    return HecTime(pyDate.strftime("%m/%d/%Y %H:%M:%S"))
