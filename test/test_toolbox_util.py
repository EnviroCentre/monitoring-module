import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

import unittest
import toolbox.util

class ToolboxUtilTestCase(unittest.TestCase):

    def test_parseMeasurement(self):
        result = toolbox.util.parseMeasurement("1.234")
        self.assertEqual(result, 1.234)

    def test_parseMeasurementSpaces(self):
        result = toolbox.util.parseMeasurement(" 1.234 ")
        self.assertEqual(result, 1.234)

    def test_parseMeasurementBelowLOD(self):
        result = toolbox.util.parseMeasurement("<2.0")
        self.assertEqual(result, 1.0)

    def test_parseMeasurementBelowLODSpaces(self):
        result = toolbox.util.parseMeasurement(" < 2.0 ")
        self.assertEqual(result, 1.0)
        
    def test_dateDefaultFormat(self):
        dt = toolbox.util.parseDateAndTime("2015/12/31", "01:00:00")
        self.assertEqual(dt.year(), 2015)
        self.assertEqual(dt.month(), 12)
        self.assertEqual(dt.day(), 31)
        self.assertEqual(dt.hour(), 1)
        self.assertEqual(dt.minute(), 0)

    def test_dateyyyymmddFormat(self):
        dt = toolbox.util.parseDateAndTime("2015/12/31", "01:00:00", "yyyy/mm/dd")
        self.assertEqual(dt.year(), 2015)
        self.assertEqual(dt.month(), 12)
        self.assertEqual(dt.day(), 31)
        self.assertEqual(dt.hour(), 1)
        self.assertEqual(dt.minute(), 0)

if __name__ == '__main__':
    unittest.main()
