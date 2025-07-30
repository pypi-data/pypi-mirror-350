from datetime import datetime

from caplib.numerics import *
from caplib.market import *
from caplib.datetime import *
from caplib.analytics import *
from caplib.processrequest import process_request

def create_pm_par_rate_curve(as_of_date, currency, curve_name, pillars):
    """
    Create a PM Par Rate Curve.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the curve.
    currency : str
        The currency of the curve.
    curve_name : str
        The name of the curve.
    pillars : list
        List of tuples representing pillar data.    

    Returns
    -------
    ParCurve
        The created PM Par Rate Curve.
    """
    try:
        pillars_list = list()
        for pillar in pillars:
            pillars_list.append(dqCreateProtoPmParRateCurve_Pillar(str(pillar[0]), 
                                                                   to_instrument_type(str(pillar[1])), 
                                                                   to_period(str(pillar[2])), 
                                                                   float(pillar[3])))
        par_curve = dqCreateProtoPmParRateCurve(create_date(as_of_date),
                                                currency,
                                                curve_name,
                                                pillars_list)
        return par_curve
    except Exception as e:
        return str(e)

def pm_yield_curve_builder(as_of_date, 
                           par_curve, 
                           inst_template, 
                           discount_curve, 
                           spot_price, 
                           curve_type, 
                           interp_method, 
                           extrap_method, 
                           day_count, 
                           curve_name, 
                           jacobian, 
                           shift, 
                           finite_diff_method, 
                           threading_mode):
    """
    Build a PM Yield Curve.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the curve.
    par_curve : ParCurve
        The par rate curve.
    inst_template : InstrumentTemplate
        The instrument template.
    discount_curve : DiscountCurve
        The discount curve.
    spot_price : float
        The spot price.
    curve_type : str
        The type of the yield curve.
    interp_method : str
        The interpolation method.
    extrap_method : str
        The extrapolation method.
    day_count : str
        The day count convention.
    curve_name : str
        The name of the curve.
    jacobian : list
        The Jacobian matrix.
    shift : float
        The shift for calculation.
    finite_diff_method : str
        The finite difference method.
    threading_mode : str
        The threading mode.

    Returns
    -------
    YieldCurve
        The built yield curve.
    """
    try:
        pb_input = dqCreateProtoPmYieldCurveBuildingInput(create_date(as_of_date),
                                                          par_curve,
                                                          discount_curve,
                                                          spot_price,
                                                          jacobian,
                                                          to_day_count_convention(day_count),
                                                          to_interp_method(interp_method),
                                                          to_extrap_method(extrap_method),
                                                          to_ir_yield_curve_type(curve_type),
                                                          inst_template,
                                                          curve_name,
                                                          shift,
                                                          to_finite_difference_method(finite_diff_method),
                                                          to_threading_mode(threading_mode))
        req_name = "PM_YIELD_CURVE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = PmYieldCurveBuildingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.yield_curve
    except Exception as e:
        return [str(e)]
    
#CreatePmMktConventions
def create_pm_mkt_conventions(atm_type,
                              short_delta_type,
                              long_delta_type,
                              short_delta_cutoff,
                              risk_reversal,
                              smile_quote_type):
    """
    Create PM market conventions.

    Parameters
    ----------
    atm_type : str
        The ATM type.
    short_delta_type : str
        The short delta type.
    long_delta_type : str
        The long delta type.
    short_delta_cutoff : str
        The short delta cutoff period.
    risk_reversal : str
        The type of risk reversal.
    smile_quote_type : str
        The type of smile quote.

    Returns
    -------
    ProtoPmMarketConventions
        The created market conventions.
    """
    return dqCreateProtoPmMarketConventions(to_atm_type(atm_type),
                                            to_delta_type(short_delta_type),
                                            to_delta_type(long_delta_type),
                                            to_period(short_delta_cutoff),
                                            to_risk_reversal(risk_reversal),
                                            to_smile_quote_type(smile_quote_type))

def create_pm_option_quote_matrix(underlying: str,
                                  as_of_date: datetime,
                                  terms: list,
                                  payoff_types: list,
                                  deltas: list,
                                  quotes: list):
    """
    Create PM option quote matrix.

    Parameters
    ----------
    underlying : str
        The underlying instrument.
    terms : list
        List of terms.
    payoff_types : list
        List of payoff types.
    deltas : list
        List of deltas.
    quotes : list
        List of quotes.

    Returns
    -------
    OptionQuoteMatrix
        The created option quote matrix.
    """
    try:        
        quote_matrix = create_option_quote_matrix(
            "OQVT_VOLATILITY",
            "OQTT_RELATIVE_TERM",
            "OQST_DELTA_STRIKE",
            "EUROPEAN",
            "SPOT_UNDERLYING_TYPE",
            as_of_date,
            terms,
            [],
            payoff_types,
            quotes,
            deltas,
            underlying)
        return quote_matrix
    except Exception as e:
        return str(e)

