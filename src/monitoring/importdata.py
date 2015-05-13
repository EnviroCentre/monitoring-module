# -*- coding: utf-8 -*-
import csv
import os.path
import toolbox.util as tbu


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
                        value = tbu.parseMeasurement(row[col])
                        if value:
                            record = {
                                'sampledate': sampleDate,
                                'site': config['site'],
                                'location': row[locationCol],
                                'parameter': param,
                                'version': config['version'],
                                'samplevalue': value, 
                                'units': config['params'][param]['unit']
                            }
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
                            value = tbu.parseMeasurement(row[col])
                            if value:
                                record = {
                                    'sampledate': sampleDate,
                                    'site': config['site'],
                                    'location': location,
                                    'parameter': param,
                                    'version': config['version'],
                                    'samplevalue': value, 
                                    'units': config['params'][param]['unit']
                                }
                                records.append(record)
                except KeyError:
                    # Skip if param not in import file
                    pass

    return records

def timeseries(config):
    ts = []

    for fileName in config['files']:
        importFile = os.path.join(config['folder'], fileName)

        with open(importFile) as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                if len([cell for cell in row if cell in config['mapping']]) < 2:
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
            print(paramCols)
            
    return ts
