# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 19:43:23 2022

@author: dingq
"""

import unittest
from datetime import datetime

from caplib.analytics import *
from caplib.fimarket import *
from caplib.datetime import *

class TestFiMarket(unittest.TestCase):
    
    def setUp(self):
        cny_ccy = 'cny'
        
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        create_calendar('CAL_CFETS', holidays, specials)
        
        shibor_3m = 'shibor_3m'
        create_ibor_index(shibor_3m, '3m', cny_ccy, ['CAL_CFETS'], 1)
        
        issue_date = datetime(2021, 12, 21)
        start_date = datetime(2021, 12, 22)
        maturity = '180d'
        self.zero_cpn_bond_tempalte = create_zero_cpn_bond_template('TestZeroCpnBond', issue_date, 1, start_date, maturity,
                                                                    'cny', 97.6, 'cal_cfets')
        maturity = '3Y'
        self.fixed_cpn_bond_template = create_fixed_cpn_bond_template('TestFixedCpnBond', issue_date, 1, start_date, maturity,
                                                                      3.05e-2, 'cny', 'cal_cfets')
        
        issue_date = datetime(2022, 3, 23)
        start_date = datetime(2022, 3, 24)
        maturity = '2Y'
        self.flt_cpn_bond_template = create_vanilla_bond_template('TestVanillaBond', 'FLOATING_COUPON_BOND', issue_date, 1, start_date,maturity,
                                                                  2.8e-3, 'CNY', 100,                                 
                                                                  'ACT_360',
                                                                  'CAL_CFETS', 'ANNUAL', 'MODIFIED_FOLLOWING', 'INITIAL', 'LONG',
                                                                  0, 'MODIFIED_FOLLOWING',
                                                                  'LPR1Y',  
                                                                  ['CAL_CFETS'], 'ANNUAL', 'MODIFIED_PRECEDING', 'IN_ADVANCE', -1,
                                                                  '0D', 'CAL_CFETS', 'INVALID_BUSINESS_DAY_CONVENTION' , False)
        fixing_dates = [datetime(2022, 3, 22), datetime(2022,3,24)]
        fixing_values = [3.01e-2, 3.02e-2]
        self.lpr1y_fixings = create_time_series(fixing_dates, fixing_values)
    
    def test_to_vanilla_bond_type(self):
        expected = FLOATING_COUPON_BOND
        test = to_vanilla_bond_type('floating_coupon_bond')    
        self.assertEqual(test, expected)
        
    def test_create_zero_cpn_bond_template(self):
        expected=b'\n\x0fTESTZEROCPNBOND\x10\x02\x18\x01"]\x08\x01\x12\x03CNY\x18\x02(\x010\x018\x01@\x01H\x05jH\n\x15\x08\x01\x1a\tcal_cfets \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tcal_cfets \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a\x0e\x08\x03\x10\x018\x01B\x04\x10\x01\x18\x01H\x02*\x02\x10\x01J\x07\x08\xe5\x0f\x10\x0c\x18\x15Z\x05\x08\xb4\x01\x10\x01affffffX@j\x07\x08\xe5\x0f\x10\x0c\x18\x16'
        issue_date = datetime(2021, 12, 21)
        start_date = datetime(2021, 12, 22)
        maturity = '180d'
        test = create_zero_cpn_bond_template('TestZeroCpnBond', issue_date, 1, start_date, maturity,
                                             'cny', 97.6, 'cal_cfets')
        #print('test_create_zero_cpn_bond_template',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)   
        
    def test_create_fixed_cpn_bond_template(self):
        expected=b'\n\x10TESTFIXEDCPNBOND\x18\x01"]\x08\x01\x12\x03CNY\x18\x02(\x010\x018\x01@\x01H\x05jH\n\x15\x08\x01\x1a\tcal_cfets \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tcal_cfets \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a\x0e\x08\x03\x10\x018\x01B\x04\x10\x01\x18\x01H\x02*\x02\x10\x01J\x07\x08\xe5\x0f\x10\x0c\x18\x15Q\x08\xac\x1cZd;\x9f?Z\x05\x08\xd0\x05\x10\x01a\x00\x00\x00\x00\x00\x00Y@j\x07\x08\xe5\x0f\x10\x0c\x18\x16'
        issue_date = datetime(2021, 12, 21)
        start_date = datetime(2021, 12, 22)
        maturity ='720d'
        test = create_fixed_cpn_bond_template('TestFixedCpnBond', issue_date, 1, start_date, maturity,
                                              3.05e-2, 'cny', 'cal_cfets')
        #print('test_create_fixed_cpn_bond_template',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)  
        
    def test_create_vanilla_bond_template(self):
        expected =b'\n\x0fTESTVANILLABOND\x10\x01\x18\x01"\x80\x01\x08\x02\x12\x03CNY\x18\x01"\x05LPR1Y(\x010\x018\x01@\x01H\x05jd\n\x15\x08\x01\x1a\tCAL_CFETS \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a*\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x040\x018\x01B\x0f\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x01\x18\x01H\x02*\x02\x10\x012\tCAL_CFETSJ\x07\x08\xe5\x0f\x10\x0c\x18\x15Qy\xe9&1\x08\xac\x9c?Z\x05\x08\xd0\x05\x10\x01a\x00\x00\x00\x00\x00\x00Y@j\x07\x08\xe5\x0f\x10\x0c\x18\x16'
        issue_date = datetime(2021, 12, 21)
        start_date = datetime(2021, 12, 22)
        maturity = '720d'
        test = create_vanilla_bond_template('TestVanillaBond', 'FLOATING_COUPON_BOND', issue_date, 1, start_date, maturity,
                                            2.8e-2, 'CNY', 100,                                 
                                            'ACT_360',
                                            'CAL_CFETS', 'ANNUAL', 'MODIFIED_FOLLOWING', 'INITIAL', 'LONG',
                                            0, 'MODIFIED_FOLLOWING',
                                            'LPR1Y',  
                                            ['CAL_CFETS'], 'ANNUAL', 'MODIFIED_PRECEDING', 'IN_ADVANCE', -1,
                                            '0D', 'CAL_CFETS', 'INVALID_BUSINESS_DAY_CONVENTION', False)
        #print('test_create_vanilla_bond_template',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)  
        
    def test_create_std_zero_cpn_bond_template(self):
        expected =b'\n\x12TESTREFZEROCPNBOND\x10\x02\x18\x01"]\x08\x01\x12\x03CNY\x18\x02(\x010\x018\x01@\x01H\x05jH\n\x15\x08\x01\x1a\tCAL_CFETS \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a\x0e\x08\x03\x10\x018\x01B\x04\x10\x01\x18\x01H\x02*\x02\x10\x01J\x07\x08\xed\x0e\x10\x01\x18\x01Z\x04\x08\x03\x10\x1ea\x00\x00\x00\x00\x00\x00Y@j\x07\x08\xed\x0e\x10\x01\x18\x01'
        test = create_std_zero_cpn_bond_template('TestRefZeroCpnBond', create_date(None), '3M', 'CNY', 'CAL_CFETS', 100.0)
        #print('test_create_std_zero_cpn_bond_template',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)  
        
    def test_create_std_fixed_cpn_bond_template(self):
        expected =b'\n\x13TESTREFFIXEDCPNBOND\x18\x01"]\x08\x01\x12\x03CNY\x18\x02(\x010\x018\x01@\x01H\x05jH\n\x15\x08\x01\x1a\tCAL_CFETS \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a\x0e\x08\x03\x10\x018\x01B\x04\x10\x01\x18\x01H\x02*\x02\x10\x01J\x07\x08\xed\x0e\x10\x01\x18\x01Z\x05\x08\x03\x10\xed\x02a\x00\x00\x00\x00\x00\x00Y@j\x07\x08\xed\x0e\x10\x01\x18\x01'
        test = create_std_fixed_cpn_bond_template('TestRefFixedCpnBond',create_date(None), '3Y','CNY', 'CAL_CFETS', 0.0)
        #print('test_create_std_fixed_cpn_bond_template',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)  
    
    def test_create_std_bond_template(self):
        expected =b'\n\x11TESTREFFLTCPNBOND\x10\x01\x18\x01"\x80\x01\x08\x02\x12\x03CNY\x18\x01"\x05LPR1Y(\x010\x018\x01@\x01H\x05jd\n\x15\x08\x01\x1a\tCAL_CFETS \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a*\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x040\x018\x01B\x0f\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x01\x18\x01H\x02*\x02\x10\x01J\x07\x08\xed\x0e\x10\x01\x18\x01Z\x05\x08\x03\x10\xed\x02a\x00\x00\x00\x00\x00\x00Y@j\x07\x08\xed\x0e\x10\x01\x18\x01'
        maturity ='3Y'
        test = create_std_bond_template('TestRefFltCpnBond', 'FLOATING_COUPON_BOND', create_date(None), 1, maturity,
                                        'CNY',                         
                                        'ACT_360',
                                        'CAL_CFETS', 'ANNUAL', 'MODIFIED_FOLLOWING', 'INITIAL', 'LONG',
                                        0, 'MODIFIED_FOLLOWING', 0.0, 100.0,
                                        'LPR1Y',  
                                        ['CAL_CFETS'], 'ANNUAL', 'MODIFIED_PRECEDING', 'IN_ADVANCE', -1)
        #print('test_create_std_bond_template',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)  
        
    def test_build_zero_cpn_bond(self):
        expected = b'\n#\n\x07\x08\xe5\x0f\x10\x0c\x18\x15\x10\x01\x1a\tCAL_CFETS"\x02\x10\x01AffffffX@\x10\x02\x1a\xb2\x01\n\x9f\x01\x08\x01\x12]\x08\x01\x12\x03CNY\x18\x02(\x010\x018\x01@\x01H\x05jH\n\x15\x08\x01\x1a\tCAL_CFETS \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a\x0e\x08\x03\x10\x018\x01B\x04\x10\x01\x18\x01H\x02\x1a<\n:\n\x07\x08\xe6\x0f\x10\x06\x18\x14\x12&\n$\n\x07\x08\xe5\x0f\x10\x0c\x18\x16\x12\x07\x08\xe5\x0f\x10\x0c\x18\x16\x1a\x07\x08\xe6\x0f\x10\x06\x18\x14)\x00\x00\x00\x00\x00\x00\xf0?\x19\x00\x00\x00\x00`\xe3FA\x1a\x0e\n\x03CNY\x11\x00\x00\x00\x00`\xe3FA'
        test = build_zero_cpn_bond(3.0e6, self.zero_cpn_bond_tempalte)
        #print('test_build_zero_cpn_bond',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)  
        
    def test_build_fixed_cpn_bond(self):
        expected =b'\n#\n\x07\x08\xe5\x0f\x10\x0c\x18\x15\x10\x01\x1a\tCAL_CFETS"\x02\x10\x01A\x00\x00\x00\x00\x00\x00Y@\x1a\xb4\x02\n\x98\x02\x08\x01\x12]\x08\x01\x12\x03CNY\x18\x02(\x010\x018\x01@\x01H\x05jH\n\x15\x08\x01\x1a\tCAL_CFETS \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a\x0e\x08\x03\x10\x018\x01B\x04\x10\x01\x18\x01H\x02\x1a\xb4\x01\n:\n\x07\x08\xe6\x0f\x10\x0c\x18\x16\x12&\n$\n\x07\x08\xe5\x0f\x10\x0c\x18\x16\x12\x07\x08\xe5\x0f\x10\x0c\x18\x16\x1a\x07\x08\xe6\x0f\x10\x0c\x18\x16)\x00\x00\x00\x00\x00\x00\xf0?\x19\x00\x00\x00\x00`\xe3FA\n:\n\x07\x08\xe7\x0f\x10\x0c\x18\x16\x12&\n$\n\x07\x08\xe6\x0f\x10\x0c\x18\x16\x12\x07\x08\xe6\x0f\x10\x0c\x18\x16\x1a\x07\x08\xe7\x0f\x10\x0c\x18\x16)\x00\x00\x00\x00\x00\x00\xf0?\x19\x00\x00\x00\x00`\xe3FA\n:\n\x07\x08\xe8\x0f\x10\x0c\x18\x17\x12&\n$\n\x07\x08\xe7\x0f\x10\x0c\x18\x16\x12\x07\x08\xe7\x0f\x10\x0c\x18\x16\x1a\x07\x08\xe8\x0f\x10\x0c\x18\x17)\x00\x00\x00\x00\x00\x00\xf0?\x19\x00\x00\x00\x00`\xe3FA\x11\x08\xac\x1cZd;\x9f?\x1a\x0e\n\x03CNY\x11\x00\x00\x00\x00`\xe3FA'
        test = build_fixed_cpn_bond(3.0e6, self.fixed_cpn_bond_template)
        #print('test_build_fixed_cpn_bond',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)   
        
    def test_build_vanilla_bond(self):     
        expected = b'\n#\n\x07\x08\xe6\x0f\x10\x03\x18\x17\x10\x01\x1a\tCAL_CFETS"\x02\x10\x01A\x00\x00\x00\x00\x00\x00Y@\x10\x01\x1a\x9b\x02\n\xff\x01\x08\x01\x12\x80\x01\x08\x02\x12\x03CNY\x18\x01"\x05LPR1Y(\x010\x018\x01@\x01H\x05jd\n\x15\x08\x01\x1a\tCAL_CFETS \x01(\x020\x018\x02\x12\x1f\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x020\x028\x01B\x04\x10\x01\x18\x01H\x02\x1a*\x08\x03\x10\x01\x1a\tCAL_CFETS \x01(\x040\x018\x01B\x0f\x08\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x10\x01\x18\x01H\x02\x1ax\n:\n\x07\x08\xe7\x0f\x10\x03\x18\x18\x12&\n$\n\x07\x08\xe6\x0f\x10\x03\x18\x17\x12\x07\x08\xe6\x0f\x10\x03\x18\x18\x1a\x07\x08\xe7\x0f\x10\x03\x18\x18)\x00\x00\x00\x00\x00\x00\xf0?\x19\x00\x00\x00\x00`\xe3FA\n:\n\x07\x08\xe8\x0f\x10\x03\x18\x19\x12&\n$\n\x07\x08\xe7\x0f\x10\x03\x18\x17\x12\x07\x08\xe7\x0f\x10\x03\x18\x18\x1a\x07\x08\xe8\x0f\x10\x03\x18\x19)\x00\x00\x00\x00\x00\x00\xf0?\x19\x00\x00\x00\x00`\xe3FA\x11\xc7\xba\xb8\x8d\x06\xf0f?\x1a\x0e\n\x03CNY\x11\x00\x00\x00\x00`\xe3FA'
        test = build_vanilla_bond(3.0e6, self.flt_cpn_bond_template, self.lpr1y_fixings)       
        #print('test_build_vanilla_bond',test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)   
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFiMarket)
    unittest.TextTestRunner(verbosity=2).run(suite)