def pm_vol_surface_builder(as_of_date,
                           vol_surf_definition,
                           option_quote_matrix,
                           mkt_conventions,
                           spot_price,
                           discount_curve,
                           fwd_curve,
                           building_settings,
                           spot_template,
                           underlying,
                           vol_surf_name):
    """
    Build PM volatility surface.

    Parameters
    ----------
    as_of_date : datetime
        The reference date.
    vol_surf_definition : VolatilitySurfaceDefinition
        The volatility surface definition.
    option_quote_matrix : OptionQuoteMatrix
        The option quote matrix.
    mkt_conventions : ProtoPmMarketConventions
        The market conventions.
    spot_price : float
        The spot price.
    discount_curve : DiscountCurve
        The discount curve.
    fwd_curve : ForwardCurve
        The forward curve.
    building_settings : list
        The building settings.
    spot_template : SpotTemplate
        The spot template.
    underlying : str
        The underlying instrument.
    vol_surf_name : str
        The name of the volatility surface.

    Returns
    -------
    VolatilitySurface
        The built volatility surface.
    """
    try:
        pb_input = dqCreateProtoPmVolatilitySurfaceBuildingInput(create_date(as_of_date),
                                                                 vol_surf_definition,
                                                                 option_quote_matrix,
                                                                 spot_price,
                                                                 discount_curve,
                                                                 fwd_curve,
                                                                 create_vol_surf_build_settings(building_settings[0], building_settings[1]),
                                                                 mkt_conventions,
                                                                 spot_template,
                                                                 underlying,
                                                                 vol_surf_name)
        req_name = "PM_VOLATILITY_SURFACE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = PmVolatilitySurfaceBuildingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.vol_surf
    except Exception as e:
        return str(e)

def create_cm_option_quote_matrix(exercise_type,
                                  underlying_type,
            as_of_date,
                                  term_dates,
                                  payoff_types,
                                  strikes,
                                  prices,
                                  underlying):
    """
    Create CM option quote matrix.

    Parameters
    ----------
    exercise_type : str
        The type of option exercise.
    underlying_type : str
        The type of option underlying.
    term_dates : list
        List of term dates.
    payoff_types : list
        List of payoff types.
    strikes : list
        List of strike prices.
    prices : list
        List of option prices.
    underlying : str
        The underlying instrument.

    Returns
    -------
    OptionQuoteMatrix
        The created option quote matrix.
    """
    try:
        quote_matrix = create_option_quote_matrix(
            "OQVT_PRICE",
            "OQTT_ABOSULTE_TERM",
            "OQST_ABOSULTE_STRIKE",
            exercise_type,
            underlying_type,
            as_of_date,
            [],
            term_dates,
            payoff_types,
            prices,
            strikes,
            underlying)
        return quote_matrix
    except Exception as e:
        return str(e)

def cm_vol_surface_builder(as_of_date,
                           smile_method,
                           wing_strike_type,
                           lower,
                           upper,
                           option_quote_matrix,
                           underlying_prices,
                           discount_curve,
                           fwd_curve,
                           building_settings,
                           underlying):
    """
    Build CM volatility surface.

    Parameters
    ----------
    as_of_date : datetime
        The reference date.
    smile_method : str
        The smile method.
    wing_strike_type : str
        The wing strike type.
    lower : float
        The lower bound.
    upper : float
        The upper bound.
    option_quote_matrix : OptionQuoteMatrix
        The option quote matrix.
    underlying_prices : list
        List of underlying prices.
    discount_curve : DiscountCurve
        The discount curve.
    fwd_curve : ForwardCurve
        The forward curve.
    building_settings : list
        The building settings.
    underlying : str
        The underlying instrument.

    Returns
    -------
    VolatilitySurface
        The built volatility surface.
    """
    try:
        p_vol_surf_defintion = create_volatility_surface_definition('STRIKE_VOL_SMILE', 
                                                                   smile_method, 
                                                                   'FLAT_EXTRAP', 
                                                                   "LINEAR_IN_VARIANCE", 
                                                                   "FLAT_IN_VOLATILITY", 
                                                                   "ACT_365_FIXED", 
                                                                   "LOG_NORMAL_VOL_TYPE", 
                                                                   wing_strike_type, 
                                                                   lower, 
                                                                   upper)
        p_building_settings = create_vol_surf_build_settings(building_settings[0], building_settings[1])
        p_fwd_curve = None
        if fwd_curve is not None:
            p_fwd_curve = fwd_curve
        else:
            p_fwd_curve = create_flat_dividend_curve(as_of_date, 0.0)
        pb_input = dqCreateProtoCmVolatilitySurfaceBuildingInput(create_date(as_of_date),
                                                                 p_vol_surf_defintion,
                                                                 option_quote_matrix,
                                                                 dqCreateProtoVector(underlying_prices),
                                                                 discount_curve,
                                                                 p_fwd_curve,
                                                                 p_building_settings,
                                                                 underlying)
        req_name = "CM_VOLATILITY_SURFACE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = CmVolatilitySurfaceBuildingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.vol_surf
    except Exception as e:
        return str(e)

