from hec.heclib.util import HecTime
import toolbox.util
import os.path


def locationsAcross(config):
    records = []

    for fileName in config['files']:
        importFile = os.path.join(config['folder'], fileName)

        header_cells = []
        try:
            try:
                f = open(importFile)
            except IOError:
                raise
            
            # Find the header row first
            while 1:
                cells = f.readline().split(',')
                if cells[0].lower() == 'date':
                    header_cells = cells
                    break

            # Potentially blank rows below the header line
            while 1:
                cells = f.readline().split(',')
                if len(cells[0]) > 0:
                    break

            # Then actual data
            while 1:
                if len(cells[config['columns']['location']-1]) > 0:
                    for param, paramConfig in config['params'].iteritems():
                        value = toolbox.util.parseMeasurement(cells[paramConfig['column']-1])
                        if value:
                            date_str = cells[config['columns']['date']-1]
                            try:
                                time_str = cells[int(config['columns']['time'])-1]
                            except (KeyError, ValueError):
                                time_str = "12:00:00"
                            
                            record = {
                                'sampledate': toolbox.util.parseDateAndTime(date_str, time_str),
                                'site': config['site'],
                                'location': cells[config['columns']['location']-1],
                                'parameter': param,
                                'version': config['version'],
                                'samplevalue': value, 
                                'units': paramConfig['unit']
                            }
                            records.append(record)
                        
                cells = f.readline().split(',')
                if len(cells[0]) == 0:
                    break

        finally:
            f.close()
        
    return records
    

def locationsDown(config):
    records = []

    dataRows = []

    for fileName in config['files']:
        importFile = os.path.join(config['folder'], fileName)

        try:
            try:
                f = open(importFile)
            except IOError:
                raise
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
                    dateStrParts = cells[5].strip().split('-')
                    sampleDate = HecTime("%s%s20%s 12:00:00" % (dateStrParts[0], dateStrParts[1], dateStrParts[2]))
                    break

            # Then actual data
            while 1:
                cells = f.readline().split(',')
                if len(cells[0]) == 0:
                    break

                try:
                    param = config['mapping'][cells[0].strip()]
                    for location in locationColumns.keys():
                        valueStr = cells[locationColumns[location]].strip()
                        value = toolbox.util.parseMeasurement(valueStr)
                        if value:
                            #row = (sampleDate, location, param, value, config['params'][param]['unit'])
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
                    pass

        finally:
            f.close()
    
    return records
