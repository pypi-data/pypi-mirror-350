# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 23:43:29 2022

@author: dingq
"""

import unittest
from datetime import datetime
import pandas as pd
import base64

from caplib.analytics import *
from caplib.fianalytics import *
from caplib.fimarket import *

class TestFiAnalytics(unittest.TestCase):
    def setUp(self):
        self.cal = 'CAL_CFETS'
        
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        create_calendar(self.cal, holidays, specials)

        self.currency = 'CNY'
        self.as_of_date = datetime(2021, 7, 22)

        self.cny_treas_zero_1m = create_std_zero_cpn_bond_template('cny_treas_zero_1m', create_date(None), ('1m'), self.currency,
                                                                   self.cal, 100.0)
                                                                   
        self.cny_treas_cpn_a_3m = create_std_fixed_cpn_bond_template('cny_treas_cpn_a_3m', create_date(None), ('3m'),
                                                                     self.currency, self.cal, 0.0)
        self.cny_treas_cpn_a_6m = create_std_fixed_cpn_bond_template('cny_treas_cpn_a_6m', create_date(None), ('6m'),
                                                                     self.currency, self.cal, 0.0)
        self.cny_treas_cpn_a_9m = create_std_fixed_cpn_bond_template('cny_treas_cpn_a_9m', create_date(None), ('9m'),
                                                                     self.currency, self.cal, 0.0)
        self.cny_treas_cpn_a_1y = create_std_fixed_cpn_bond_template('cny_treas_cpn_a_1y', create_date(None), ('1y'),
                                                                     self.currency, self.cal, 0.0)
        self.cny_treas_cpn_a_2y = create_std_fixed_cpn_bond_template('cny_treas_cpn_a_2y', create_date(None), ('2Y'),
                                                                     self.currency, self.cal, 0.0)
        self.cny_treas_cpn_a_3y = create_std_fixed_cpn_bond_template('cny_treas_cpn_a_3y', create_date(None), ('3Y'),
                                                                     self.currency, self.cal, 0.0)
        self.cny_treas_cpn_a_5y = create_std_fixed_cpn_bond_template('cny_treas_cpn_a_5y', create_date(None), ('5Y'),
                                                                     self.currency, self.cal, 0.0)
        self.cny_treas_cpn_sa_7y = create_std_fixed_cpn_bond_template('cny_treas_cpn_sa_7y', create_date(None), ('7Y'),
                                                                      self.currency, self.cal, 0.0)
        self.cny_treas_cpn_sa_10y = create_std_fixed_cpn_bond_template('cny_treas_cpn_sa_10y',create_date(None),  ('10Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_treas_cpn_sa_15y = create_std_fixed_cpn_bond_template('cny_treas_cpn_sa_15y', create_date(None), ('15Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_treas_cpn_sa_20y = create_std_fixed_cpn_bond_template('cny_treas_cpn_sa_20y', create_date(None), ('20Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_treas_cpn_sa_30y = create_std_fixed_cpn_bond_template('cny_treas_cpn_sa_30y', create_date(None),  ('30Y'),
                                                                       self.currency, self.cal, 0.0)

        self.cny_mtn_aaa_cpn_a_1m = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_1m', create_date(None), ('1M'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_3m = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_3m', create_date(None), ('3M'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_6m = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_6m',create_date(None),  ('6M'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_9m = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_9m', create_date(None), ('9M'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_1y = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_1y',create_date(None),  ('1Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_2y = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_2y', create_date(None), ('2Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_3y = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_3y', create_date(None), ('3Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_4y = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_4y', create_date(None), ('4Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_5y = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_5y', create_date(None), ('5Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_7y = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_7y', create_date(None), ('7Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_8y = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_8y',create_date(None), ('8Y'),
                                                                       self.currency, self.cal, 0.0)
        self.cny_mtn_aaa_cpn_a_9y = create_std_fixed_cpn_bond_template('cny_mtn_aaa_cpn_a_9y',create_date(None),  ('9Y'),
                                                                       self.currency, self.cal, 0.0)

        self.cny_treas_cpn_bond_200014_template = create_fixed_cpn_bond_template('cny_treas_cpn_bond_200014',
                                                                                 datetime(2020, 10, 9), 1,
                                                                                 datetime(2020, 10, 10),
                                                                                 ('5Y'),
                                                                                 2.15e-2, self.currency, self.cal,
                                                                                 frequency='ANNUAL',
                                                                                 day_count='ACT_365_FIXED',
                                                                                 issue_price=100.0,
                                                                                 interest_day_convention='MODIFIED_FOLLOWING',
                                                                                 stub_policy='INITIAL',
                                                                                 broken_period_type='LONG',
                                                                                 pay_day_offset=0,
                                                                                 pay_day_convention='MODIFIED_FOLLOWING',
                                                                                 ex_cpn_period=('0d'),
                                                                                 ex_cpn_calendar='',
                                                                                 ex_cpn_day_convention='INVALID_BUSINESS_DAY_CONVENTION',
                                                                                 ex_cpn_eom=False)

        self.cny_treas_std_cfets_name = 'cny_treas_std_cfets'
        bond_names = ['CNY_TREAS_ZERO_1M',
                      'CNY_TREAS_CPN_A_3M',
                      'CNY_TREAS_CPN_A_6M',
                      'CNY_TREAS_CPN_A_9M',
                      'CNY_TREAS_CPN_A_1Y',
                      'CNY_TREAS_CPN_A_2Y',
                      'CNY_TREAS_CPN_A_3Y',
                      'CNY_TREAS_CPN_A_5Y',
                      'CNY_TREAS_CPN_SA_7Y',
                      'CNY_TREAS_CPN_SA_10Y',
                      'CNY_TREAS_CPN_SA_15Y',
                      'CNY_TREAS_CPN_SA_20Y',
                      'CNY_TREAS_CPN_SA_30Y']
        bond_quotes = [1.7112E-02,
                       1.8317E-02,
                       1.9413E-02,
                       1.9500E-02,
                       2.1563E-02,
                       2.4985E-02,
                       2.5538E-02,
                       2.7550E-02,
                       2.9175E-02,
                       2.9263E-02,
                       3.2984E-02,
                       3.3462E-02,
                       3.5023E-02]

        self.par_cny_treas_std_cfets = create_bond_par_curve(self.as_of_date, self.currency,
                                                             bond_names, bond_quotes,
                                                             'YIELD_TO_MATURITY', self.cny_treas_std_cfets_name)

        build_settings = create_bond_curve_build_settings(self.cny_treas_std_cfets_name, 'ZERO_RATE', 'LINEAR_INTERP',
                                                          'FLAT_EXTRAP')

        self.cny_treas_std_cfets = build_bond_yield_curve(build_settings, self.cny_treas_std_cfets_name,
                                                          self.as_of_date, self.par_cny_treas_std_cfets,
                                                          day_count='ACT_365_FIXED',
                                                          compounding_type='CONTINUOUS_COMPOUNDING', freq='ANNUAL',
                                                          build_method='BOOTSTRAPPING_METHOD', calc_jacobian=False,
                                                          fwd_curve=None)

        self.cny_mtn_aaa_sprd_std_cfets_name = 'cny_mtn_aaa_sprd_std_cfets'
        bond_names = ['CNY_MTN_AAA_CPN_A_1M',
                      'CNY_MTN_AAA_CPN_A_3M',
                      'CNY_MTN_AAA_CPN_A_6M',
                      'CNY_MTN_AAA_CPN_A_9M',
                      'CNY_MTN_AAA_CPN_A_1Y',
                      'CNY_MTN_AAA_CPN_A_2Y',
                      'CNY_MTN_AAA_CPN_A_3Y',
                      'CNY_MTN_AAA_CPN_A_4Y',
                      'CNY_MTN_AAA_CPN_A_5Y',
                      'CNY_MTN_AAA_CPN_A_7Y',
                      'CNY_MTN_AAA_CPN_A_8Y',
                      'CNY_MTN_AAA_CPN_A_9Y']
        bond_quotes = [0.022916,
                       0.024213,
                       0.025822,
                       0.026675,
                       0.027216,
                       0.028916,
                       0.031112,
                       0.032824,
                       0.033816,
                       0.036816,
                       0.037026,
                       0.037311]
        self.par_cny_mtn_aaa_sprd_std_cfets = create_bond_par_curve(self.as_of_date, self.currency,
                                                                    bond_names, bond_quotes,
                                                                    'YIELD_TO_MATURITY',
                                                                    self.cny_mtn_aaa_sprd_std_cfets_name)
        build_settings = create_bond_curve_build_settings(self.cny_mtn_aaa_sprd_std_cfets_name,
                                                          'ZERO_RATE', 'LINEAR_INTERP', 'FLAT_EXTRAP')
        self.cny_mtn_aaa_sprd_std_cfets = build_bond_sprd_curve(build_settings, self.cny_mtn_aaa_sprd_std_cfets_name,
                                                                self.as_of_date, self.par_cny_mtn_aaa_sprd_std_cfets,
                                                                self.cny_treas_std_cfets,
                                                                build_method='BOOTSTRAPPING_METHOD', calc_jacobian=False,
                                                                fwd_curve=None)

    def test_create_bond_yield_curve_build_settings(self):
        expected = b'\n\tCNY_TREAS\x18\x01 \x01'
        test = create_bond_curve_build_settings('CNY_TREAS', 'ZERO_RATE',
                                                'LINEAR_INTERP', 'FLAT_EXTRAP')
        #print(test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_bond_par_curve(self):
        expected = b'\n\x07\x08\xe5\x0f\x10\x07\x18\x16\x12\x03CNY\x1a\x18\n\rCNYGOVBOND_1Y\x11\x9a\x99\x99\x99\x99\x99\x99?\x1a\x18\n\rCNYGOVBOND_2Y\x11y\xe9&1\x08\xac\x9c?*\tCNY_TREAS'
        test = create_bond_par_curve(self.as_of_date, self.currency,
                                     ['CNYGOVBOND_1Y', 'CNYGOVBOND_2Y'],
                                     [2.5e-2, 2.8e-2],
                                     'YIELD_TO_MATURITY', 'CNY_TREAS')
        # print('test_create_bond_par_curve', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_bond_yield_curve_builder(self):
        expected = b'\x12\xc2\x02\n\xbd\x02\n\x07\x08\xe5\x0f\x10\x07\x18\x16\x10\x02\x1a\x07\x08\xe5\x0f\x10\x08\x18\x17\x1a\x07\x08\xe5\x0f\x10\n\x18\x19\x1a\x07\x08\xe6\x0f\x10\x01\x18\x18\x1a\x07\x08\xe6\x0f\x10\x04\x18\x19\x1a\x07\x08\xe6\x0f\x10\x07\x18\x19\x1a\x07\x08\xe7\x0f\x10\x07\x18\x18\x1a\x07\x08\xe8\x0f\x10\x07\x18\x17\x1a\x07\x08\xea\x0f\x10\x07\x18\x17\x1a\x07\x08\xec\x0f\x10\x07\x18\x18\x1a\x07\x08\xef\x0f\x10\x07\x18\x17\x1a\x07\x08\xf4\x0f\x10\x07\x18\x17\x1a\x07\x08\xf9\x0f\x10\x07\x18\x17\x1a\x07\x08\x83\x10\x10\x07\x18\x18"\x021M"\x023M"\x026M"\x029M"\x021Y"\x022Y"\x023Y"\x025Y"\x027Y"\x0310Y"\x0315Y"\x0320Y"\x0330Y*j\nht\xa2\xc8\x1f\xdc_\x91?\x18[\x84U\xfa\x92\x92?\r)_\xe5\x0c\xad\x93?\xb3o\'\x1cc\xc4\x93?\xd4\x0elHk\xd5\x95?\xf5\'(/lB\x99?\x81\xc7\x9f4\x9b\xd0\x99?7\x1f\xff\x93\xe8\xd2\x9b?\xb0\x16\x7f\xa8fq\x9d?@.\xaa\x9b+\x88\x9d?\x11\xac\x0e\x96#\x9d\xa0?e]%r\xdc\xd9\xa0?\x91,\x83\x87\xc4\x9f\xa1?0\x018\x01B\x13CNY_TREAS_STD_CFETS\x10\x01\x1a\x03CNY \x01'
        curve_name = 'cny_treas_std_cfets'
        currency = 'CNY'
        build_settings = create_bond_curve_build_settings(curve_name, 'ZERO_RATE', 'LINEAR_INTERP', 'FLAT_EXTRAP')
        test = build_bond_yield_curve(build_settings, curve_name, self.as_of_date, self.par_cny_treas_std_cfets,
                                      day_count='ACT_365_FIXED', compounding_type='CONTINUOUS_COMPOUNDING', freq='ANNUAL',
                                      build_method='BOOTSTRAPPING_METHOD', calc_jacobian=False,
                                      fwd_curve=None)
        #print('test_bond_yield_curve_builder', test.SerializeToString())
        #print(curve_name)
        #print(print_term_structure_curve(test.curve.curve))
        self.assertEqual(test.SerializeToString(), expected)

    def test_bond_spread_curve_builder(self):
        expected =  b'\n\xab\x02\n\x07\x08\xe5\x0f\x10\x07\x18\x16\x10\x02\x1a\x07\x08\xe5\x0f\x10\x08\x18\x17\x1a\x07\x08\xe5\x0f\x10\n\x18\x19\x1a\x07\x08\xe6\x0f\x10\x01\x18\x18\x1a\x07\x08\xe6\x0f\x10\x04\x18\x19\x1a\x07\x08\xe6\x0f\x10\x07\x18\x19\x1a\x07\x08\xe7\x0f\x10\x07\x18\x18\x1a\x07\x08\xe8\x0f\x10\x07\x18\x17\x1a\x07\x08\xe9\x0f\x10\x07\x18\x17\x1a\x07\x08\xea\x0f\x10\x07\x18\x17\x1a\x07\x08\xec\x0f\x10\x07\x18\x18\x1a\x07\x08\xed\x0f\x10\x07\x18\x17\x1a\x07\x08\xee\x0f\x10\x07\x18\x17"\x021M"\x023M"\x026M"\x029M"\x021Y"\x022Y"\x023Y"\x024Y"\x025Y"\x027Y"\x028Y"\x029Y*b\n`-\xce-\xaf\xf3\xab??<\xf5\x1c(!\\X?\x83\xd2\xb7\xc2\xbb\x05j?h+B>\xab\xb8u?KPWD1\xbav?k\xd0\x16n\x90f\x7f?\xf8n,\x17\xbb\xaa\x90?)\xceU\xf4`\x00\x99?\x9e\xcd\xd0\x92\xdd$\x9f?\xa2\x06\xa6v\xb7\x8a\xaa?@\xd1\r\x81^\x08\xaf?\x05\x8c\xe9\xef\xb2\x05\xb2?0\x018\x01B\x1aCNY_MTN_AAA_SPRD_STD_CFETS\x12b\n`{\'b8\x15\x94v?f<Dm\xf7ew?\xb4(c\xd4`\x88y?\xb6c<7<\x9f|?U\xb0\xc8\xf3\xc2\x8av?}\x96\xe8\xd3\x99Po?S\xb1\xe9@\x9a.v?U*/\x82\x9f\xf7x?\xa4}\x9cfO\xe3x?\xed\xa1\x97\x96@I~?gx\xb4+7\x00\x7f?s\xf1{\xebR\x01\x80?'
        curve_name = 'cny_mtn_aaa_sprd_std_cfets'
        build_settings = create_bond_curve_build_settings(curve_name, 'ZERO_RATE', 'LINEAR_INTERP', 'FLAT_EXTRAP')
        test = build_bond_sprd_curve(build_settings, curve_name,
                                     self.as_of_date, self.par_cny_mtn_aaa_sprd_std_cfets,
                                     self.cny_treas_std_cfets,
                                     build_method='BOOTSTRAPPING_METHOD', calc_jacobian=False,
                                     fwd_curve=None)
        #print('test_bond_spread_curve_builder', test.SerializeToString())
        #print(curve_name)
        #print(print_term_structure_curve(test.curve))
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_fi_mkt_data_set(self):
        expected = b'\n\x07\x08\xe6\x0f\x10\x03\x18\t\x12X\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03CNY \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01\x1aM\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10\xfc\xa9\xf1\xd2Mb`?{\x14\xaeG\xe1zd?0\x018\x01\x12\x12\n\x10\xfc\xa9\xf1\xd2Mb`?{\x14\xaeG\xe1zd?"\x00*X\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03CNY \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x012X\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03CNY \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01'
        as_of_date = datetime(2022, 3, 9)
        discount_curve = create_ir_yield_curve(as_of_date, 'CNY', [datetime(2022, 3, 10), datetime(2025, 3, 10)],
                                               [0.02, 0.025])
        cs_curve = create_credit_curve(datetime(2022, 3, 9), [datetime(2022, 3, 10), datetime(2025, 3, 10)],
                                       [0.2e-2, 0.25e-2])
        fwd_curve = IrYieldCurve()
        test = create_fi_mkt_data_set(as_of_date, discount_curve, cs_curve, fwd_curve, discount_curve, discount_curve)
        #print('test_create_fi_mkt_data_set', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_fi_risk_settings(self):
        expected = b'\n\x1b!-C\x1c\xeb\xe26\x1a?){\x14\xaeG\xe1zt?A-C\x1c\xeb\xe26\x1a?\x12\x0b\x10\x01\x19\x1ag\x016\x9fqf?\x1a\x12!-C\x1c\xeb\xe26\x1a?A-C\x1c\xeb\xe26\x1a?'
        ir_curve_settings = create_ir_curve_risk_settings()
        cs_curve_settings = create_credit_curve_risk_settings()
        theta_settings = create_theta_risk_settings()
        test = create_fi_risk_settings(ir_curve_settings, cs_curve_settings, theta_settings)
        self.assertEqual(test.SerializeToString(), expected)

    def test_vanilla_bond_pricer(self):
        expected = 972294.9381034705
        bond = build_fixed_cpn_bond(1000000.0, self.cny_treas_cpn_bond_200014_template)
        mkt_data = create_fi_mkt_data_set(self.as_of_date, self.cny_treas_std_cfets, self.cny_mtn_aaa_sprd_std_cfets,
                                          self.cny_treas_std_cfets, self.cny_treas_std_cfets, self.cny_treas_std_cfets)
        ir_curve_settings = create_ir_curve_risk_settings()
        cs_curve_settings = create_credit_curve_risk_settings()
        theta_settings = create_theta_risk_settings()
        risk_settings = create_fi_risk_settings(ir_curve_settings, cs_curve_settings, theta_settings)
        pricing_settings = create_model_free_pricing_settings()
        test = vanilla_bond_pricer(bond, self.as_of_date, mkt_data, pricing_settings, risk_settings)
        self.assertEqual(test.present_value, expected)

    def test_vanilla_bond_greeks(self):
        expected = b'\t\x1c\x19O\xe0\r\xac-A\x1a\xef\x07\n?\n\x0eCURVATURE_DOWN\x12-\n\rINTEREST_RATE\x12\x1c\n\x03CNY\x12\x15\n\n\n\x08\xbb\x85\xddq\xe4E.A\x12\x05TOTAL\x1a\x00\n=\n\x0cCURVATURE_UP\x12-\n\rINTEREST_RATE\x12\x1c\n\x03CNY\x12\x15\n\n\n\x08!\x93\x15\xb5a\x15-A\x12\x05TOTAL\x1a\x00\n\x9d\x03\n\x05DELTA\x12\xc0\x01\n\x06CREDIT\x12\xb5\x01\n\x1aCNY_MTN_AAA_SPRD_STD_CFETS\x12\x96\x01\nb\n`\x00\xc0\xac{\xbe\xf8y\xc0\x00$\xd4\xb3\xc9\xdd\xb0\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xbc\xc8~b\x1b\xd0\xc0\x80\xc6\x08\x02y\xd1\xe3\xc0\x00!\x1e_\xfc\xc0\xec\xc0\xae&\xe9a\x15tE\xc1\x18\tQ%\x89q-\xc1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x021M\x12\x023M\x12\x026M\x12\x029M\x12\x021Y\x12\x022Y\x12\x023Y\x12\x024Y\x12\x025Y\x12\x027Y\x12\x028Y\x12\x029Y\x1a\x00\x12\xd0\x01\n\rINTEREST_RATE\x12\xbe\x01\n\x13CNY_TREAS_STD_CFETS\x12\xa6\x01\nj\nh\x000S\x8aho\x90\xc0\x00H\xf4\xf1\xf6\xc2\xac\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\t\x7f(z\xd3\xc0\x00\xdf#\xffu\xc9\xe3\xc0\xbc\x0c\xe2\x1eTz7\xc1\x02\x84V\x0b\xb4\x7fA\xc1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x021M\x12\x023M\x12\x026M\x12\x029M\x12\x021Y\x12\x022Y\x12\x023Y\x12\x025Y\x12\x027Y\x12\x0310Y\x12\x0315Y\x12\x0320Y\x12\x0330Y\x1a\x00\n\xa6\x03\n\x0eDELTA_EXPOSURE\x12\xc0\x01\n\x06CREDIT\x12\xb5\x01\n\x1aCNY_MTN_AAA_SPRD_STD_CFETS\x12\x96\x01\nb\n`\x00\x00\x80\xb1\xa6F\xa5\xbf\x00\x00\x90\x81C\xa2\xdb\xbf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0\xe9\xc0c\xfa\xbf\x00\x00\xddV0<\x10\xc0\x00\x00b\x9d\x1e\x8e\x17\xc0\x00\x1c\x19e\x1d\x93q\xc0\x000\xed\xcf\xbf\x1eX\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x021M\x12\x023M\x12\x026M\x12\x029M\x12\x021Y\x12\x022Y\x12\x023Y\x12\x024Y\x12\x025Y\x12\x027Y\x12\x028Y\x12\x029Y\x1a\x00\x12\xd0\x01\n\rINTEREST_RATE\x12\xbe\x01\n\x13CNY_TREAS_STD_CFETS\x12\xa6\x01\nj\nh\x00\x00\xc0\xf8j\xed\xba\xbf\x00\x00\x90\x99\xbd\x8f\xd7\xbf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xccRR\xe9\xff\xbf\x00\x00\x9e&\xa05\x10\xc0\x00\xf8|C\xa9;c\xc0\x00\x88\x04\xbf\x8b\xabl\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x021M\x12\x023M\x12\x026M\x12\x029M\x12\x021Y\x12\x022Y\x12\x023Y\x12\x025Y\x12\x027Y\x12\x0310Y\x12\x0315Y\x12\x0320Y\x12\x0330Y\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\x00\xb7\xe6\xec\x06X@\x12\x00\x1a\x00"\xcb\x04\x11\x1c\x19O\xe0\r\xac-A"i\n\x07\x08\xe4\x0f\x10\n\x18\x0c\x12\x07\x08\xe5\x0f\x10\n\x18\x0b\x1a\x07\x08\xe4\x0f\x10\n\x18\x0c"\n\n\x08\x99\xfe\xc9`\x8e\xe9\xef?)j\xbct\x93\x18\x04\x96?14\xbe\xda\xb6A\xd5\xef?9\xc4\x88\x11#F\xf0\xd4@A\xaa\x90\x86DN\xd4\xd4@J\x07\x08\xe5\x0f\x10\n\x18\x0bR\n\n\x08\x00\x00\x00\x00\x00\x00\x00\x00Y\x00\x00\x00\x00\x80\x84.A"i\n\x07\x08\xe5\x0f\x10\n\x18\x0b\x12\x07\x08\xe6\x0f\x10\n\x18\n\x1a\x07\x08\xe5\x0f\x10\n\x18\x0b"\n\n\x08\x99\xfe\xc9`\x8e\xe9\xef?)j\xbct\x93\x18\x04\x96?1\xde\xe5\xc0\\:\xf7\xee?9\xc4\x88\x11#F\xf0\xd4@A\xd2@o\x8e\x06C\xd4@J\x07\x08\xe6\x0f\x10\n\x18\nR\n\n\x08\x00\x00\x00\x00\x00\x00\x00\x00Y\x00\x00\x00\x00\x80\x84.A"i\n\x07\x08\xe6\x0f\x10\n\x18\n\x12\x07\x08\xe7\x0f\x10\n\x18\n\x1a\x07\x08\xe6\x0f\x10\n\x18\n"\n\n\x08\x00\x00\x00\x00\x00\x00\xf0?)j\xbct\x93\x18\x04\x96?1E\xad\xdaEB\x00\xee?9\x00\x00\x00\x00\x00\xff\xd4@A\xe0R\xc5{;\xaf\xd3@J\x07\x08\xe7\x0f\x10\n\x18\nR\n\n\x08\x00\x00\x00\x00\x00\x00\x00\x00Y\x00\x00\x00\x00\x80\x84.A"i\n\x07\x08\xe7\x0f\x10\n\x18\n\x12\x07\x08\xe8\x0f\x10\n\x18\n\x1a\x07\x08\xe7\x0f\x10\n\x18\n"\n\n\x08\xb4\x00\x9b\xcf8\x0b\xf0?)j\xbct\x93\x18\x04\x96?1\x16K\x92\x13\xd4\xf4\xec?9<w\xee\xdc\xb9\r\xd5@A\xaf\x00U\xd2\x16\r\xd3@J\x07\x08\xe8\x0f\x10\n\x18\nR\n\n\x08\x00\x00\x00\x00\x00\x00\x00\x00Y\x00\x00\x00\x00\x80\x84.A"i\n\x07\x08\xe8\x0f\x10\n\x18\n\x12\x07\x08\xe9\x0f\x10\n\x18\n\x1a\x07\x08\xe8\x0f\x10\n\x18\n"\n\n\x08\x00\x00\x00\x00\x00\x00\xf0?)j\xbct\x93\x18\x04\x96?1(\x16\x08\xd3\xda\xe5\xeb?9\x00\x00\x00\x00\x00\xff\xd4@AJ\xb6\xa6k\xf8M\xd2@J\x07\x08\xe9\x0f\x10\n\x18\nR\n\n\x08\x00\x00\x00\x00\x00\x00\x00\x00Y\x00\x00\x00\x00\x80\x84.A2$\t(\x16\x08\xd3\xda\xe5\xeb?\x11\x00\x00\x00\x00\x80\x84.A\x19Ab\xe9\xe3\x00\x9b*A"\x07\x08\xe9\x0f\x10\n\x18\nB\x03CNY*\x03CNY2\x00'
        bond = build_fixed_cpn_bond(1000000.0, self.cny_treas_cpn_bond_200014_template)
        mkt_data = create_fi_mkt_data_set(self.as_of_date, self.cny_treas_std_cfets, self.cny_mtn_aaa_sprd_std_cfets,
                                          self.cny_treas_std_cfets, self.cny_treas_std_cfets, self.cny_treas_std_cfets)
        ir_curve_settings = create_ir_curve_risk_settings(True, False, True, granularity='TERM_BUCKET_RISK')
        cs_curve_settings = create_credit_curve_risk_settings(True, granularity='TERM_BUCKET_RISK')
        theta_settings = create_theta_risk_settings(True)
        risk_settings = create_fi_risk_settings(ir_curve_settings, cs_curve_settings, theta_settings)
        pricing_settings = create_model_free_pricing_settings('CNY', True, cash_flows=True)
        test = vanilla_bond_pricer(bond, self.as_of_date, mkt_data, pricing_settings, risk_settings)
        #print('test_vanilla_bond_greeks', test)
        #print('test_vanilla_bond_greeks', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_yield_to_maturity_calculator(self):
        expected = 0.03293703213453388
        price = 972294.9381034705
        bond = build_fixed_cpn_bond(1000000.0, self.cny_treas_cpn_bond_200014_template)
        forward_curve = None
        test = yield_to_maturity_calculator(self.as_of_date, 
                                     ('DISCRETE_COMPOUNDING'), 
                                     bond, 
                                     forward_curve, 
                                     price, 
                                     ('DIRTY_PRICE'), 
                                     ('ANNUAL'))
        self.assertEqual(test, expected)
        
    def test_fixed_cpn_bond_par_rate_calculator(self):
        expected = 0.022305497802670465
        bond = build_fixed_cpn_bond(1000000.0, self.cny_treas_cpn_bond_200014_template)
        test = fixed_cpn_bond_par_rate_calculator(self.as_of_date, 
                                                  bond, 
                                                  self.cny_treas_std_cfets,
                                                  None)
        self.assertEqual(test, expected)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFiAnalytics)
    unittest.TextTestRunner(verbosity=2).run(suite)
