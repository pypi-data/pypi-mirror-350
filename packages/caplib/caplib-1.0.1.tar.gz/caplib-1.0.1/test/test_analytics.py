# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from caplib.analytics import *

class TestAnalytics(unittest.TestCase):
    
    def test_create_default_model_settings(self):
        expected = b'\x08\x01\x12\x08\x00\x00\x00\x00\x00\x00\x00\x00'
        test = create_model_settings('BLACK_SCHOLES_MERTON')
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_model_settings(self):
        expected = b'\x08\x01\x12\x08{\x14\xaeG\xe1z\x84?\x1a\x00"\nEURIBOR_3M'
        model_name = 'BLACK_SCHOLES_MERTON'
        const_params = [0.01]
        ts_params = [TermStructureCurve()]
        underlying = 'EURIBOR_3M'
        calib = False
        test = create_model_settings(model_name, const_params, ts_params, underlying, calib)
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_pde_settings(self):
        expected = b'\x082\x10d\x19\x00\x00\x00\x00\x00\x00\x10\xc0!\x00\x00\x00\x00\x00\x00\x10@0\x039\x00\x00\x00\x00\x00\x00\x10\xc0A\x00\x00\x00\x00\x00\x00\x10@P\x03Y\x00\x00\x00\x00\x00\x00\x10\xc0a\x00\x00\x00\x00\x00\x00\x10@q\x00\x00\x00\x00\x00\x00\xf0?y\x00\x00\x00\x00\x00\x00\xf0?\x81\x01\x00\x00\x00\x00\x00\x00\xf0?\x88\x01\x01\x90\x01\x01\x98\x01\x01\xa0\x01\x01\xa8\x01\x01\xb0\x01\x01'
        test = create_pde_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_pde_settings(self):
        expected = b'\x08e\x10\xc9\x01\x19\x00\x00\x00\x00\x00\x00\x14\xc0!\x00\x00\x00\x00\x00\x00\x14@0\x0bA\x00\x00\x00\x00\x00\x00$@H\x01P\x03Y\x00\x00\x00\x00\x00\x00\x10\xc0a\x00\x00\x00\x00\x00\x00\x10@q\x9a\x99\x99\x99\x99\x99\xb9?y\x9a\x99\x99\x99\x99\x99\xb9?\x81\x01\x00\x00\x00\x00\x00\x00\xf0?\x88\x01\x02\x90\x01\x01\x98\x01\x01\xa0\x01\x02\xa8\x01\x01\xb0\x01\x01'
        test = create_pde_settings(101,201, -5, 5, 'MMT_NUM_STDEVS', 0.1, 'ADAPTIVE_GRID', 'CUBIC_SPLINE_INTERP',
                                   11, 0, 10, 'MMT_ABOSLUTE', 0.1, 'UNIFORM_GRID', 'LINEAR_INTERP')
        self.assertEqual(test.SerializeToString(), expected)
    
    def test_create_default_monte_carlo_settings(self):
        expected = b'\x08\x80\x08\x18\x80\x08 \x01(\x018\x01'
        test = create_monte_carlo_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_monte_carlo_settings(self):
        expected = b'\x08\xb8\x17\x10\x01\x18\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01 \x02(\x010\x018e'
        test = create_monte_carlo_settings(3000, 
                                           'MERSENNE_TWIST_19937_NUMBER',  
                                           -1, 
                                           'INCREMENTAL_METHOD', 
                                           'INVERSE_CUMULATIVE_METHOD', True, 101)
        self.assertEqual(test.SerializeToString(), expected)
     
    def test_create_model_free_pricing_settings(self):
        expected = b'\nl\x082\x10d\x19\x00\x00\x00\x00\x00\x00\x10\xc0!\x00\x00\x00\x00\x00\x00\x10@0\x039\x00\x00\x00\x00\x00\x00\x10\xc0A\x00\x00\x00\x00\x00\x00\x10@P\x03Y\x00\x00\x00\x00\x00\x00\x10\xc0a\x00\x00\x00\x00\x00\x00\x10@q\x00\x00\x00\x00\x00\x00\xf0?y\x00\x00\x00\x00\x00\x00\xf0?\x81\x01\x00\x00\x00\x00\x00\x00\xf0?\x88\x01\x01\x90\x01\x01\x98\x01\x01\xa0\x01\x01\xa8\x01\x01\xb0\x01\x01\x12\x0c\x08\x80\x08\x18\x80\x08 \x01(\x018\x01\x1a\x0c\x08\x01\x12\x08\x00\x00\x00\x00\x00\x00\x00\x00'
        test = create_model_free_pricing_settings('', False)
        #print('test_create_model_free_pricing_settings', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_pricing_settings(self):
        expected = b'\nl\x082\x10d\x19\x00\x00\x00\x00\x00\x00\x10\xc0!\x00\x00\x00\x00\x00\x00\x10@0\x039\x00\x00\x00\x00\x00\x00\x10\xc0A\x00\x00\x00\x00\x00\x00\x10@P\x03Y\x00\x00\x00\x00\x00\x00\x10\xc0a\x00\x00\x00\x00\x00\x00\x10@q\x00\x00\x00\x00\x00\x00\xf0?y\x00\x00\x00\x00\x00\x00\xf0?\x81\x01\x00\x00\x00\x00\x00\x00\xf0?\x88\x01\x01\x90\x01\x01\x98\x01\x01\xa0\x01\x01\xa8\x01\x01\xb0\x01\x01\x12\x0c\x08\x80\x08\x18\x80\x08 \x01(\x018\x01\x1a\x0c\x08\x01\x12\x08\x00\x00\x00\x00\x00\x00\x00\x00:\x03CNY'
        test = create_pricing_settings('CNY', False, create_model_settings('BLACK_SCHOLES_MERTON'), 'ANALYTICAL', create_pde_settings(), create_monte_carlo_settings())
        #print('test_create_pricing_settings', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_ir_curve_risk_settings(self):
        expected = b'!-C\x1c\xeb\xe26\x1a?){\x14\xaeG\xe1zt?A-C\x1c\xeb\xe26\x1a?'
        test = create_ir_curve_risk_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_ir_curve_risk_settings(self):
        expected = b'\x08\x01\x10\x01\x18\x01!-C\x1c\xeb\xe26*?){\x14\xaeG\xe1zt?8\x01A-C\x1c\xeb\xe26*?H\x01'
        test = create_ir_curve_risk_settings(True,True, True,2.0e-4, 50e-4, 
                                             'CENTRAL_DIFFERENCE_METHOD', 
                                             'TERM_BUCKET_RISK', 2.0e-4, 
                                             'MULTI_THREADING_MODE')
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_credit_curve_risk_settings(self):
        expected = b'!-C\x1c\xeb\xe26\x1a?A-C\x1c\xeb\xe26\x1a?'
        test = create_credit_curve_risk_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_theta_risk_settings(self):
        expected = b'\x10\x01\x19\x1ag\x016\x9fqf?'
        test = create_theta_risk_settings()
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_theta_risk_settings(self):
        expected = b'\x08\x01\x10\x01\x19\x1ag\x016\x9fqf?'
        test = create_theta_risk_settings(True, 1, 1./365.)
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_default_ir_yield_curve(self):
        expected = b'\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03CNY \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01'
        test = create_ir_yield_curve(datetime(2022,3,9),'CNY', [datetime(2022,3,10), datetime(2025,3,10)], [0.02, 0.025])
        #pprint('test_create_default_ir_yield_curve', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_ir_yield_curve(self):
        expected = b'\x12P\nL\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x02ON"\x023Y*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01B\rCNY_SHIBOR_3M\x10\x02\x1a\x03CNY \x01:!\n\rCNY_SHIBOR_3M\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01'
        test = create_ir_yield_curve(datetime(2022,3,9),'CNY', 
                                     [datetime(2022,3,10), datetime(2025,3,10)], 
                                     [0.02, 0.025], 
                                     'ACT_365_FIXED', 'LINEAR_INTERP', 'FLAT_EXTRAP', 'DISCRETE_COMPOUNDING', 'ANNUAL', 
                                     [0.0], 'CNY_SHIBOR_3M', ['ON', '3Y'])
        #pprint('test_create_ir_yield_curve', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
        
    def test_create_credit_curve(self):
        expected =  b'\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10\xfc\xa9\xf1\xd2Mb`?{\x14\xaeG\xe1zd?0\x018\x01\x12\x12\n\x10\xfc\xa9\xf1\xd2Mb`?{\x14\xaeG\xe1zd?'
        test = create_credit_curve(datetime(2022,3,9), 
                                   [datetime(2022,3,10), datetime(2025,3,10)], [0.2e-2, 0.25e-2])
        #print('test_create_credit_curve', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)
   
    def test_create_ir_yield_curve_from_binary(self):
       expected = b'\x12\xe7\x03\n\xe2\x03\n\x07\x08\xe8\x0f\x10\x08\x18\x1b\x10\x02\x1a\x07\x08\xe8\x0f\x10\t\x18\x12\x1a\x07\x08\xe8\x0f\x10\n\x18\x19\x1a\x07\x08\xe8\x0f\x10\x0b\x18\x12\x1a\x07\x08\xe9\x0f\x10\x01\x18\r\x1a\x07\x08\xe9\x0f\x10\x04\x18\x19\x1a\x07\x08\xe9\x0f\x10\x07\x18\x19\x1a\x07\x08\xea\x0f\x10\x06\x18\x0f\x1a\x07\x08\xea\x0f\x10\x0c\x18\x07\x1a\x07\x08\xec\x0f\x10\x04\x18\x11\x1a\x07\x08\xec\x0f\x10\t\x18\x19\x1a\x07\x08\xed\x0f\x10\t\x18\x19\x1a\x07\x08\xef\x0f\x10\x06\x18\x19\x1a\x07\x08\xf0\x0f\x10\x02\x18\x11\x1a\x07\x08\xf1\x0f\x10\x02\x18\x19\x1a\x07\x08\xf2\x0f\x10\x05\x18\x19\x1a\x07\x08\xfc\x0f\x10\x05\x18\x19\x1a\x07\x08\x80\x10\x10\x07\x18\x17\x1a\x07\x08\x8c\x10\x10\x05\x18\x18\x1a\x07\x08\x95\x10\x10\x06\x18\x18"\x0321D"\x0358D"\x0382D"\x04138D"\x04240D"\x04331D"\x04656D"\x04831D"\x051328D"\x051489D"\x051854D"\x052492D"\x052729D"\x053103D"\x053557D"\x057210D"\x058730D"\x0613053D"\x0616371D*\x9b\x01\n\x98\x01\x00\x00\x00\x00\x00\x00\xf0?c|Hs\n\xe1\xb5\xbfk\xea6\xd2\xa7\xa6\x9b?\xeft\xb0\x1b7\x14\x97?\xbb*\xe2\xed\xde\xe1\x85?K\x00\xeb\x1d\xd3\xe5\x90?\t\xf7\x88W\x19\x89\x8e?e\x10\x15\x8fr\x9d}?\xa4\xbd\xef\xd1p\xb7\x90?x\xf3\x88\xa4+)\x8a?\xc8\x80\xdf\x91\xcf\x0c\x8d?\xf69(\xe3\x8ag\x95?\xa2\x15|w\x0f\xbb\x95??Y/\xccVj\x96?\xef\x127c\x0c-\x96?\t<\xe9\x0c\x99\x00\x98?#d\x06b$\x83\x98?p\xec\x8f\x19=\xdc\x97?\x00\xd1\xae\x16\xd9m\x98?0\x018\x01B\x0cCN_TREAS_MKT\x10\x01\x1a\x03CNY \x01'
       data = [18, -25, 3, 10, -30, 3, 10, 7, 8, -24, 15, 16, 8, 24, 27, 16, 2, 26, 7, 8, -24, 15, 16, 9, 24, 18, 26, 7, 8, -24, 15, 16, 10, 24, 25, 26, 7, 8, -24, 15, 16, 11, 24, 18, 26, 7, 8, -23, 15, 16, 1, 24, 13, 26, 7, 8, -23, 15, 16, 4, 24, 25, 26, 7, 8, -23, 15, 16, 7, 24, 25, 26, 7, 8, -22, 15, 16, 6, 24, 15, 26, 7, 8, -22, 15, 16, 12, 24, 7, 26, 7, 8, -20, 15, 16, 4, 24, 17, 26, 7, 8, -20, 15, 16, 9, 24, 25, 26, 7, 8, -19, 15, 16, 9, 24, 25, 26, 7, 8, -17, 15, 16, 6, 24, 25, 26, 7, 8, -16, 15, 16, 2, 24, 17, 26, 7, 8, -15, 15, 16, 2, 24, 25, 26, 7, 8, -14, 15, 16, 5, 24, 25, 26, 7, 8, -4, 15, 16, 5, 24, 25, 26, 7, 8, -128, 16, 16, 7, 24, 23, 26, 7, 8, -116, 16, 16, 5, 24, 24, 26, 7, 8, -107, 16, 16, 6, 24, 24, 34, 3, 50, 49, 68, 34, 3, 53, 56, 68, 34, 3, 56, 50, 68, 34, 4, 49, 51, 56, 68, 34, 4, 50, 52, 48, 68, 34, 4, 51, 51, 49, 68, 34, 4, 54, 53, 54, 68, 34, 4, 56, 51, 49, 68, 34, 5, 49, 51, 50, 56, 68, 34, 5, 49, 52, 56, 57, 68, 34, 5, 49, 56, 53, 52, 68, 34, 5, 50, 52, 57, 50, 68, 34, 5, 50, 55, 50, 57, 68, 34, 5, 51, 49, 48, 51, 68, 34, 5, 51, 53, 53, 55, 68, 34, 5, 55, 50, 49, 48, 68, 34, 5, 56, 55, 51, 48, 68, 34, 6, 49, 51, 48, 53, 51, 68, 34, 6, 49, 54, 51, 55, 49, 68, 42, -101, 1, 10, -104, 1, 0, 0, 0, 0, 0, 0, -16, 63, 99, 124, 72, 115, 10, -31, -75, -65, 107, -22, 54, -46, -89, -90, -101, 63, -17, 116, -80, 27, 55, 20, -105, 63, -69, 42, -30, -19, -34, -31, -123, 63, 75, 0, -21, 29, -45, -27, -112, 63, 9, -9, -120, 87, 25, -119, -114, 63, 101, 16, 21, -113, 114, -99, 125, 63, -92, -67, -17, -47, 112, -73, -112, 63, 120, -13, -120, -92, 43, 41, -118, 63, -56, -128, -33, -111, -49, 12, -115, 63, -10, 57, 40, -29, -118, 103, -107, 63, -94, 21, 124, 119, 15, -69, -107, 63, 63, 89, 47, -52, 86, 106, -106, 63, -17, 18, 55, 99, 12, 45, -106, 63, 9, 60, -23, 12, -103, 0, -104, 63, 35, 100, 6, 98, 36, -125, -104, 63, 112, -20, -113, 25, 61, -36, -105, 63, 0, -47, -82, 22, -39, 109, -104, 63, 48, 1, 56, 1, 66, 12, 67, 78, 95, 84, 82, 69, 65, 83, 95, 77, 75, 84, 16, 1, 26, 3, 67, 78, 89, 32, 1]
       test = create_ir_yield_curve_from_binary(data)
       #print('test_create_ir_yield_curve', test.SerializeToString())
       self.assertEqual(test.SerializeToString(), expected)     
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnalytics)
    unittest.TextTestRunner(verbosity=2).run(suite)