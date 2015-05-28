import collections


class Record(object):
    def __init__(self, site="", location="", parameter="", version="",
                 units="-", startTime=None, interval=-1, values=[]):
        self.site = site.upper()
        self.location = location.upper()
        self.parameter = parameter.upper()
        self.version = version.upper()
        self.units = units
        self.startTime = startTime
        self.interval = interval
        self.type = "INST-VAL"
        self.values = values
    
    @property
    def origin(self):
        if len(self._values) == 1:
            return "sample"
        elif len(self._values) > 1:
            return "logger"
        else:
            return None

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, v):
        if isinstance(v, collections.Sequence):
            self._values = v
        else:
            self._values = [v]
            self.interval = -1
            
    @property
    def fullName(self):
        return "/{0.site}/{0.location}/{0.parameter}//{0.intervalStr}/{0.version}/".format(self)
    
    @property
    def times(self):
        if len(self) > 1:
            return range(self.startTime, 
                         self.startTime + len(self) * self.interval, 
                         self.interval)
        elif len(self) == 1:
            return [self.startTime]
        else:
            return []
        
    @property
    def intervalStr(self):
        if self.interval == -1:
            return "IR-YEAR"
        else:
            units = [
                ('MIN', 60),
                ('HOUR', 60 * 24),
                ('DAY', 1e9),
            ]
            factor = 1
            for unit in units:
                if self.interval < unit[1]:
                    unitStr = unit[0]
                    break
                else:
                    factor = unit[1]
            return "{0:d}{1}".format(self.interval/factor, unitStr)
        
    @property
    def endTime(self):
        return self.times[-1]
        
    def __len__(self):
        return len(self._values)
        
    def __repr__(self):
        return "Record: {0.origin} data at {0.location}".format(self)