def create_cm_risk_settings(ir_curve_settings,
                            price_settings,
                            vol_settings,
                            price_vol_settings,
                            dividend_curve_settings,                            
                            theta_settings):
    """
    Create CM risk settings.

    Parameters
    ----------
    ir_curve_settings : Various settings for interest rate curve.
    price_settings : Various settings for pricing.
    vol_settings : Various settings for volatility.
    price_vol_settings : Various settings for price volatility.
    dividend_curve_settings : Settings for dividend curve.
    theta_settings : Settings for theta.

    Returns
    -------
    ProtoCmRiskSettings
        The created risk settings.
    """
    return dqCreateProtoCmRiskSettings(ir_curve_settings,
                                       price_settings,
                                       vol_settings,
                                       price_vol_settings,
                                       theta_settings,
                                       dividend_curve_settings)

def create_cm_mkt_data_set(as_of_date: datetime,
                           discount_curve,
                           underlying_price,
                           vol_surf,
                           fwd_curve = None,
                           quanto_discount_curve = None,
                           quanto_fx_vol_curve = None,
                           quanto_correlation: float = 0.0,
                           underlying: str = ''):
    """
    Create CM market data set.

    Parameters
    ----------
    as_of_date : datetime
        The reference date.
    discount_curve : DiscountCurve
        The discount curve.
    underlying_price : float
        The underlying price.
    vol_surf : VolatilitySurface
        The volatility surface.
    fwd_curve : ForwardCurve
        The forward curve.
    quanto_discount_curve : DiscountCurve
        The quanto discount curve.
    quanto_fx_vol_curve : VolatilityCurve
        The quanto FX volatility curve.
    quanto_correlation : float
        The quanto correlation.
    underlying : str, optional
        The underlying instrument.

    Returns
    -------
    ProtoCmMktDataSet
        The created market data set.
    """
    if fwd_curve is not None:
        fwd_curve = fwd_curve
    else:
        fwd_curve = create_flat_dividend_curve(as_of_date, 0.0)
    if quanto_discount_curve is not None:
        quanto_discount_curve = quanto_discount_curve
    else:
        quanto_discount_curve = create_flat_ir_yield_curve(as_of_date, 'USD', 0.0)
    if quanto_fx_vol_curve is not None:
        quanto_fx_vol_curve = quanto_fx_vol_curve
    else:
        quanto_fx_vol_curve = create_flat_vol_curve(as_of_date, 0.0)
    return dqCreateProtoCmMktDataSet(create_date(as_of_date),
                                     discount_curve,
                                     fwd_curve,
                                     underlying_price,
                                     vol_surf,
                                     quanto_discount_curve,
                                     quanto_fx_vol_curve,
                                     quanto_correlation,
                                     underlying)

def run_cm_pricing(req_name, pb_input):
    """
    Run CM pricing.

    Parameters
    ----------
    req_name : str
        The request name.
    pb_input : ProtoBuffer
        The serialized proto buffer input.

    Returns
    -------
    CmPricingOutput
        The pricing output.

    Raises
    ------
    Exception
        If pricing fails.
    """
    pb_output = CmPricingOutput()
    res_msg = process_request(req_name, pb_input)
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output

# CmEuropeanOptionPricer
def cm_european_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM European option.

    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.

    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    pb_input = dqCreateProtoCmEuropeanOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, b'', b'', b'', b'', 
                                                                                     scn_settings),
                                                         instrument)
    req_name = "CM_EUROPEAN_OPTION_PRICER"
    return run_cm_pricing(req_name,  pb_input.SerializeToString())

