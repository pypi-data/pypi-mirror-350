# -*- coding: utf-8 -*-
import unittest
import datetime

from caplib.datetime import *

class TestDateTime(unittest.TestCase):
    def test_to_frequency(self):
        expected = ANNUAL
        test = to_frequency('annual')    
        self.assertEqual(test, expected)
        
    def test_to_day_count_convention(self):
        expected = ACT_365_FIXED
        test = to_day_count_convention('act_365_fixed')    
        self.assertEqual(test, expected)
        
    def test_to_business_day_convention(self):
        expected = MODIFIED_FOLLOWING
        test = to_business_day_convention('modified_following')    
        self.assertEqual(test, expected)
        
    def test_to_stub_policy(self):
        expected = FINAL
        test = to_stub_policy('final')    
        self.assertEqual(test, expected)
        
    def test_to_broken_period_type(self):
        expected = LONG
        test = to_broken_period_type('long')    
        self.assertEqual(test, expected)
    
    def test_to_sched_gen_method(self):
        expected = ABSOLUTE_NORMAL
        test = to_sched_gen_method('absolute_normal')    
        self.assertEqual(test, expected)
    
    def test_to_date_roll_convention(self):
        expected = EOM
        test = to_date_roll_convention('eom')    
        self.assertEqual(test, expected)
    
    def test_to_date_gen_mode(self):
        expected = IN_ARREAR
        test = to_date_gen_mode('in_arrear')    
        self.assertEqual(test, expected)
        
    def test_to_period(self):
        expected = b'\x08\x03\x10\x1e'
        test = to_period('3m') 
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_date(self):
        expected = b'\x08\xe6\x0f\x10\x03\x18\x18'
        test = create_date(datetime(2022,3,24))        
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_date(self):
        expected = b'\x08\xed\x0e\x10\x01\x18\x01' 
        test = create_date(None)
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_calendar(self):
        # List of serial numbers
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        test = create_calendar('CAL_CFETS', holidays, specials)
        self.assertEqual(test, True)
        
    def test_create_period(self):
        expected = b'\x08\x03\x10\x1e\x18\x01'
        test = create_period(3, 'MONTHS') 
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_year_frac_calculator(self):
        start = create_date(datetime(2022, 3, 7))
        end = create_date(datetime(2023,6,7))
        day_count = 'ACT_365_FIXED'
        test = year_frac_calculator(start, end, day_count, start, end, end)
        self.assertEqual(test, 1.252054794520548)
        
    def test_simple_year_frac_calculator(self):
        start = create_date(datetime(2022, 3, 7))
        end = create_date(datetime(2023,6,7))
        day_count = 'ACT_365_FIXED'
        test = simple_year_frac_calculator(start, end, day_count)
        self.assertEqual(test, 1.252054794520548)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDateTime)
    unittest.TextTestRunner(verbosity=2).run(suite)