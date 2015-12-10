# -*- coding: utf-8 -*-
import unittest
import yaml
import codecs
import os.path
from monitoring import importdata
from operator import attrgetter
from hec.heclib.util import HecTime
 

class FieldDataImportTestCase(unittest.TestCase):
    def setUp(self):
        configFileName = 'field_import.yml'
        with codecs.open(configFileName, encoding='utf-8') as configFile:
            self.config = yaml.load(configFile.read())
            self.config['config_folder'] = os.path.abspath('test')
        
    def testHIHandheld(self):
        config = self.config

        records = importdata.locationsDown(config)
        # Records are not in the same order as input file
        records.sort(key=attrgetter('location', 'parameter'))
        
        self.assertEqual(len(records), 40)
        self.assertTrue(all(record.site == 'SITE NAME' for record in records))
        self.assertTrue(all(record.version == 'RAW' for record in records))
        
        seen = set()
        seen_add = seen.add
        # One date/time per location
        times = [record.times[0] for record in records 
            if not (record.location in seen or seen_add(record.location))]
        expected = [
            HecTime("25MAR2015 12:15").value(),
            HecTime("25MAR2015 11:36").value(),
            HecTime("25MAR2015 13:06").value(),
            HecTime("25MAR2015 10:49").value(),
            HecTime("25MAR2015 12:57").value(),
            HecTime("25MAR2015 11:49").value(),
            HecTime("25MAR2015 12:02").value(),
            HecTime("25MAR2015 13:42").value()
        ]
        self.assertEqual(times, expected)
        
        expected = [
            [4.91, 42.4, 100, 5.77, 7.92],
            [5.68, 49.3, 64, 4.86, 8.25],
            [8.26, 70, 55, 6.01, 7.33],
            [6.86, 57.1, 95, 5.24, 6.62],
            [9.75, 82, 41, 5.82, 6.95],
            [6.97, 57.9, 91, 5.64, 6.26],
            [9.9, 81.1, 49, 5.53, 5.99],
            [8.45, 72.2, 17, 8.2, 7.48],
        ]
        values = [record.values[0] for record in records]
        values = [values[i:i + 5] for i in range(0, len(values), 5)]
        self.assertEqual(values, expected)
        
        qualities = [record.qualities[0] for record in records]
        self.assertEqual(qualities, [3] * len(records))
    
    def testHIHandheldNoTime(self):
        config = self.config
        del config['columns']['time']

        records = importdata.locationsDown(config)
        records.sort(key=attrgetter('location', 'parameter'))
        
        times = [record.times[0] for record in records] 
        self.assertTrue(all(time == HecTime("25MAR2015 12:00").value()
                        for time in times))

    def testHIHandheldNoneTime(self):
        config = self.config
        config['columns']['time'] = None

        records = importdata.locationsDown(config)
        records.sort(key=attrgetter('location', 'parameter'))
        
        times = [record.times[0] for record in records] 
        self.assertTrue(all(time == HecTime("25MAR2015 12:00").value()
                        for time in times))