# CmAmericanOptionPricer
def cm_american_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM American option.

    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.

    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmAmericanOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                      mkt_data_set, pricing_settings, risk_settings, 
                                                                                      False, b'', b'', b'', b'', 
                                                                                      scn_settings),
                                                         instrument)
        req_name = "CM_AMERICAN_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())        
    except Exception as e:
        return str(e)

# CmAsianOptionPricer
def cm_asian_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Asian option.

    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.

    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmAsianOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date),
                                                                                      mkt_data_set, pricing_settings, risk_settings, 
                                                                                      False, b'', b'', b'', b'', 
                                                                                      scn_settings),
                                                         instrument)
        req_name = "CM_ASIAN_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())        
    except Exception as e:
        return str(e)

# CmDigitalOptionPricer
def cm_digital_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Digital option.

    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.

    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmDigitalOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date),
                                                                                      mkt_data_set, pricing_settings, risk_settings, 
                                                                                      False, b'', b'', b'', b'', 
                                                                                      scn_settings),
                                                         instrument)
        req_name = "CM_DIGITAL_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())  
    except Exception as e:
        return str(e)

# CmSingleBarrierOptionPricer
def cm_single_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Single Barrier option.

    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.

    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmSingleBarrierOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                      mkt_data_set, pricing_settings, risk_settings, 
                                                                                      False, b'', b'', b'', b'', 
                                                                                      scn_settings),
                                                         instrument)
        req_name = "CM_SINGLE_BARRIER_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())  
    except Exception as e:
        return str(e)
        
#CmDoubleBarrierOptionPricer
def cm_double_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Double Barrier option.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmDoubleBarrierOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                      mkt_data_set, pricing_settings, risk_settings, 
                                                                                      False, b'', b'', b'', b'', 
                                                                                      scn_settings),
                                                         instrument)
        req_name = "CM_DOUBLE_BARRIER_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

def cm_one_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM One Touch option.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmOneTouchOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                      mkt_data_set, pricing_settings, risk_settings, 
                                                                                      False, b'', b'', b'', b'', 
                                                                                      scn_settings),
                                                         instrument)
        req_name = "CM_ONE_TOUCH_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

def cm_double_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Double Touch option.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmDoubleTouchOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                      mkt_data_set, pricing_settings, risk_settings, 
                                                                                      False, b'', b'', b'', b'', 
                                                                                      scn_settings),
                                                         instrument)
        req_name = "CM_DOUBLE_TOUCH_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())
    except Exception as e:
        return str(e)

def cm_range_accrual_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Range Accrual option.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmRangeAccrualOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                      mkt_data_set, pricing_settings, risk_settings, 
                                                                                      False, b'', b'', b'', b'', 
                                                                                      scn_settings),
                                                         instrument)
        req_name = "CM_RANGE_ACCRUAL_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString())
    except Exception as e:
        return str(e)

def cm_single_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Single Shark Fin option.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmSingleSharkFinOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date),
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, b'', b'', b'', b'', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_SINGLE_SHARK_FIN_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

def cm_double_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Double Shark Fin option.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmDoubleSharkFinOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, b'', b'', b'', b'', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_DOUBLE_SHARK_FIN_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

def cm_ping_pong_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Ping Pong option.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmPingPongOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, b'', b'', b'', b'', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_PING_PONG_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

def cm_airbag_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Airbag option.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmAirbagOptionPricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, b'', b'', b'', b'', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_AIRBAG_OPTION_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

def cm_snowball_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Snowball Auto Callable Note.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmSnowballAutoCallableNotePricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, b'', b'', b'', b'', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_SNOWBALL_AUTOCALLABLE_NOTE_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)

def cm_phoenix_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price a CM Phoenix Auto Callable Note.
    
    Parameters
    ----------
    instrument : Instrument
        The option instrument.
    pricing_date : datetime
        The pricing date.
    mkt_data_set : MarketDataSet
        The market data set.
    pricing_settings : PricingSettings
        The pricing settings.
    risk_settings : RiskSettings
        The risk settings.
    scn_settings : ScenarioSettings
        The scenario settings.
    
    Returns
    -------
    CmPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoCmPhoenixAutoCallableNotePricingInput(dqCreateProtoCmPricingInput(create_date(pricing_date), 
                                                                                     mkt_data_set, pricing_settings, risk_settings, 
                                                                                     False, b'', b'', b'', b'', 
                                                                                     scn_settings),
                                                         instrument)
        req_name = "CM_PHOENIX_AUTOCALLABLE_NOTE_PRICER"
        return run_cm_pricing(req_name,  pb_input.SerializeToString()) 
    except Exception as e:
        return str(e)
