# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

import unittest
import yaml
import codecs
from monitoring import importdata

class DataImportTestCase(unittest.TestCase):
    def testChemtest(self):
        configFileName = 'lab_import.yml'
        configFile = codecs.open(configFileName, encoding='utf-8')
        config = yaml.load(configFile.read()).next()
        configFile.close()
        
        records = importdata.locationsAcross(config)
        self.assertEqual(len(records), 106)
        
        sites = [record['site'] for record in records] 
        self.assertEqual(sites, ['Site name'] * len(sites))
        
        versions = [record['version'] for record in records] 
        self.assertEqual(versions, ['RAW'] * len(versions))

        ymds = [(record['sampledate'].year(), 
                 record['sampledate'].month(),
                 record['sampledate'].day()) for record in records] 
        self.assertEqual(ymds, [(2015, 2, 10)] * len(ymds))
        
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
