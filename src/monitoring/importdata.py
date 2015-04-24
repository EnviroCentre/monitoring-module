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
                            date_parts = cells[config['columns']['date']-1].split("/")
                            date_str = "%s/%s/%s" % (date_parts[1], date_parts[2], date_parts[0])
                            try:
                                time_str = cells[int(config['columns']['time'])-1].strip()
                            except (KeyError, ValueError):
                                time_str = "12:00:00"
                            sample_date = HecTime()
                            sample_date.set(date_str, time_str)
                            record = {
                                'sampledate': sample_date,
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
    
    return records
