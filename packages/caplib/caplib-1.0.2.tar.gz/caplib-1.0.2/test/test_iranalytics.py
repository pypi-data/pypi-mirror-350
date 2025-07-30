# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

from caplib.analytics import *
from caplib.fxmarket import create_fx_swap_template
from caplib.iranalytics import *
from caplib.irmarket import *


class TestIrAnalytics(unittest.TestCase):
    def setUp(self):
        cal_cfets = 'CAL_CFETS'
        
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        create_calendar(cal_cfets, holidays, specials)
        
        create_ibor_index('shibor_3m', '3m', 'CNY', ['CAL_CFETS'], 1,
                          'ACT_360', 'MODIFIED_FOLLOWING', 'INVALID_DATE_ROLL_CONVENTION', 'STANDARD_IBOR_INDEX')

        fixed_leg = create_fixed_leg_definition('cny', 'cal_cfets', 'QUARTERLY')
        floating_leg = create_floating_leg_definition('cny', 'shibor_3m', 'cal_cfets', ['cal_cfets'], 'QUARTERLY',
                                                      'QUARTERLY', day_count='ACT_360',
                                                      payment_discount_method='NO_DISCOUNT', rate_calc_method='STANDARD',
                                                      spread=False,
                                                      interest_day_convention='MODIFIED_FOLLOWING', stub_policy='INITIAL',
                                                      broken_period_type='LONG',
                                                      pay_day_offset=0, pay_day_convention='MODIFIED_FOLLOWING',
                                                      fixing_day_convention='MODIFIED_PRECEDING', fixing_mode='IN_ADVANCE',
                                                      fixing_day_offset=-1,
                                                      notional_exchange='INVALID_NOTIONAL_EXCHANGE')
        create_fx_swap_template(inst_name="TestFxSwap",
                                start_convention="INVALID_INSTRUMENT_START_CONVENTION",
                                currency_pair="USDCNY",
                                calendars=["CAL_CFETS"],
                                start_day_convention="MODIFIED_PRECEDING",
                                end_day_convention="MODIFIED_PRECEDING",
                                fixing_offset="180d",
                                fixing_day_convention="MODIFIED_PRECEDING")

        create_fx_spot_template(inst_name="TestFxSpot",
                                currency_pair="USDCNY",
                                spot_day_convention="FOLLOWING",
                                calendars=["CAL_CFETS"],
                                spot_delay="1d")

        self.cny_shibor_3m_swap_template = create_ir_vanilla_swap_template('cny_shibor_3m', 1, fixed_leg, floating_leg,
                                                                           'SPOTSTART')

        self.as_of_date = datetime(2022, 3, 9)
        self.cny_shibor_3m_curve = create_ir_yield_curve(self.as_of_date, 'CNY',
                                                         [datetime(2022, 3, 10), datetime(2025, 3, 10)],
                                                         [0.02, 0.025],
                                                         day_count='ACT_365_FIXED',
                                                         interp_method='LINEAR_INTERP',
                                                         extrap_method='FLAT_EXTRAP',
                                                         compounding_type='CONTINUOUS_COMPOUNDING',
                                                         frequency='ANNUAL',
                                                         jacobian=[0.0],
                                                         curve_name='CNY_SHIBOR_3M',
                                                         pillar_names=['1D', '3Y'])

    def test_create_ir_curve_build_settings(self):
        expected = b'\n\rCNY_SHIBOR_3M\x1a\x16\n\x14\n\x03CNY\x12\rCNY_SHIBOR_3M"\x1c\n\x1a\n\tSHIBOR_3M\x12\rCNY_SHIBOR_3M'
        discount_curves = {'CNY': 'CNY_SHIBOR_3M'}
        forward_curves = {'SHIBOR_3M': 'CNY_SHIBOR_3M'}
        test = create_ir_curve_build_settings('CNY_SHIBOR_3M', discount_curves, forward_curves, False)
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_ir_par_rate_curve(self):
        expected = b'\n\x07\x08\xe6\x0f\x10\x03\x18\t\x12\x03CNY\x1a\rCNY_SHIBOR_3M"\x1f\n\tSHIBOR_3M\x10\xe9\x07\x1a\x04\x08\x03\x10\x1e!\xda\xe6\xc6\xf4\x84%.?(\x01"#\n\rCNY_SHIBOR_3M\x10\xd2\x0f\x1a\x04\x08\x06\x10\x1e!i\x1dUM\x10u/?(\x01"$\n\rCNY_SHIBOR_3M\x10\xd2\x0f\x1a\x05\x08\x01\x10\xed\x02!C\xc58\x7f\x13\n1?(\x01'

        currency = 'CNY'
        curve_name = 'CNY_SHIBOR_3M'
        inst_names = ['SHIBOR_3M', 'CNY_SHIBOR_3M', 'CNY_SHIBOR_3M']
        inst_types = ['DEPOSIT', 'IR_VANILLA_SWAP', 'IR_VANILLA_SWAP']
        inst_terms = ['3M', '6M', '1Y']
        factors = [100, 100, 100]
        quotes = [2.3e-2, 2.4e-2, 2.6e-2]
        test = create_ir_par_rate_curve(self.as_of_date,
                                        currency,
                                        curve_name,
                                        inst_names,
                                        inst_types,
                                        inst_terms,
                                        factors,
                                        quotes)
        self.assertEqual(test.SerializeToString(), expected)

    def test_ir_single_ccy_curve_builder(self):
        expected = b'\x12e\na\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\t\x18\x0c\x1a\x07\x08\xe7\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x026M"\x021Y"\x023Y*\x1a\n\x18\xb7A\xd5g\xb6{\x97?\xa4xW\xd9\xbb\x81\x98?\xbf\xc4$\xa5{\x93\x9a?0\x018\x01B\rCNY_SHIBOR_3M\x10\x01\x1a\x03CNY \x01'
        
        currency = 'CNY'
        curve_name = 'CNY_SHIBOR_3M'

        discount_curves = {'CNY': 'CNY_SHIBOR_3M'}
        forward_curves = {'SHIBOR_3M': 'CNY_SHIBOR_3M'}
        cny_shibor_3m_settings = create_ir_curve_build_settings('CNY_SHIBOR_3M', discount_curves, forward_curves, False)
        build_settings = [cny_shibor_3m_settings]

        inst_names = ['CNY_SHIBOR_3M', 'CNY_SHIBOR_3M', 'CNY_SHIBOR_3M']
        inst_types = ['IR_VANILLA_SWAP', 'IR_VANILLA_SWAP', 'IR_VANILLA_SWAP']
        inst_terms = ['6M', '1Y', '3Y']
        factors = [100, 100, 100]
        quotes = [2.3, 2.4, 2.6]
        cny_shibor_3m_par_curve = create_ir_par_rate_curve(self.as_of_date, currency, curve_name,
                                                           inst_names, inst_types, inst_terms, factors, quotes)
        par_curves = [cny_shibor_3m_par_curve]

        target_curve_names = [curve_name]
        day_count = 'ACT_365_FIXED'
        compounding_type = 'CONTINUOUS_COMPOUNDING'
        frequency = 'ANNUAL'
        other_curves = []
        building_method = 'BOOTSTRAPPING_METHOD'
        test = ir_single_ccy_curve_builder(self.as_of_date, target_curve_names, build_settings, par_curves,
                                           day_count, compounding_type, frequency, other_curves, building_method)
        #print('test_ir_single_ccy_curve_builder', test[0].SerializeToString())
        self.assertEqual(test[0].SerializeToString(), expected)

    def test_create_ir_mkt_data_set(self):
        expected = b'\n\x07\x08\xe6\x0f\x10\x03\x18\t\x12X\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03CNY \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01\x1a\tshibor_3m"X\x12;\n7\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x00*\x12\n\x10{\x14\xaeG\xe1z\x94?\x9a\x99\x99\x99\x99\x99\x99?0\x018\x01\x10\x01\x1a\x03CNY \x01:\x12\x12\x10\x08\x01\x10\x01\x1a\x08\x00\x00\x00\x00\x00\x00\x00\x00 \x01'
        
        cny_shibor_3m = create_ir_yield_curve(self.as_of_date, 'CNY',
                                              [datetime(2022, 3, 10), datetime(2025, 3, 10)], [0.02, 0.025])
        test = create_ir_mkt_data_set(self.as_of_date, cny_shibor_3m, ['shibor_3m'], [cny_shibor_3m])
        #print('test_create_ir_mkt_data_set', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_create_ir_risk_settings(self):
        expected = b'\n\x1b!-C\x1c\xeb\xe26\x1a?){\x14\xaeG\xe1zt?A-C\x1c\xeb\xe26\x1a?\x12\x0b\x10\x01\x19\x1ag\x016\x9fqf?'
        ir_curve_settings = create_ir_curve_risk_settings()
        theta_settings = create_theta_risk_settings()
        test = create_ir_risk_settings(ir_curve_settings, theta_settings)
        self.assertEqual(test.SerializeToString(), expected)

    def test_ir_vanilla_instrument_pricer(self):
        expected = b'\t\x90T\xdf2C\x1a\xe5@\x1a\xe4\x03\n?\n\x0eCURVATURE_DOWN\x12-\n\rINTEREST_RATE\x12\x1c\n\x03CNY\x12\x15\n\n\n\x08\x9b\x07wC\x84J\xe3@\x12\x05TOTAL\x1a\x00\n=\n\x0cCURVATURE_UP\x12-\n\rINTEREST_RATE\x12\x1c\n\x03CNY\x12\x15\n\n\n\x08\x11\xfc3\xb5\x1d\xe7\xe6@\x12\x05TOTAL\x1a\x00\nI\n\x05DELTA\x12@\n\rINTEREST_RATE\x12/\n\rCNY_SHIBOR_3M\x12\x1e\n\x12\n\x10Y\x11\xdf\xaf\xe6_\x1aA\xe9\x16wG\x87\xc5\x12A\x12\x021D\x12\x023Y\x1a\x00\nR\n\x0eDELTA_EXPOSURE\x12@\n\rINTEREST_RATE\x12/\n\rCNY_SHIBOR_3M\x12\x1e\n\x12\n\x10\x00\xd2BK(\x9bE@\x00\xe4\x9f\xb6`\xc1>@\x12\x021D\x12\x023Y\x1a\x00\nI\n\x05GAMMA\x12@\n\rINTEREST_RATE\x12/\n\rCNY_SHIBOR_3M\x12\x1e\n\x12\n\x10\x00\xe2\x10A\xab\xe0\x17\xc1\x00p\xa8f\xac\x1e\xfa\xc0\x12\x021D\x12\x023Y\x1a\x00\nR\n\x0eGAMMA_EXPOSURE\x12@\n\rINTEREST_RATE\x12/\n\rCNY_SHIBOR_3M\x12\x1e\n\x12\n\x10\x00\x00\x00\x88$\x06p\xbf\x00\x00\x00\xc0Y\x87Q\xbf\x12\x021D\x12\x023Y\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\x00\xaf@X\x87\x11\xc0\x12\x00\x1a\x00"\xf4\x06\tf\xd5\xb9\x0cn\x18\xe8\xc0\x11\xfb\x94\xcc\x9fX\x99\xf6@\x1ai\n\x07\x08\xe6\x0f\x10\x03\x18\x07\x12\x07\x08\xe6\x0f\x10\x06\x18\x07\x1a\x07\x08\xe6\x0f\x10\x03\x18\x07"\n\n\x08\x1b\x02\xd1n\xaa!\xd0?)\x9a\x99\x99\x99\x99\x99\xa9?1*\x06@m\xe2\xd6\xef?9\xd7\xabW\xaf^\x9d\xc8\xc0A!\x89\x87N\xbe}\xc8\xc0J\x07\x08\xe6\x0f\x10\x06\x18\x07R\n\n\x08\x9a\x99\x99\x99\x99\x99\xa9?Y\x00\x00\x00\x00\x80\x84.\xc1\x1ai\n\x07\x08\xe6\x0f\x10\x06\x18\x07\x12\x07\x08\xe6\x0f\x10\t\x18\x07\x1a\x07\x08\xe6\x0f\x10\x06\x18\x07"\n\n\x08\x1b\x02\xd1n\xaa!\xd0?)\x9a\x99\x99\x99\x99\x99\xa9?1x\x87h&_\xab\xef?9\xd7\xabW\xaf^\x9d\xc8\xc0A\x9bK\x92\xdcE\\\xc8\xc0J\x07\x08\xe6\x0f\x10\t\x18\x07R\n\n\x08\x9a\x99\x99\x99\x99\x99\xa9?Y\x00\x00\x00\x00\x80\x84.\xc1\x1ai\n\x07\x08\xe6\x0f\x10\t\x18\x07\x12\x07\x08\xe6\x0f\x10\x0c\x18\x07\x1a\x07\x08\xe6\x0f\x10\t\x18\x07"\n\n\x08\x99\xfe\xc9`\x8e\xe9\xcf?)\x9a\x99\x99\x99\x99\x99\xa9?1\x8b:\xb8\xc8\xe1~\xef?9\x0e\x1c8p\xe0X\xc8\xc0Ay\xf3\x11*\xa3\xf6\xc7\xc0J\x07\x08\xe6\x0f\x10\x0c\x18\x07R\n\n\x08\x9a\x99\x99\x99\x99\x99\xa9?Y\x00\x00\x00\x00\x80\x84.\xc1\x1ai\n\x07\x08\xe6\x0f\x10\x0c\x18\x07\x12\x07\x08\xe7\x0f\x10\x03\x18\x07\x1a\x07\x08\xe6\x0f\x10\x0c\x18\x07"\n\n\x08\xfc\xf8\xf1\xe3\xc7\x8f\xcf?)\x9a\x99\x99\x99\x99\x99\xa9?1\xcej<\x1d}Q\xef?9F\x8c\x181b\x14\xc8\xc0Ab\x8d\xbb\xdd\x10\x91\xc7\xc0J\x07\x08\xe7\x0f\x10\x03\x18\x07R\n\n\x08\x9a\x99\x99\x99\x99\x99\xa9?Y\x00\x00\x00\x00\x80\x84.\xc1"i\n\x07\x08\xe6\x0f\x10\x03\x18\x07\x12\x07\x08\xe6\x0f\x10\x06\x18\x07\x1a\x07\x08\xe6\x0f\x10\x03\x18\x04"\n\n\x08\xb0\x05[\xb0\x05[\xd0?)333333\xd3?1*\x06@m\xe2\xd6\xef?9\xaa\xaa\xaa\xaa\xaa\xb7\xf2@AE\x10\xb7\x0b\x9e\x9f\xf2@J\x07\x08\xe6\x0f\x10\x06\x18\x07R\n\n\x08333333\xd3?Y\x00\x00\x00\x00\x80\x84.A"i\n\x07\x08\xe6\x0f\x10\x06\x18\x07\x12\x07\x08\xe6\x0f\x10\t\x18\x07\x1a\x07\x08\xe6\x0f\x10\x06\x18\x06"\n\n\x08\xb0\x05[\xb0\x05[\xd0?)Z\x87\x0e\to\x81\x95?1x\x87h&_\xab\xef?9\xdfA\xfc\xeb\x10\xf7\xb4@A5\x88\xad\xfd\x9e\xbf\xb4@J\x07\x08\xe6\x0f\x10\t\x18\x07R\n\n\x08Z\x87\x0e\to\x81\x95?Y\x00\x00\x00\x00\x80\x84.A"i\n\x07\x08\xe6\x0f\x10\t\x18\x07\x12\x07\x08\xe6\x0f\x10\x0c\x18\x07\x1a\x07\x08\xe6\x0f\x10\t\x18\x06"\n\n\x08\xd8\x82-\xd8\x82-\xd0?)y\xa3\xc4\xbfKZ\x96?1\x8b:\xb8\xc8\xe1~\xef?9\xe1^\x06\x9e\xd7\x8d\xb5@A\xbf\x0e\x9bv\xdf6\xb5@J\x07\x08\xe6\x0f\x10\x0c\x18\x07R\n\n\x08y\xa3\xc4\xbfKZ\x96?Y\x00\x00\x00\x00\x80\x84.A"i\n\x07\x08\xe6\x0f\x10\x0c\x18\x07\x12\x07\x08\xe7\x0f\x10\x03\x18\x07\x1a\x07\x08\xe6\x0f\x10\x0c\x18\x06"\n\n\x08\x00\x00\x00\x00\x00\x00\xd0?)\x00$z\xf8\xcd0\x97?1\xcej<\x1d}Q\xef?9}[\xcb-\xc7\x1d\xb6@Ak\xb4\x0f\xcd*\xa5\xb5@J\x07\x08\xe7\x0f\x10\x03\x18\x07R\n\n\x08\x00$z\xf8\xcd0\x97?Y\x00\x00\x00\x00\x80\x84.A:\x03CNYB\x03CNY*\x03CNY2\x00'
        
        shibor_3m_fixings = create_time_series([datetime(2022, 3, 3), datetime(2022, 3, 4)],
                                               [0.1, 0.3],
                                              'TS_FORWARD_MODE', 'shibor_3m')
        leg_fixings = create_leg_fixings([['shibor_3m', shibor_3m_fixings]])
        swap = build_ir_vanilla_instrument('PAY', 0.05, 0.0,
                                           datetime(2022, 3, 7), datetime(2023, 3, 7),
                                           self.cny_shibor_3m_swap_template, 1000000, leg_fixings)

        mkt_data = create_ir_mkt_data_set(self.as_of_date, self.cny_shibor_3m_curve, ['shibor_3m'],
                                          [self.cny_shibor_3m_curve])

        pricing_settings = create_model_free_pricing_settings('CNY', True, cash_flows=True)

        ir_curve_settings = create_ir_curve_risk_settings(True, True, True, 1e-4, 50e-4, 'CENTRAL_DIFFERENCE_METHOD',
                                                          'TERM_BUCKET_RISK')
        theta_settings = create_theta_risk_settings(True)
        risk_settings = create_ir_risk_settings(ir_curve_settings, theta_settings)

        test = ir_vanilla_instrument_pricer(swap, self.as_of_date, mkt_data, pricing_settings, risk_settings)
        #print(test)
        #print('test_ir_vanilla_instrument_pricer', test.SerializeToString())
        self.assertEqual(test.SerializeToString(), expected)

    def test_ir_cross_ccy_curve_builder(self):
        expected = b'\x12\x8f\x02\n\x8a\x02\n\x07\x08\xe6\x0f\x10\x03\x18\t\x10\x02\x1a\x07\x08\xe6\x0f\x10\x03\x18\n\x1a\x07\x08\xe6\x0f\x10\x03\x18\x0b\x1a\x07\x08\xe6\x0f\x10\x03\x18\x11\x1a\x07\x08\xe6\x0f\x10\x04\x18\x08\x1a\x07\x08\xe6\x0f\x10\x05\x18\n\x1a\x07\x08\xe6\x0f\x10\x06\x18\n\x1a\x07\x08\xe6\x0f\x10\t\x18\t\x1a\x07\x08\xe6\x0f\x10\x0c\x18\t\x1a\x07\x08\xe7\x0f\x10\x03\x18\n\x1a\x07\x08\xe8\x0f\x10\x03\x18\x08\x1a\x07\x08\xe9\x0f\x10\x03\x18\n"\x02ON"\x02TN"\x021W"\x021M"\x022M"\x023M"\x026M"\x029M"\x0312M"\x022Y"\x023Y*Z\nX\x1e\x87\x88H\xe1z\x94?\n\xa9\xcfo\x13|\x94?\xba~\xc5Ud_\x90?v\x8d\x00\xe1Rm\x90?\xee\xa6\xd5"\xa4\xc7\x90?68HF\xe2\x1c\x91?\x07\xcctl\xa5^\x91?\xb3\xfc\xbd|h\xcf\x91?L\xdc\x8c\x8a{\x19\x92?\xce\xd4W\x18\xa2)\x90?\x86C\xed\xe2\x08d\x8e?0\x018\x01B\rUSD_USDCNY_FX\x10\x01\x1a\x03USD \x01'
        currency = 'USD'
        curve_name = 'USD_USDCNY_FX'
        discount_curves = {"USD": "USD_USDCNY_FX", "CNY": "CNY_SHIBOR_3M"}
        forward_curves = {}
        usdcny_fx_swap_settings = create_ir_curve_build_settings(curve_name=curve_name,
                                                                 discount_curves=discount_curves,
                                                                 forward_curves=forward_curves,
                                                                 use_on_tn_fx_swap=True)
        build_settings = [usdcny_fx_swap_settings]

        inst_names = ['USDCNY', 'USDCNY', 'USDCNY', 'USDCNY', 'USDCNY', 'USDCNY',
                      'USDCNY', 'USDCNY', 'USDCNY', 'USDCNY', 'USDCNY']
        inst_types = ['FX_SWAP', 'FX_SWAP', 'FX_SWAP', 'FX_SWAP', 'FX_SWAP',
                      'FX_SWAP', 'FX_SWAP', 'FX_SWAP', 'FX_SWAP', 'FX_SWAP', 'FX_SWAP']
        inst_terms = ['ON', 'TN', '1W', '1M', '2M', '3M', '6M', '9M', '12M', '2Y', '3Y']
        factors = [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
        quotes = [2.01000, 3.91000, 5.93000, 22.50000, 44.25000, 63.25000, 130.75000, 194.75000, 268.25000, 1017.00000,
                  2075.00000]

        usd_usdcny_fx_par_curve = create_ir_par_rate_curve(self.as_of_date,
                                                           currency,
                                                           curve_name,
                                                           inst_names,
                                                           inst_types,
                                                           inst_terms,
                                                           factors,
                                                           quotes)
        par_curves = [usd_usdcny_fx_par_curve]
        target_curve_names = [curve_name]
        day_count = 'ACT_365_FIXED'
        compounding_type = 'CONTINUOUS_COMPOUNDING'
        frequency = 'ANNUAL'
        other_curves = [self.cny_shibor_3m_curve]

        foreign_exchange_rate = create_foreign_exchange_rate(6.6916, "USD", "CNY")
        fx_spot = create_fx_spot_rate(foreign_exchange_rate, datetime(2022, 3, 9), datetime(2022, 3, 9))
        test = ir_cross_ccy_curve_builder(self.as_of_date,
                                          target_curve_names,
                                          build_settings,
                                          par_curves,
                                          day_count,
                                          compounding_type,
                                          frequency,
                                          other_curves,
                                          fx_spot)
        #print('test_ir_cross_ccy_curve_builder', test[0])
        #print('test_ir_cross_ccy_curve_builder', test[0].SerializeToString())
        self.assertEqual(test[0].SerializeToString(), expected)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIrAnalytics)
    unittest.TextTestRunner(verbosity=2).run(suite)
