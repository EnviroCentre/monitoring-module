import hec.heclib 
import hec.io

def locationsAcross(config, dssFilePath):
    records = []
    
    _saveIrregularRecords(records, dssFilePath)

def locationsDown(config, dssFilePath):
    records = []
    
    _saveIrregularRecords(records, dssFilePath)

def _saveIrregularRecords(records, dssFilePath):
    try:
        dssFile = hec.heclib.dss.HecDss.open(dssFilePath)
        for record in records:
            dssFile.put(_timeSeriesContainer(record))
    finally:
        dssFile.close()

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
    tsc.times = [record['sampledate']]
    tsc.startTime = tsc.times[0]
    tsc.endTime = tsc.times[-1]
    tsc.numberValues = 1
    tsc.units = record['units']
    tsc.type = "INST-VAL"
    
    return tsc