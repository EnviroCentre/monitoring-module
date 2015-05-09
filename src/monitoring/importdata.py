# -*- coding: utf-8 -*-
import os.path
import toolbox.util as tbu


def locationsDown(config):
    records = []

    for fileName in config['files']:
        importFile = os.path.join(config['folder'], fileName)

        with open(importFile) as f:
            # Find the header row first
            while 1:
                cells = f.readline().split(',')
                try:
                    # If header row, we must have date and location
                    dateColumn = cells.index(config['columns']['date'])
                    locationColumn = cells.index(config['columns']['location'])
                except ValueError:
                    # We're not in a header row
                    continue
                
                # Optional time column
                try:
                    timeColumn = cells.index(config['columns']['time'])
                except KeyError:
                    timeColumn = None

                # Parameter columns
                paramColumns = {}
                for idx, param in enumerate(cells):
                    try:
                        paramColumns[
                            # Weird non-utf chars in header row compare 
                            # ascii chars only
                            config['mapping'][param.encode(encoding='ascii',
                                                           errors='ignore')]
                        ] = idx
                    except KeyError:
                        pass
                break

            # Potentially blank rows below the header line
            while 1:
                cells = f.readline().split(',')
                if len(cells[0]) > 0:
                    break

            # Then actual data
            while 1:
                if len(cells[locationColumn]) > 0:
                    
                    dateStr = cells[dateColumn]
                    if not timeColumn is None:
                        timeStr = cells[timeColumn]
                    else:
                        timeStr = "12:00:00"
                    sampleDate = tbu.parseDateAndTime(dateStr, timeStr)
                    
                    for param, column in paramColumns.iteritems():
                        value = tbu.parseMeasurement(cells[column])
                        if value:
                            record = {
                                'sampledate': sampleDate,
                                'site': config['site'],
                                'location': cells[locationColumn],
                                'parameter': param,
                                'version': config['version'],
                                'samplevalue': value, 
                                'units': config['params'][param]['unit']
                            }
                            records.append(record)
                        
                cells = f.readline().split(',')
                if len(cells[0]) == 0:
                    break

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
