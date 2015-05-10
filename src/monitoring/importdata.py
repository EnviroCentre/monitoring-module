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
                    dateColumn = row.index(config['columns']['date'])
                    locationColumn = row.index(config['columns']['location'])
                except ValueError:
                    # We're not in a header row, move to next line
                    continue
                
                # Optional time column
                try:
                    timeColumn = row.index(config['columns']['time'])
                except KeyError:
                    timeColumn = None

                # Parameter columns
                paramColumns = {}
                for column, cell in enumerate(row):
                    try:
                        # Map cell onto param. Ignore non-ascii characters.
                        param = config['mapping'][cell.encode(encoding='ascii',
                                                              errors='ignore')]
                        # Only use param if in `config['params']`
                        if param in config['params']:
                            paramColumns[param] = column
                    except KeyError:
                        # Cell doesn't map onto param
                        pass
                break

            # Then actual data
            for row in csvReader:
                if len(row[locationColumn]) > 0:
                    
                    dateStr = row[dateColumn]
                    if not timeColumn is None:
                        timeStr = row[timeColumn]
                    else:
                        timeStr = "12:00:00"
                    sampleDate = tbu.parseDateAndTime(dateStr, timeStr)
                    
                    for param, column in paramColumns.iteritems():
                        value = tbu.parseMeasurement(row[column])
                        if value:
                            record = {
                                'sampledate': sampleDate,
                                'site': config['site'],
                                'location': row[locationColumn],
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
            # Find the row with locations
            while 1:
                cells = f.readline().split(',')
                if cells[1].lower() == 'client sample id.:':
                    # Dict of {'locationId': columnNo}
                    locationColumns = {}
                    for i in range(5, len(cells)):
                        if len(cells[i].strip()) > 0:
                            locationColumns[cells[i].upper()] = i 
                    break

            # Date row (use first value for just now)
            while 1:
                cells = f.readline().split(',')
                if cells[1].lower() == 'date sampled:':
                    sampleDate = tbu.parseDateAndTime(cells[5], "12:00:00",
                                                      "dd-mmm-yy")
                    break

            # Then actual data
            while 1:
                cells = f.readline().split(',')
                if len(cells[0]) == 0:
                    break

                try:
                    param = config['mapping'][cells[0].strip()]
                    for location, column in locationColumns.iteritems():
                        value = tbu.parseMeasurement(cells[column])
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
