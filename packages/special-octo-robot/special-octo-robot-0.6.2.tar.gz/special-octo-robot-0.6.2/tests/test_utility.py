import unittest
from datetime import datetime
import time
from app.utility import convert_time_to_epoch, convert_epoch_to_time, get_week_start, get_weekend

class ConvertToEpoch(unittest.TestCase):
    def test_positive(self):
        date_obj = datetime(2020, 12, 31, hour=23, minute=59, second=59)
        epoch_time = int(time.mktime(date_obj.timetuple()))
        self.assertEqual(convert_time_to_epoch("2020-12-31"), epoch_time)
        self.assertEqual(convert_time_to_epoch("2020/12/31"), epoch_time)
        self.assertEqual(convert_time_to_epoch("31.12.2020"), epoch_time)
        self.assertEqual(convert_time_to_epoch("31-12-2020"), epoch_time)
        self.assertEqual(convert_time_to_epoch("31/12/2020"), epoch_time)
        self.assertEqual(convert_time_to_epoch("31\\12\\2020"), epoch_time)
        self.assertEqual(convert_time_to_epoch("31|12|2020"), epoch_time)
        self.assertEqual(convert_time_to_epoch("31_12_2020"), epoch_time)
        self.assertEqual(convert_time_to_epoch("31,12,2020"), epoch_time)
        date_obj = datetime(2020, 12, 31, hour=0, minute=0, second=0)
        epoch_time = int(time.mktime(date_obj.timetuple()))
        self.assertEqual(convert_time_to_epoch("2020-12-31", False), epoch_time)
    
    def test_negative(self):
        self.assertEqual(convert_time_to_epoch("2020-12-31-12"), "Length not 3")
        self.assertEqual(convert_time_to_epoch("20020100"),"No separator found")
        self.assertEqual(convert_time_to_epoch("20-00-03"),"month must be in 1..12")
        self.assertEqual(convert_time_to_epoch("20-13-03"),"month must be in 1..12")
        self.assertEqual(convert_time_to_epoch("20-12-00"),"year 0 is out of range")
        self.assertEqual(convert_time_to_epoch("a-b-c"),"invalid literal for int() with base 10: 'c'")
        
class ConvertEpochToTime(unittest.TestCase):
    def test_positive(self):
        date_str = "31-12-2020"
        epoch = convert_time_to_epoch(date_str)
        self.assertEqual(convert_epoch_to_time(epoch), date_str)
    
    def test_negative(self):
        self.assertEqual(convert_epoch_to_time(0), "None")
        self.assertEqual(convert_epoch_to_time("abc"), "'str' object cannot be interpreted as an integer")
        
class GetWeekEnds(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(get_weekend(), "01-09-2024")
        self.assertEqual(get_week_start(), "26-08-2024")