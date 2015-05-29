# -*- coding: utf-8 -*-
import csv
import monitoring as mon
import os.path
import toolbox.util as tbu
from collections import defaultdict
from datetime import datetime
from hec.script import Constants


def locationsDown(config):
    records = []

    for fileName in config['files']:
        importFile = os.path.join(config['folder'], fileName)

        with open(importFile) as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                # Find the header row first
                try:
                    # If header row, we must have date and location
                    dateCol = row.index(config['columns']['date']['title'])
                    locationCol = row.index(config['columns']['location']['title'])
                except ValueError:
                    # We're not in a header row, move to next line
                    continue
                
                # Optional time col
                try:
                    if config['columns']['time']:
                        timeCol = row.index(config['columns']['time']['title'])
                    else:
                        timeCol = None
                except KeyError:
                    timeCol = None

                # Parameter columns
                paramCols = {}
                for col, cell in enumerate(row):
                    try:
                        # Map cell onto param. Ignore non-ascii characters.
                        param = config['mapping'][cell.encode(encoding='ascii',
                                                              errors='ignore')]
                        # Only use param if in `config['params']`
                        if param in config['params']:
                            paramCols[param] = col
                    except KeyError:
                        # Cell doesn't map onto param
                        pass
                break

            # Then actual data
            for row in csvReader:
                if len(row[locationCol]) > 0:
                    
                    dateStr = row[dateCol]
                    if not timeCol is None:
                        timeStr = row[timeCol]
                    else:
                        timeStr = "12:00:00"
                    sampleDate = tbu.parseDateTime(dateStr, timeStr, 
                                                   config['columns']['date']['format'])
                    
                    for param, col in paramCols.iteritems():
                        value, quality = tbu.parseMeasurement(row[col])
                        if value:
                            record = mon.Record(site=config['site'],
                                                location=row[locationCol],
                                                parameter=param,
                                                version=config['version'],
                                                units=config['params'][param]['unit'], 
                                                startTime=sampleDate.value(),
                                                values=value,
                                                qualities=quality)
                            records.append(record)
                        
    return records
    

def locationsAcross(config):
    records = []

    for fileName in config['files']:
        importFile = os.path.join(config['folder'], fileName)

        with open(importFile) as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                # Find the row with locations
                try:
                    startCol = row.index(config['rows']['location']['title']) + 1
                    # Dict of {'locationId': columnNo}
                    locationCols = {}
                    for col, cell in enumerate(row[startCol:]):
                        if cell.strip():
                            locationCols[cell.upper()] = col + startCol
                    firstDataCol = min(locationCols.values())
                    break
                except ValueError:
                    continue

            # Date row (use first value for just now)
            for row in csvReader:
                if config['rows']['date']['title'] in row:
                    sampleDate = tbu.parseDateTime(row[firstDataCol], "12:00:00", 
                                                   config['rows']['date']['format'])
                    break
                    
            # Find data header row
            for row in csvReader:
                # If header row, we must have parameter and unit header
                try:
                    paramCol = row.index(config['columns']['parameter']['title'])
                    unitCol = row.index(config['columns']['unit']['title'])
                    break
                except ValueError:
                    continue

            # Then actual data
            for row in csvReader:
                try:
                    param = config['mapping'][row[paramCol]]
                    if param in config['params']:
                        for location, col in locationCols.iteritems():
                            value, quality = tbu.parseMeasurement(row[col])
                            if value:
                                record = mon.Record(site=config['site'],
                                                    location=location,
                                                    parameter=param,
                                                    version=config['version'],
                                                    units=config['params'][param]['unit'], 
                                                    startTime=sampleDate.value(),
                                                    values=value,
                                                    qualities=quality)
                                records.append(record)
                except KeyError:
                    # Skip if param not in import file
                    pass

    return records

def timeseries(config):
    records = []

    for fileName, loc in config['files'].iteritems():
        importFile = os.path.join(config['folder'], fileName)

        with open(importFile) as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                if len([cell for cell in row if cell in config['mapping']]) < 2:
                    # Not in header if less than 2 parameter headings found
                    continue
                
                # Parameter columns
                paramCols = {}
                for col, cell in enumerate(row):
                    try:
                        # Map cell onto param. Ignore non-ascii characters.
                        param = config['mapping'][cell.encode(encoding='ascii',
                                                              errors='ignore')]
                        # Only use param if in `config['params']`
                        if param in config['params']:
                            paramCols[param] = col
                    except KeyError:
                        # Cell doesn't map onto param
                        pass
                break
                
            dateCol = timeCol = interval = startTime = None
            # Dict of {'param': [value1, values2, ...]}
            values = defaultdict(list)
            for row in csvReader:
                # Find date and time columns
                if dateCol is None or timeCol is None:
                    for col, cell in enumerate(row):
                        if dateCol is None:
                            try:
                                datetime.strptime(cell, config['date_format'])
                                dateCol = col
                            except ValueError:
                                pass
                        if timeCol is None:
                            try:
                                datetime.strptime(cell, "%H:%M:%S")
                                timeCol = col
                            except ValueError:
                                pass
                
                # If date and time columns founds, we're on a data row
                if dateCol >= 0 and timeCol >= 0:
                    # First row gives start time
                    if startTime is None:
                        startTime = tbu.parseDateTime(row[dateCol], row[timeCol], 
                                                      config['date_format']).value()
                    # Second row gives interval
                    elif interval is None:
                        interval = tbu.parseDateTime(row[dateCol], row[timeCol], 
                                                     config['date_format']).value() - startTime
                            
                    # In all rows we read all params
                    for param, col in paramCols.iteritems():
                        try:
                            values[param].append(float(row[col])) 
                        except ValueError:
                            values[param].append(Constants.UNDEFINED)

        # Check if interval matches number of row and end date/time
        endTime = tbu.parseDateTime(row[dateCol], row[timeCol], 
                                    config['date_format']).value()
        if not endTime == startTime + interval * (len(values[param])-1):
            raise ValueError("Import file {} does not appear to have a regular interval".format(importFile))
        
        # Shift the times to match proper interval times
        if config['interval_snap']:
            startTime = int(round(startTime / float(interval))) * interval
            
        for param in paramCols:
            record = mon.Record(site=config['site'],
                                location=loc,
                                parameter=param, 
                                version=config['version'],
                                units=config['params'][param]['unit'], 
                                startTime=startTime,
                                interval=interval,
                                values=values[param])
            records.append(record)
            
    return records
