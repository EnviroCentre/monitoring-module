import unittest
import toolbox.util

class ToolboxUtilTestCase(unittest.TestCase):

    def testParseMeasurement(self):
        result = toolbox.util.parseMeasurement("1.234")
        self.assertEqual(result, (1.234, 3))

    def testParseMeasurementSpaces(self):
        result = toolbox.util.parseMeasurement(" 1.234 ")
        self.assertEqual(result, (1.234, 3))

    def testParseMeasurementBelowLOD(self):
        result = toolbox.util.parseMeasurement("<2.0")
        self.assertEqual(result, (1.0, 16777347))

    def testParseMeasurementBelowLODSpaces(self):
        result = toolbox.util.parseMeasurement(" < 2.0 ")
        self.assertEqual(result, (1.0, 16777347))
        
    def testDateDefaultFormat(self):
        dt = toolbox.util.parseDateTime("2015/12/31", "01:00:00")
        self.assertEqual(dt.year(), 2015)
        self.assertEqual(dt.month(), 12)
        self.assertEqual(dt.day(), 31)
        self.assertEqual(dt.hour(), 1)
        self.assertEqual(dt.minute(), 0)

    def testDateyyyymmddFormat(self):
        dt = toolbox.util.parseDateTime("2015/12/31", "01:00:00", "%Y/%m/%d")
        self.assertEqual(dt.year(), 2015)
        self.assertEqual(dt.month(), 12)
        self.assertEqual(dt.day(), 31)
        self.assertEqual(dt.hour(), 1)
        self.assertEqual(dt.minute(), 0)

    def testDateddmmmyyFormat(self):
        dt = toolbox.util.parseDateTime("31-Dec-15", "01:00:00", "%d-%b-%y")
        self.assertEqual(dt.year(), 2015)
        self.assertEqual(dt.month(), 12)
        self.assertEqual(dt.day(), 31)
        self.assertEqual(dt.hour(), 1)
        self.assertEqual(dt.minute(), 0)
        
    def testIndexIgnoreCase(self):
        row = ['hello', 'World']
        self.assertEqual(toolbox.util.index_ign_case(row, 'HELLO'), 0)
        self.assertEqual(toolbox.util.index_ign_case(row, 'world'), 1)
        self.assertEqual(toolbox.util.index_ign_case(row, 'World'), 1)


if __name__ == '__main__':
    unittest.main()
