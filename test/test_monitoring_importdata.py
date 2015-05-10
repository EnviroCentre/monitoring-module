# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

import unittest
import yaml
import codecs
from monitoring import importdata
from operator import itemgetter
 

class FieldDataImportTestCase(unittest.TestCase):
    def setUp(self):
        configFileName = 'field_import.yml'
        with codecs.open(configFileName, encoding='utf-8') as configFile:
            self.config = yaml.load(configFile.read())
        
    def testHIHandheld(self):
        config = self.config

        records = importdata.locationsDown(config)
        # Records are not in the same order as input file
        records.sort(key=itemgetter('location', 'parameter'))
        
        self.assertEqual(len(records), 40)
        self.assertTrue(all(record['site'] == 'Site name' 
                        for record in records))
        self.assertTrue(all(record['version'] == 'RAW' 
                        for record in records))

        ymds = [(record['sampledate'].year(), 
                 record['sampledate'].month(),
                 record['sampledate'].day()) for record in records] 
        self.assertTrue(all(ymd == (2015, 3, 25) for ymd in ymds))
        
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
        values = [record['samplevalue'] for record in records]
        values = [values[i:i + 5] for i in range(0, len(values), 5)]

        self.assertEqual(values, expected)
    
    def testHIHandheldNoTime(self):
        config = self.config
        del config['columns']['time']

        records = importdata.locationsDown(config)
        records.sort(key=itemgetter('location', 'parameter'))
        
        hmss = [(record['sampledate'].hour(), 
                 record['sampledate'].minute(),
                 record['sampledate'].second()) for record in records] 
        self.assertTrue(all(hms == (12, 0, 0) for hms in hmss))

    def testHIHandheldNoneTime(self):
        config = self.config
        config['columns']['time'] = None

        records = importdata.locationsDown(config)
        records.sort(key=itemgetter('location', 'parameter'))
        
        hmss = [(record['sampledate'].hour(), 
                 record['sampledate'].minute(),
                 record['sampledate'].second()) for record in records] 
        self.assertTrue(all(hms == (12, 0, 0) for hms in hmss))

class LabDataImportTestCase(unittest.TestCase):
    def testChemtest(self):
        configFileName = 'lab_import.yml'
        with codecs.open(configFileName, encoding='utf-8') as configFile:
            config = yaml.load(configFile.read())

        records = importdata.locationsAcross(config)
        self.assertEqual(len(records), 106)
        self.assertTrue(all(record['site'] == 'Site name' 
                        for record in records))
        self.assertTrue(all(record['version'] == 'RAW' 
                        for record in records))

        ymds = [(record['sampledate'].year(), 
                 record['sampledate'].month(),
                 record['sampledate'].day()) for record in records] 
        self.assertTrue(all(ymd == (2015, 2, 10) for ymd in ymds))

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
            units = [record['units'] for record in records 
                if record['parameter'] == param]
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
            values = [record['samplevalue'] for record in records 
                if record['location'] == location]
            self.assertEqual(values, expected[i], 
                             "Error in records %s for location %s" 
                             % (values[i], location))
        

if __name__ == '__main__':
    unittest.main()
