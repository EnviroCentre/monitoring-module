# -*- coding: utf-8 -*-
import hec.heclib
import hec.io
import os
from datetime import datetime
from hec.heclib.util import HecTime
from os import path


def relativeFolder(folder, dssFilePath, createFolder='ifrelative'):
    """
    Return an absolute path to ``folder`` relative to ``dssFilePath``.

    If the path ``folder`` is already absolute, it will simply return the path.
    ``createFolder`` is one of 'ifrelative', 'ifabsolute' or 'allways'.
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
    if not record.qualities is None:
        tsc.quality = record.qualities
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
    Return numeric value of measurement string and quality flag as tuple.

    If ``valueStr`` starts with ``<`` (i.e. below limit of detection), the
    returned value is 50% of the value after the ``<``.
    """
    # HEC quality flags
    TESTED = 1 << 0
    VALID = 1 << 1
    MISSING = 1 << 2
    CHANGED = 1 << 7
    FUT_USE_1 = 1 << 23
    USER_DEF = 1 << 24
    replaceValues = {
        # string to replace: (replacement value, flag)
        'ND': (0.0, TESTED | VALID | CHANGED | FUT_USE_1 )
    }
    try:
        try:
            # Try to replace specific values if needed
            return replaceValues[valueStr]
        except KeyError:
            # Otherwise try to parse the string as a float
            return float(valueStr), TESTED | VALID
    except ValueError:
        # If that doesn't work, check if it's below limited of detection
        if valueStr.strip().startswith('<'):
            return (float(valueStr.strip(' <')) * 0.5,
                    TESTED | VALID | CHANGED | USER_DEF)
        else:
            # Nothing works, just return None, i.e. missing value
            return None, TESTED | MISSING


def parseDateTime(dateStr, timeStr, dateFmt='%Y/%m/%d'):
    """
    Return HecTime from date and time strings.

    Time format is always `%H:%M:%S`.
    """

    pyDate = datetime.strptime(dateStr + timeStr, dateFmt + "%H:%M:%S")
    # Create HecTime from USA date format
    return HecTime(pyDate.strftime("%m/%d/%Y %H:%M:%S"))


def index_ign_case(haystack, needle):
    """
    Return index of needle in haystack. Case insensitive.
    """
    return list(map(str.lower, haystack)).index(needle.lower())
