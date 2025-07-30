# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:54:12 2022

@author: dingq
"""
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from caplib.datetime import *
from caplib.market import *

class TestMarket(unittest.TestCase):
    def setUp(self) -> None:
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        create_calendar('CAL_CFETS', holidays, specials)
        
    def test_create_time_series(self):
        expected = b'\n\x07\x08\xe6\x0f\x10\x03\x18\x03\n\x07\x08\xe6\x0f\x10\x03\x18\x04\x12\x18\x08\x02\x10\x01\x1a\x10{\x14\xaeG\xe1z\x84?\xb8\x1e\x85\xebQ\xb8\x9e? \x01"\tSHIBOR_3M'
        dates = [datetime(2022, 3, 3), datetime(2022, 3, 4)]
        values = [0.01, 0.03]
        test = create_time_series(dates, values, 'TS_FORWARD_MODE', 'shibor_3m')
        self.assertEqual(test.SerializeToString(), expected)

    def test_to_time_series_mode(self):
        expected = TimeSeries.Mode.TS_FORWARD_MODE
        test = to_time_series_mode('TS_FORWARD_MODE')
        self.assertEqual(test, expected)

    def test_to_ccy_pair(self):
        expected = b'\n\x05\n\x03USD\x12\x05\n\x03CNY'
        test = to_ccy_pair('usdcny')
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_foreign_exchange_rate(self):
        expected = b'\t\x87\xa7W\xca2\xc4\x1a@\x12\x03CNY\x1a\x03USD'
        test = create_foreign_exchange_rate(6.6916, "USD", "CNY")
        #print('test_create_foreign_exchange_rate:', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_fx_spot_rate(self):
        expected = b'\n\x13\t\x87\xa7W\xca2\xc4\x1a@\x12\x03CNY\x1a\x03USD\x12\x07\x08\xe6\x0f\x10\x03\x18\t\x1a\x07\x08\xe6\x0f\x10\x03\x18\t'
        foreign_exchange_rate = create_foreign_exchange_rate(6.6916, "USD", "CNY")
        test = create_fx_spot_rate(foreign_exchange_rate, datetime(2022, 3, 9), datetime(2022, 3, 9))
        #print('test_create_fx_spot_rate:', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_fx_spot_template(self):
        expected = b'\x08\xb9\x17\x12\nTestFxSpot\x1a\x0e\n\x05\n\x03USD\x12\x05\n\x03CNY \x012\x04\x08\x01\x10\x01:\tCAL_CFETS'
        test = create_fx_spot_template(inst_name="TestFxSpot",
                                       currency_pair="USDCNY",
                                       spot_day_convention="FOLLOWING",
                                       calendars=["CAL_CFETS"],
                                       spot_delay="1d")
        self.assertEqual(test.SerializeToString(), expected)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMarket)
    unittest.TextTestRunner(verbosity=2).run(suite)
