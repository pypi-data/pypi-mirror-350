import unittest
from datetime import datetime

from caplib.market import *
from caplib.analytics import *
from caplib.cmmarket import *
from caplib.cmanalytics import *

class TestPmAnalytics(unittest.TestCase):

    def setUp(self):

        '''Static Data'''
        # Calendars
        cal_gblo = 'CAL_GBLO'  
        
        create_calendar(cal_gblo, [], [])
        
        # Instruments
        xauusd_cash = create_pm_cash_template(inst_name = 'XAUUSD',
                                            start_delay = 2,
                                            delivery_day_convention = 'FOLLOWING',
                                            calendars = [cal_gblo],
                                            day_count = 'ACT_360')
        
        xagusd_cash = create_pm_cash_template(inst_name = 'XAGUSD',
                                            start_delay = 2,
                                            delivery_day_convention = 'FOLLOWING',
                                            calendars = [cal_gblo],
                                            day_count = 'ACT_360')

        
        ''' Mkt Data'''        
        self.as_of_date = datetime(2019, 9, 4)

        # USD Depo Curve
        usd_depo_curve = create_ir_yield_curve(
            as_of_date = self.as_of_date,
            currency='USD',
            term_dates=[
                datetime(2019, 9, 9),
                datetime(2019, 9, 13),
                datetime(2019, 9, 20),
                datetime(2019, 9, 27),
                datetime(2019, 10, 7),
                datetime(2019, 11, 6),
                datetime(2019, 12, 6),
                datetime(2020, 1, 6),
                datetime(2020, 2, 6),
                datetime(2020, 3, 6),
                datetime(2020, 6, 8),
                datetime(2020, 9, 8),
                datetime(2021, 3, 8),
                datetime(2021, 9, 7),
                datetime(2022, 9, 6),
                datetime(2023, 9, 6),
                datetime(2024, 9, 6),
                datetime(2026, 9, 7),
                datetime(2029, 9, 6),
                datetime(2031, 9, 8),
                datetime(2034, 9, 6),
                datetime(2039, 9, 6),
                datetime(2044, 9, 6),
                datetime(2049, 9, 6),
                datetime(2059, 9, 8),
                datetime(2069, 9, 6)
            ],
            zero_rates=[
                0.021594,
                0.021592,
                0.021224,
                0.020529,
                0.019932,
                0.019103,
                0.018401,
                0.017694,
                0.017112,
                0.016575,
                0.015248,
                0.014216,
                0.012617,
                0.011520,
                0.006978,
                0.010018,
                0.007867,
                0.011028,
                0.013598,
                0.014042,
                0.013473,
                0.015213,
                0.014612,
                0.015525,
                0.015183,
                0.014780
            ],
            curve_name='USD_DEPO'
        )
        
        # PM Spot
        xauusd_spot = 1544.06
        xagusd_spot = 19.40
        
        xau_par_curve = create_pm_par_rate_curve(self.as_of_date,
                                                'USD',
                                                'XAU_XAUUSD',
                                                [
                                                    ('XAUUSD', 'PM_SWAP', '1W', 0.025),
                                                    ('XAUUSD', 'PM_SWAP', '2W', 0.025),
                                                    ('XAUUSD', 'PM_SWAP', '1M', 0.0248),
                                                    ('XAUUSD', 'PM_SWAP', '2M', 0.024),
                                                    ('XAUUSD', 'PM_SWAP', '3M', 0.0235),
                                                    ('XAUUSD', 'PM_SWAP', '6M', 0.0223),
                                                    ('XAUUSD', 'PM_SWAP', '9M', 0.0203),
                                                    ('XAUUSD', 'PM_SWAP', '12M', 0.0192),
                                                    ('XAUUSD', 'PM_SWAP', '2Y', 0.0152)
                                                ]
        )
        xag_par_curve = create_pm_par_rate_curve(self.as_of_date,
                                                'USD',
                                                'XAG_XAGUSD',
                                                [
                                                    ('XAGUSD', 'PM_SWAP', '1W', 0.026),
                                                    ('XAGUSD', 'PM_SWAP', '1M', 0.0258),
                                                    ('XAGUSD', 'PM_SWAP', '2M', 0.0257),
                                                    ('XAGUSD', 'PM_SWAP', '3M', 0.0254),
                                                    ('XAGUSD', 'PM_SWAP', '6M', 0.024),
                                                    ('XAGUSD', 'PM_SWAP', '9M', 0.0223),
                                                    ('XAGUSD', 'PM_SWAP', '12M', 0.0215),
                                                    ('XAGUSD', 'PM_SWAP', '2Y', 0.018)
                                                ]
        )
        #print(xau_par_curve)

        # PM Yield Curves
        pm_xau_yield_curve = pm_yield_curve_builder(
            as_of_date = self.as_of_date,
            par_curve = xau_par_curve,
            inst_template = xauusd_cash,
            discount_curve = usd_depo_curve,
            spot_price = xauusd_spot,
            curve_type = 'ZERO_RATE',
            interp_method = 'LINEAR_INTERP',
            extrap_method = 'FLAT_EXTRAP',
            day_count = 'ACT_365_FIXED',
            curve_name = 'XAU_XAUUSD',
            jacobian = False,
            shift = 1.0e-4,
            finite_diff_method = 'CENTRAL_DIFFERENCE_METHOD',
            threading_mode = 'SINGLE_THREADING_MODE'
        )
        pm_xag_yield_curve = pm_yield_curve_builder(
            as_of_date = self.as_of_date,
            par_curve = xag_par_curve,
            inst_template = xagusd_cash,
            discount_curve = usd_depo_curve,
            spot_price = xagusd_spot,
            curve_type = 'ZERO_RATE',
            interp_method = 'LINEAR_INTERP',
            extrap_method = 'FLAT_EXTRAP',
            day_count = 'ACT_365_FIXED',
            curve_name = 'XAG_XAGUSD',
            jacobian = False,
            shift = 1.0e-4,
            finite_diff_method = 'CENTRAL_DIFFERENCE_METHOD',
            threading_mode = 'SINGLE_THREADING_MODE'
        )
        #print(pm_xau_yield_curve)
        # Option Quote Matrix
        xauusd_option_quote_matrix = create_pm_option_quote_matrix(
            underlying = 'XAUUSD', 
            as_of_date = self.as_of_date,
            terms = [
                "ON",
                "1W",
                "2W",
                "3W",
                "1M",
                "2M",
                "3M",
                "4M",
                "6M",
                "9M",
                "1Y",
                "18M",
                "2Y",
                "3Y",
                "4Y",
                "5Y"
            ], 
            payoff_types = [
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"],
                ["ATM_STRADDLE", "RISK_REVERSAL", "BUTTERFLY", "RISK_REVERSAL", "BUTTERFLY"]
            ],
            deltas = [
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10],
                [0, 0.25, 0.25, 0.10, 0.10]
            ],
            quotes = [
                [0.21333, 0.02598, 0.00680, 0.04815, 0.02910],
                [0.15970, 0.02710, 0.00365, 0.05005, 0.01155],
                [0.15400, 0.02945, 0.00410, 0.05490, 0.01205],
                [0.16143, 0.03648, 0.00498, 0.06565, 0.01293],
                [0.15505, 0.03405, 0.00485, 0.06315, 0.01410],
                [0.15340, 0.03623, 0.00578, 0.06738, 0.01753],
                [0.15208, 0.03845, 0.00645, 0.07160, 0.01870],
                [0.15163, 0.03943, 0.00698, 0.07413, 0.01948],
                [0.15153, 0.04255, 0.00808, 0.08120, 0.02148],
                [0.15255, 0.04523, 0.00943, 0.08705, 0.02465],
                [0.15383, 0.04725, 0.01070, 0.09253, 0.02838],
                [0.15960, 0.04803, 0.01123, 0.09233, 0.03128],
                [0.16320, 0.05028, 0.01230, 0.09620, 0.03600],
                [0.17135, 0.05033, 0.02660, 0.09993, 0.09383],
                [0.17750, 0.05300, 0.01280, 0.10865, 0.04935],
                [0.18250, 0.05300, 0.01293, 0.10865, 0.05023]
            ]
        )
        #print(xauusd_option_quote_matrix)
        xauusd_market_conventions = create_pm_mkt_conventions(
            atm_type = "ATM_DNS_PIPS",
            short_delta_type = "PIPS_SPOT_DELTA",
            long_delta_type = "PIPS_FORWARD_DELTA",
            short_delta_cutoff = "1Y",
            risk_reversal = "RR_CALL_PUT",
            smile_quote_type = "BUTTERFLY_QUOTE"
        )
        #print(xauusd_market_conventions)
        vol_surf_definitions = create_volatility_surface_definition(
            vol_smile_type = "STRIKE_VOL_SMILE",
            smile_method = "SVI_SMILE_METHOD",
            smile_extrap_method = "FLAT_EXTRAP",
            time_interp_method = "LINEAR_IN_VARIANCE",
            time_extrap_method = "FLAT_IN_VOLATILITY",
            day_count_convention = "ACT_365_FIXED",
            vol_type = "LOG_NORMAL_VOL_TYPE",
            wing_strike_type = "DELTA",
            lower = -1e-4,
            upper = 1e-4)
        #print(vol_surf_definitions)
        # Build Volatility Surface
        self.xauusd_vol_surf = pm_vol_surface_builder(
            as_of_date=self.as_of_date, 
            vol_surf_definition = vol_surf_definitions,
            option_quote_matrix = xauusd_option_quote_matrix, 
            mkt_conventions = xauusd_market_conventions, 
            spot_price = xauusd_spot, 
            discount_curve=usd_depo_curve, 
            fwd_curve = pm_xau_yield_curve,
            building_settings = [1, 0.5],
            spot_template = xauusd_cash,
            underlying='XAUUSD',
            vol_surf_name='XAUUSD'
            )
        
        # XAUUSD
        self.xauusd_mkt_data_set = create_cm_mkt_data_set(self.as_of_date,
                                                        usd_depo_curve,
                                                        xauusd_spot,
                                                        self.xauusd_vol_surf,
                                                        pm_xau_yield_curve)
        #print(self.xauusd_mkt_data_set)
        '''Settings'''
        # BLACK_SCHOLES_MERTON model and ANALYTICAL method 
        self.bsm_analytical_pricing_settings = create_pricing_settings(
            'USD', False, 
            create_model_settings('BLACK_SCHOLES_MERTON'), 
            'ANALYTICAL', 
            create_pde_settings(), 
            create_monte_carlo_settings()
            )

        # BLACK_SCHOLES_MERTON model and PDE method
        self.bsm_pde_pricing_settings = create_pricing_settings(
            'USD', False, 
            create_model_settings('BLACK_SCHOLES_MERTON'), 
            'PDE', 
            create_pde_settings(201, 401, -5, 5, 'MMT_NUM_STDEVS', 0.001, 'ADAPTIVE_GRID', 'CUBIC_SPLINE_INTERP'), 
            create_monte_carlo_settings()
            )

        # BLACK_SCHOLES_MERTON model and MONTE_CARLO method
        self.bsm_mc_pricing_settings = create_pricing_settings(
            'USD', False, 
            create_model_settings('BLACK_SCHOLES_MERTON'), 
            'MONTE_CARLO', 
            create_pde_settings(), 
            create_monte_carlo_settings(8096, 'SOBOL_NUMBER', 1023, 'BROWNIAN_BRIDGE_METHOD', 'INVERSE_CUMULATIVE_METHOD',False, 1)
            )

        # Duprie Local Vol model and PDE method 
        self.duprie_pde_pricing_settings = create_pricing_settings(
            'USD', False, 
            create_model_settings('DUPIRE_LOCAL_VOL_MODEL',[201,401,4, 0.001]), 
            'PDE', 
            create_pde_settings(201, 401, -5, 5, 'MMT_NUM_STDEVS', 0.001, 'ADAPTIVE_GRID', 'CUBIC_SPLINE_INTERP'), 
            create_monte_carlo_settings()
            )

        # Duprie Local Vol model and MONTE_CARLO method
        self.duprie_mc_pricing_settings = create_pricing_settings(
            'USD', False, 
            create_model_settings('DUPIRE_LOCAL_VOL_MODEL',[201,401,4, 0.001]), 
            'MONTE_CARLO', 
            create_pde_settings(), 
            create_monte_carlo_settings(8096, 'SOBOL_NUMBER', 1023, 'BROWNIAN_BRIDGE_METHOD', 'INVERSE_CUMULATIVE_METHOD', False, 201)
            )
        
        # Create Risk Settings
        self.risk_settings = create_cm_risk_settings(
            create_ir_curve_risk_settings(
                delta=True, gamma=False, curvature=False, 
                shift=1.0e-4, curvature_shift=5.0e-1, 
                method='CENTRAL_DIFFERENCE_METHOD', granularity='TOTAL_RISK', 
                scaling_factor=1.0e-4, threading_mode='SINGLE_THREADING_MODE'),
            create_price_risk_settings(
                delta=True, gamma=True, curvature=False, 
                shift=1.0e-2, curvature_shift=5.0e-1, 
                method='CENTRAL_DIFFERENCE_METHOD', 
                scaling_factor=1.0e-2, threading_mode='SINGLE_THREADING_MODE'), 
            create_vol_risk_settings(
                vega=True, volga=True, 
                shift=1.0e-2, 
                method='CENTRAL_DIFFERENCE_METHOD', granularity='TOTAL_RISK', 
                scaling_factor=1.0e-2, threading_mode='SINGLE_THREADING_MODE'),
            create_price_vol_risk_settings(
                vanna=True, 
                price_shift=1.0e-2, vol_shift=1.0e-2, 
                method='CENTRAL_DIFFERENCE_METHOD', granularity='TOTAL_RISK', 
                price_scaling_factor=1.0e-2, vol_scaling_factor=1.0e-2, threading_mode='SINGLE_THREADING_MODE'), 
            create_dividend_curve_risk_settings(
                delta=True, gamma=False, 
                shift=1.0e-4, 
                method="CENTRAL_DIFFERENCE_METHOD", granularity="TOTAL_RISK", 
                scaling_factor=1.0e-4, threading_mode="SINGLE_THREADING_MODE"), 
            create_theta_risk_settings(
                theta=True, shift=1, scaling_factor=1./365.)
            )

        # Create Scenario Analysis Settings
        self.scenario_analysis_settings = create_scn_analysis_settings(
            scn_analysis_type = 'PRICE_VOL_SCN_ANALYSIS', 
            min_underlying_price=-20e-2, 
            max_underlying_price=20e-2, 
            num_price_scns = 11,
            price_scn_gen_type = 1,
            min_vol = -5.e-2, 
            max_vol = 5.e-2,
            num_vol_scns = 12, 
            vol_scn_gen_type=0,
            threading_mode='SINGLE_THREADING_MODE'
            )
        #print(self.bsm_analytical_pricing_settings)
        #print(self.risk_settings)
        #print(self.scenario_analysis_settings)

    def test_pm_vol_surface_builder(self):
        expected = b'\n \x08\x01\x10\x03\x18\x01 \x01(\x010\x028\x01I-C\x1c\xeb\xe26\x1a\xbfQ-C\x1c\xeb\xe26\x1a?\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\x0e\x17W\x8a\x9c3\x96@!`\xceM\x92\xea\x8d\x9a@*:\n8\x0e\x17W\x8a\x9c3\x96@\x8f\x1b\x17=A\xc7\x97@\xa1\xf1/\x17\x06\xf4\x97@\x01q\xdf\xce\r!\x98@\xf0\xeb\x17\x89-T\x98@\xc0H\x06\xcb\xb1\x90\x98@`\xceM\x92\xea\x8d\x9a@0\x039\x1ag\x016\x9fqf?B:\n8\x0b\rNs*o\xdb?\xa4\x83\xf5\x7f\x0e\xf3\xcb?\xa4\xc2\xd8B\x90\x83\xca?\x1f\xba\xa0\xbeeN\xcb?\x10\x92\x05L\xe0\xd6\xcd?X\x1c\xce\xfcj\x0e\xd1?\x1b\xce\\\xba}f\xdf?J*\n(\x95\xf7\x19@\xeby\xd1>\x9e\t\xe3\xb7O\xe0y?\xe4\x0eo+2\x06m?\xfe\xdfYd\x1chx\xbf\x0b\x90\x06V\xf4l\x92?R"\n \x1ag\x016\x9fqf?\x06Yd:\xab \x98@\x0e\x17W\x8a\x9c3\x96@`\xceM\x92\xea\x8d\x9a@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\x16D\xe5\x8dRk\x96@!\xac)\x9a_\xba\x1f\x9c@*:\n8\x16D\xe5\x8dRk\x96@[\xf2\xc3\xda,\x86\x97@\xcf\xf2\xb6\xd3\xaf\xce\x97@\x9e\xa4\xda\xff\xc0$\x98@N\x16\xe8\xa5\x16\x8c\x98@\xfc\xa65\x89\xa7\x00\x99@\xac)\x9a_\xba\x1f\x9c@0\x0397:AOk\xa3\x93?B:\n8\x95H\xf7\xb8\x7fg\xc2?\xd7\xc5m4\x80\xb7\xc2?"lxz\xa5,\xc3?\xe2\xe9\x95\xb2\x0cq\xc4?\x86\xc9T\xc1\xa8\xa4\xc6?\x01\xde\x02\t\x8a\x1f\xc9?\xb7\xafz$\xc5\xe3\xd2?J*\n(\xebi\xb3\x8f\xf7\xfd8?\x04\x8b\xf3\xdc[\x96p?k\x93\x8bz\xcf6\xef?-\x95l(t"\x80\xbf\xc2As\x13\x02@\x91?R"\n 7:AOk\xa3\x93?\xc5\x19 \x16>#\x98@\x16D\xe5\x8dRk\x96@\xac)\x9a_\xba\x1f\x9c@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\r]\xa00X\xe2\x95@!=\xcf\xac\x16@0\x9e@*:\n8\r]\xa00X\xe2\x95@\xcf\x1a\xd63\x11U\x97@4\xb5\x9ce\xa1\xb4\x97@\xee\xcf\xc9\xcc\x0e)\x98@\xccBaG\xa8\xb8\x98@2\x85\xc5u\x96^\x99@=\xcf\xac\x16@0\x9e@0\x0397:AOk\xa3\xa3?B:\n8)C\xb8\x9c\x13_\xc1?v\xe0\x9c\x11\xa5\xbd\xc1?\'1\x08\xac\x1cZ\xc2?\x83\xc0\xca\xa1E\xb6\xc3?\x8f1w-!\x1f\xc6?\xf8S\xe3\xa5\x9b\xc4\xc8??\xf7\xbe\xbd\xd9t\xd3?J*\n(\xf9\x0c\x85\xe7\x85\xb2E?\xbf\xcc<h\x90\x92y?\t\xb0J3B\xc5\xee?\xef\xd5\t\xe9\xf9z\x87\xbf\xe9\xdd?q\x81s\x9a?R"\n 7:AOk\xa3\xa3?\xa0\xd2,\xcd>&\x98@\r]\xa00X\xe2\x95@=\xcf\xac\x16@0\x9e@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\xabPAs\xc4a\x95@!\xd6`\x81\xd2\x92P\xa0@*:\n8\xabPAs\xc4a\x95@\xc2M\xc2X=%\x97@\x1a#\xb8\xc6s\x9a\x97@\xa9q\xfbD\xd3-\x98@[\xd5\x8e\x02\x0f\xeb\x98@w\x8b`\xc3\x1d\xc8\x99@\xd6`\x81\xd2\x92P\xa0@0\x039R\xd7\xe1\xf6 u\xad?B:\n8\xf073J[\x9c\xc1?Y\xa3\x1e\xa2\xd1\x1d\xc2?\xf3\xc8\x1f\x0c<\xf7\xc2?\x99\xf0K\xfd\xbc\xa9\xc4?Qk\x9aw\x9c\xa2\xc7?\xa1b\x9c\xbf\t\x85\xca?\x8de\xff\x8d\x0bT\xd5?J*\n(\x14FW\x83\xbb\nQ?iA\x92\xf9\xa1:\x81?\x98O\x1c`\x91v\xef?\xd5jg\xb1\xb3\xf2\x93\xbf\xe3\xc4\xa2\x9a\xe7\xfc\x9d?R"\n R\xd7\xe1\xf6 u\xad?V\xfb(\xce/)\x98@\xabPAs\xc4a\x95@\xd6`\x81\xd2\x92P\xa0@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\xb1\xaf\xdd\xf3g\xf7\x94@!)|\xed\x94\xc7&\xa1@*:\n8\xb1\xaf\xdd\xf3g\xf7\x94@"\xa7\x84P\xeb\x04\x97@\xaa\x8aH\x0f\x8c\x8b\x97@\xb9\x1c*H}2\x98@T\x8fW3X\x08\x99@\x14\xe4\x98\xb5\xb6\x08\x9a@)|\xed\x94\xc7&\xa1@0\x039pE\xf1H\xf8V\xb4?B:\n8F?\x96!\x01y\xc1?@\xa4\xdf\xbe\x0e\x9c\xc1?|?5^\xbaI\xc2?\x9bU\x9f\xab\xad\xd8\xc3?h"lxz\xa5\xc6?6\xab>W[\xb1\xc9?\xb70\x84K\xd1\x19\xd5?J*\n(\xd3\xbc\x1c\x010nU?\xfap\'W\x15P\x85?\xf9l\x00\x15\x7f\x0f\xed?\xf4\x89\xa5\x8f\x04\x9f\x92\xbf$\x13\xb4\x01\xe5\x87\xa2?R"\n pE\xf1H\xf8V\xb4?\x0bN\xd0\x85\x93,\x98@\xb1\xaf\xdd\xf3g\xf7\x94@)|\xed\x94\xc7&\xa1@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\x1b\x16\xf3\xfe\xc5\xb9\x93@!(c_8\x1e\xbd\xa4@*:\n8\x1b\x16\xf3\xfe\xc5\xb9\x93@\x0c\xee\x8c\x98#\x94\x96@\xc2\x03V\xaa\x8dV\x97@\xa2\xa2Tg\xa7E\x98@m\xb6\xf6\xb2\x99\x81\x99@O\xa5D\xf8\xad\x0f\x9b@(c_8\x1e\xbd\xa4@0\x039EVy\xbfKd\xc5?B:\n8\x12\xb6o\x9e\xe7l\xc1?7\xfd\xd9\x8f\x14\x91\xc1?Y\x1c\xce\xfcj\x0e\xc2?Qk\x9aw\x9c\xa2\xc3?\xe1E_A\x9a\xb1\xc6?7\xc3\r\xf8\xfc0\xca?\x06\x80a\xde\x9e6\xd6?J*\n(= b$\xe1\xb3g?\t\xbf\x1b\x00\x143\x90?F\xffy{D\x8a\xee?\xcfP\x8e\x04\xd3~\x93\xbfPT\x04n\xd5\xd2\xa4?R"\n EVy\xbfKd\xc5?\xb1\x12\xac\xa2r9\x98@\x1b\x16\xf3\xfe\xc5\xb9\x93@(c_8\x1e\xbd\xa4@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\xd7?\xdd\xf0=\xf2\x92@!R\xb1\xb2|\x9e\x13\xa8@*:\n8\xd7?\xdd\xf0=\xf2\x92@H!\x85\xfc\x94O\x96@\xd6\x16\xe8\xeb36\x97@`R\xdb\x87\xf9V\x98@\xed>\xfa=\xfd\xde\x99@\xf5Z\xfa\xc6z\xd9\x9b@R\xb1\xb2|\x9e\x13\xa8@0\x039\x99\xfe\xc9`\x8e\xe9\xcf?B:\n8\x86\xb5\xfc\xdc\xf48\xc1?,\x9a\xceN\x06G\xc1?\xf8\xaa\x95\t\xbf\xd4\xc1?H\x160\x81[w\xc3?T\xa9\xd9\x03\xad\xc0\xc6?\xa8\xfb\x00\xa46q\xca?U\t\x8b\x08\xf1\r\xd7?J*\n(\xfaE\x99\xc4\xcb\xf6p?G\xbfo*\xda\xf9\x94?\xa9\x11\xdb\xa7\xf0-\xee?\xbd\xf1\xf8.\x7f<\x97\xbf\xc0\x10j6TK\xa9?R"\n \x99\xfe\xc9`\x8e\xe9\xcf?Cs34\tE\x98@\xd7?\xdd\xf0=\xf2\x92@R\xb1\xb2|\x9e\x13\xa8@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\xe0*\xda1$\x9d\x8c@!\xd3\xc7ug\xcfO\xa8@*:\n8\xe0*\xda1$\x9d\x8c@\x92\x9d\xd9Y:\x18\x96@&\x88\xdev^\x1c\x97@\xb6\x84;\x94`g\x98@\xbd\xec\x05\x1d\x1e0\x9a@\xd1\xc8\xa0\xcdN\x89\x9c@\xd3\xc7ug\xcfO\xa8@0\x039\xa8P\xa1B\x85\n\xd5?B:\n8\x94\xb3\xa7\xc6\x82:\xd0?\xf0\x9d\x98\xf5b(\xc1?G\xf9I\xb5O\xc7\xc1?b\xd6\x8b\xa1\x9ch\xc3?\xdd\x93\x87\x85Z\xd3\xc6?h"lxz\xa5\xca?\xf3\x82\xe1\x13:\xea\xd6?J*\n(\x00\x00\x00\x00\x00\x00\x00\x007\xf8)\r\xf9]\xa9?\x7f\x9a\xe6\xa5\x9f\xd9\xb6?\xd2\xe7&\xa9dF\xb4\xbft\xe4\x05\x1b\xab\xee\xbe?R"\n \xa8P\xa1B\x85\n\xd5?\xd3\xc7ug\xcfO\x98@\xe0*\xda1$\x9d\x8c@\xd3\xc7ug\xcfO\xa8@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19"\xae\x9eI\xc1\x06\x89@!\xbc\x9d\xd1t\x0bf\xa8@*:\n8"\xae\x9eI\xc1\x06\x89@\x1b\xcds\xc8\x1c\xbc\x95@\x80r\xa8qi\xf2\x96@\xf39\x96H\xe7\x89\x98@\x1d\xbe&\x14\xd1\xd1\x9a@+\t\xf9\xe7\xb0\xf2\x9d@\xbc\x9d\xd1t\x0bf\xa8@0\x039\x99\xfe\xc9`\x8e\xe9\xdf?B:\n8\xe3\x7f\x9fW\xc2\xae\xd0?\xfb\xe8\xd4\x95\xcf\xf2\xc0?M2r\x16\xf6\xb4\xc1?\xdar.\xc5Ue\xc3?\x81!\xab[=\'\xc7?\x9d\x9d\x0c\x8e\x92W\xcb?\xd9\xb21l\x9e[\xd5?J*\n(\x00\x00\x00\x00\x00\x00\x00\x00\x89(o\xbf\x9d8\xb0?>z\x9d\x89\x8fl\xb8?\x08\xdf\x94T\x0bt\xb8\xbf\x89b\x16\x1a\xb3\x05\xc2?R"\n \x99\xfe\xc9`\x8e\xe9\xdf?\xbc\x9d\xd1t\x0bf\x98@"\xae\x9eI\xc1\x06\x89@\xbc\x9d\xd1t\x0bf\xa8@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19mI\xa7M=\x80\x88@!mI\xa7M=\x80\xa8@*:\n8mI\xa7M=\x80\x88@\xd1\x943\x13\tB\x95@\xd1)J\x1f\xc8\xbd\x96@\xa4 \x83\x1eD\xb7\x98@\x0f*W*$\xa8\x9b@6\xef\xc1;\xa0\xe5\x9f@mI\xa7M=\x80\xa8@0\x039Z\x80\xcdg\x9c\x05\xe8?B:\n8\x98\n\x9f\xb5\xf2{\xce?xz\xa5,C\x1c\xc1?I\x80\x9aZ\xb6\xd6\xc1?I\x9d\x80&\xc2\x86\xc3?\xc5\xa7\x00\x18\xcf\xa0\xc7?\xc6m4\x80\xb7@\xcc?\x95\x10\xb2z\xa30\xd4?J*\n(\x00\x00\x00\x00\x00\x00\x00\x00\xfb\x10\x0f(X\x95\xb4?\x80`A\xd6\x04\x94\xc2?!\xeawp\xb6-\xba\xbf\xdc\xdf\x9f\x10\xe3\xf8\xc5?R"\n Z\x80\xcdg\x9c\x05\xe8?mI\xa7M=\x80\x98@mI\xa7M=\x80\x88@mI\xa7M=\x80\xa8@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\xf2\xbeL.\xfd\x98\x88@!\xf2\xbeL.\xfd\x98\xa8@*:\n8\xf2\xbeL.\xfd\x98\x88@w\xa0\xc9\xb8H\xdb\x94@\x93\x06c\xf96\x97\x96@\\\x11\xb6\xb9\xef\xe3\x98@\xd7\x01\xc6q\xbal\x9c@\x91\xc3G\xfb\x1f\xeb\xa0@\xf2\xbeL.\xfd\x98\xa8@0\x039\x00\x00\x00\x00\x00\x00\xf0?B:\n8\xa24\xbe\x10\x9b\x0f\xcd?\x10\x01\x87P\xa5f\xc1?}\xe3k\xcf,\t\xc2?\x1bd\x92\x91\xb3\xb0\xc3?\xbd\x18\xca\x89v\x15\xc8?\x90\x0fz6\xab>\xcd?\xe5w\xccf\xb2\x90\xd3?J*\n(\x00\x00\x00\x00\x00\x00\x00\x00\x98\xea=Y\x95-\xb9?D\xb5V\x1b\x98\xe5\xc4?\xbdSD#\xc8\x92\xba\xbf\x8c\xe6\xce\xfe\xc5\xc6\xc8?R"\n \x00\x00\x00\x00\x00\x00\xf0?\xf2\xbeL.\xfd\x98\x98@\xf2\xbeL.\xfd\x98\x88@\xf2\xbeL.\xfd\x98\xa8@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19y\xbb\xfd\xbap\x12\x8a@!i\x87\xe1\xae\x15\xc0\xa8@*:\n8y\xbb\xfd\xbap\x12\x8a@\x97\x7f\xa5s\x07\t\x94@e\x80\xcf9\x1cH\x96@\x13\xa1\x8eT.:\x99@\xfe\t\x00\xc1\xc8\xe8\x9d@\x8a\x9d\xc20\xc4\xb8\xa2@i\x87\xe1\xae\x15\xc0\xa8@0\x039\xa6\x7f2\x98c\xfa\xf7?B:\n8\xebb\xf6zft\xc2?J\xcd\x1eh\x05\x86\xc2?z\xf7\xc7{\xd5\xca\xc2?Y\x868\xd6\xc5m\xc4?\xe2\x01eS\xae\xf0\xc8?\xba\x14W\x95}W\xce?\x9f\xfe\x1c\xea\xe6\x00\xd2?J*\n(a\xc4\xc5L\xe9\xc6\x9e?\x10\xb8\xa4\x0b\x0c\x02\xb0?)\x7f6G\x96c\xef?\'q\x1c\x1b\xc1\x8f\x93\xbf\xcd\x81\x02\xa0\x0c\x87\xb5?R"\n \xa6\x7f2\x98c\xfa\xf7?i\x87\xe1\xae\x15\xc0\x98@y\xbb\xfd\xbap\x12\x8a@i\x87\xe1\xae\x15\xc0\xa8@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\x90>t\xca0\xdf\x88@!\x90>t\xca0\xdf\xa8@*:\n8\x90>t\xca0\xdf\x88@\xd3\xdb\nP}Z\x93@{$\xc0\xd2\xf6\n\x96@\xf6\x94\xc4\xdc\xd0\x8a\x99@\xc8\xf98ejY\x9f@nb\xf8\x99\'\xb0\xa4@\x90>t\xca0\xdf\xa8@0\x039L\xffd0\xc7\xf4\xff?B:\n8z\x149\xdf:\x14\xc5?\x10z6\xab>W\xc3?\x1f3P\x19\xff>\xc3?\x88\x85Z\xd3\xbc\xe3\xc4?\x03}"O\x92\xae\xc9?\x9e\x80&\xc2\x86\xa7\xcf?\xb9\xe8\xd79\xf2\x8e\xd1?J*\n(\x1d~$\xa4\xcbO\xa3?V\x99e\xfc@\xc7\xb6?\xb0\xc5\xd4\xf7\xd7\x9b\xe7?\xb44\t\xbb\xbf#\x9e\xbf\xef\xe4\xc2}\xb1\xc4\xbe?R"\n L\xffd0\xc7\xf4\xff?\x90>t\xca0\xdf\x98@\x90>t\xca0\xdf\x88@\x90>t\xca0\xdf\xa8@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\x98x%\x10\x92\xe9\x88@!\x98x%\x10\x92\xe9\xa8@*:\n8\x98x%\x10\x92\xe9\x88@\xe7\xf77\xabG\x8f\x90@\xc4#rr@J\x95@Q\xa8\x80\xd7\xfd\x08\x9a@\xd6\x93l\x96\x03l\xa1@:T\xb2\xb3\xe2\x1c\xad@\x98x%\x10\x92\xe9\xa8@0\x039Z\x80\xcdg\x9c\x05\x08@B:\n8P!\xa9\xb2\xf9\x0c\xd1?\xe9\xe7ME*\x8c\xcb?Z\xa3\x1e\xa2\xd1\x1d\xc6?t\xb5\x15\xfb\xcb\xee\xc5?\x02\x9f\x1fF\x08\x8f\xcc?\xeb\xdd\x1f\xefU+\xd4?^\x11kX_\x86\xd2?J*\n(\xa9\xe74\xbf\xdff\x88?\xefY\x8b\xf5\xd59\xd3?\x9fJ\xfe%p\xb9\xa2?f\x8dk\x19C\xe7\xa4\xbf9\xb7\x0cs\xd91\xce?R"\n Z\x80\xcdg\x9c\x05\x08@\x98x%\x10\x92\xe9\x98@\x98x%\x10\x92\xe9\x88@\x98x%\x10\x92\xe9\xa8@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19\x92)Wg\xe5{\x89@!\x92)Wg\xe5{\xa9@*:\n8\x92)Wg\xe5{\x89@\x81*\x94\xd7\ra\x91@\x1b\x9bW\x0c\xa3\x8e\x95@\x8c\xa5R\xdd\x82$\x9b@\x0b\xfa\x99w\x9d\xc1\xa2@HIj\x00\x95\xb1\xae@\x92)Wg\xe5{\xa9@0\x039-\xc0\xe63\xce\x02\x10@B:\n8M\xa4\xf6B\x81Y\xca?\xf6\x06_\x98L\x15\xc6?\xba\xda\x8a\xfde\xf7\xc4?\xb8\x1e\x85\xebQ\xb8\xc6?\x1c\xeb\xe26\x1a\xc0\xcb?\xad\xfa\\m\xc5\xfe\xd1?uP\xbf\x00\xb9x\xd0?J*\n(\x00\x00\x00\x00\x00\x00\x00\x00&\xe2\xc3\xc0\t\x07\xd1?\xa8+,\x08\x93`\xb2?\x88\x01\xfd#\xbcP\xc3\xbfn&a\xe1\xbf\xe2\xd9?R"\n -\xc0\xe63\xce\x02\x10@\x92)Wg\xe5{\x99@\x92)Wg\xe5{\x89@\x92)Wg\xe5{\xa9@X\x01\x1a\xf2\x01\x08\x01\x12\x07\x08\xe3\x0f\x10\t\x18\x04\x19;h!\xda\x1c\x90\x89@!;h!\xda\x1c\x90\xa9@*:\n8;h!\xda\x1c\x90\x89@=\x97\xd5\xba\x11\x99\x90@\xe1\x054n\x02G\x95@\x033\xc1s\xfd\xc8\x9b@\x86\xfbrQ\xaf5\xa4@\x9b\xa8@\xe5J\xe3\xb1@;h!\xda\x1c\x90\xa9@0\x039Z\x80\xcdg\x9c\x05\x14@B:\n8-)S\x88s\xea\xc9?J\xb08\x9c\xf9\xd5\xc6?\x8f\x19\xa8\x8c\x7f\x9f\xc5?\\\x8f\xc2\xf5(\\\xc7?\xf1)\x00\xc63h\xcc?W\xcfI\xef\x1b_\xd2?8\\Y\xbd\x07\xf1\xcf?J*\n(\x00\x00\x00\x00\x00\x00\x00\x00*\xdf\x15 \\^\xd3?\x1e\xe5z8C\xc1\xac?\xfb\xc8\x8a.\xe3_\xc5\xbfe;\xbeQ\xe6F\xde?R"\n Z\x80\xcdg\x9c\x05\x14@;h!\xda\x1c\x90\x99@;h!\xda\x1c\x90\x89@;h!\xda\x1c\x90\xa9@X\x01"\x07\x08\xe3\x0f\x10\t\x18\x05"\x07\x08\xe3\x0f\x10\t\x18\x0b"\x07\x08\xe3\x0f\x10\t\x18\x12"\x07\x08\xe3\x0f\x10\t\x18\x19"\x07\x08\xe3\x0f\x10\n\x18\x03"\x07\x08\xe3\x0f\x10\x0b\x18\x04"\x07\x08\xe3\x0f\x10\x0c\x18\x04"\x07\x08\xe4\x0f\x10\x01\x18\x02"\x07\x08\xe4\x0f\x10\x03\x18\x04"\x07\x08\xe4\x0f\x10\x06\x18\x04"\x07\x08\xe4\x0f\x10\t\x18\x03"\x07\x08\xe5\x0f\x10\x03\x18\x04"\x07\x08\xe5\x0f\x10\t\x18\x02"\x07\x08\xe6\x0f\x10\t\x18\x04"\x07\x08\xe7\x0f\x10\t\x18\x04"\x07\x08\xe8\x0f\x10\t\x18\x04*\x06XAUUSD'
        
        result = self.xauusd_vol_surf
        
        
        self.assertEqual(result.SerializeToString(), expected)
  
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPmAnalytics)
    unittest.TextTestRunner(verbosity=2).run(suite)

