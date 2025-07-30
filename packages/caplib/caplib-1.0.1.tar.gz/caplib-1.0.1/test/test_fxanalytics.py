import unittest
from datetime import datetime
import numpy as np

from caplib.market import *
from caplib.analytics import *
from caplib.fxmarket import *
from caplib.fxanalytics import *

class TestFxAnalytics(unittest.TestCase):

    def setUp(self):

        '''Static Data'''
        # Calendars
        cal_cfets = 'CAL_CFETS'
        cal_euta = 'CAL_EUTA'
        cal_gblo = 'CAL_GBLO'
        cal_hkhk = 'CAL_HKHK'
        
        hol_serial_numbers =[44654, 44954]
        sbd_serial_numbers = [44655]
        # Convert list of serial numbers to datetime objects
        holidays = [datetime.fromordinal(sn) for sn in hol_serial_numbers]
        specials = [datetime.fromordinal(sn) for sn in sbd_serial_numbers]
        create_calendar(cal_euta, [],[])#holidays, specials)
        create_calendar(cal_gblo, [],[])#holidays, specials)
        create_calendar(cal_hkhk, [],[])#holidays, specials)
        create_calendar(cal_cfets, holidays, specials)
        
        # Instruments
        eurusd_spot = create_fx_spot_template(inst_name = 'EURUSD',
                                             currency_pair = 'EURUSD',
                                             spot_day_convention = 'FOLLOWING',
                                             calendars = [cal_euta, cal_gblo],
                                             spot_delay = '2d')
        
        self.eurusd_fwd = create_fx_forward_template(inst_name = 'EURUSD',
                                                fixing_offset = '-2d',
                                                currency_pair = 'EURUSD',
                                                delivery_day_convention = 'FOLLOWING',
                                                fixing_day_convention = 'PRECEDING',
                                                calendars = [cal_euta, cal_gblo])

        eurusd_swap_on = create_fx_swap_template(inst_name = 'EURUSD',
                                                start_convention = 'TODAYSTART',
                                                calendars = [cal_euta, cal_gblo],
                                                currency_pair = 'EURUSD',
                                                start_day_convention = 'FOLLOWING',
                                                end_day_convention = 'FOLLOWING',
                                                fixing_offset = '-2d',
                                                fixing_day_convention = 'PRECEDING')

        eurusd_swap_tn = create_fx_swap_template(inst_name = 'EURUSD',
                                                start_convention = 'TOMORROWSTART',
                                                calendars = [cal_euta, cal_gblo],
                                                currency_pair = 'EURUSD',
                                                start_day_convention = 'FOLLOWING',
                                                end_day_convention = 'FOLLOWING',
                                                fixing_offset = '-2d',
                                                fixing_day_convention = 'PRECEDING')

        self.eurusd_swap = create_fx_swap_template(inst_name = 'EURUSD',
                                                start_convention = 'SPOTSTART',
                                                calendars = [cal_euta, cal_gblo],
                                                currency_pair = 'EURUSD',
                                                start_day_convention = 'FOLLOWING',
                                                end_day_convention = 'FOLLOWING',
                                                fixing_offset = '-2d',
                                                fixing_day_convention = 'PRECEDING')
                                            
        usdcny_spot = create_fx_spot_template(inst_name = 'USDCNY',
                                             currency_pair = 'USDCNY',
                                             spot_day_convention = 'FOLLOWING',
                                             calendars = [cal_cfets, cal_gblo],
                                             spot_delay = '1d')
        
        self.usdcny_fwd = create_fx_forward_template(inst_name = 'USDCNY',
                                                fixing_offset = '-1d',
                                                currency_pair = 'USDCNY',
                                                delivery_day_convention = 'FOLLOWING',
                                                fixing_day_convention = 'PRECEDING',
                                                calendars = [cal_cfets, cal_gblo])

        self.usdcnh_fwd = create_fx_forward_template(inst_name = 'USDCNH',
                                                fixing_offset = '-2d',
                                                currency_pair = 'USDCNH',
                                                delivery_day_convention = 'FOLLOWING',
                                                fixing_day_convention = 'PRECEDING',
                                                calendars = [cal_hkhk, cal_gblo])

        usdcny_swap_on = create_fx_swap_template(inst_name = 'USDCNY',
                                                start_convention = 'TODAYSTART',
                                                calendars = [cal_cfets, cal_gblo],
                                                currency_pair = 'USDCNY',
                                                start_day_convention = 'FOLLOWING',
                                                end_day_convention = 'FOLLOWING',
                                                fixing_offset = '-1d',
                                                fixing_day_convention = 'PRECEDING')

        usdcny_swap_tn = create_fx_swap_template(inst_name = 'USDCNY',
                                                start_convention = 'TOMORROWSTART',
                                                calendars = [cal_cfets, cal_gblo],
                                                currency_pair = 'USDCNY',
                                                start_day_convention = 'FOLLOWING',
                                                end_day_convention = 'FOLLOWING',
                                                fixing_offset = '-1d',
                                                fixing_day_convention = 'PRECEDING')

        usdcny_swap = create_fx_swap_template(inst_name = 'USDCNY',
                                                start_convention = 'SPOTSTART',
                                                calendars = [cal_cfets, cal_gblo],
                                                currency_pair = 'USDCNY',
                                                start_day_convention = 'FOLLOWING',
                                                end_day_convention = 'FOLLOWING',
                                                fixing_offset = '-1d',
                                                fixing_day_convention = 'PRECEDING')

        eurcny_spot = create_fx_spot_template(inst_name = 'EURCNY',
                                             currency_pair = 'EURCNY',
                                             spot_day_convention = 'FOLLOWING',
                                             calendars = [cal_cfets, cal_euta],
                                             spot_delay = '1d') 

        eurusd_fwd = create_fx_forward_template(inst_name = 'EURCNY',
                                                fixing_offset = '-1d',
                                                currency_pair = 'EURCNY',
                                                delivery_day_convention = 'FOLLOWING',
                                                fixing_day_convention = 'PRECEDING',
                                                calendars = [cal_euta, cal_gblo])                                 

        ''' Mkt Data'''        
        self.as_of_date = datetime(2021, 3, 30)

        # USD Depo Curve
        usd_depo_curve = create_ir_yield_curve(
            as_of_date = self.as_of_date,
            currency='USD',
            term_dates=[
                datetime(2021, 4, 6), datetime(2021, 4, 13), datetime(2021, 4, 20), datetime(2021, 4, 30), 
                datetime(2021, 6, 1), datetime(2021, 6, 30), datetime(2021, 7, 30), datetime(2021, 8, 30), 
                datetime(2021, 9, 30), datetime(2021, 12, 30), datetime(2022, 3, 30), datetime(2022, 9, 30), 
                datetime(2023, 3, 30), datetime(2024, 4, 1), datetime(2025, 3, 31), datetime(2026, 3, 30), 
                datetime(2027, 3, 30), datetime(2028, 3, 30), datetime(2031, 3, 31)
            ],
            zero_rates=[
                0.00016, 0.00016, 0.00016, 0.00017, 0.00016, 0.00019, 0.00023, 0.00026, 0.00028, 0.00034, 0.00042, 0.00063, 0.00108, 0.00292, 0.00546, 0.00798, 0.01025, 0.01217, 0.01624
            ],
            curve_name='USD_DEPO'
        )
        # EUR EURUSD FX
        eur_eurusd_fx_curve = create_ir_yield_curve(
            as_of_date = self.as_of_date,
            currency = 'EUR',
            term_dates=[
                datetime(2021, 4, 6), datetime(2021, 4, 13), datetime(2021, 4, 20), datetime(2021, 4, 30), 
                datetime(2021, 5, 31), datetime(2021, 6, 30), datetime(2021, 7, 30), datetime(2021, 8, 30), 
                datetime(2021, 9, 30), datetime(2021, 12, 30), datetime(2022, 3, 30), datetime(2022, 9, 30), 
                datetime(2023, 3, 30), datetime(2024, 4, 2), datetime(2025, 3, 31), datetime(2026, 3, 30), 
                datetime(2027, 3, 30), datetime(2028, 3, 30), datetime(2031, 3, 31)
            ],
            zero_rates=[
                -0.00814, -0.00766, -0.00761, -0.00764, -0.00753, -0.00765, -0.00758, -0.00754, -0.00759, -0.00828, -0.00814, -0.00801, -0.00801, -0.00777, -0.00735, -0.0068, -0.00612, -0.00547, -0.00355
            ],
            curve_name='EUR_EURUSD_FX'
        )
        # CNH_USDCNH_FX Curve
        cnh_usdcnh_fx_curve = create_ir_yield_curve(
            as_of_date = self.as_of_date,
            currency='CNH',
            term_dates=[
                datetime(2021, 4, 1),
                datetime(2021, 4, 7),
                datetime(2021, 4, 14),
                datetime(2021, 4, 30),
                datetime(2021, 6, 30),
                datetime(2021, 9, 30),
                datetime(2021, 12, 31),
                datetime(2022, 3, 31),
                datetime(2023, 3, 31),
                datetime(2024, 4, 1),
                datetime(2025, 3, 31),
                datetime(2026, 3, 31),
                datetime(2028, 3, 31),
                datetime(2031, 3, 31)
            ],
            zero_rates=[
                0.01825,
                0.02184,
                0.02375,
                0.02515,
                0.02622,
                0.02770,
                0.02851,
                0.02958,
                0.03150,
                0.03289,
                0.03400,
                0.03497,
                0.03659,
                0.03814
            ],
            curve_name='CNH_USDCNH_FX'
        )
        # FX Spot
        eurusd_spot_rate = create_fx_spot_rate(create_foreign_exchange_rate(1.1761, "EUR", "USD"), 
                                               self.as_of_date, datetime(2021,4,1))

        usdcny_spot_rate = create_fx_spot_rate(create_foreign_exchange_rate(6.7, "USD", "CNY"), 
                                               self.as_of_date, datetime(2021,4,1))
        usdcnh_spot_rate = create_fx_spot_rate(create_foreign_exchange_rate(6.7, "USD", "CNH"), 
                                               self.as_of_date, datetime(2021,4,1))
        
        # FX Option Quote Matrix
        eurusd_option_quote_matrix = create_fx_option_quote_matrix(
            currency_pair = 'EURUSD', 
            as_of_date = self.as_of_date,
            terms = [
                "ON", "1W", "2W", "3W", "1M", "2M", "3M", "4M", "6M", "9M", "1Y", "18M", "2Y", "3Y", "4Y", "5Y", "7Y", "10Y"
            ], 
            deltas = [
                "ATM", "D25_RR", "D25_BF", "D10_RR", "D10_BF"
            ],
            quotes = np.array([
                [0.06035, -0.0031, 0.00115, -0.00565, 0.0031],
                [0.05515, -0.0029, 0.00135, -0.00520, 0.00385],
                [0.05730, -0.00285, 0.00135, -0.00520, 0.00415],
                [0.0587, -0.0023, 0.00140, -0.00415, 0.00405],
                [0.06115, -0.00248, 0.00147, -0.00450, 0.00450],
                [0.06105, -0.00213, 0.00177, -0.00380, 0.00530],
                [0.06135, -0.00180, 0.00205, -0.00330, 0.00625],
                [0.0621, -0.0016, 0.00220, -0.00290, 0.00678],
                [0.0625, -0.00135, 0.00250, -0.00240, 0.00815],
                [0.06315, -0.00105, 0.00295, -0.00195, 0.00995],
                [0.0633, -0.00100, 0.00325, -0.00185, 0.01120],
                [0.06635, -0.00182, 0.00330, -0.00360, 0.01100],
                [0.0678, -0.00248, 0.00333, -0.00480, 0.01150],
                [0.07125, -0.00165, 0.00345, -0.00330, 0.01205],
                [0.07338, -0.00138, 0.00350, -0.00275, 0.01225],
                [0.07533, -0.00120, 0.00350, -0.00245, 0.01240],
                [0.07825, -0.00168, 0.00322, -0.00373, 0.01058],
                [0.0819, -0.00197, 0.00307, -0.00410, 0.01035]
            ])
        )
        #print(eurusd_option_quote_matrix)
        eurusd_market_conventions = create_fx_mkt_conventions(
            atm_type = "ATM_DNS_PIPS",
            short_delta_type = "PIPS_SPOT_DELTA",
            long_delta_type = "PIPS_FORWARD_DELTA",
            short_delta_cutoff = "1Y",
            risk_reversal = "RR_CALL_PUT",
            smile_quote_type = "BUTTERFLY_QUOTE",
            currency_pair = "EURUSD"
        )
        #print(eurusd_market_conventions)
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
            upper = 1e-4
        )
        # Build Volatility Surface
        self.eurusd_vol_surf = fx_volatility_surface_builder(
            as_of_date=self.as_of_date, 
            currency_pair="EURUSD",
            fx_market_conventions  = eurusd_market_conventions, 
            quotes = eurusd_option_quote_matrix, 
            fx_spot_rate = eurusd_spot_rate,
            dom_discount_curve=usd_depo_curve, 
            for_discount_curve=eur_eurusd_fx_curve,
            vol_surf_definitions = vol_surf_definitions,
            vol_surf_building_settings = [1, 0.5]
            )
        #print(self.eurusd_vol_surf)
        # EURUSD
        self.eurusd_mkt_data_set = create_fx_mkt_data_set(self.as_of_date,
                                                        usd_depo_curve,
                                                        eur_eurusd_fx_curve,
                                                        eurusd_spot_rate,
                                                        self.eurusd_vol_surf)
        # USDCNH
        self.usdcnh_mkt_data_set = create_fx_mkt_data_set(self.as_of_date,
                                                        cnh_usdcnh_fx_curve,
                                                        usd_depo_curve,
                                                        usdcnh_spot_rate,
                                                        None)
        #print(self.eurusd_mkt_data_set)
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
        self.risk_settings = create_fx_risk_settings(
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

    def test_fx_forward_pricer(self):
        expected =b'\t[M\x80\x90i\xf3\xa1@\x1a\xee\x03\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xe3\x1f\x13\xd5a\x93.A\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\xc3\xdb\xcf\nH\xee\x11\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x080\x8f<E"\xe5\x11A\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xea:\x10\xad\xb3\x03\xc7@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\xc0I\xeb\x91\xb7`=\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x7f*\xa5\xcf\xbaQ=@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xf0\xe0~\xcc\x8d=L\xbe\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xff\xff\xff\xff\xff\xff\x7f\xbd\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00p\xeb,\x8f\x98\xfc?\x12\x00\x1a\x00"\x00*\x03USD2\x00'
        
        fx_forward = create_fx_forward(buy_currency = "EUR",
                                       buy_amount = 1e6,
                                       sell_currency = "USD",
                                       sell_amount = 1.1761e6,
                                       delivery = datetime(2021, 4+3, 1),
                                       expiry = datetime(2021, 3+3, 30))
        result = fx_forward_pricer(pricing_date=self.as_of_date,
                                 instrument=fx_forward,
                                 mkt_data=self.eurusd_mkt_data_set,
                                 pricing_settings=create_pricing_settings(
                                    'USD', False, 
                                    create_model_settings(None), 
                                    'ANALYTICAL', 
                                    create_pde_settings(), 
                                    create_monte_carlo_settings()
                                    ),
                                 risk_settings=self.risk_settings)
        #print('test_fx_forward_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)
    
    def test_fx_ndf_pricer(self):
        expected =  b'\t\x1c\xd2J\xd0\xe9fS@\x1a\xee\x03\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_USDCNH\x12\x10\n\n\n\x08?\xd7\xf7\x12\x1e$\x97@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rCNH_USDCNH_FX\x12\x15\n\n\n\x08\x98\x86\xccO\\S\xa3@\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\xdc\xcbn\xa6\xe8z\xa3\xc0\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_USDCNH\x12\x10\n\n\n\x08\xf4DMh\xa7\xceX@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rCNH_USDCNH_FX\x12\x15\n\n\n\x08\xff\x12\xacn\xc1\xa9\xcf?\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\x92\xfb%\x8d\xea\xcf\xbf\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_USDCNH\x12\x10\n\n\n\x08)y \xb7\x92\xa1{\xc0\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_USDCNH\x12\x10\n\n\n\x08\xc02\x11H\xd6\xc0\xff\xbf\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00{B>L2\xd0\xbf\x12\x00\x1a\x00"\x00*\x03USD2\x00'

        fx_ndf = create_fx_non_deliverable_forwad(buy_currency="USD",
                                                  buy_amount=10000,
                                                  sell_currency="CNH",
                                                  sell_amount=66916,
                                                  delivery_date=datetime(2021, 4+3, 1),
                                                  expiry_date=datetime(2021, 3+3, 30),
                                                  settlement_currency="USD"
                                                  )
        
        
        result = fx_ndf_pricer(pricing_date=self.as_of_date,
                             instrument=fx_ndf,
                             mkt_data=self.usdcnh_mkt_data_set,
                             pricing_settings=create_pricing_settings(
                                    'USD', False, 
                                    create_model_settings(None), 
                                    'ANALYTICAL', 
                                    create_pde_settings(), 
                                    create_monte_carlo_settings()
                                    ),
                             risk_settings=self.risk_settings)
        #print('test_fx_ndf_pricer:', result.SerializeToString())
        self.assertEqual(result.SerializeToString(), expected)
    
    def test_fx_swap_pricer(self):
        expected = b'\x1a\x00"\x00*\x03USD2\x00'
        
        fx_swap = create_fx_swap(near_buy_currency="EUR",
                                 near_buy_amount=1000000,
                                 near_sell_currency="USD",
                                 near_sell_amount=1176100,
                                 near_delivery_date=datetime(2021, 4+0, 1),
                                 near_expiry_date=None,
                                 far_buy_currency="USD",
                                 far_buy_amount=1000000,
                                 far_sell_currency="EUR",
                                 far_sell_amount=1176100,
                                 far_delivery_date=datetime(2021, 4+3, 1),
                                 far_expiry_date=None)

        result = fx_swap_pricer(pricing_date=self.as_of_date,
                                 instrument=fx_swap,
                                 mkt_data=self.eurusd_mkt_data_set,
                                 pricing_settings=create_pricing_settings(
                                    'USD', False, 
                                    create_model_settings(None), 
                                    'ANALYTICAL', 
                                    create_pde_settings(), 
                                    create_monte_carlo_settings()
                                    ),
                                 risk_settings=self.risk_settings)
        #print('test_fx_swap_pricer:', result.SerializeToString())
        self.assertEqual(result.SerializeToString(), expected)

    def test_fx_european_option_pricer(self):
        expected = b'\n\xae\x07\t9\xfd\xcf\xb1\xfb\x85\xd6@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xd6\x07\xf8\xfb0\xa6 A\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x89\x0b\t-Wp\x13\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\xa2\xe0\xeaj\xa2\xbd\x12A\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xf9\xbb7BV\x10\xb9@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00d\xda\x7f<\xd9?\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\x08\xdf\xbbq\xb4>@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08J\x16\x94\x97\xce5]A\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08@\xfeW\xae\xa6\x8c\x90@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\x00O8_\x1b0\xc0\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08_\x07&\xc8\xca\x89\x19\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\xf3n\x94\xe8\x9aH\xc0\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x087 ;7\xe3\x0f\x14A\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x84\n\xdb\xa2\xef\xad\xa9@\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xf0c\xb1\xb7\xca\n\xe3@\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\xc0\xeb\xe6\xdb2\x0f@\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\xd6\xed\x9c\x86\xf7\xfa\xba$\xab\xd9\x8c\x15\xa7%\x9a/\xe0\x8c\xe1]\xbd#u7Y\xde\xfe"\xc9\x99\xb0<\xe7\x9c\xec\xd5\x124\xa3?\xf8)\x81[>\xdb\xba@&(\xad=\xf2L\xe9@R_\x97\xa8\xcd-\xf8@TL\xd2\x1b\x91\xda\x01A\x07\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rATj\xdcP\xf1w\xf66H\xa8\xb6\xec9\x1d\xaf:\xc0\xe9\x1e2\xc8\x1eb=\x8b\xba:\xe8\x9e<4?+\\\xe40p\xdeF@ox\xe7K\xa6\xf8\xc2@\xbbOF@\x92N\xe9@\xc1:k\xa9\xcd-\xf8@TL\xd2\x1b\x91\xda\x01A\x07\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rA\x8c\x15\x1b\x9eW\xd4\xb7;\x93\t\xc1\x0cG\n\x97=h\xc0&[\xe6"\xf6>\xa2\xd2\xa8|\x8b\'\xe7?\xa5\xf6\xfbZ\xb0M|@\x0e\xccL\xba\xf3\xb2\xc8@\xf7,\xfb\xb1Pi\xe9@\x14\xb1mI\xd7-\xf8@u\xbc\x1f\x1c\x91\xda\x01A\x89\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rA\x99\x99\xbe\x10\x01\x00\xa6=\x9c#\x16\xc7]o\xc8>~Yq\x1a>e\xa0?\x9d8\xdc\x12\x7f\x8c5@M\xfd\xf3\xed\xcf?\x96@\x15\x0b\x9e\xdd\x97|\xce@u\xceP\xb0O\xbe\xe9@\x1fq~\xa2\t/\xf8@>\xba\xd0\xff\x91\xda\x01A\x0e\x08\xb4c;\x9e\x07A\xcf\x90\xdf\xaa\xe5a\rA\xd4\xb1\xa5S\xee\xa0\xa1>w\x83\x8c\x96SCe?\xe1\xc4]\xe3\x94\xe7\xf7?-\xad"\x01-ca@\xa6\xe1D\x969\x81\xa6@\t\xf4l\xd9\x86&\xd2@e\xff\xa0"YQ\xea@\xd3\x7f\x85J,6\xf8@\xce;a`\xae\xda\x01A\xad\xd4{\xbd;\x9e\x07A\x8c\xcc`\xab\xe5a\rA!\xaa\t\xeb\x8eN3?\xc2F\xad\x02\':\xc2?U_\x0c\xd6\xc5R.@\xec\x9c\x9fS+*|@\xa5\xa3Q\xae\xb3T\xb2@\xfe\xcf\x88\xd3\x8c\x10\xd5@\xc9\x0f\xe4\xd6)\x17\xeb@\x07iE%\xb5I\xf8@\xa5\xb0\xe4\xf7\x83\xdb\x01A\xf9IW\xcdD\x9e\x07A\xfaC\t\xe2\xe5a\rA\x18\x85&x\x80>\x91?J#\x16A\xcc{\xfe?SD\x99\xe0\xcf\x97Q@2;a7\x9a\xb3\x8f@\x1av\xe2\x8f8e\xba@\'\n\xa2\xee\x9d\xfb\xd7@\xab5/\x94i\x03\xec@\x85\xc1\xbe\xaa\xc8m\xf8@\xe7\xac\x00\x06r\xde\x01A\r\x83\x0b\xb0\x8b\x9e\x07A\xa4\x1a9\x1a\xeaa\rA\xa3\xb8\x00\x84\x8a\'\xd1?"\xcb\xa9\x91D\x01\'@\x94DH \t\x1bj@\xa5b2=0\xcd\x9c@\x1e\x04\x0f-K\x95\xc1@\xf3j4}T\xe7\xda@\x95\xdb|\x9fM\x0c\xed@\xc0Uv4\x87\xa3\xf8@\x19\xb0\x8b?"\xe5\x01A\xf4A\xce\t\xa2\x9f\x07A\x8bI\xc4_\tb\rA\xef\xf4\xd8\xb7>u\xff?\xf5\x86\xee\xad\x17\\E@\\\xd4\xc2\xce\xb3]}@\xde\x93\xc8\xdb]\xd4\xa6@]W\xaeN\r:\xc6@\xe2\x89\xf2.u\xd3\xdd@\x0eL\x01\'\xad*\xee@`j\x86\xe1 \xea\xf8@,,\xa2\xb7\xf0\xf0\x01A\x93:\xf5\xa0p\xa2\x07A\xf9\x12o\x06\x88b\rAG\x8c\x8f\xa3\'\x84!@.\x7f\xfa+\xc1\xef\\@ED\xad\x0f\x0e\x87\x8b@k\x8d\xe3\xb4O\x80\xb0@K\x8a\'=(\x10\xcb@&3\x1f^\xed_\xe0@\xf9A\x06PcY\xef@\x97\x14\xb0\x9c\xe5?\xf9@\x8aH\xb7q\xac\x02\x02A\xd8\xf6\xc1|\xfd\xa7\x07A\xa5\x96\xcd\xc3\xe3c\rA\x96\xd2\xeb\xd0+\xda;@\xadm\xbf\x8bd\x9fo@\xd84i\x8a\xe7\xbf\x96@Q\x8c\xa5\r@X\xb6@\xd7\xb6&\x0e\xf2\x05\xd0@\xad\x0f\xd6\x1f6\xd6\xe1@\xf29<\xc5\\J\xf0@\xe9qu\xcb\xe8\xa2\xf9@`\x1b\xf1\x19\xa1\x1a\x02A\x16\x04\xc1\x8a0\xb1\x07A\xdd\x0e\xd7\x83\xc4f\rA\xe0\r\xfbO\x98yQ@\x91<=\x8d\xa4\xad}@\x9fx*&\x82,\xa1@\xb8\xa4<{5\xd6\xbc@\xeb\x1b8\xc7n\x92\xd2@\xc03\x94\x1c\x8cL\xe3@\xf6\xd6\xbdi\xfc\xec\xf0@\xecQ$\xbaP\x11\xfa@\x85z\xb0\xaa\xbb8\x02A\x81\xa1\xfb\x8e\xb3\xbe\x07A\xbb\x83\x0b5\xdek\rA \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_european_option(
            payoff_type='CALL',
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            strike=1.176100,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )
        
        result = fx_european_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_analytical_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_european_option_pricer:', result.SerializeToString())
        self.assertEqual(result.SerializeToString(), expected)
        
    def test_fx_american_option_pricer(self):
        expected = b'\n\xae\x07\t9g\x891Z\x82\xd6@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08#\xe4\x8b\x19\x83\xa4 A\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x9d\xac=#\xe2R\x13\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x1fh\xc4\xc8F\xa1\x12A\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x18pn\x1b\xcf\r\xb9@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00\xd6(C\xf9\xa8?\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00<\xee\x8c\xfb\x85>@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x8eo\xb4\x8c\x106]A\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xa0:\xd6\x0c\xcc\x8c\x90@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\xc0w\xdf\xe1U\xf9\xbf\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xf4\xfag\xe4\x08W\x19\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x80l\xedx\x01jH\xc0\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xec\x96\xe2\x16\x13\x10\x14A\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08l\xcb\x17\xea,\xae\xa9@\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x080\r|\xa7\xc8\xcd\xe2@\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\xc0`D\xe7\xce\x0e@\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\xef\x07\xe1<\x98U\xb9$\xda|v/G\xe5\x98/k\xdaW\xdfAet7\x80\xcaLW\xe47\xb0<\xf9\x05\xdd?%\xfb\xa2?\xd5\xec\xcc\x17Q\xc9\xba@\xb8F\x84\xe7yI\xe9@\xe3S)0\x01,\xf8@|\x88\xf7\xb8\xa2\xd9\x01A\x07g\xda\xd9D\x9d\x07A\x8bE\xbd\xfa\xe6`\rA\x82I\xb0\xbd\xb1\xfd\xf56&\x8e,\xd1{\x98\xae:\x8f\xf8\x9a\xbe\xb0\xe5a=\x94V\xeb\x15\x1b\x124?\x8f\x95\x1dY)\xc4F@bJ\xa7\x02\x96\xf0\xc2@%g)\xff\x1bK\xe9@\xcc\xf5\xfe0\x01,\xf8@|\x88\xf7\xb8\xa2\xd9\x01A\x07g\xda\xd9D\x9d\x07A\x8bE\xbd\xfa\xe6`\rA+\xc1|/\xdb\x92\xb7;\x1e7\xb6\xb5g\xd8\x96=E\x0c\xc8\xb2$\xff\xf5>\x8c\xf4\xce\xf6\xef\r\xe7?a\x04,\x9a%;|@23\xfa^C\xab\xc8@\xbe\xc4e\x98\xece\xe9@\x99\x15\xca\xdb\n,\xf8@\xfaoE\xb9\xa2\xd9\x01A\x90g\xda\xd9D\x9d\x07A\x8bE\xbd\xfa\xe6`\rA\xc3V+\xbfe\xdb\xa5=c\x80-D"O\xc8>7\xf7\xf5Q\xe5T\xa0?Z\x1aS\xd2^}5@\x1d\xe3\x86>\xec5\x96@\xd3}x\x95\x1au\xce@\xad\xe9\xf95\r\xbb\xe9@$\xbe\x92\t>-\xf8@\xddw\xce\x9d\xa3\xd9\x01A\xb9\xf25\xdaD\x9d\x07A\xb8P\xbd\xfa\xe6`\rA;\xd9F\x10&\x8d\xa1>S\xa3\x1c\xa5D0e?\x08C>\xc8)\xd7\xf7?`\x13\x18?\x8aZa@\xbd\x81\x0f\xa1\xc0y\xa6@\xd8\x1d\x19\xa1\xd7"\xd2@\xa1w\xe9\xd7;N\xea@\xf1)\x14\xfdc4\xf8@\xba@\xa8\x10\xc0\xd9\x01ANlF4E\x9d\x07Af\t?\xfb\xe6`\rA\x10w5\xb4\xdc>3?\x8ah\x86u8.\xc2?\x17\xe0\xdc\xa8YC.@t\xc34X\x8d\x1f|@^\xe3n\xa6\xdfO\xb2@\xf4\xb0\x0c\x9e\xe7\x0c\xd5@\xc4\xa9N\x01/\x14\xeb@{\xd6\xb7+\xf3G\xf8@o\x95\x85\n\x96\xda\x01A\xfb\xf9mIN\x9d\x07A\xa9\xbc\r2\xe7`\rA\xd41^(\xd03\x91?\xc5^g\xebtl\xfe?\xdd\x9e\xc6\x07\xd7\x90Q@g\xe3\xe1\xda\x14\xaa\x8f@\xa9\x1dH4z_\xba@\xb8\x86\xb0\x81\xff\xf7\xd7@b\x90\x8a\xaf\x8c\x00\xec@f\xce0G\x0fl\xf8@\xfe\xc2\x18\x19\x85\xdd\x01A\xe3\xbb4K\x95\x9d\x07A\x16\xd3wl\xeb`\rA%\xbd\x868\x1e\x1f\xd1?\x90\x8e\xdc=\x05\xf8&@\xa5\t6u\xaa\x12j@\xd3{\xec\xc6\x0c\xc6\x9c@N\xdeK \n\x92\xc1@k>\x8a\xc4\xba\xe3\xda@\xd6a\r,\x8a\t\xed@`\x81\xc9\x92\xd7\xa1\xf8@\x8e\xc3\x02\x147\xe4\x01A\xb1\xdd7\x03\xac\x9e\x07A5\x8c\xd6\xbe\na\rA\xc5\xe6D\x14\xa4h\xff?\x01`\x02y\x07UE@\x84\xe3E\x08\xddU}@\xa5\x16DB\x92\xcf\xa6@\xbf\'\xc2\xfay6\xc6@\xe0\xa8\xb7\xbf\xde\xcf\xdd@\xff\x84\xee4\xff\'\xee@\xa9\x19 S{\xe8\xf8@4\x90 \xfe\x07\xf0\x01A\xf3\x13-[{\xa1\x07A\x1d\x8a\xd5\x8e\x89a\rA:`\x14\x86J~!@\xcd\xc2vU\xb2\xe7\\@\xbdoH\x1d\xcc\x80\x8b@v\x94T\x10P}\xb0@\x13i0\x0fO\x0c\xcb@\xe3O\x08J#^\xe0@d1n\x94\xc7V\xef@\xdd\x00d\xe9I>\xf9@@4\x9b\xaf\xc6\x01\x02A\x8c\xf4\xb4k\t\xa7\x07A\xfdnY\xa8\xe5b\rA\xce\xa6\x83\xc8:\xd2;@\x1d3l\xe9\xd5\x97o@\x08,\xf7\x88k\xbb\x96@\x8cD\n\xe0\xadT\xb6@\xeb\x81\xdb~\xe7\x03\xd0@\xc9\xa3\x07\xd0l\xd4\xe1@\x04`\x88\xa7\x16I\xf0@\xad\x10\x06pV\xa1\xf9@\xa3\x19[\xa4\xbe\x19\x02AV\xfc\xd1\x1f>\xb0\x07A5\xce\xbd\t\xc7e\rA\xed\x00\x1fgHuQ@\x99\n\x87\xe3u\xa7}@\tAcr\x87)\xa1@\x9dN\xf0\xfe\x19\xd2\xbc@H\xba\xad:J\x90\xd2@\x01T\xd5H\xc3J\xe3@Y\xeb\xe3\xee\xbc\xeb\xf0@p\xb5\xad\x10\xc7\x0f\xfa@g7\xe2\xac\xdc7\x02A\xfb\x9d\x8b+\xc3\xbd\x07A=\x81\xe7\xaa\xe1j\rA \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_american_option(
            payoff_type='CALL',
            expiry=datetime(2021, 9, 26),
            strike=1.176100,
            settlement_days=1,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_american_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_analytical_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_american_option_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)
    
    def test_fx_asian_option_pricer(self):
        expected = b'\n\xae\x07\t\x83\x18\x97y$C\xc9@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08,}\x90\x89\xd5\xe9\x1fA\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\xd0\x96{2~B\x03\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x99\x14\x1a\xc4){\x02A\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xd1\xc0\x1e\x82w\x05\xb8@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00b,\xa2\x1e\x8e/\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\xc6\xdf\xa6\x89G.@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xf5\x9d?\x08\x1eClA\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xca\x12\x1c\xeb&\x03\xa0@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x080\x7f\x85\xb4\xbbt\xa9\xc0\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\n\x92\x14\xd4\x90Y\x17\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08`c3\xf5&\x7fF\xc0\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xe5\x84Q\rU<\x07A\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08D\x06\xb0\x81\xdd\xbd\x9d@\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08`\xdf\xcb^\x83x\xc2@\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\x80\x15+2C\xee?\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00V\xe2U\x86\x99\xa0\xab@R\xc0\xf9G\n \xe8@\xd5n\r\x19\x91\x91\xf7@\xc0\xfe\x0e\x87\x8e\x89\x01A\rF\x97\x81TJ\x07Ai\x8d\x1f|\x1a\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00J@.\xcc\x9aI\xb4@\xe5?8\xa5\x19 \xe8@oXP\x13\x99\x91\xf7@|H\x02\xaa\x92\x89\x01A\xb6d\\\xcaXJ\x07A\xf3\x80\xb6\xea\x1e\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x07.\xcd\xf2R\xf0?UY\xbb!\x7f\xf1\xba@\xc9\x15P\xed& \xe8@E\xc6w\x91\x9e\x91\xf7@\x8d5 \x83\x95\x89\x01A\xf9\x87\x84\xbd[J\x07Ah\xda\xe8\xf7!\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xca\x112\xc4\xa4dD@\xde\xa2zd\xbc\xd3\xc0@\xfb\x8a\xcdM\x12"\xe8@\xf2\x8e\x02\xe5\xa1\x91\xf7@\xa8\x8a\xaa<\x97\x89\x01A\xdb\xcd\xd3\x86]J\x07A\n\x11\xfd\xd0#\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\'\xf2\xdf\xae\x1e\xa5h@\x8f\xe4\x99g"2\xc4@\x02\xc9\x9c\x91\xb8/\xe8@\xd5\xb0:\x18\xa3\x91\xf7@\x04\x0e\xf7\xdb\x97\x89\x01A\x9f\xc3\xd0+^J\x07A,y\xaa{$\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00L.(\x1f\xfdf\xdb?\xbaW\xc5\xedB~\x80@\xb5\xf5l\xd5\x93\x92\xc7@\x85A\xbc\xb2\xd3P\xe8@\x9c\x85)d\xa4\x91\xf7@\xb6W-d\x97\x89\x01A\x15\xd9\xbf\xaf]J\x07AtZR\xfb#\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xdd\xe0\xe0\xceU\x1f@E\x89\xe7\xf1Bf\x90@8\x1eiY\xc8\xf3\xca@\xf9|\xd3!\xdf\x88\xe8@0,\xb61\xec\x91\xf7@#\xfd\x07\xd8\x95\x89\x01A\xad\x96t\x15\\J\x07A<0\xe1R"\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd8\xdc\xa0\xda\xe2\x07B@m\xeb9q\xc5\r\x9b@n[\xceqOU\xce@c\x8a\xd3\xf3\xab\xd7\xe8@\xfd\xa5\xf5\xdc\x89\x93\xf7@\x15\xc9\x18:\x93\x89\x01AXE\x98_YJ\x07A\xa0\xc1\x17\x85\x1f\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Pk\x86\n\x95\x9b]@ye\xa8\xf7\x98\xf6\xa3@\xf5m\xb8%\x81\xdb\xd0@\xdbl\x8c\xa1\xef8\xe9@y\xbb\xc1\xecb\x98\xf7@\xa2\x8d\xf2U\x92\x89\x01A\x11~\xb9\x90UJ\x07A\x18:\x9b\x94\x1b\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d6ow\xdb\xb9\x02@\x98\x99\xaa[6@p@\xac\xc4\x80\xa6\xf6{\xab@\x8e\xd7K\x0b|\x8c\xd2@-4\xbd\xf4\x06\xab\xe9@2\xa0B\xa3\r\xa2\xf7@\xa3\xad\xe1\xf6\xa8\x89\x01A\xe6LP\xabPJ\x07A$q\xf9\x83\x16\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\xdb\xdeL\x101*@\xdd\xf9\xa6\x1a\x93p}@\x8e=\xec\xba"\xe4\xb1@\xd1\xfc\xb5l\x84=\xd4@\xa3\x1c\xedu\xf2*\xea@\xf9\xbffQ\xe4\xb0\xf7@\xe8\x9f\x10 \x15\x8a\x01AMf\xbf\xb1JJ\x07AU*\xaaU\x10\x0b\rA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00g\xd4\xd7\xf5\xc7)B@\x94\xef}\xaf\xe3\x10\x88@\x0b\xfd\xf0\x86N]\xb6@\xe1.\x8aQ\x86\xee\xd5@\n\xb4]\xb9\xcd\xb6\xea@\r\xfc\x04\x97\xc2\xc5\xf7@j}\xb0\x96"\x8b\x01A\xd1\xf3\x89LIJ\x07A\x99u\x0f\x0c\t\x0b\rA \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_asian_option(
            payoff_type='CALL',
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            strike_type='FIXED_STRIKE',
            strike=1.176100,
            avg_method='ARITHMETIC_AVERAGE_METHOD',
            obs_type='DISCRETE_OBSERVATION_TYPE',
            fixing_schedule= [
                    [
                        datetime(2021, 3, 31), datetime(2021, 4, 1), datetime(2021, 4, 2), 
                        datetime(2021, 4, 3), datetime(2021, 4, 4), datetime(2021, 4, 5), 
                        datetime(2021, 4, 6), datetime(2021, 4, 7), datetime(2021, 4, 8), 
                        datetime(2021, 4, 9), datetime(2021, 4, 10), datetime(2021, 4, 11), 
                        datetime(2021, 4, 12), datetime(2021, 4, 13), datetime(2021, 4, 14), 
                        datetime(2021, 4, 15), datetime(2021, 4, 16), datetime(2021, 4, 17), 
                        datetime(2021, 4, 18), datetime(2021, 4, 19), datetime(2021, 4, 20), 
                        datetime(2021, 4, 21), datetime(2021, 4, 22), datetime(2021, 4, 23), 
                        datetime(2021, 4, 24), datetime(2021, 4, 25), datetime(2021, 4, 26), 
                        datetime(2021, 4, 27), datetime(2021, 4, 28), datetime(2021, 4, 29), 
                        datetime(2021, 4, 30), datetime(2021, 5, 1), datetime(2021, 5, 2), 
                        datetime(2021, 5, 3), datetime(2021, 5, 4), datetime(2021, 5, 5), 
                        datetime(2021, 5, 6), datetime(2021, 5, 7), datetime(2021, 5, 8), 
                        datetime(2021, 5, 9), datetime(2021, 5, 10), datetime(2021, 5, 11), 
                        datetime(2021, 5, 12), datetime(2021, 5, 13), datetime(2021, 5, 14), 
                        datetime(2021, 5, 15), datetime(2021, 5, 16), datetime(2021, 5, 17), 
                        datetime(2021, 5, 18), datetime(2021, 5, 19), datetime(2021, 5, 20), 
                        datetime(2021, 5, 21), datetime(2021, 5, 22), datetime(2021, 5, 23), 
                        datetime(2021, 5, 24), datetime(2021, 5, 25), datetime(2021, 5, 26), 
                        datetime(2021, 5, 27), datetime(2021, 5, 28), datetime(2021, 5, 29), 
                        datetime(2021, 5, 30), datetime(2021, 5, 31), datetime(2021, 6, 1), 
                        datetime(2021, 6, 2), datetime(2021, 6, 3), datetime(2021, 6, 4), 
                        datetime(2021, 6, 5), datetime(2021, 6, 6), datetime(2021, 6, 7), 
                        datetime(2021, 6, 8), datetime(2021, 6, 9), datetime(2021, 6, 10), 
                        datetime(2021, 6, 11), datetime(2021, 6, 12), datetime(2021, 6, 13), 
                        datetime(2021, 6, 14), datetime(2021, 6, 15), datetime(2021, 6, 16), 
                        datetime(2021, 6, 17), datetime(2021, 6, 18), datetime(2021, 6, 19), 
                        datetime(2021, 6, 20), datetime(2021, 6, 21), datetime(2021, 6, 22), 
                        datetime(2021, 6, 23), datetime(2021, 6, 24), datetime(2021, 6, 25), 
                        datetime(2021, 6, 26), datetime(2021, 6, 27), datetime(2021, 6, 28), 
                        datetime(2021, 6, 29), datetime(2021, 6, 30), datetime(2021, 7, 1), 
                        datetime(2021, 7, 2), datetime(2021, 7, 3), datetime(2021, 7, 4), 
                        datetime(2021, 7, 5), datetime(2021, 7, 6), datetime(2021, 7, 7), 
                        datetime(2021, 7, 8), datetime(2021, 7, 9), datetime(2021, 7, 10), 
                        datetime(2021, 7, 11), datetime(2021, 7, 12), datetime(2021, 7, 13), 
                        datetime(2021, 7, 14), datetime(2021, 7, 15), datetime(2021, 7, 16), 
                        datetime(2021, 7, 17), datetime(2021, 7, 18), datetime(2021, 7, 19), 
                        datetime(2021, 7, 20), datetime(2021, 7, 21), datetime(2021, 7, 22), 
                        datetime(2021, 7, 23), datetime(2021, 7, 24), datetime(2021, 7, 25), 
                        datetime(2021, 7, 26), datetime(2021, 7, 27), datetime(2021, 7, 28), 
                        datetime(2021, 7, 29), datetime(2021, 7, 30), datetime(2021, 7, 31), 
                        datetime(2021, 8, 1), datetime(2021, 8, 2), datetime(2021, 8, 3), 
                        datetime(2021, 8, 4), datetime(2021, 8, 5), datetime(2021, 8, 6), 
                        datetime(2021, 8, 7), datetime(2021, 8, 8), datetime(2021, 8, 9), 
                        datetime(2021, 8, 10), datetime(2021, 8, 11), datetime(2021, 8, 12), 
                        datetime(2021, 8, 13), datetime(2021, 8, 14), datetime(2021, 8, 15), 
                        datetime(2021, 8, 16), datetime(2021, 8, 17), datetime(2021, 8, 18), 
                        datetime(2021, 8, 19), datetime(2021, 8, 20), datetime(2021, 8, 21), 
                        datetime(2021, 8, 22), datetime(2021, 8, 23), datetime(2021, 8, 24), 
                        datetime(2021, 8, 25), datetime(2021, 8, 26), datetime(2021, 8, 27), 
                        datetime(2021, 8, 28), datetime(2021, 8, 29), datetime(2021, 8, 30), 
                        datetime(2021, 8, 31), datetime(2021, 9, 1), datetime(2021, 9, 2), 
                        datetime(2021, 9, 3), datetime(2021, 9, 4), datetime(2021, 9, 5), 
                        datetime(2021, 9, 6), datetime(2021, 9, 7), datetime(2021, 9, 8), 
                        datetime(2021, 9, 9), datetime(2021, 9, 10), datetime(2021, 9, 11), 
                        datetime(2021, 9, 12), datetime(2021, 9, 13), datetime(2021, 9, 14), 
                        datetime(2021, 9, 15), datetime(2021, 9, 16), datetime(2021, 9, 17), 
                        datetime(2021, 9, 18), datetime(2021, 9, 19), datetime(2021, 9, 20), 
                        datetime(2021, 9, 21), datetime(2021, 9, 22), datetime(2021, 9, 23), 
                        datetime(2021, 9, 24), datetime(2021, 9, 25), datetime(2021, 9, 26)
                    ],
                [0] * 180,  # All values are 0
                [1] * 180  # All weights are 1
            ],                
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_asian_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_mc_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_asian_option_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)
    
    def test_fx_digital_option_pricer(self):
        expected = b'\n\xae\x07\t\xb8q"\xcdE\x1f$A\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08+V\x8e\x17\xab\x1abA\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08|d\xf4\xda\x05IU\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\xaa\x946o\xb7\tTA\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x085\xf6f\x18\x11A\xfb@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00x\xe4\xeb\xd6o\x81\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\x94\xc0\x87Cj\x80@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xae\x1b\xb4U9\xc5p\xc1\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x01\xcd\x061\xc4\x00\xa3\xc0\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\xe0ELl_k\xc0\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xf2\xb5\x02G\xf9\xfb\xa0\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xf0\xbd\xbe\x88\x1a]\xd0\xc0\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xcc\xf7\xab\x9f\xe1\x03\x1f\xc1\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xc0\xfa\xbf(\x86\xd9\xb3\xc0\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x94W\xd9\xd2RttA\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\xa8\xe5\xa2\x98\xc1\xa0@\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\x86\x06-b\xd6Lr%\xbc@\xfe\xcb\xea\xa2K0\x16\x04\xa7\xaa\xe4R 8\xedJ\x0bHu\xacP=j\x88\x06cUG3@6\xed+Gl,(A\xba&\x95\xa3\xe8\xbb2A\x92\xffh\xb1^t3A(\xd3Y\xfa\xd3,4A\xbe\xa6JCI\xe54ASz;\x8c\xbe\x9d5A2\xaePQ\x07\xce\x947\xad\x83[\xf1\xc6\x89F;\xb4,\xee\x8b$X\xf3=\xbf\xf3\x0b\xb6O\xc0\xbc?OT}t\xbc\xbc\xc1@\x16\xb5z\xabS\xbf%Aj\x1d?\xe6\xb7\xb02A\x1b\xe3g\x9d^t3A(\xd3Y\xfa\xd3,4A\xbe\xa6JCI\xe54ASz;\x8c\xbe\x9d5A\xeb\xb4\xb4\x95\r,F<I\x8c\xb8\r\xd4\xdd >)\x8b\xfc\x14\xe1(x?Bk<\xe5+Ia@\r\xb7\xbf\xc7|\x03\xe9@\xc7G\xbe\x86>\xbd$A\xdd\x19\x11\xb4\rO2A;\xf4\xd8\xae\xeas3A\x14T\\\xf0\xd3,4A\xce\xa6JCI\xe54ASz;\x8c\xbe\x9d5A\xf9\xec\x18\x9b\xbb\xbc(>\x0cG\x8dWk\xc4E?+"\x14r\xdc\x10\x16@L\xdb\x08\xd7ph\xa4@d\xf1P\xbdY\xad\xfa@\x88}\x13\x9cU4$A\xc0\xbb&\x03 \x9a1A\xcd%"@\xfaj3A\xa8\x93@\xc9\xc1,4A\x87\xddN9I\xe54A\x04\xc2\xe3\x88\xbe\x9d5A\x03\x13\xcd\x9c\xb4\xb5\x1a?\xee\x07\xd4\x1f\xea\xb8\xd9?\x9e\xe2C\x93\xe2&f@\xd7]\xea\xf0#L\xc7@\x9a\xcf\xe5\xd6[(\x04A\xbe\xfd\xcd\xa5\x16\xe2#A\xde\xe9m\x01\n\xd20A`\xd6\xbf\xac\x85G3A\xadk\xa3S8+4A\x93\xe0\xe3!C\xe54A\x17vD\x82\xbe\x9d5A\x81\xc2F\xe5\x92.\xa5?\x13\xdeD|"\x190@\xfe\xcf\xee\x05\xd9\xcd\x94@\xf1\x024h)\xa4\xdc@V\xee\r\xe5=\r\nA@\xba\x81;\x13\xad#A\xec\x99\xe1C\xb2\x180A\x08R\xa2\xd3m\x033A\xb7%\xe8\xbc\xf3"4A\x95\xd6\xfa \xd1\xe44Ab\xe6\xc5H\xbb\x9d5AO\xc4\xe5?L\xd7\xfc?\x1b\xaa\xac\xa2\xca\xb1d@\xb6HS\xd2\x00\xcf\xb2@\x1f\xb2Y/p\xaf\xe9@\xbc\xad\xc1p\xbc\xfe\x0eA\x94\xd4\xe6\xf1\x80\x89#A\xd7\xf2\x138t\xef.A#W\x11+\x0c\xa72A\xc3\xc4\xfe0d\r4A\xa7\xa0\xden4\xe24Ay\xd25]\x8b\x9d5A\xb7\xb8\xea\x12{\xb96@>\x91\xa8\x18v\xf2\x88@\x8c\x16\xd7\xa8k\x94\xc6@\xd7\xc3\x8cr\x8eB\xf3@\x8f\xbaeLI\x90\x11AS\xce\x1b\xec*q#AP\xf0\xecf\x10\xde-A?\xab\xd3\x9b\x16>2A\x0bp\\\xdc\x9d\xe73A\x15y\xbe\x0bH\xda4A\x05\xd4\xd3Uw\x9c5A\x8ex\xf0\xc3_\x00a@7\xa9\xd4\xb1%\x0e\xa3@\x16\xe1\xc7\xd03&\xd5@\xbd6}\xf0\x16\xe1\xf9@|\x17pTIM\x13A\xf4\x0cP\xa5}`#A\x87@\x17u\'\xf7,ABZ>\xcf\xbe\xd11Av\xd8@N\x00\xb33A\xbd\xd9\xd7\xfc\x12\xca4A\x81\xab\x97\xe5\xfd\x985AXYf\x8di\xa3\x7f@\x91\xafR\rg\xbd\xb5@Go\xee\x19s\xe2\xe0@r5y\x0cq/\x00AN\xe7{|i\xc7\x14A\x04S\xd6\x9dDU#A\xc4\xc7~\x1e\xc53,A\xb2\x04\x13U\xceg1A\xf2\\9\x131s3AD\xe5\x963 \xb04A_\xa9\x03\x00?\x915A\x07\xaci\xe0\xf9l\x95@,\x7f\x86\xf0\xfac\xc4@k\xc1\x95v\x034\xe8@\xa7\xb4Xa8G\x03A\xb3\x90\x15\xf81\x0c\x16A+\xces\xf7\x10N#A\x93\xc4\xc8\xfc\xa5\x8d+A/\xd3Q\xffl\x031A=\x84\xce\x1f@,3A\x85Q%\x89\xa7\x8c4A\'\xd1\xe0B\xaf\x835A\'b\xdc\xf5\xfeD\xa7@\'\x87Y\x89\xc7\xae\xd0@\xcc89\xcf\x0f\x15\xf0@iEM\xd7\x80-\x06A\x15\xe8\x99\xd3!&\x17A\x152\x13\xd2\xe9I#A;\x14\x828\x92\xff*A\xd6H\xec\x14\x0f\xa60A8\x89@\x9a\xb3\xe12Atv\xee\xc1\x02a4Ap\x84\x06)\x85o5A \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_digital_option(
            payoff_type='CALL',
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            strike=1.176100,
            cash = 1.0,
            asset= 0.0,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )
        
        result = fx_digital_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_analytical_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_digital_option_pricer:', result.SerializeToString())
        self.assertEqual(result.SerializeToString(), expected)
        
    def test_fx_single_barrier_option_pricer(self):
        expected = b'\n\xae\x07\t\x83V\x15\xda\x8aW\xd1@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xee]\n\x078\x07 A\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\xc2\xe8\x88\xc4\x07\x91\x11\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08m(&Po\x07\x11A\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xa58\x01\xbc\x04!\xb8@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00\xaaD<\xef\xc7<\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\x16,}\x7f\xe6;@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08 \xe4^8Z4hA\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xd9\xe4R|@m\x9b@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00 \xbc\xf8\xa1\x84\x02\xc0\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x9e\xd7Y\x86\xff\x03CA\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x0c\xffb\x7f Rr@\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xb9\x9c\xe3\xa8PU\x1dA\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xdd&\xa6.\xf6\xc5\xb2@\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08v*\xc8\xae\x18\x89N\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\xacA\xf0\xc3\x03y\xc0\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x0805\x8d\x85\xf5"\xaf\x17]\x08\xf0X\xe7\xc7<%\x8a\xe4\'\xbd\x9c\xf2\xa3/\x1d\xb6\xc1\xeb2\x0cI7-\x11\xaa\xe0\x1aG\x82<\x18\x10\xf7y:\xff\x98?\x1c\xa7\x9c\x89@u\xd9@R_\x97\xa8\xcd-\xf8@TL\xd2\x1b\x91\xda\x01A\x07\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rAP\xb7\x95i\xcc\x8a\xc32\x19\xf4\xb8\xf1*]`7\xfd\xf0\xc8(\xdaE\xea:\xc5\xe72\x17tX\x86=\xa6\xb9:3t+R?\xf2\xdf!\xf9\xbf\x80f@S\x93\xc8\x15X\x7f\xe2@\xc1:k\xa9\xcd-\xf8@TL\xd2\x1b\x91\xda\x01A\x07\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rAU\xbc\xb2\xd2\xc5b\xc39y\xc6\xf0b\xfbq\x11<\x9b\x94\xb3\xe44\xbf\xd6=\x84\xba\xbf\x92\x02\xb1&?\x8e\xf6\xb2\xaa\x92\xa5\x10@\xc0\xe6\xca\x1aRx\xa0@=5\x1e\x10m|\xe5@\x14\xb1mI\xd7-\xf8@u\xbc\x1f\x1c\x91\xda\x01A\x89\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rA-WP:\xb3\x0b\x92<\x07\x8eGT\xb6x\xf3=\xca\xablO \x89\x04?6\xc2\xf3\xa7\xad\xa0\xd0?\r\x1e\x14\x8d\xeb\xd1^@\x1d!\x07\xcc\xab\xd7\xb7@\xc1\x86M\xf9\xcda\xe7@\x1fq~\xa2\t/\xf8@>\xba\xd0\xff\x91\xda\x01A\x0e\x08\xb4c;\x9e\x07A\xcf\x90\xdf\xaa\xe5a\rA\x01p\xb5\xd5\xeb\x96\xf8=CcR\x1d\xa9\x08\xe5>\x0cn+\xb7\n\xb3\x9c?\x0e6ES\xb2\'%@"c\x02h0\x18\x86@\x9e\x1f<M\xbe0\xc5@\xbd\xe6\xf3QO\xd4\xe8@\xd3\x7f\x85J,6\xf8@\xce;a`\xae\xda\x01A\xad\xd4{\xbd;\x9e\x07A\x8c\xcc`\xab\xe5a\rA\xf5\xd0\x88\xc5N\x00\xc6>\x80\xa0+\x19g\xb0p?\xe1\xd9Q\x0b\xea\xc5\xf3?VCJ\xef\x01\xc6V@x\x1f\x8e(!\x0e\x9f@H\xa3\x8e\xc3\x9dU\xce@\xb3\xe8zR\xaa\x1b\xea@\x07iE%\xb5I\xf8@\xa5\xb0\xe4\xf7\x83\xdb\x01A\xf9IW\xcdD\x9e\x07A\xfaC\t\xe2\xe5a\rA\xf9@\x86?\x82\xb4F?\xcf\xc4?)I\xbd\xc6?Pb]F\x9e\x03+@\x18j\x1bz\xd5xv@W$\x8e`\xadp\xae@\xb9\xb8PK\x07o\xd3@\x16\x90\xb2\x89cV\xeb@\x85\xc1\xbe\xaa\xc8m\xf8@\xe7\xac\x00\x06r\xde\x01A\r\x83\x0b\xb0\x8b\x9e\x07A\xa4\x1a9\x1a\xeaa\rAF\xfa7\xc7_\xaa\x9d?\xf03\xd8\x89\xc0\xf0\x01@\xd4_\x8d=\xbc\xfcP@\xa4H\xae?\xe3\xb3\x8c@\xc4\x0c\xb1o\xd8a\xb8@\xf1\xfc\xc6|\xe5b\xd7@\x028\x88\xd1\xea\x90\xec@\xc0Uv4\x87\xa3\xf8@\x19\xb0\x8b?"\xe5\x01A\xf4A\xce\t\xa2\x9f\x07A\x8bI\xc4_\tb\rA\xf7\xee\xedg\xf2\xab\xd9?\xb7T\xb7\xba\xdd\xe9*@\xf1\x86\x15^\x93\xcfj@\xe8x\x98\xf8\x857\x9c@y\x1a\xfa\x18\x8eI\xc1@t\x9eG%%\x15\xdb@HTj8\xf2\xcf\xed@`j\x86\xe1 \xea\xf8@,,\xa2\xb7\xf0\xf0\x01A\x93:\xf5\xa0p\xa2\x07A\xf9\x12o\x06\x88b\rA\xe9\x05\x8e9\x9d\x00\x06@\x12d\x8cc\x85\'I@w\x9ej)7s\x7f@\xf6wsGCy\xa7@k6\x14\xc8e\xab\xc6@\xf1\xca\x84h\xcd\x95\xde@\xb1B\xedV\xe6\x14\xef@\x97\x14\xb0\x9c\xe5?\xf9@\x8aH\xb7q\xac\x02\x02A\xd8\xf6\xc1|\xfd\xa7\x07A\xa5\x96\xcd\xc3\xe3c\rA\x83;y\xf0|\x9d\'@\xbe\x19\x04~\xf1&a@\x0e\x1dR\x19\xa2D\x8e@\x04E\x14R\x1bw\xb1@\xc8\x14\xca\xdep3\xcc@$\x99\x14J\xff\xf8\xe0@\xfb\xee\x93\n\xed/\xf0@\xe9qu\xcb\xe8\xa2\xf9@`\x1b\xf1\x19\xa1\x1a\x02A\x16\x04\xc1\x8a0\xb1\x07A\xdd\x0e\xd7\x83\xc4f\rA\xd0\xe0\x85q\xb0UB@\xc6 O\x1bY\xcer@4\xcd]c\xf8e\x99@c\x1c\xe5\x96d\x0c\xb8@e\xda="\x1c\xe7\xd0@:\x08D\xe0\xc4\x99\xe2@\xc5\xb0m\x84-\xd8\xf0@\xecQ$\xbaP\x11\xfa@\x85z\xb0\xaa\xbb8\x02A\x81\xa1\xfb\x8e\xb3\xbe\x07A\xbb\x83\x0b5\xdek\rA \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_single_barrier_option(
            payoff_type='CALL',
            strike=1.176100,
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            barrier_type='UP_IN',
            barrier_value=1.176100*1.05,    
            barrier_obs_type='CONTINUOUS_OBSERVATION_TYPE',
            obs_schedule=[[],[],[]],
            payment_type='PAY_AT_MATURITY',
            cash_rebate=0.0,
            asset_rebate=0.0,
            settlement_days=1,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_single_barrier_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_analytical_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_single_barrier_option_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)

    def test_fx_double_barrier_option_pricer(self):
        expected = b'\n\xae\x07\tn\xc1\x90\xed\xdf{\xd1@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08Qs\xa7(\x90}\x1fA\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08A\xfd\xcb\xb3\xc8\x9b\x11\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\xd6\x9cj\xfa\x0f\x11\x11A\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xc6\x80\xcd\x86\xf8\xb3\xb7@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00f\xbc\xa4\x8d\xd9<\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\xd8\xa4\x98E\xf6;@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xb4\x14l\xf7\x042iA\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08O\x8d\xd5N\xb0\x8c\x9c@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\xc0\xf3\x92B\x1d\x03\xc0\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x93&\xa0M\xe7a=A\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x08\'\xe0\xc4\x0fOl@\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xe1\xcc\xde\xf5X=\x1eA\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x90\xc0\xea_vZ\xb3@\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xba~>t\xff\xa4H\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x80\x8d\xe4\xbfT0t\xc0\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\xd6\xed\x9c\x86\xf7\xfa\xba$\xab\xd9\x8c\x15\xa7%\x9a/\xe0\x8c\xe1]\xbd#u7Y\xde\xfe"\xc9\x99\xb0<\x00&\x82\xf1O\xdcV>0\xf0x\x96:\xff\x98?l\xa7\x9c\x89@u\xd9@R_\x97\xa8\xcd-\xf8@TL\xd2\x1b\x91\xda\x01A\x07\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rATj\xdcP\xf1w\xf66H\xa8\xb6\xec9\x1d\xaf:\xc0\xe9\x1e2\xc8\x1eb=\x8b\xba:\xe8\x9e<4?)\x99\xd9W!\xde\xcc?h\xef/\xf9\xbf\x80f@`\x93\xc8\x15X\x7f\xe2@\xc1:k\xa9\xcd-\xf8@TL\xd2\x1b\x91\xda\x01A\x07\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rA\x8c\x15\x1b\x9eW\xd4\xb7;\x93\t\xc1\x0cG\n\x97=h\xc0&[\xe6"\xf6>\xa2\xd2\xa8|\x8b\'\xe7?\xf8\x8e\'f;\xa3<@@y\x91\x0fUx\xa0@\xb0b\x1e\x10m|\xe5@\x14\xb1mI\xd7-\xf8@u\xbc\x1f\x1c\x91\xda\x01A\x89\xe9Xc;\x9e\x07A\xb3\x85\xdf\xaa\xe5a\rA\x99\x99\xbe\x10\x01\x00\xa6=\x9c#\x16\xc7]o\xc8>~Yq\x1a>e\xa0?\x9d8\xdc\x12\x7f\x8c5@\xf5\xb9\x89\xe0\xd3St@\xd9y\x85[\xbf\xd8\xb7@\xc4o\x81\x02\xcea\xe7@\x1fq~\xa2\t/\xf8@>\xba\xd0\xff\x91\xda\x01A\x0e\x08\xb4c;\x9e\x07A\xcf\x90\xdf\xaa\xe5a\rA\xd4\xb1\xa5S\xee\xa0\xa1>w\x83\x8c\x96SCe?\xe1\xc4]\xe3\x94\xe7\xf7?-\xad"\x01-ca@4\x01\xde\x80u\x97\x94@ \x95\n[/9\xc5@\xbe\x0ct\x03T\xd4\xe8@\xd3\x7f\x85J,6\xf8@\xce;a`\xae\xda\x01A\xad\xd4{\xbd;\x9e\x07A\x8c\xcc`\xab\xe5a\rA!\xaa\t\xeb\x8eN3?\xc2F\xad\x02\':\xc2?U_\x0c\xd6\xc5R.@\xec\x9c\x9fS+*|@U\x7fAh\xd9-\xa8@{\xe4[\xcc\xa2\x7f\xce@\x8a\x8d\xf8%\xf8\x1b\xea@\x07iE%\xb5I\xf8@\xa5\xb0\xe4\xf7\x83\xdb\x01A\xf9IW\xcdD\x9e\x07A\xfaC\t\xe2\xe5a\rA\x18\x85&x\x80>\x91?J#\x16A\xcc{\xfe?SD\x99\xe0\xcf\x97Q@2;a7\x9a\xb3\x8f@K0\xc1\x14\x91\x1b\xb5@\x93\x9d\xf6\x9c\xe4\xa6\xd3@\xf2\x06\xe2\xdf\x12X\xeb@\x85\xc1\xbe\xaa\xc8m\xf8@\xe7\xac\x00\x06r\xde\x01A\r\x83\x0b\xb0\x8b\x9e\x07A\xa4\x1a9\x1a\xeaa\rA\xa3\xb8\x00\x84\x8a\'\xd1?"\xcb\xa9\x91D\x01\'@\x94DH \t\x1bj@\xa5b2=0\xcd\x9c@\x96\x06N\xe2\xe5(\xbf@\xbe\x99\rF3\xc9\xd7@\xf7\xd93\xe2\xd0\x95\xec@\xc0Uv4\x87\xa3\xf8@\x19\xb0\x8b?"\xe5\x01A\xf4A\xce\t\xa2\x9f\x07A\x8bI\xc4_\tb\rA\xef\xf4\xd8\xb7>u\xff?\xf5\x86\xee\xad\x17\\E@\\\xd4\xc2\xce\xb3]}@\xde\x93\xc8\xdb]\xd4\xa6@}>\x19\xbcS\xd0\xc4@f\x7f\xda\x04@\xa9\xdb@n \xb2\x1bw\xd9\xed@`j\x86\xe1 \xea\xf8@,,\xa2\xb7\xf0\xf0\x01A\x93:\xf5\xa0p\xa2\x07A\xf9\x12o\x06\x88b\rAG\x8c\x8f\xa3\'\x84!@.\x7f\xfa+\xc1\xef\\@ED\xad\x0f\x0e\x87\x8b@k\x8d\xe3\xb4O\x80\xb0@\x9br\xd3\x0c\xee\x1d\xca@e{\xceXFM\xdf@C~\x80\n##\xef@\x97\x14\xb0\x9c\xe5?\xf9@\x8aH\xb7q\xac\x02\x02A\xd8\xf6\xc1|\xfd\xa7\x07A\xa5\x96\xcd\xc3\xe3c\rA\x96\xd2\xeb\xd0+\xda;@\xadm\xbf\x8bd\x9fo@\xd84i\x8a\xe7\xbf\x96@Q\x8c\xa5\r@X\xb6@\x95\x7f\xdbA\x8cp\xcf@\xe6=R\x80\x05_\xe1@2G\x98S\xdc8\xf0@\xe9qu\xcb\xe8\xa2\xf9@`\x1b\xf1\x19\xa1\x1a\x02A\x16\x04\xc1\x8a0\xb1\x07A\xdd\x0e\xd7\x83\xc4f\rA\xe0\r\xfbO\x98yQ@\x91<=\x8d\xa4\xad}@\x9fx*&\x82,\xa1@\xb8\xa4<{5\xd6\xbc@\xe2e\x9d\x80\x93b\xd2@X-\x12K\xd4\x02\xe3@\x88\xf8\x11\r\x1f\xe2\xf0@\xecQ$\xbaP\x11\xfa@\x85z\xb0\xaa\xbb8\x02A\x81\xa1\xfb\x8e\xb3\xbe\x07A\xbb\x83\x0b5\xdek\rA \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_double_barrier_option(
            payoff_type='CALL',
            strike=1.176100,
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            lower_barrier_type='DOWN_IN',
            lower_barrier_value=1.176100*0.95,    
            upper_barrier_type='UP_IN',
            upper_barrier_value=1.176100*1.05,    
            barrier_obs_type='CONTINUOUS_OBSERVATION_TYPE',
            obs_schedule=[[],[],[]],
            payment_type='PAY_AT_MATURITY',
            lower_cash_rebate=0.0,
            lower_asset_rebate=0.0,
            upper_cash_rebate=0.0,
            upper_asset_rebate=0.0,
            settlement_days=1,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_double_barrier_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_analytical_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_double_barrier_option_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)

    def test_fx_one_touch_option_pricer(self):
        expected = b'\n\xae\x07\t\x05f)\x85\x8d\x8f\x11A\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\'|"\xd7w\x9f_A\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\xd14\xc9\x0e\x8d\x7fJ\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08.\x0cXb\xe3hIA\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x84t\xf2\xc1}\xcd\xf7@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00\xc2\x90\xc1\x15\xb5u\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\x1c\x14\xef\xcd\xd0t@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x087r\x16y\xb9u\xa6A\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08 \x16/y*s\xd9@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\xc0Df\x9d\xa6A\xc0\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xd2\x17_Yd\xbepA\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xe0.\x82\xa3\xc5!\xa0@\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x0f\x97\xee5\xf3\xe7[A\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xf5A[\xc6 \xdc\xf1@\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xc0\x15\xfc\xf8\x84\xc6\x98\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xc0\xdb\xc3\xba\xcaK\xc4\xc0\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\x842\xf8\xd7*\x8b\xf0\x176\x12X<\xd7\x94~%\xba\x1d\x14\xbfA1\xe5/\xddv\xfd\xbf(\x9a\x8a7\x0c\xcd\x95\xccse\xc3<\x10\xd7{]Eq\xda?\xdc`\x11\x99\x01\x15\x1aA\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A<\xa1\xa9\xeep\xc2\x043+.xK\ra\xa17^\xb7\x0e\x8c\x05\xe4+;\xc9\x90\x11ki\xb3\xc7=\x9e\xbep\x92\x13;\x93?:\x96\xce\x1f5\xa6\xa7@\x7f\x86t\x8e\x08\xb5"A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\xcd\xde\xd7MK\x95\x04:US\x8a\x82\x9a\x83R<\x93\x1d\xd6;\xea\x1e\x18>/\xd5\x8b\x7f\xfd\x05h?be\x07UC\x8fQ@\xda+Eo\x9c1\xe1@\x99\xa0\xb6`\xd0\x91%A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\x98vm"\xdb%\xd3<`\xa8&\xc96\xa54>\xff(\x8dR\xe9\xbeE?]\xc6\x17\xb6\xa5\x90\x11@\xee\xde\xbb^\xf61\xa0@h\x0b\xd3\xb4\xbb\xbb\xf8@L\xe7H\xde<L\'A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\xfc\x7f\x9a\x8d0\x12:>7\x9a\x13\xe8\x03G&?\xd1\x8e\xdb\xba\x84W\xde?5\xceg\x01\xeeJf@,&\x02fF \xc7@O\xfc\x94\xe7\xca\xd2\x05A\'\xf3\xc3\x98\xc5t(A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\x07\x1f\xedRJN\x07?\xc3\xcc\xa0SM\xa7\xb1?\xe4\xc20\xa6\xa4\xdd4@\xc4GX%\x18\xed\x97@\xceiH\x02T*\xe0@9\x1b\xa9\xf60\xec\x0eA\xec\xdb7\xc0\x87I)A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.AVTL2\xa9\x06\x88?n\x00_\x8d\x16\x04\x08@\xd2nfy\x8aol@\xaef\x03"\x9b\x81\xb7@\xcd\x94\xcb\x9b\x7fo\xef@\xaf\t\xed\xad\xbe\x86\x13A\x91\xa7\xb5 \xb0\xe9)A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.AV&\xb3|\xc0X\xdf?\xa7Z\xcaO\x88\xe7B@@v}S\xde\xcf\x91@\xae\xd8\xcd\xd7\x0e\xd2\xcd@\x0c\xab\x8d\x8f\xc3\xe2\xf8@\xfb\x8b8kd\x0f\x17A7\xdb\xcd\x8d\xa2f*A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A8/f\xdd\r\x11\x1b@\x9b\xbf!+\xb7Al@\xdc\xdf\xceOS\xf1\xab@+r\x19\x9et\x06\xdd@\xa8g\x13b\xb3^\x01AY\x1f\x81P{\x1b\x1aA!\xbc\xce\xa0\xd8\xca*A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.AGE\xd4\xd5\xb3\x1dG@\xbf\x7f\xd7\xaa\xe5B\x8a@\xf4\xb9\x07\x13\x9e>\xc0@\xd3\xd8\xf0\x81\xe2\xd2\xe7@f\xe6\xfav5W\x06A~u\xd9Mn\xbc\x1cAz*-\x02\x03\x1d+A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\xb2M\x93\x1fb\xadh@\xa9\'\xe4\xd8&\xc3\xa1@]J\xc9Q\xf0\xe5\xce@\xd8~\xfbE\nn\xf1@1\x97\xe9\x18\xf9+\x0bA>\t\x9f\x03_\x03\x1fA8\x1d\x1c5\x9ba+A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\xe5\x82\xbaf\xa5\x03\x83@\xcb\xb2\xe2\x86\xf8C\xb3@\t>_w\xce\x8a\xd9@T\x8f\x8b\x9a\xe4\x86\xf7@\xea2\xcf\xc6g\xc3\x0fA\xfc\xe3\t\x06\x9f\x7f A\x94\xad \x9a\xbc\x9b+A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_one_touch_option(
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            barrier_type='UP_IN',
            barrier_value=1.176100*1.05,     
            barrier_obs_type='CONTINUOUS_OBSERVATION_TYPE',
            obs_schedule=[[],[],[]],
            payment_type='PAY_AT_MATURITY',
            cash=1.0,
            asset=0.0,
            settlement_days=1,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_one_touch_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_analytical_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_one_touch_option_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)

    def test_fx_double_touch_option_pricer(self):
        expected = b'\n\xae\x07\t\xd6\xc6\xb2&\xd6x\x1fA\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08Z\x16\x95 \xd1\xb6\x18A\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\xe4\x92\xf9\xfaF\xfa+\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08(\xbf\x11\xa4,"$A\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x01\x85\x82k8\x9a\xb2@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00H\xd6hV\xebV\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00P\xeb\xb5L~P@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xdc\xad\x85\xc9\xc5\x05\xb8A\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08@\xec\xd7\x97x8\xeb@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\x00]\x91{\xcdQ\xc0\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xf5\xfa\xf8\x9d\x87d\x83\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08@t@\xa3!\xaf\xb2\xc0\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x085<\x96\xa8\xfd\xe3kA\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08"\xc0\xf9\x19\x98\xd9\x01A\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xd1S\xd4b\xfe\x90\xa7\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xe0\x80\xbdz:N\xd3\xc0\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\x83\xb0\xdcy-$\xe3\xc0\x06\xd2\xb0^\x7f\'\xc7@O\n\xed3_\xcc\x1aA\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\xd7\xeb_\x10OS\x19A"\xd3\xea5\xb7X\xbc@\xb1\x0c\x9a\x81\xd1\xd3"A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\xdc\x166\x9b\xe8\xb9!A_^\x81\xf9B\xe5\xe8@\x8f\xaf\x9b\xfdp\xb0%A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.AoC\xfd\x92\xae\xc8$Am\x83\xc2@\xcb[\x03A\xc6\x04a\xc6\xc3p\'A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.AE\xf6\x94m\x0b\xf6&A\x7f\xfe\xcb\x87\x94V\x12A\x06\xca\x04\x88]\xbe(A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A#25J\xe6\xbe(A0\x16_\xd8i@\x1bA\xbd\xf0\xdfk\xd5\xe7)A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\x95\xeb<JV@*A\x1b\xae\xa3\x85\xd1\xb7!A\xc9\xd0LE\xa2\xfb*A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\x9d\x81\x05T\x06|+A}\xbf^G\xaf7%AI\x1fk\x14r\xef+A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\x05\xbd\xccL\xb5s,A\x15\xd5\xe6\xb7o\n(A\xfb@>^\x80\xb9,A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\x98\xe97P\x8c--A\xa1\xfe\xd3\x18/3*AMw\xf1[\xf5V-A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\xd9\xe6^\x00\xde\xb2-A\xb0T\xe9\x99\x04\xc5+A\xa3&[P\xeb\xca-A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\x9f\xb2%EO\x0e.A\x82^\xd26=\xdb,A\x82\xaaQ\xd6\xf1\x1b.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A\'\xe8m=l\x83.A \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_double_touch_option( 
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            lower_barrier_type='DOWN_IN',
            lower_barrier_value=1.176100*0.95,      
            upper_barrier_type='UP_IN',
            upper_barrier_value=1.176100*1.05,       
            barrier_obs_type='CONTINUOUS_OBSERVATION_TYPE',
            obs_schedule=[[],[],[]],
            payment_type='PAY_AT_MATURITY',
            cash=1.0,
            asset=0.0,
            settlement_days=1,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_double_touch_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_analytical_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_double_touch_option_pricer:', result.SerializeToString())

        self.assertEqual(result.SerializeToString(), expected)
    
    def test_fx_single_shark_fin_option_pricer(self):
        expected = b'\n\xae\x07\t(Z >\x07\xb0\xb3@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xc4V\x96\xc4\xf6o\xc8@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08V\xb1\x92n\xee\x8b\xdd\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\xb0\xc4\xaf\xd4\x9f\x1e\xdb@\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x10\xb2\xb4\x9a\xe3db@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00l\x8ba_4\x08\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00`\x0f\xdae7\x06@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xdfg.\x920?I\xc1\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08q\xd1F\xc3\x9c\x9b|\xc0\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\xf2\x88n\n\x1f7@\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xd9\xfd\x83\xcb\x9b{E\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08HC\x9c\xb6\xa8\xb2t\xc0\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xb9\x9f_\x89\xedm\xff\xc0\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08/\x8f\xcc\xd2d\x1d\x94\xc0\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08v\xc1\xec\xa1]FFA\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08@P/\xc6`?r@\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00f8l\xe7w\xbf\xa0?0>\x8e\xe5o\xc6\xb6@\\l\x1e\x8eK0\xd6@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xa6\xac\xf6M\xfbgC@L\xd5\xc0&+\xae\xbf@7]\x84\xfaZ.\xc9@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf4z\x1b p\x03\xe4?\xea|b\x8a_\xd4w@6\xf2/`\x8f\xc8\xc1@AP(:\xa0e\xbe@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xde\x1e,+@\x9d?q\xfa\xd0_\xa5@2@y\xb1\x8b\x1anp\x91@\x91\xe1A\x1b\x12n\xc0@g\xb3\xa5\xd6!0\xb3@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00IGI\xb3\xcd\xe9F?\x02|\x9c\xdb_\xc2\xf4?ul2\xd2\x07\xa5[@\xf1\xab\xca\xce;\xb4\x9d@\xe4\xe78b\x88{\xbb@\x86K\n\'3D\xa9@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00n|_\x1b\x9a%\xc0?\xe4S\x8e\xa0\xae@(@mKAG\x9f\xa0s@\xd4\x8a\x11\xd3Z\xee\xa2@lO\x8a.\xe3\x0f\xb6@_\xfb\xb3\x98\x96z\xa1@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe0\xb7a`\x95\x91\x8e?\x07\xe4\xbf.\xa7\x9a\xf8?\xf1D\xf5\xdf\x0b\xfaH@qm^\xd5\x99=\x82@\x96\x0c|\x02\xf6\x7f\xa4@\x95:\x17\xb7L\x85\xb1@\xbe\xe1\x8a:]!\x99@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x92\x86E\x86\x19\x89\xce?\xe6\xb6\xc013| @?\x0fw\x949s_@\xf7\x90\x05}\xef`\x8a@\x16\x95_(\x99Q\xa4@\x95\xe1\x0c\x8b\x18\xdb\xab@\xa7\xd8\x9d\xfb\xdf\xd2\x92@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe8\xb1\x13L\xe8\xc4\xf6?X\x05\x1c\x02\xcdT:@\xe6\x08\x8f\xb3\xe2!m@\xa5\x9f\x18\x84}L\x90@\x93\x9f\x84eK\x19\xa3@\x9b98\nqL\xa6@\xf7\xc1A\xc8\x9b\x04\x8d@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0023\x93\xb9,\xf3\x15@\xbf|\x81L\xce\xf7M@\xb6\x81\xe0\xb3,\x08v@K\xf9\x1f\x9d\x02A\x92@R\xd6.\x93\xb0h\xa1@w\xf4\xdb\x07\xa3\x01\xa2@+(\x8dj|\xbd\x86@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x005Q\xca`\xa4\xa4-@\x85B\\\x8c\xee\x0f[@"\xaew\xdf\xd1\x0e}@\xc5$\xecx\xc9$\x93@\x97\x80<Z\xff/\x9f@\xa85\x9b1\xd2\x8d\x9d@\x14:\xf0\x02}V\x82@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x89S\x00\xa1\rB?@(\x12\x1b\xc6\x84\xc2d@=\xc1\xe2\x1a\xb9x\x81@\x14\x98\x00\x08\x057\x93@\xde/\x1cAu\xac\x9b@\r\xc2\xac\xa5 l\x98@_@\xdeTl\x1c~@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_single_shark_fin_option(
            payoff_type='CALL',
            strike=1.176100,
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            gearing = 1.0,
            performance_type='RELATIVE_PERFORM_TYPE',
            barrier_type='UP_OUT',
            barrier_value=1.176100*1.05,        
            barrier_obs_type='DISCRETE_OBSERVATION_TYPE',
            obs_schedule=[
                    [
                        datetime(2021, 3, 31), datetime(2021, 4, 1), datetime(2021, 4, 2), 
                        datetime(2021, 4, 3), datetime(2021, 4, 4), datetime(2021, 4, 5), 
                        datetime(2021, 4, 6), datetime(2021, 4, 7), datetime(2021, 4, 8), 
                        datetime(2021, 4, 9), datetime(2021, 4, 10), datetime(2021, 4, 11), 
                        datetime(2021, 4, 12), datetime(2021, 4, 13), datetime(2021, 4, 14), 
                        datetime(2021, 4, 15), datetime(2021, 4, 16), datetime(2021, 4, 17), 
                        datetime(2021, 4, 18), datetime(2021, 4, 19), datetime(2021, 4, 20), 
                        datetime(2021, 4, 21), datetime(2021, 4, 22), datetime(2021, 4, 23), 
                        datetime(2021, 4, 24), datetime(2021, 4, 25), datetime(2021, 4, 26), 
                        datetime(2021, 4, 27), datetime(2021, 4, 28), datetime(2021, 4, 29), 
                        datetime(2021, 4, 30), datetime(2021, 5, 1), datetime(2021, 5, 2), 
                        datetime(2021, 5, 3), datetime(2021, 5, 4), datetime(2021, 5, 5), 
                        datetime(2021, 5, 6), datetime(2021, 5, 7), datetime(2021, 5, 8), 
                        datetime(2021, 5, 9), datetime(2021, 5, 10), datetime(2021, 5, 11), 
                        datetime(2021, 5, 12), datetime(2021, 5, 13), datetime(2021, 5, 14), 
                        datetime(2021, 5, 15), datetime(2021, 5, 16), datetime(2021, 5, 17), 
                        datetime(2021, 5, 18), datetime(2021, 5, 19), datetime(2021, 5, 20), 
                        datetime(2021, 5, 21), datetime(2021, 5, 22), datetime(2021, 5, 23), 
                        datetime(2021, 5, 24), datetime(2021, 5, 25), datetime(2021, 5, 26), 
                        datetime(2021, 5, 27), datetime(2021, 5, 28), datetime(2021, 5, 29), 
                        datetime(2021, 5, 30), datetime(2021, 5, 31), datetime(2021, 6, 1), 
                        datetime(2021, 6, 2), datetime(2021, 6, 3), datetime(2021, 6, 4), 
                        datetime(2021, 6, 5), datetime(2021, 6, 6), datetime(2021, 6, 7), 
                        datetime(2021, 6, 8), datetime(2021, 6, 9), datetime(2021, 6, 10), 
                        datetime(2021, 6, 11), datetime(2021, 6, 12), datetime(2021, 6, 13), 
                        datetime(2021, 6, 14), datetime(2021, 6, 15), datetime(2021, 6, 16), 
                        datetime(2021, 6, 17), datetime(2021, 6, 18), datetime(2021, 6, 19), 
                        datetime(2021, 6, 20), datetime(2021, 6, 21), datetime(2021, 6, 22), 
                        datetime(2021, 6, 23), datetime(2021, 6, 24), datetime(2021, 6, 25), 
                        datetime(2021, 6, 26), datetime(2021, 6, 27), datetime(2021, 6, 28), 
                        datetime(2021, 6, 29), datetime(2021, 6, 30), datetime(2021, 7, 1), 
                        datetime(2021, 7, 2), datetime(2021, 7, 3), datetime(2021, 7, 4), 
                        datetime(2021, 7, 5), datetime(2021, 7, 6), datetime(2021, 7, 7), 
                        datetime(2021, 7, 8), datetime(2021, 7, 9), datetime(2021, 7, 10), 
                        datetime(2021, 7, 11), datetime(2021, 7, 12), datetime(2021, 7, 13), 
                        datetime(2021, 7, 14), datetime(2021, 7, 15), datetime(2021, 7, 16), 
                        datetime(2021, 7, 17), datetime(2021, 7, 18), datetime(2021, 7, 19), 
                        datetime(2021, 7, 20), datetime(2021, 7, 21), datetime(2021, 7, 22), 
                        datetime(2021, 7, 23), datetime(2021, 7, 24), datetime(2021, 7, 25), 
                        datetime(2021, 7, 26), datetime(2021, 7, 27), datetime(2021, 7, 28), 
                        datetime(2021, 7, 29), datetime(2021, 7, 30), datetime(2021, 7, 31), 
                        datetime(2021, 8, 1), datetime(2021, 8, 2), datetime(2021, 8, 3), 
                        datetime(2021, 8, 4), datetime(2021, 8, 5), datetime(2021, 8, 6), 
                        datetime(2021, 8, 7), datetime(2021, 8, 8), datetime(2021, 8, 9), 
                        datetime(2021, 8, 10), datetime(2021, 8, 11), datetime(2021, 8, 12), 
                        datetime(2021, 8, 13), datetime(2021, 8, 14), datetime(2021, 8, 15), 
                        datetime(2021, 8, 16), datetime(2021, 8, 17), datetime(2021, 8, 18), 
                        datetime(2021, 8, 19), datetime(2021, 8, 20), datetime(2021, 8, 21), 
                        datetime(2021, 8, 22), datetime(2021, 8, 23), datetime(2021, 8, 24), 
                        datetime(2021, 8, 25), datetime(2021, 8, 26), datetime(2021, 8, 27), 
                        datetime(2021, 8, 28), datetime(2021, 8, 29), datetime(2021, 8, 30), 
                        datetime(2021, 8, 31), datetime(2021, 9, 1), datetime(2021, 9, 2), 
                        datetime(2021, 9, 3), datetime(2021, 9, 4), datetime(2021, 9, 5), 
                        datetime(2021, 9, 6), datetime(2021, 9, 7), datetime(2021, 9, 8), 
                        datetime(2021, 9, 9), datetime(2021, 9, 10), datetime(2021, 9, 11), 
                        datetime(2021, 9, 12), datetime(2021, 9, 13), datetime(2021, 9, 14), 
                        datetime(2021, 9, 15), datetime(2021, 9, 16), datetime(2021, 9, 17), 
                        datetime(2021, 9, 18), datetime(2021, 9, 19), datetime(2021, 9, 20), 
                        datetime(2021, 9, 21), datetime(2021, 9, 22), datetime(2021, 9, 23), 
                        datetime(2021, 9, 24), datetime(2021, 9, 25), datetime(2021, 9, 26)
                    ],
                [0] * 180,  # All values are 0
                [1] * 180  # All weights are 1
            ],
            payment_type='PAY_AT_MATURITY',
            cash_rebate=0.0,
            asset_rebate=0.0,
            settlement_days=1,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_single_shark_fin_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_pde_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_single_shark_fin_option_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)

    def test_fx_double_shark_fin_option_pricer(self):
        expected = b'\n\xae\x07\tzs\x10e\x94\xcf\xc6@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08m\xabe4=g\xc5\xc0\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\xa8\xc8\xa7\xa20\xb5\xc3@\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\xc0\x19\x14\x8ao\xf4\xce\xc0\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08 6\xa9\xc3>\x1c`\xc0\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00P\xae\x06\x05%\xf0?\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\x80+\x9e\xb2[\xf9\xbf\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\rI5\xcd*\xe8`\xc1\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08)\xea\xc1\x89\\(\x93\xc0\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00=\xf1\x07I;M@\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x17s0\x0b4\xfd)A\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xe0\x8fyJ\x1a\nY@\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x91\x9a"Q\xc09\x12\xc1\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xce\xee\x9c])T\xa7\xc0\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xbc\\x\x99YyDA\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x80\xd1Z\xc3\xb6\xc5p@\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x81e\xadwwv\xe1@\xbau\x03\x9fd\xdd\xc1@\x00\x057\xcd\x90\x1c\xda@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00u\x1b?=F\x8a\xd4@&\xa9\x90lN\x9c\xcc@\xde\x06\xdc\xe8\x04\x80\xcd@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x10\xb8\x99~\xbe\xc8@\xad\xbe\xcc\xb8\x99\xbb\xd1@F%\xc6\xbb\xbaJ\xc2@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x003\xbc\xc0\x0e\x08\xda\xc0@\xc7FS\xdea\xac\xd1@$.\x0b\x98:J\xb9@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00=V\xb8\xd1\x1d\x9d\xb9@e\x9f\xa4\x13\xfc\x0f\xcf@\x86d\xd3\xd8\x92\xd4\xb3@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd1\x97J\xd0,J\xb4@\x15\xdc\xb6\x8f\xc4\x86\xc9@#\xf3\xfe\xdbwg\xb0@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\x17\x16\xbc\xd2\x8c\xaf@~`\xf4\x18_*\xc4@\xc4\xb6uG\x15\x99\xaa@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000\xf7rHv$\xa8@\x81\x1c\xbf:\xa0\xde\xbe@+\x05.\xd0\xfb\xe6\xa4@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\xebB\x0f\x94\xfa\xa1@\x15\x81\xc7\xd6\x94\xd4\xb6@\x12w\xef\xcd"\x07\xa0@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05guX*I\x9a@Q\x9b\x11{ei\xb0@\xa7<\xb4\xe25\xb9\x97@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\xfc \xdd9\x8a\x92@H\xe8\x91\xab~\x05\xa7@\x189f\xe6<\xeb\x90@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x006\xc5\xe7\x90>v\x89@0\xa38G\x94\x9c\x9f@$\x80\x05/1\xa7\x87@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_double_shark_fin_option(
            lower_strike=1.176100*1.0,    
            upper_strike=1.176100*1.0,   
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            lower_participation = 1.0,
            upper_participation = 1.0,
            performance_type='ABSOLUTE_PERFORM_TYPE',
            lower_barrier=1.176100*0.95,    
            upper_barrier=1.176100*1.05,                  
            barrier_obs_type='DISCRETE_OBSERVATION_TYPE',
            obs_schedule=[
                   [
                        datetime(2021, 3, 31), datetime(2021, 4, 1), datetime(2021, 4, 2), 
                        datetime(2021, 4, 3), datetime(2021, 4, 4), datetime(2021, 4, 5), 
                        datetime(2021, 4, 6), datetime(2021, 4, 7), datetime(2021, 4, 8), 
                        datetime(2021, 4, 9), datetime(2021, 4, 10), datetime(2021, 4, 11), 
                        datetime(2021, 4, 12), datetime(2021, 4, 13), datetime(2021, 4, 14), 
                        datetime(2021, 4, 15), datetime(2021, 4, 16), datetime(2021, 4, 17), 
                        datetime(2021, 4, 18), datetime(2021, 4, 19), datetime(2021, 4, 20), 
                        datetime(2021, 4, 21), datetime(2021, 4, 22), datetime(2021, 4, 23), 
                        datetime(2021, 4, 24), datetime(2021, 4, 25), datetime(2021, 4, 26), 
                        datetime(2021, 4, 27), datetime(2021, 4, 28), datetime(2021, 4, 29), 
                        datetime(2021, 4, 30), datetime(2021, 5, 1), datetime(2021, 5, 2), 
                        datetime(2021, 5, 3), datetime(2021, 5, 4), datetime(2021, 5, 5), 
                        datetime(2021, 5, 6), datetime(2021, 5, 7), datetime(2021, 5, 8), 
                        datetime(2021, 5, 9), datetime(2021, 5, 10), datetime(2021, 5, 11), 
                        datetime(2021, 5, 12), datetime(2021, 5, 13), datetime(2021, 5, 14), 
                        datetime(2021, 5, 15), datetime(2021, 5, 16), datetime(2021, 5, 17), 
                        datetime(2021, 5, 18), datetime(2021, 5, 19), datetime(2021, 5, 20), 
                        datetime(2021, 5, 21), datetime(2021, 5, 22), datetime(2021, 5, 23), 
                        datetime(2021, 5, 24), datetime(2021, 5, 25), datetime(2021, 5, 26), 
                        datetime(2021, 5, 27), datetime(2021, 5, 28), datetime(2021, 5, 29), 
                        datetime(2021, 5, 30), datetime(2021, 5, 31), datetime(2021, 6, 1), 
                        datetime(2021, 6, 2), datetime(2021, 6, 3), datetime(2021, 6, 4), 
                        datetime(2021, 6, 5), datetime(2021, 6, 6), datetime(2021, 6, 7), 
                        datetime(2021, 6, 8), datetime(2021, 6, 9), datetime(2021, 6, 10), 
                        datetime(2021, 6, 11), datetime(2021, 6, 12), datetime(2021, 6, 13), 
                        datetime(2021, 6, 14), datetime(2021, 6, 15), datetime(2021, 6, 16), 
                        datetime(2021, 6, 17), datetime(2021, 6, 18), datetime(2021, 6, 19), 
                        datetime(2021, 6, 20), datetime(2021, 6, 21), datetime(2021, 6, 22), 
                        datetime(2021, 6, 23), datetime(2021, 6, 24), datetime(2021, 6, 25), 
                        datetime(2021, 6, 26), datetime(2021, 6, 27), datetime(2021, 6, 28), 
                        datetime(2021, 6, 29), datetime(2021, 6, 30), datetime(2021, 7, 1), 
                        datetime(2021, 7, 2), datetime(2021, 7, 3), datetime(2021, 7, 4), 
                        datetime(2021, 7, 5), datetime(2021, 7, 6), datetime(2021, 7, 7), 
                        datetime(2021, 7, 8), datetime(2021, 7, 9), datetime(2021, 7, 10), 
                        datetime(2021, 7, 11), datetime(2021, 7, 12), datetime(2021, 7, 13), 
                        datetime(2021, 7, 14), datetime(2021, 7, 15), datetime(2021, 7, 16), 
                        datetime(2021, 7, 17), datetime(2021, 7, 18), datetime(2021, 7, 19), 
                        datetime(2021, 7, 20), datetime(2021, 7, 21), datetime(2021, 7, 22), 
                        datetime(2021, 7, 23), datetime(2021, 7, 24), datetime(2021, 7, 25), 
                        datetime(2021, 7, 26), datetime(2021, 7, 27), datetime(2021, 7, 28), 
                        datetime(2021, 7, 29), datetime(2021, 7, 30), datetime(2021, 7, 31), 
                        datetime(2021, 8, 1), datetime(2021, 8, 2), datetime(2021, 8, 3), 
                        datetime(2021, 8, 4), datetime(2021, 8, 5), datetime(2021, 8, 6), 
                        datetime(2021, 8, 7), datetime(2021, 8, 8), datetime(2021, 8, 9), 
                        datetime(2021, 8, 10), datetime(2021, 8, 11), datetime(2021, 8, 12), 
                        datetime(2021, 8, 13), datetime(2021, 8, 14), datetime(2021, 8, 15), 
                        datetime(2021, 8, 16), datetime(2021, 8, 17), datetime(2021, 8, 18), 
                        datetime(2021, 8, 19), datetime(2021, 8, 20), datetime(2021, 8, 21), 
                        datetime(2021, 8, 22), datetime(2021, 8, 23), datetime(2021, 8, 24), 
                        datetime(2021, 8, 25), datetime(2021, 8, 26), datetime(2021, 8, 27), 
                        datetime(2021, 8, 28), datetime(2021, 8, 29), datetime(2021, 8, 30), 
                        datetime(2021, 8, 31), datetime(2021, 9, 1), datetime(2021, 9, 2), 
                        datetime(2021, 9, 3), datetime(2021, 9, 4), datetime(2021, 9, 5), 
                        datetime(2021, 9, 6), datetime(2021, 9, 7), datetime(2021, 9, 8), 
                        datetime(2021, 9, 9), datetime(2021, 9, 10), datetime(2021, 9, 11), 
                        datetime(2021, 9, 12), datetime(2021, 9, 13), datetime(2021, 9, 14), 
                        datetime(2021, 9, 15), datetime(2021, 9, 16), datetime(2021, 9, 17), 
                        datetime(2021, 9, 18), datetime(2021, 9, 19), datetime(2021, 9, 20), 
                        datetime(2021, 9, 21), datetime(2021, 9, 22), datetime(2021, 9, 23), 
                        datetime(2021, 9, 24), datetime(2021, 9, 25), datetime(2021, 9, 26)
                    ],
                [0] * 180,  # All values are 0
                [1] * 180  # All weights are 1
            ],
            payment_type='PAY_AT_MATURITY',
            lower_cash_rebate=0.0,
            lower_asset_rebate=0.0,
            upper_cash_rebate=0.0,
            upper_asset_rebate=0.0,
            settlement_days=1,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_double_shark_fin_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_pde_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_double_shark_fin_option_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)

    def test_fx_range_accrual_option_pricer(self):
        expected = b'\n\xae\x07\t\xb9\x1fN3\xb4I\xc1@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08-m\x03\xea\x00\xe5\xb0\xc0\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08@0\x1f$_J\x9b@\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08`D<\xb0\xeb\xf7\xb7\xc0\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x00y\x1c\x1d\xe5nI\xc0\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00\x80\xa8S<[\xc6?\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\xc0\xf4\xd3\x8b\xa2\xe3\xbf\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x7f7\xac\x06\xab\x12;\xc1\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08~)\xed\x12S\xadn\xc0\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\x00\x0c\x03?5\xd3\xbf\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08mLp\xb8\x18m\xd6@\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\x1c|\xc5R\x9b\x05@\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xc5\x03\\j\x0e\xb5\xe3\xc0\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x080\x94B\r\xac9y\xc0\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x9c\x1am\x0c\xf2\xaa\xf4\xc0\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\xb8\xb4\xb1W\xee \xc0\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08y,G\xe3m\x1e\xea/eW^\xf7\x9ci\xf67\xb7\x0b]\xfc\xddp(=\xbe\x9dp\xbe\xba\x02\xec?\xc5O\x89\xf2s\x0c\xc3@B\xad\r\x7fO\x87\xc3@\x8a\x81k\xf6\xe9L\xc1@_?\t\x9cA*\xce?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe4\x91\xac\x0b\x06\xc7\xa5:\xc2x\xd5\xc5$Tp=\xe2p\xe1\xcc\xec\xe4E?\xd3=\x8c]\x8c\x1bS@y\\\xf7\x06|a\xc1@\x0e\xc7\xf7\xae\x15\x86\xc3@-\xf2l\xbc\xd5\xca\xbe@\xbcg\xd4\xbasWJ@\x1f\x10\xd1\xe2z\xf6m?\xa1\xf7\xfe|\xc5\xc1\xc0\xbe\x00\x00\x00\x00\x00\x00\x00\x00~\x94\xad;\x00\x82w=\x9e\x18J7\xce*\xe5>-\xcf\xa7P_\x99\xdd? D\xca+\xfbZt@^\xfe\x14\xaa\xdd\xdb\xbf@v\x01\xf3h\xc7l\xc3@\x9eby\xce~r\xbc@\x94#`\x93\x0f\xbcq@\xfe\xae\xfay=\xaa\xf4?^_\xf1D@\xd7H?\xbe\xec\xa4\xe6\xd4[!=\xaa\x94dX\xcaV\xa0>\xb3XtZH\xe2\x81?\xd0P\x10\x1a\x98\xfb\x1f@\xf9\x82\x86\x84\\\x94\x84@fh\x1c\x0b\x9d\xba\xbd@5\xa5\xf9Hv\x14\xc3@\xb2\xe9v\xb0\xe7\xe8\xba@\xd2\xf5\x92\x0c\xc0\xa1\x83@\xb6\xae\xf2\xd6\x9a\xc90@H\x92\x89\x95\x03W\xc2?-\x034\x8e\xedT9?\xf1\xe0\xcaRB\xa26?\t:\x1b\xa7\xba,\xd3?\xad\xfb\xe2\xb0\xe1\xd0B@\xcd\x85\xbb\\\x10 \x8f@\x88\xe8\xfe{\x81 \xbc@\x0bly%\x9b|\xc2@\xbav\xe6W\x89\xd1\xb9@\xf39\xf1X\xa2\x08\x8f@\x9f1\xd4k\xb8\xf7P@9\xae\x16\x91\xc3.\x02@.\xc5\xa50w/\xa3?\x9e\xf5\xc3\rC\xc3\x90?DCm\x9e\xaa\xee\x03@ {\x00\xf30\x90X@\x13\x8e\xd0\x86\xe6g\x94@;\x95\xe4\x9c&\xd5\xba@\xa8~\xa5N\xbe\xbc\xc1@S~\xafb\x0f\xf6\xb8@?\xf7d\xee\r\xdd\x94@\x89\x0f\xa9\xe6\xfc/d@\x92\xe10\xebf"(@@\xecY\x14\x0f\xe0\xe1?\x98\xa8\x15s\xc37\xc9?\xf4\xd5\x9aCc\x02$@w\x9d\x88\xd7\xbexg@\x981\xfb^X\xa8\x98@\xf6\xf8\x06\xe3k\xb5\xb9@\xeb\x89\x11\xb1u\xeb\xc0@\xdck7>\x106\xb8@\x06\x9e\x1a{L\x9e\x99@\x14\xcb\x82e\xa0!r@\xdcB3\xfd\x930B@\xca\x90\xb97\x01\xf1\t@\xa5\xcf\xdagw\x80\xf1?\x1e\x13\xf1\xf8\xd1y:@*\x11\xf8\x84\x18\xa7r@\xd9\xf1\x82,\xd2G\x9c@/\x07\xba\xc3\x03\xaf\xb8@\xa5x""\xcd\x17\xc0@g\x92T\xb3\xb0\x80\xb7@\xe6>R5i\xb6\x9d@\xba\x18_p\x0c\x93{@\xedJq\xcc\xb9\xc8S@\xbdx\xd4\x06\xa6\x06&@\xcf\x0b\xf7\xdcAG\x0e@\xc3\tn_\xda\tK@r\xa5%\xe8\xcbVz@\x8d?\x16NHJ\x9f@!]\xe0\xffy\xb9\xb7@\xc8\xe3\x0f\xe0\xb4\x94\xbe@3\xe3\x85\x99\xdc\xce\xb6@\x99\' +\xc0\x92\xa0@\x96"\xeanu\xd6\x82@\xbd\xc2\xcdw\xf8\x8aa@\x13j\x0b\x89\xf6\xe0:@k\xc4g\xa2@A#@M\xa9\x1e\x19FCW@|-c\x8c)\'\x81@\xebe^M\x8e\xdd\xa0@\x06\x04\xbc\xb5=\xd1\xb6@W\x1bM\x84\xef\x0e\xbd@ 5U<\xa3\x1e\xb6@\x08i,G\x93\xfa\xa1@+~\x00w\xb5\xea\x87@-\x8c:W\xb6%k@\x1aa9\x87XgJ@\xbd\x92]j\xaa\xd73@\xecL\xd8\x83`\xc3a@\x95\x9d\xa3:"\x16\x85@\xdc\xa0\xac\xe3\xe1\xd4\xa1@\x9f\x8e\x99\xe7\xe4\xf4\xb5@\xc7&\x9ec\xf9\xa1\xbb@\xf9\xec\x1e\x8eUp\xb5@\x80\x0e+\x980\x1a\xa3@DHIH\xb7\xce\x8c@\x83w\xdet\x0b\x17s@yaz\x87\xe2SV@\x19\xe7\x0e\x8f\xe2\x99A@;D]\xf7\xdb\xe1h@m\xc7\xbeD\x05\xd6\x88@\xe75\xc71\xa0\x93\xa2@\xe5\xa3%^\xd9#\xb5@\xc0\xcdP\xf6\xafN\xba@N p1\x04\xc5\xb4@\xbatg\xf0[\xfa\xa3@\x1e\x85\x8ev%\xaf\x90@\x81\xa2\x9a_y\ny@k\x80h\xe3\xa5\xf3`@ \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_range_accrual_option(
            expiry_date=datetime(2021, 9, 26),
            delivery_date=datetime(2021, 9, 27),
            cash=0.01,
            asset=0.0,
            lower_barrier=1.176100*0.95,    
            upper_barrier=1.176100*1.05,                
            obs_schedule=[
                    [
                        datetime(2021, 3, 31), datetime(2021, 4, 1), datetime(2021, 4, 2), 
                        datetime(2021, 4, 3), datetime(2021, 4, 4), datetime(2021, 4, 5), 
                        datetime(2021, 4, 6), datetime(2021, 4, 7), datetime(2021, 4, 8), 
                        datetime(2021, 4, 9), datetime(2021, 4, 10), datetime(2021, 4, 11), 
                        datetime(2021, 4, 12), datetime(2021, 4, 13), datetime(2021, 4, 14), 
                        datetime(2021, 4, 15), datetime(2021, 4, 16), datetime(2021, 4, 17), 
                        datetime(2021, 4, 18), datetime(2021, 4, 19), datetime(2021, 4, 20), 
                        datetime(2021, 4, 21), datetime(2021, 4, 22), datetime(2021, 4, 23), 
                        datetime(2021, 4, 24), datetime(2021, 4, 25), datetime(2021, 4, 26), 
                        datetime(2021, 4, 27), datetime(2021, 4, 28), datetime(2021, 4, 29), 
                        datetime(2021, 4, 30), datetime(2021, 5, 1), datetime(2021, 5, 2), 
                        datetime(2021, 5, 3), datetime(2021, 5, 4), datetime(2021, 5, 5), 
                        datetime(2021, 5, 6), datetime(2021, 5, 7), datetime(2021, 5, 8), 
                        datetime(2021, 5, 9), datetime(2021, 5, 10), datetime(2021, 5, 11), 
                        datetime(2021, 5, 12), datetime(2021, 5, 13), datetime(2021, 5, 14), 
                        datetime(2021, 5, 15), datetime(2021, 5, 16), datetime(2021, 5, 17), 
                        datetime(2021, 5, 18), datetime(2021, 5, 19), datetime(2021, 5, 20), 
                        datetime(2021, 5, 21), datetime(2021, 5, 22), datetime(2021, 5, 23), 
                        datetime(2021, 5, 24), datetime(2021, 5, 25), datetime(2021, 5, 26), 
                        datetime(2021, 5, 27), datetime(2021, 5, 28), datetime(2021, 5, 29), 
                        datetime(2021, 5, 30), datetime(2021, 5, 31), datetime(2021, 6, 1), 
                        datetime(2021, 6, 2), datetime(2021, 6, 3), datetime(2021, 6, 4), 
                        datetime(2021, 6, 5), datetime(2021, 6, 6), datetime(2021, 6, 7), 
                        datetime(2021, 6, 8), datetime(2021, 6, 9), datetime(2021, 6, 10), 
                        datetime(2021, 6, 11), datetime(2021, 6, 12), datetime(2021, 6, 13), 
                        datetime(2021, 6, 14), datetime(2021, 6, 15), datetime(2021, 6, 16), 
                        datetime(2021, 6, 17), datetime(2021, 6, 18), datetime(2021, 6, 19), 
                        datetime(2021, 6, 20), datetime(2021, 6, 21), datetime(2021, 6, 22), 
                        datetime(2021, 6, 23), datetime(2021, 6, 24), datetime(2021, 6, 25), 
                        datetime(2021, 6, 26), datetime(2021, 6, 27), datetime(2021, 6, 28), 
                        datetime(2021, 6, 29), datetime(2021, 6, 30), datetime(2021, 7, 1), 
                        datetime(2021, 7, 2), datetime(2021, 7, 3), datetime(2021, 7, 4), 
                        datetime(2021, 7, 5), datetime(2021, 7, 6), datetime(2021, 7, 7), 
                        datetime(2021, 7, 8), datetime(2021, 7, 9), datetime(2021, 7, 10), 
                        datetime(2021, 7, 11), datetime(2021, 7, 12), datetime(2021, 7, 13), 
                        datetime(2021, 7, 14), datetime(2021, 7, 15), datetime(2021, 7, 16), 
                        datetime(2021, 7, 17), datetime(2021, 7, 18), datetime(2021, 7, 19), 
                        datetime(2021, 7, 20), datetime(2021, 7, 21), datetime(2021, 7, 22), 
                        datetime(2021, 7, 23), datetime(2021, 7, 24), datetime(2021, 7, 25), 
                        datetime(2021, 7, 26), datetime(2021, 7, 27), datetime(2021, 7, 28), 
                        datetime(2021, 7, 29), datetime(2021, 7, 30), datetime(2021, 7, 31), 
                        datetime(2021, 8, 1), datetime(2021, 8, 2), datetime(2021, 8, 3), 
                        datetime(2021, 8, 4), datetime(2021, 8, 5), datetime(2021, 8, 6), 
                        datetime(2021, 8, 7), datetime(2021, 8, 8), datetime(2021, 8, 9), 
                        datetime(2021, 8, 10), datetime(2021, 8, 11), datetime(2021, 8, 12), 
                        datetime(2021, 8, 13), datetime(2021, 8, 14), datetime(2021, 8, 15), 
                        datetime(2021, 8, 16), datetime(2021, 8, 17), datetime(2021, 8, 18), 
                        datetime(2021, 8, 19), datetime(2021, 8, 20), datetime(2021, 8, 21), 
                        datetime(2021, 8, 22), datetime(2021, 8, 23), datetime(2021, 8, 24), 
                        datetime(2021, 8, 25), datetime(2021, 8, 26), datetime(2021, 8, 27), 
                        datetime(2021, 8, 28), datetime(2021, 8, 29), datetime(2021, 8, 30), 
                        datetime(2021, 8, 31), datetime(2021, 9, 1), datetime(2021, 9, 2), 
                        datetime(2021, 9, 3), datetime(2021, 9, 4), datetime(2021, 9, 5), 
                        datetime(2021, 9, 6), datetime(2021, 9, 7), datetime(2021, 9, 8), 
                        datetime(2021, 9, 9), datetime(2021, 9, 10), datetime(2021, 9, 11), 
                        datetime(2021, 9, 12), datetime(2021, 9, 13), datetime(2021, 9, 14), 
                        datetime(2021, 9, 15), datetime(2021, 9, 16), datetime(2021, 9, 17), 
                        datetime(2021, 9, 18), datetime(2021, 9, 19), datetime(2021, 9, 20), 
                        datetime(2021, 9, 21), datetime(2021, 9, 22), datetime(2021, 9, 23), 
                        datetime(2021, 9, 24), datetime(2021, 9, 25), datetime(2021, 9, 26)
                    ],
                [0] * 180,  # All values are 0
                [1] * 180  # All weights are 1
            ],   
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_range_accrual_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_analytical_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_range_accrual_option_pricer:', result.SerializeToString())
                
        self.assertEqual(result.SerializeToString(), expected)
    
    def test_fx_airbag_option_pricer(self):
        expected = b'\n\xae\x07\t_1P\x8a\xde\x80\xd6@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08&\xf3\xcf\x07n7 A\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\n\x85\xfbc\x06k\x13\xc1\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x01I`\xe0s\xb9\x12A\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x87\x1c\x06|\x98i\xb8@\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00\xa8\x1a\xfd\x86\xd0?\xc0\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00f[\xc2\x97\xad>@\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08`\x8a\xa9>_6aA\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08O\x10<<\xfa\x80\x93@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\x00\xe6OB\x0c\xbfR\xc0\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08(1:\xb2(9\x19\xc1\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xc0\xe2\x9d\xbb8MH\xc0\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08oTG\xf8\xc4\t\x14A\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xcc\x8ae\xd7\x1a\xa6\xa9@\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x80Q\xfe\x90Ou\xbb@\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x00\x00SRi~\xe6?\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08E\xd6\x06J\xff\xf3\t\xc1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xbf\xfaQo\xb7\xb5\xa3?\x01\xa9\xdb!=\xc9\xba@\x13:\xc6\xe4yI\xe9@\xb5\xbf\x0c\xbb\x00,\xf8@\xce\xf1\xc9?\xa2\xd9\x01A\xdd((\rD\x9d\x07A\xfd\xed\xb0\x03\xe6`\rA\x90\x97\xca\xdc\xa7>\x08\xc1\xd8QO\x15\x086^\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x13\xce#\x1f\xd2F@\'\xff\xf4Sf\xf0\xc2@\x08\xc1\xae\xb5\x1cK\xe9@\x13\xca\x80"\x01,\xf8@\r\x8c\xddq\xa2\xd9\x01A1\x12\'MD\x9d\x07A\xaf+J>\xe6`\rA\x91\xecR\xe0\xe0l\x06\xc1z\xb8\xd4+\xca\x1c\xaa\xc0z;\xb5H\xeb\x8c\xee\xbfN\x81\xae\xcf\xe1\x91\xe7?]\x94\r\x9a~=|@&H\xff\xee\xac\xaa\xc8@"\x87\xd5\xcb\xede\xe9@\x9e5S\x1a\x0b,\xf8@\x80w\xec\xaa\xa2\xd9\x01A6\xc6\xf4\x8eD\x9d\x07A\x97\xb2My\xe6`\rA\x12\xbb\xd0\xbe\x17r\t\xc1!F\x00s}\xd1\xca\xc0F\xc6\x8d\xda\x8f\xa6U\xc0\xdf\xf2e\xbc\xbb\xa35@\x92\x11d\x0c\xea5\x96@\x16\x10\x0bWDt\xce@\xbb\x05h\xc5\t\xbb\xe9@e\xce:2@-\xf8@b\xea\xaf\xab\xa3\xd9\x01A\xd3\xd34\xc7D\x9d\x07A&[l\xb2\xe6`\rAo\x80~[\xc2\xf6\t\xc1*\xe3S4\xb3N\xdc\xc0jHUG\x14\xf7\x8a\xc0\xc1=V[H\x99`@E\x82\xa5\xb0/y\xa6@\'\xa7r\x126"\xd2@\xceQ\xc7R*N\xea@\xfb\xdf\xed\x92h4\xf8@o>\x1c\xa9\xc0\xd9\x01AwXy;E\x9d\x07Ag\x9e+\xe6\xe6`\rA\xdc\xc6M>\x045\x04\xc1\xfc|\xb7\xf1\x96?\xe6\xc0\x01\xe0\xe1\x81\xd1\x14\xaa\xc0\xcc0\xb0I8Qv@\xf6\xb7X)\xadM\xb2@\x05PG\xf0\xc9\x0b\xd5@\x0f\xb6q\x17\x0b\x14\xeb@\x9d\x87\xe9\x0b\xf8G\xf8@\x99;n\xff\x97\xda\x01A\xba\x86\x80\x99N\x9d\x07A\xcanK5\xe7`\rA\xa7\xf5"\x18\x84\xfb\x05\xc1\x1dX\x86\xa9\xf0\x0f\xee\xc0W\\e\xb7\x83\x16\xbf\xc0i\xd0\x83a?\x17\x7f@O\xcc\xcc\x98\xeaJ\xba@\x96\xd3&\xa9{\xf6\xd7@\xf9\xdac\x81R\x00\xec@\xb1\x15\xb7\x8b\x11l\xf8@3A#\xa8\x88\xdd\x01A\x05\xd4\x0b\x83\x96\x9d\x07A\x86\x87\xc4\x90\xeb`\rAd\x01B\x97]L\x07\xc1\x0e!\x0f\xddc\x89\xf2\xc0\x0e\x17\x15B\r+\xcc\xc0:2\x97\x84\x92kh@C\xe0\xd9\x05\x10W\xc1@<k\x03MN\xe0\xda@\xcd\x9a\x14\x18\x1a\t\xed@\xbd\xc5\xfd\xae\xd4\xa1\xf8@\x92\x97\x12\xb5;\xe4\x01A\x7fp-\xc1\xae\x9e\x07A\xf7\xbf\'S\x0ba\rA\xdc\xe7M\xab\xdd\x1a\x0b\xc1\x0e\xe1\xab3\'\xa7\xf5\xc0\x92\xabRr\xfd\x8c\xd5\xc0\x80i\x1a0\x88P\x8a\xc0}\xfe\xe3\xea8]\xc5@Ud\xa4\x81\xf5\xc4\xdd@\xc55\x8d\x97"\'\xee@\xdcRS%p\xe8\xf8@`\x89_\xcf\x0c\xf0\x01A\x85Gb\xd6\x7f\xa1\x07A\x1eE$\xff\x8aa\rAE\xd8Fr\x8e\xec\x0b\xc1\xcd\x18\x0e\xca\xd7k\xf8\xc0!\xf1\xad\xfd)\xa7\xdd\xc0\xb7\xd0<\xf3ok\xa5\xc0\xaa\xbd>}\x82\xd0\xc8@\xb4\x9b\xd4)6K\xe0@\xcc\xeb7bTT\xef@\xd2&\x04s\x1e>\xf9@u9\xeb\x01\xcb\x01\x02AO\x89\x19p\x0f\xa7\x07A\xebvbH\xe8b\rAL\xc3\xf9X1\x89\t\xc1\xa9\xb8\xae\xec\xd6\xcd\xfa\xc0\x83\xeb\xf8\x9d=\xec\xe2\xc0\xef\x8b\xc9\xd7\x88E\xb5\xc0e\xae\xbd\xcdnQ\xcb@\xb6Z\x7f\x0fo\x9f\xe1@\n;\xd4\x82\x0fE\xf0@=j\x13\xed\xc2\xa0\xf9@\xb7J\xfa\xb2\xbc\x19\x02A:\x9b\x1d~E\xb0\x07A\xc8\x9bs\xf8\xcae\rA\\\xcb\xeb\xa8\'\xce\x0b\xc1;\xd8]\x048\xdf\xfc\xc0\x0eR\x9f}<\xe5\xe6\xc0N}\xe0\xeb\xc8\x1b\xc1\xc0J\xacC|\x17\xb1\xcc@\\r#\x9bW\xd2\xe2@\xd9\xa0\xc2\x0f2\xe0\xf0@\xf2/\x91"\xcf\r\xfa@r\t\x82&\xbd7\x02AUbh\x95\xc9\xbd\x07A\xddF\xc7\x02\xe7j\rA \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_airbag_option(
            payoff_type='CALL',  
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            lower_strike=1.176100*1.0,    
            upper_strike=1.176100*1.2,                
            lower_participation = 1.0,
            upper_participation = 1.0,
            knock_in_strike = 1.176100*1.0, 
            barrier_type='DOWN_IN',
            barrier_value=1.176100*0.8,               
            barrier_obs_type='DISCRETE_OBSERVATION_TYPE',
            obs_schedule=[
                    [
                        datetime(2021, 3, 31), datetime(2021, 4, 1), datetime(2021, 4, 2), 
                        datetime(2021, 4, 3), datetime(2021, 4, 4), datetime(2021, 4, 5), 
                        datetime(2021, 4, 6), datetime(2021, 4, 7), datetime(2021, 4, 8), 
                        datetime(2021, 4, 9), datetime(2021, 4, 10), datetime(2021, 4, 11), 
                        datetime(2021, 4, 12), datetime(2021, 4, 13), datetime(2021, 4, 14), 
                        datetime(2021, 4, 15), datetime(2021, 4, 16), datetime(2021, 4, 17), 
                        datetime(2021, 4, 18), datetime(2021, 4, 19), datetime(2021, 4, 20), 
                        datetime(2021, 4, 21), datetime(2021, 4, 22), datetime(2021, 4, 23), 
                        datetime(2021, 4, 24), datetime(2021, 4, 25), datetime(2021, 4, 26), 
                        datetime(2021, 4, 27), datetime(2021, 4, 28), datetime(2021, 4, 29), 
                        datetime(2021, 4, 30), datetime(2021, 5, 1), datetime(2021, 5, 2), 
                        datetime(2021, 5, 3), datetime(2021, 5, 4), datetime(2021, 5, 5), 
                        datetime(2021, 5, 6), datetime(2021, 5, 7), datetime(2021, 5, 8), 
                        datetime(2021, 5, 9), datetime(2021, 5, 10), datetime(2021, 5, 11), 
                        datetime(2021, 5, 12), datetime(2021, 5, 13), datetime(2021, 5, 14), 
                        datetime(2021, 5, 15), datetime(2021, 5, 16), datetime(2021, 5, 17), 
                        datetime(2021, 5, 18), datetime(2021, 5, 19), datetime(2021, 5, 20), 
                        datetime(2021, 5, 21), datetime(2021, 5, 22), datetime(2021, 5, 23), 
                        datetime(2021, 5, 24), datetime(2021, 5, 25), datetime(2021, 5, 26), 
                        datetime(2021, 5, 27), datetime(2021, 5, 28), datetime(2021, 5, 29), 
                        datetime(2021, 5, 30), datetime(2021, 5, 31), datetime(2021, 6, 1), 
                        datetime(2021, 6, 2), datetime(2021, 6, 3), datetime(2021, 6, 4), 
                        datetime(2021, 6, 5), datetime(2021, 6, 6), datetime(2021, 6, 7), 
                        datetime(2021, 6, 8), datetime(2021, 6, 9), datetime(2021, 6, 10), 
                        datetime(2021, 6, 11), datetime(2021, 6, 12), datetime(2021, 6, 13), 
                        datetime(2021, 6, 14), datetime(2021, 6, 15), datetime(2021, 6, 16), 
                        datetime(2021, 6, 17), datetime(2021, 6, 18), datetime(2021, 6, 19), 
                        datetime(2021, 6, 20), datetime(2021, 6, 21), datetime(2021, 6, 22), 
                        datetime(2021, 6, 23), datetime(2021, 6, 24), datetime(2021, 6, 25), 
                        datetime(2021, 6, 26), datetime(2021, 6, 27), datetime(2021, 6, 28), 
                        datetime(2021, 6, 29), datetime(2021, 6, 30), datetime(2021, 7, 1), 
                        datetime(2021, 7, 2), datetime(2021, 7, 3), datetime(2021, 7, 4), 
                        datetime(2021, 7, 5), datetime(2021, 7, 6), datetime(2021, 7, 7), 
                        datetime(2021, 7, 8), datetime(2021, 7, 9), datetime(2021, 7, 10), 
                        datetime(2021, 7, 11), datetime(2021, 7, 12), datetime(2021, 7, 13), 
                        datetime(2021, 7, 14), datetime(2021, 7, 15), datetime(2021, 7, 16), 
                        datetime(2021, 7, 17), datetime(2021, 7, 18), datetime(2021, 7, 19), 
                        datetime(2021, 7, 20), datetime(2021, 7, 21), datetime(2021, 7, 22), 
                        datetime(2021, 7, 23), datetime(2021, 7, 24), datetime(2021, 7, 25), 
                        datetime(2021, 7, 26), datetime(2021, 7, 27), datetime(2021, 7, 28), 
                        datetime(2021, 7, 29), datetime(2021, 7, 30), datetime(2021, 7, 31), 
                        datetime(2021, 8, 1), datetime(2021, 8, 2), datetime(2021, 8, 3), 
                        datetime(2021, 8, 4), datetime(2021, 8, 5), datetime(2021, 8, 6), 
                        datetime(2021, 8, 7), datetime(2021, 8, 8), datetime(2021, 8, 9), 
                        datetime(2021, 8, 10), datetime(2021, 8, 11), datetime(2021, 8, 12), 
                        datetime(2021, 8, 13), datetime(2021, 8, 14), datetime(2021, 8, 15), 
                        datetime(2021, 8, 16), datetime(2021, 8, 17), datetime(2021, 8, 18), 
                        datetime(2021, 8, 19), datetime(2021, 8, 20), datetime(2021, 8, 21), 
                        datetime(2021, 8, 22), datetime(2021, 8, 23), datetime(2021, 8, 24), 
                        datetime(2021, 8, 25), datetime(2021, 8, 26), datetime(2021, 8, 27), 
                        datetime(2021, 8, 28), datetime(2021, 8, 29), datetime(2021, 8, 30), 
                        datetime(2021, 8, 31), datetime(2021, 9, 1), datetime(2021, 9, 2), 
                        datetime(2021, 9, 3), datetime(2021, 9, 4), datetime(2021, 9, 5), 
                        datetime(2021, 9, 6), datetime(2021, 9, 7), datetime(2021, 9, 8), 
                        datetime(2021, 9, 9), datetime(2021, 9, 10), datetime(2021, 9, 11), 
                        datetime(2021, 9, 12), datetime(2021, 9, 13), datetime(2021, 9, 14), 
                        datetime(2021, 9, 15), datetime(2021, 9, 16), datetime(2021, 9, 17), 
                        datetime(2021, 9, 18), datetime(2021, 9, 19), datetime(2021, 9, 20), 
                        datetime(2021, 9, 21), datetime(2021, 9, 22), datetime(2021, 9, 23), 
                        datetime(2021, 9, 24), datetime(2021, 9, 25), datetime(2021, 9, 26)
                    ],
                [0] * 180,  # All values are 0
                [1] * 180  # All weights are 1
            ],            
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_airbag_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_pde_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_airbag_option_pricer:', result.SerializeToString())

        self.assertEqual(result.SerializeToString(), expected)

    def test_fx_ping_pong_option_pricer(self):
        expected = b'\n\xae\x07\tv\t\x0e\x07\xe5\xa3\x1d@\x1a\x99\x07\n\x99\x01\n\x05DELTA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\x83Ld\x8cl\xb0c\xc0\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00\x00\x00\x00\x00\x00\x00\x00\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08p\xf6\xdal\xf3;\r\xc0\x12\x05TOTAL\x1a\x00\n\xa2\x01\n\x0eDELTA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08p\t\x0e\x07\xe5\xa3\xfd\xbf\x12\x00\x1a\x00\x12Z\n\rINTEREST_RATE\x12&\n\rEUR_EURUSD_FX\x12\x15\n\n\n\x08\x00\x00\x00\x00\x00\x00\x00\x00\x12\x05TOTAL\x1a\x00\x12!\n\x08USD_DEPO\x12\x15\n\n\n\x08\x00\xe0jA\xda\xf27\xbf\x12\x05TOTAL\x1a\x00\n=\n\x05GAMMA\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08\xdc;U*l(\xfa@\x12\x00\x1a\x00\nF\n\x0eGAMMA_EXPOSURE\x124\n\x10FOREIGN_EXCHANGE\x12 \n\x0cPRICE_EURUSD\x12\x10\n\n\n\x08w\t\x0e\x07\xe5\xa3-@\x12\x00\x1a\x00\n$\n\x05THETA\x12\x1b\n\x05THETA\x12\x12\x12\x10\n\n\n\x08\xe8\x87*\xc1\xde\xa3\xfd\xbf\x12\x00\x1a\x00\nA\n\x05VANNA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x1f\xec\xa6\x01o\xd7\xec\xc0\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVANNA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xe4(\x9d\xb6\xa6\xc9\x1b\xc0\x12\x05TOTAL\x1a\x05TOTAL\n@\n\x04VEGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xd8&[\x9c\x8b\x9a\xa8@\x12\x05TOTAL\x1a\x05TOTAL\nI\n\rVEGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\n\xea~W#~?@\x12\x05TOTAL\x1a\x05TOTAL\nA\n\x05VOLGA\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\x10D\x87\xdf\xd5e\x1dA\x12\x05TOTAL\x1a\x05TOTAL\nJ\n\x0eVOLGA_EXPOSURE\x128\n\x10FOREIGN_EXCHANGE\x12$\n\x06EURUSD\x12\x1a\n\n\n\x08\xaeg\xbb\x15*\x15H@\x12\x05TOTAL\x1a\x05TOTAL"\x00*\x03USD2\x00\x10\x01"\xa9\x08\x08\x0b\x10\x0c\x1a\xa0\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00v\t\x0e\x07\xe5\xa3\xfd?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xea\xc5h$o\x862@\x00\x00\x00\x00\x00\x00\x00\x00GH,fh\xef)@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00R\xe5\xf7\xd30\xac0@\x10\xfe\x84\xb8\xfe\xfcR@v\t\x0e\x07\xe5\xa3\xfd?w\x1d\x14h\xc0"Q@\x19\x87J\xc5\xeb:&@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00v\t\x0e\x07\xe5\xa3\xfd?\xce\x16\x12\x9d\xccMU@\x08a\xb9J6@l@\xe9\xc5h$o\x862@U\xdbt#\xc3\xecf@\x0b\xea~W#~O@v\t\x0e\x07\xe5\xa3\xfd?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00GH,fh\xef)@\xed\xbb\xe5s\x01\xc7h@\xd0(\x9d\xb6\xa6\xc9{@\xbc\xf0\x80"\x17S[@\xc4\x1a\x96\xd1\x02\xac{@|\x13\x91\xb7Rcg@\xe9\xc5h$o\x862@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00v\t\x0e\x07\xe5\xa3\xfd?c\xf7\x82\xed\n(G@\xdc\xbb\xe5s\x01\xc7x@~\x13\x91\xb7Rc\x87@%\x9f\xd4Z\xfd\x17p@t\x05\x8a\xd2\xaeE\x87@\xd2\xad\xde\x8e]\xa9x@\x0b\xea~W#~O@\xe9\xc5h$o\x86"@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x19\x87J\xc5\xeb:&@p\x80H\xfa\xf7eZ@[n\xbd\xe0\x1d\xea\x83@\xd1\x06\xc9\x9d\r\x01\x92@\x15\x14\x94\x06\x0f\xd7\x7f@\xc2q>\xc6\x97\xd4\x91@\xbc\xfa\x03\xd3\x84\x12\x85@%\x1a\x93\x82F8c@\x19\x87J\xc5\xeb:6@v\t\x0e\x07\xe5\xa3\xfd?v\t\x0e\x07\xe5\xa3\xfd?\xdf(\x9d\xb6\xa6\xc9;@\x14\xf4\x01\x08\x91=i@\xe3\x87M\x14\xa8\xae\x8e@\xae0\xc0\x0e(6\x99@C:%\x81\xc4\xd1\x89@S+\xfd\x0e\x93\x1c\x98@\xbep\x1d9\n=\x90@\xc2\x8dL\x90\xdf\x0fr@R\xe5\xf7\xd30\xacP@\x19\x87J\xc5\xeb:&@\xe9\xc5h$o\x86"@\r\xea~W#~O@\xc6\x16\x12\x9d\xccMu@\xb2Ik1\xc7\xaa\x94@\xf8\xf9\xf1\xe4\xdf\x0c\xa0@@\xaf\x1dZ\xbcd\x93@<\x9f\xd4Z\xfd\x17\xa0@N*\xdc\x81\x05\x85\x96@\x873#\xb6\xd0\xfc}@\x00\xe2v\xee\xb6\xc1b@v\t\x0e\x07\xe5\xa3=@ \x01*Z\nX@\xbc\xae_\xb0\x1b\xee?C\xdf\xdd\xca\x12\x9d\xef?#\x81\x06\x9b:\x8f\xf0?\xa5\x12\x9e\xd0\xebO\xf1?\'\xa45\x06\x9d\x10\xf2?\xa95\xcd;N\xd1\xf2?+\xc7dq\xff\x91\xf3?\xadX\xfc\xa6\xb0R\xf4?/\xea\x93\xdca\x13\xf5?\xb1{+\x12\x13\xd4\xf5?3\r\xc3G\xc4\x94\xf6?2b\n`\x9a\x99\x99\x99\x99\x99\xa9\xbf\xf2\x94 O\t\xf2\xa4\xbfJ\x90\xa7\x04yJ\xa0\xbfD\x17]t\xd1E\x97\xbf\xe9\x1b\xd6\xbea\xed\x8b\xbf\x94\x12\xe4)A\x9er\xbf\xaa\x12\xe4)A\x9er?\xf4\x1b\xd6\xbea\xed\x8b?J\x17]t\xd1E\x97?M\x90\xa7\x04yJ\xa0?\xf5\x94 O\t\xf2\xa4?\x9d\x99\x99\x99\x99\x99\xa9?'
        
        inst = create_ping_pong_option(
            expiry=datetime(2021, 9, 26),
            delivery=datetime(2021, 9, 27),
            lower_barrier_type='DOWN_IN',
            lower_barrier_value=1.176100*0.95,   
            upper_barrier_type='UP_IN',
            upper_barrier_value=1.176100*1.05, 
            barrier_obs_type='DISCRETE_OBSERVATION_TYPE',
            obs_schedule=[
                    [
                        datetime(2021, 3, 31), datetime(2021, 4, 1), datetime(2021, 4, 2), 
                        datetime(2021, 4, 3), datetime(2021, 4, 4), datetime(2021, 4, 5), 
                        datetime(2021, 4, 6), datetime(2021, 4, 7), datetime(2021, 4, 8), 
                        datetime(2021, 4, 9), datetime(2021, 4, 10), datetime(2021, 4, 11), 
                        datetime(2021, 4, 12), datetime(2021, 4, 13), datetime(2021, 4, 14), 
                        datetime(2021, 4, 15), datetime(2021, 4, 16), datetime(2021, 4, 17), 
                        datetime(2021, 4, 18), datetime(2021, 4, 19), datetime(2021, 4, 20), 
                        datetime(2021, 4, 21), datetime(2021, 4, 22), datetime(2021, 4, 23), 
                        datetime(2021, 4, 24), datetime(2021, 4, 25), datetime(2021, 4, 26), 
                        datetime(2021, 4, 27), datetime(2021, 4, 28), datetime(2021, 4, 29), 
                        datetime(2021, 4, 30), datetime(2021, 5, 1), datetime(2021, 5, 2), 
                        datetime(2021, 5, 3), datetime(2021, 5, 4), datetime(2021, 5, 5), 
                        datetime(2021, 5, 6), datetime(2021, 5, 7), datetime(2021, 5, 8), 
                        datetime(2021, 5, 9), datetime(2021, 5, 10), datetime(2021, 5, 11), 
                        datetime(2021, 5, 12), datetime(2021, 5, 13), datetime(2021, 5, 14), 
                        datetime(2021, 5, 15), datetime(2021, 5, 16), datetime(2021, 5, 17), 
                        datetime(2021, 5, 18), datetime(2021, 5, 19), datetime(2021, 5, 20), 
                        datetime(2021, 5, 21), datetime(2021, 5, 22), datetime(2021, 5, 23), 
                        datetime(2021, 5, 24), datetime(2021, 5, 25), datetime(2021, 5, 26), 
                        datetime(2021, 5, 27), datetime(2021, 5, 28), datetime(2021, 5, 29), 
                        datetime(2021, 5, 30), datetime(2021, 5, 31), datetime(2021, 6, 1), 
                        datetime(2021, 6, 2), datetime(2021, 6, 3), datetime(2021, 6, 4), 
                        datetime(2021, 6, 5), datetime(2021, 6, 6), datetime(2021, 6, 7), 
                        datetime(2021, 6, 8), datetime(2021, 6, 9), datetime(2021, 6, 10), 
                        datetime(2021, 6, 11), datetime(2021, 6, 12), datetime(2021, 6, 13), 
                        datetime(2021, 6, 14), datetime(2021, 6, 15), datetime(2021, 6, 16), 
                        datetime(2021, 6, 17), datetime(2021, 6, 18), datetime(2021, 6, 19), 
                        datetime(2021, 6, 20), datetime(2021, 6, 21), datetime(2021, 6, 22), 
                        datetime(2021, 6, 23), datetime(2021, 6, 24), datetime(2021, 6, 25), 
                        datetime(2021, 6, 26), datetime(2021, 6, 27), datetime(2021, 6, 28), 
                        datetime(2021, 6, 29), datetime(2021, 6, 30), datetime(2021, 7, 1), 
                        datetime(2021, 7, 2), datetime(2021, 7, 3), datetime(2021, 7, 4), 
                        datetime(2021, 7, 5), datetime(2021, 7, 6), datetime(2021, 7, 7), 
                        datetime(2021, 7, 8), datetime(2021, 7, 9), datetime(2021, 7, 10), 
                        datetime(2021, 7, 11), datetime(2021, 7, 12), datetime(2021, 7, 13), 
                        datetime(2021, 7, 14), datetime(2021, 7, 15), datetime(2021, 7, 16), 
                        datetime(2021, 7, 17), datetime(2021, 7, 18), datetime(2021, 7, 19), 
                        datetime(2021, 7, 20), datetime(2021, 7, 21), datetime(2021, 7, 22), 
                        datetime(2021, 7, 23), datetime(2021, 7, 24), datetime(2021, 7, 25), 
                        datetime(2021, 7, 26), datetime(2021, 7, 27), datetime(2021, 7, 28), 
                        datetime(2021, 7, 29), datetime(2021, 7, 30), datetime(2021, 7, 31), 
                        datetime(2021, 8, 1), datetime(2021, 8, 2), datetime(2021, 8, 3), 
                        datetime(2021, 8, 4), datetime(2021, 8, 5), datetime(2021, 8, 6), 
                        datetime(2021, 8, 7), datetime(2021, 8, 8), datetime(2021, 8, 9), 
                        datetime(2021, 8, 10), datetime(2021, 8, 11), datetime(2021, 8, 12), 
                        datetime(2021, 8, 13), datetime(2021, 8, 14), datetime(2021, 8, 15), 
                        datetime(2021, 8, 16), datetime(2021, 8, 17), datetime(2021, 8, 18), 
                        datetime(2021, 8, 19), datetime(2021, 8, 20), datetime(2021, 8, 21), 
                        datetime(2021, 8, 22), datetime(2021, 8, 23), datetime(2021, 8, 24), 
                        datetime(2021, 8, 25), datetime(2021, 8, 26), datetime(2021, 8, 27), 
                        datetime(2021, 8, 28), datetime(2021, 8, 29), datetime(2021, 8, 30), 
                        datetime(2021, 8, 31), datetime(2021, 9, 1), datetime(2021, 9, 2), 
                        datetime(2021, 9, 3), datetime(2021, 9, 4), datetime(2021, 9, 5), 
                        datetime(2021, 9, 6), datetime(2021, 9, 7), datetime(2021, 9, 8), 
                        datetime(2021, 9, 9), datetime(2021, 9, 10), datetime(2021, 9, 11), 
                        datetime(2021, 9, 12), datetime(2021, 9, 13), datetime(2021, 9, 14), 
                        datetime(2021, 9, 15), datetime(2021, 9, 16), datetime(2021, 9, 17), 
                        datetime(2021, 9, 18), datetime(2021, 9, 19), datetime(2021, 9, 20), 
                        datetime(2021, 9, 21), datetime(2021, 9, 22), datetime(2021, 9, 23), 
                        datetime(2021, 9, 24), datetime(2021, 9, 25), datetime(2021, 9, 26)
                    ],
                [0] * 180,  # All values are 0
                [1] * 180  # All weights are 1
            ],  
            payment_type='PAY_AT_MATURITY',
            cash=0.015,
            asset=0.0,
            settlement_days=1,
            nominal=1000000.0,
            payoff_ccy='USD',
            underlying_type='SPOT',
            underlying_ccy='USD',
            underlying='EURUSD'
        )

        result = fx_ping_pong_option_pricer(
            instrument=inst,
            pricing_date=self.as_of_date,
            mkt_data_set=self.eurusd_mkt_data_set,
            pricing_settings=self.bsm_mc_pricing_settings,
            risk_settings=self.risk_settings,
            scn_settings=self.scenario_analysis_settings
        )
        #print('test_fx_ping_pong_option_pricer:', result.SerializeToString())
        
        self.assertEqual(result.SerializeToString(), expected)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFxAnalytics)
    unittest.TextTestRunner(verbosity=2).run(suite)