class LabDataImportTestCase(unittest.TestCase):
    def testChemtest(self):
        configFileName = 'lab_import.yml'
        with codecs.open(configFileName, encoding='utf-8') as configFile:
            config = yaml.load(configFile.read())
            config['config_folder'] = os.path.abspath('test')

        records = importdata.locationsAcross(config)
        self.assertEqual(len(records), 106)
        self.assertTrue(all(record.site == 'SITE NAME' for record in records))
        self.assertTrue(all(record.version == 'RAW' for record in records))
        
        times = [record.times[0] for record in records] 
        self.assertTrue(all(time == HecTime("10FEB2015 12:00").value()
                        for time in times))

        params = {
            'PH': ('-', 8),
            'SS': ('mg/l', 6),
            'COLOUR': ('Pt/Co', 8),
            'BOD': ('mg/l', 6),
            'COD': ('mg/l', 6),
            'DOC': ('mg/l', 6),
            'CHLORIDE': ('mg/l', 8),
            'NITRATE': ('mg/l', 6),
            'SULPHATE': ('mg/l', 8),
            'CALCIUM': ('mg/l', 8),
            'SODIUM': ('mg/l', 2),
            'ALUMINIUM': (u'\u03BCg/l', 8),
            'MANGANESE': (u'\u03BCg/l', 8),
            'ZINC': (u'\u03BCg/l', 2),
            'IRON': (u'\u03BCg/l', 8),
            'TPH': (u'\u03BCg/l', 8)
        }

        for param, paramConfig in params.iteritems():
            units = [record.units for record in records 
                if record.parameter == param]
            self.assertEqual(units, [paramConfig[0]] * paramConfig[1],
                             "Error in units %s for parameter %s" 
                             % (units, param))

        locations = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'PWS1', 'PWS2']
        expected = [
            [8.5, 2.5, 42, 2.0, 18, 19, 0.25, 1.8, 7.1, 35, 31, 200, 2.8, 990],
            [8.4, 2.5, 49, 2.0, 16, 22, 0.25, 2, 2.5, 58, 23, 190, 4, 280],
            [8.3, 5, 49, 2.0, 18, 18, 0.25, 0.5, 2.5, 33, 19, 190, 3, 270],
            [8.2, 20, 57, 2.0, 18, 18, 0.25, 0.5, 2.5, 18, 26, 240, 4.9, 700],
            [8.2, 2.5, 35, 2.0, 16, 17, 0.25, 2.7, 2.5, 43, 14, 200, 1.25, 320],
            [8.1, 2.5, 44, 2.0, 15, 17, 2.4, 1.1, 2.5, 43, 16, 160, 3.1, 630],
            [8.5, 5.6, 18, 7.8, 8.8, 8.1, 19, 2.5, 3.1, 10, 1600],
            [8.5, 8.2, 12, 4.3, 2.5, 6.7, 5, 6.3, 1.8, 20, 140]
        ]
        for i, location in enumerate(locations):
            values = [record.values[0] for record in records 
                if record.location == location]
            self.assertEqual(values, expected[i], 
                             "Error in records %s for location %s" 
                             % (values[i], location))
        
    def testExova(self):
        configFileName = 'lab_import_exova.yml'
        with codecs.open(configFileName, encoding='utf-8') as configFile:
            config = yaml.load(configFile.read())
            config['config_folder'] = os.path.abspath('test')

        records = importdata.locationsAcross(config)
        self.assertEqual(len(records), 16)
        

class LoggerImportTestCase(unittest.TestCase):
    def setUp(self):
        configFileName = 'logger_import.yml'
        with codecs.open(configFileName, encoding='utf-8') as configFile:
            self.config = yaml.load(configFile.read())
            self.config['config_folder'] = os.path.abspath('test')
    
    def testInSituLogger(self):
        config = self.config
        
        records = importdata.timeseries(config)
        records.sort(key=attrgetter('parameter'))
        
        self.assertEqual(len(records), 6)
        self.assertTrue(all(r.site == 'SITE NAME' for r in records))
        self.assertTrue(all(r.location == 'LOCATION A' for r in records))
        self.assertTrue(all(r.version == 'RAW' for r in records))
        self.assertTrue(all(r.interval == 15 for r in records))
        self.assertTrue(all(r.startTime == HecTime("25MAR2015 14:15").value() 
                        for r in records))
        self.assertTrue(all(r.endTime == HecTime("21APR2015 15:30").value() 
                        for r in records))
        self.assertTrue(all(len(r) == 2598 for r in records))
        self.assertEqual([r.parameter for r in records], 
                         ['DO', 'DO%', 'EC', 'PH', 'TEMP', 'TURB'])
        self.assertEqual([r.units for r in records], 
                         ['mg/l', '%', u'µS/cm', '-', 'degC', 'FNU'])
        # First values
        self.assertEqual([r.values[0] for r in records],
                         [10.94, 93.786, 0.66, 8.32, 7.68, 0])
        # Last values
        self.assertEqual([r.values[-1] for r in records],
                         [9.64, 101.7251, 41.62, 5.96, 16.79, 1])

    def testInSituLoggerNoSnap(self):
        config = self.config
        config['interval_snap'] = False
        
        records = importdata.timeseries(config)

        self.assertTrue(all(r.startTime == HecTime("25MAR2015 14:09").value() 
                        for r in records))
        self.assertTrue(all(r.endTime == HecTime("21APR2015 15:24").value() 
                        for r in records))


if __name__ == '__main__':
    unittest.main()
