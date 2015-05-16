# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

import unittest
import monitoring as mon


class RecordTestCase(unittest.TestCase):

    def testRecordValueList(self):
        r = mon.Record(values=[1, 2, 3])
        self.assertEqual(r.values, [1, 2, 3])

    def testRecordSingleValue(self):
        r = mon.Record(values=1)
        self.assertEqual(r.values, [1])

    def testRecordLoggerOrigin(self):
        r = mon.Record(values=[1, 2, 3])
        self.assertEqual(r.origin, 'logger')

    def testRecordSampleOrigin(self):
        r = mon.Record(values=1)
        self.assertEqual(r.origin, 'sample')

    def testRecordTimesList(self):
        r = mon.Record(values=[1, 2, 3], startTime=0, interval=10)
        self.assertEqual(r.times, [0, 10, 20])

    def testRecordEndTime(self):
        r = mon.Record(values=[1, 2, 3], startTime=0, interval=10)
        self.assertEqual(r.endTime, 20)

    def testRecordLength(self):
        r = mon.Record(values=[1, 2, 3])
        self.assertEqual(len(r), 3)

    def testRecordSingleTime(self):
        r = mon.Record(values=1, startTime=0)
        self.assertEqual(r.times, [0])

    def testRecordIrregularInterval(self):
        r = mon.Record(values=1)
        self.assertEqual(r.interval, -1)

    def testRecordIrregularIntervalForce(self):
        """Single-value records always treated as irregular"""
        r = mon.Record(values=1, interval=999)
        self.assertEqual(r.interval, -1)
        
    def testIntervalStr15Min(self):
        r = mon.Record(interval=15)
        self.assertEqual(r.intervalStr, '15MIN')

    def testIntervalStr59Min(self):
        r = mon.Record(interval=59)
        self.assertEqual(r.intervalStr, '59MIN')

    def testIntervalStr1Hour(self):
        r = mon.Record(interval=60)
        self.assertEqual(r.intervalStr, '1HOUR')

    def testIntervalStr23Hour(self):
        r = mon.Record(interval=23*60)
        self.assertEqual(r.intervalStr, '23HOUR')

    def testIntervalStr1Day(self):
        r = mon.Record(interval=24*60)
        self.assertEqual(r.intervalStr, '1DAY')

    def testIntervalStr2Day(self):
        r = mon.Record(interval=24*60*2)
        self.assertEqual(r.intervalStr, '2DAY')


if __name__ == '__main__':
    unittest.main()

