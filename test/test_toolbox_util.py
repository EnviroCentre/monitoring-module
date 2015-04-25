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

if __name__ == '__main__':
    unittest.main()

