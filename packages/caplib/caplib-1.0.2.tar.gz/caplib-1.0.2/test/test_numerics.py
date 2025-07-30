# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:01:40 2022

@author: dingq
"""
# -*- coding: utf-8 -*-

import unittest
from caplib.numerics import *

class TestNumerics(unittest.TestCase):
    
    def test_to_interp_method(self):
        expected=LINEAR_INTERP
        test = to_interp_method('LINEAR_INTERP')
        self.assertEqual(test, expected)
        
    def test_to_extrap_method(self):
        expected=FLAT_EXTRAP
        test = to_extrap_method('FLAT_EXTRAP')
        self.assertEqual(test, expected)
        
    def test_to_uniform_random_number_type(self):
        expected=SOBOL_NUMBER
        test = to_uniform_random_number_type('SOBOL_NUMBER')
        self.assertEqual(test, expected)
    
    def test_to_wiener_process_build_method(self):
        expected=BROWNIAN_BRIDGE_METHOD
        test = to_wiener_process_build_method('BROWNIAN_BRIDGE_METHOD')
        self.assertEqual(test, expected)
    
    def test_to_grid_type(self):
        expected=UNIFORM_GRID
        test = to_grid_type('UNIFORM_GRID')
        self.assertEqual(test, expected)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNumerics)
    unittest.TextTestRunner(verbosity=2).run(suite)