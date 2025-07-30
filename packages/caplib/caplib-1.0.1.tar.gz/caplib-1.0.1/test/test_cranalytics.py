import unittest
from datetime import datetime

from caplib.market import *
from caplib.analytics import *
from caplib.crmarket import *
from caplib.cranalytics import *

class TestCrAnalytics(unittest.TestCase):

    def setUp(self):

        '''Static Data'''
        # Calendars
        cal_cfets = 'CAL_CFETS'      
        
        create_calendar(cal_cfets, [], [])
        
        # Instruments
        cds_template = create_cds_template(inst_name='CFETS-SHCH-GTJA',
                                        start_delay='1d',
                                        settlement_type='CASH_SETTLEMENT',
                                        reference_price=0,
                                        leverage=1,
                                        credit_protection_type='PAY_PROTECTION_AT_MATURITY',
                                        recovery_rate=0.4,
                                        credit_premium_type='PAY_PREMIUM_UPTO_CURRENT_PERIOD',
                                        day_count='ACTUAL_360',
                                        frequency='QUARTERLY',
                                        business_day_convention='MODIFIED_FOLLOWING',
                                        calendars=[cal_cfets],
                                        rebate_accrual=False
        )
        
        ''' Mkt Data'''        
        self.as_of_date = datetime(2020, 2, 21)

        # CGB yield curve
        cn_treas_curve = create_ir_yield_curve(
            as_of_date = self.as_of_date,
            currency='CNY',
            term_dates = [
                datetime(2020, 3, 24),
                datetime(2020, 4, 24),
                datetime(2020, 5, 22),
                datetime(2020, 8, 22),
                datetime(2020, 11, 22),
                datetime(2021, 2, 21),
                datetime(2022, 2, 22),
                datetime(2023, 2, 24),
                datetime(2025, 2, 21),
                datetime(2027, 2, 22),
                datetime(2030, 2, 22),
                datetime(2035, 2, 23),
                datetime(2040, 2, 24),
                datetime(2050, 2, 22),
                datetime(2060, 2, 22),
                datetime(2070, 2, 22)
            ],
            zero_rates = [
                0.016587,  # 1.6587%
                0.019987,  # 1.9987%
                0.020290,  # 2.0290%
                0.021068,  # 2.1068%
                0.021139,  # 2.1139%
                0.021222,  # 2.1222%
                0.023163,  # 2.3163%
                0.024260,  # 2.4260%
                0.026628,  # 2.6628%
                0.028458,  # 2.8458%
                0.028658,  # 2.8658%
                0.030162,  # 3.0162%
                0.031016,  # 3.1016%
                0.033171,  # 3.3171%
                0.033777,  # 3.3777%
                0.034289   # 3.4289%
            ],
            curve_name='CN_TREAS'
        )

        bond_credit_curve = create_credit_curve(
            as_of_date=datetime(2020, 2, 21),
            term_dates=[
                datetime(2020, 2, 29),
                datetime(2020, 3, 7),
                datetime(2020, 3, 24),
                datetime(2020, 4, 24),
                datetime(2020, 5, 22),
                datetime(2020, 8, 22),
                datetime(2020, 11, 22),
                datetime(2021, 2, 21),
                datetime(2022, 2, 22),
                datetime(2023, 2, 24),
                datetime(2024, 2, 23),
                datetime(2025, 2, 21),
                datetime(2026, 2, 22),
                datetime(2027, 2, 22),
                datetime(2028, 2, 22),
                datetime(2029, 2, 23),
                datetime(2030, 2, 22),
                datetime(2035, 2, 23)
            ],
            hazard_rates = [
                0.001249,
                0.002330,
                0.005956,
                0.005516,
                0.005307,
                0.006861,
                0.008471,
                0.008545,
                0.010818,
                0.011579,
                0.011327,
                0.010564,
                0.008867,
                0.008566,
                0.008979,
                0.008981,
                0.011045,
                0.013547
            ]
        )
        #print(cn_treas_curve)
        credit_par_curve = create_credit_par_curve(
            as_of_date = self.as_of_date,
            currency = 'CNY',
            name = 'CFETS-SHCH-GTJA',
            pillars = [
                ('CFETS-SHCH-GTJA', 'CREDIT_DEFAULT_SWAP', '3M', 0.002694),  # 0.2694%
                ('CFETS-SHCH-GTJA', 'CREDIT_DEFAULT_SWAP', '6M', 0.002960),  # 0.2960%
                ('CFETS-SHCH-GTJA', 'CREDIT_DEFAULT_SWAP', '1Y', 0.003184),  # 0.3184%
                ('CFETS-SHCH-GTJA', 'CREDIT_DEFAULT_SWAP', '2Y', 0.003422),  # 0.3422%
                ('CFETS-SHCH-GTJA', 'CREDIT_DEFAULT_SWAP', '3Y', 0.003673),  # 0.3673%
                ('CFETS-SHCH-GTJA', 'CREDIT_DEFAULT_SWAP', '4Y', 0.004223),  # 0.4223%
                ('CFETS-SHCH-GTJA', 'CREDIT_DEFAULT_SWAP', '5Y', 0.004868)   # 0.4868%
            ]
        )
        
        #print(credit_par_curve)

        # credit curve
        self.credit_curve = credit_curve_builder(
            as_of_date = self.as_of_date,
            curve_name = 'CFETS-SHCH-GTJA',
            par_curve = credit_par_curve,
            discount_curve = cn_treas_curve,
            building_method = 'BOOTSTRAPPING_METHOD',
            calc_jacobian = False
        )
        #print(self.credit_curve)
                
        # Mkt Data Set
        self.mkt_data_set = create_cr_mkt_data_set(self.as_of_date,
                                                        cn_treas_curve,
                                                        self.credit_curve)
        #print(self.mkt_data_set)
        '''Settings'''
        
        self.pricing_settings = create_cds_pricing_settings(
                                pricing_currency = 'CNY',
                                include_current_flow = False,
                                cash_flows = True,
                                numerical_fix = 'TAYLOR',
                                accrual_bias = 'HALFDAYBIAS',
                                fwds_in_cpn_period = 'PIECEWISE'
                                )
        
        #print(self.pricing_settings)
        # Create Risk Settings
        self.risk_settings = create_cr_risk_settings(
            create_ir_curve_risk_settings(
                delta=True, gamma=False, curvature=False, 
                shift=1.0e-4, curvature_shift=5.0e-1, 
                method='CENTRAL_DIFFERENCE_METHOD', granularity='TERM_BUCKET_RISK', 
                scaling_factor=1.0e-4, threading_mode='SINGLE_THREADING_MODE'),
            create_credit_curve_risk_settings(
                delta=True, gamma=False, 
                shift=1.0e-4, 
                method='CENTRAL_DIFFERENCE_METHOD', granularity='TERM_BUCKET_RISK', 
                scaling_factor=1.0e-4, threading_mode='SINGLE_THREADING_MODE'),
            create_theta_risk_settings(
                theta=True, shift=1, scaling_factor=1./365.)
            )

    def test_credit_curve_builder(self):
        expected = b'\n\xc7\x01\n\x07\x08\xe4\x0f\x10\x02\x18\x15\x10\x02\x1a\x07\x08\xe4\x0f\x10\x05\x18\x18\x1a\x07\x08\xe4\x0f\x10\x08\x18\x18\x1a\x07\x08\xe5\x0f\x10\x02\x18\x18\x1a\x07\x08\xe6\x0f\x10\x02\x18\x18\x1a\x07\x08\xe7\x0f\x10\x02\x18\x18\x1a\x07\x08\xe8\x0f\x10\x02\x18\x18\x1a\x07\x08\xe9\x0f\x10\x02\x18\x18"\x0393D"\x04185D"\x04369D"\x04734D"\x051099D"\x051464D"\x051830D*:\n8\xed\x03Y\x84\xf9\xf3R??\xaavh\xf2\x95d?DU\xf97|\'v?w\x12\x89$\x0e\xbc\x87?rZ\nQ\xd0\x1c\x93?Vb\xb3\x01\xff{\x9d?\x18\xb1\xea\x8c\xc2_\xa5?0\x018\x01B\x0fCFETS-SHCH-GTJA\x12:\n8\x0e\x15O\x90\xac\x98r?u\xd1\x89=\xbbNt?\x02\xff\x7fv\x01\xeau?\xc11Xw\xf1\x9aw?\x14\xf4\\\xe0\x01dy?\xae\xcb\xb0\x88_g}?Ox\x95\xa5r\r\x81?'
        
        result = self.credit_curve        
        #print(result.SerializeToString())
        self.assertEqual(result.SerializeToString(), expected)
    
    def test_credit_default_swap_pricer(self):
        expected = b'\n\xc4\x05\t\x8c\x0f3\x04\xe6\xe5\xd7@\x1a\xaf\x05\n\xbd\x02\n\x05DELTA\x12\x87\x01\n\x06CREDIT\x12}\n\x0fCFETS-SHCH-GTJA\x12j\n:\n8\x80\xdd\xfb"\xc2*\x99\xc0\xc0_\xd6N\'\xf6\xb0\xc0(\xec\xd8H\x9e\x92\xd1\xc0\x807\xdd\xc4\xf7\xaf\xe7\xc0\xc2\x1c\x9f\xe2\xf7\xea\xf1\xc0\x06/\xcb\x1a$\xc56\xc1\xb1\x17Z!^\x95)\xc1\x12\x0393D\x12\x04185D\x12\x04369D\x12\x04734D\x12\x051099D\x12\x051464D\x12\x051830D\x1a\x00\x12\xa9\x01\n\rINTEREST_RATE\x12\x97\x01\n\x08CN_TREAS\x12\x8a\x01\n\x83\x01\n\x80\x01\x00X\xcafV\xa1e\xc0\x00\x80\xe8\xba\xef\xe3B@\x00@d\x7fF\xe3{\xc0\x00#k\xfe\x12\xbe\x8a\xc0\x00=\xe4\xe0\x8ai\x93\xc0\xa0q\x06\x08\xb0G\xb5\xc0\xa0\x0e\xb5\x15H\xd2\xc6\xc0\x88H\xe5\xd0!\xd1\xd2\xc0\x80\xbf\xdf;\x98k\xbe\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x1a\x00\n\xc6\x02\n\x0eDELTA_EXPOSURE\x12\x87\x01\n\x06CREDIT\x12}\n\x0fCFETS-SHCH-GTJA\x12j\n:\n8\x00\x00\xebZ\xe8\x9d\xc4\xbf\x00\x00\xef2/\xca\xdb\xbf\x00\xa0\xcaE\x89\xca\xfc\xbf\x00\x00\xdf:\x9ag\x13\xc0\x00\x88\x17\xf3I[\x1d\xc0\xc0\'Mz;\xa7b\xc0\x80\xca\xd1\xf4=\xf5T\xc0\x12\x0393D\x12\x04185D\x12\x04369D\x12\x04734D\x12\x051099D\x12\x051464D\x12\x051830D\x1a\x00\x12\xa9\x01\n\rINTEREST_RATE\x12\x97\x01\n\x08CN_TREAS\x12\x8a\x01\n\x83\x01\n\x80\x01\x00\x00\xb0\xd7/\xb8\x91\xbf\x00\x00\x00\xc22\xf3n?\x00\x00\x80\x90~\xd8\xa6\xbf\x00\x00\xa6\xd1M\xe8\xb5\xbf\x00\x0042\x19\xce\xbf\xbf\x00@7\xe6\xben\xe1\xbf\x00@\x11@\xff\xb1\xf2\xbf\x00 \x14\xa4c\xd4\xfe\xbf\x00\x00\xef\xf8\x98\xeb\xe8\xbf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\xb8}\xcf\x8286@\x12\x00\x1a\x00"\x00*\x03CNY2\x00\x10\x01'

        inst = build_credit_default_swap(nominal = 1000000.00,
                                        currency = 'CNY',
                                        issue_date = datetime(2019, 6, 20),
                                        maturity = datetime(2024, 6, 20),
                                        protection_leg_pay_receive = 'PAY',
                                        protection_leg_settlement_type = 'CASH_SETTLEMENT',
                                        protection_leg_reference_price = 0.0,
                                        protection_leg_leverage = 1.0,
                                        credit_protection_type = 'PAY_PROTECTION_AT_MATURITY',
                                        protection_leg_recovery_rate = 0.4,
                                        coupon_rate = 0.01,
                                        credit_premium_type = 'PAY_PREMIUM_UPTO_CURRENT_PERIOD',
                                        day_count_convention = 'ACTUAL_360',
                                        frequency = 'QUARTERLY',
                                        business_day_convention = 'MODIFIED_FOLLOWING',
                                        calendars = ['CAL_CFETS'],
                                        upfront_rate = 0.01,
                                        rebate_accrual = False)
        
        result = credit_default_swap_pricer(inst,
                                            self.as_of_date,
                                            self.mkt_data_set, 
                                            self.pricing_settings, 
                                            self.risk_settings)      
        #print(result.SerializeToString())
        self.assertEqual(result.SerializeToString(), expected)
        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCrAnalytics)
    unittest.TextTestRunner(verbosity=2).run(suite)

