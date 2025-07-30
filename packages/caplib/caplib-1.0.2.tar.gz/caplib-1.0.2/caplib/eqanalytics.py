from datetime import datetime

from caplib.numerics import *
from caplib.market import *
from caplib.datetime import *
from caplib.analytics import *
from caplib.processrequest import process_request


def create_eq_risk_settings(ir_curve_settings,
                            price_settings,
                            vol_settings,
                            price_vol_settings,
                            dividend_curve_settings,
                            theta_settings):
    """
    Create equity risk settings.

    Parameters
    ----------
    ir_curve_settings : IrCurveRiskSettings
        Settings for interest rate curve risk.
    price_settings : PriceRiskSettings
        Settings for price risk.
    vol_settings : VolRiskSettings
        Settings for volatility risk.
    price_vol_settings : PriceVolRiskSettings
        Settings for price-volatility risk.
    dividend_curve_settings : DividendCurveRiskSettings
        Settings for dividend curve risk.
    theta_settings : ThetaRiskSettings
        Settings for theta risk.

    Returns
    -------
    EqRiskSettings
        The created equity risk settings.
    """

    return dqCreateProtoEqRiskSettings(ir_curve_settings,
                                       price_settings,
                                       vol_settings,
                                       price_vol_settings,
                                       theta_settings,
                                       dividend_curve_settings)


def create_eq_mkt_data_set(as_of_date: datetime,
                           discount_curve,
                           underlying_price,
                           vol_surf,
                           dividend_curve,
                           quanto_discount_curve,
                           quanto_fx_vol_curve,
                           quanto_correlation,
                           underlying: str = ''):
    """
    Create equity market data set.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the market data.
    discount_curve : DiscountCurve
        The discount curve for the equity.
    underlying_price : float
        The price of the underlying equity.
    vol_surf : VolatilitySurface
        The volatility surface for the equity.
    dividend_curve : DividendCurve
        The dividend curve for the equity.
    quanto_discount_curve : DiscountCurve, optional
        The quanto discount curve, if applicable.
    quanto_fx_vol_curve : VolatilityCurve, optional
        The quanto FX volatility curve, if applicable.
    quanto_correlation : float, optional
        The quanto correlation, if applicable.
    underlying : str, optional
        The identifier for the underlying equity.

    Returns
    -------
    ProtoEqMktDataSet
        The created equity market data set.
    """

    return dqCreateProtoEqMktDataSet(create_date(as_of_date),
                                     discount_curve,
                                     dividend_curve,
                                     underlying_price,
                                     vol_surf,
                                     quanto_discount_curve,
                                     quanto_fx_vol_curve,
                                     quanto_correlation,
                                     underlying)


# BuildEqIndexDividendCurve
def build_eq_index_dividend_curve(term_dates,
                                  future_prices,
                                  call_price_matrix,
                                  put_price_matrix,
                                  strike_matrix,
                                  spot,
                                  discount_curve):
    """
    Build an equity index dividend curve.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the dividend curve.
    term_dates : list
        List of term dates for the dividend curve.
    future_prices : list
        List of future prices corresponding to term dates.
    call_price_matrix : list of lists
        Matrix of call option prices.
    put_price_matrix : list of lists
        Matrix of put option prices.
    strike_matrix : list of lists
        Matrix of strike prices corresponding to option prices.
    spot : float
        The spot price of the underlying equity index.
    discount_curve : DiscountCurve
        The discount curve used for calculations.
    name : str
        Name of the dividend curve.

    Returns
    -------
    DividendCurve
        The built equity index dividend curve.

    Raises
    ------
    Exception
        If the curve building process fails.
    """

    try:
        p_call_price_matrix = [dqCreateProtoVector(row) for row in call_price_matrix]
        p_put_price_matrix = [dqCreateProtoVector(row) for row in put_price_matrix]
        p_strike_matrix = [dqCreateProtoVector(row) for row in strike_matrix]
        pb_input = dqCreateProtoEqIndexDividendCurveBuildingInput([create_date(d) for d in term_dates],
                                                                  p_call_price_matrix,
                                                                  p_put_price_matrix,
                                                                  p_strike_matrix,
                                                                  spot,
                                                                  discount_curve,
                                                                  dqCreateProtoVector(future_prices))
        req_name = "EQ_INDEX_DIVIDEND_CURVE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = EqIndexDividendCurveBuildingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.dividend_curve
    except Exception as e:
        return str(e)


# CreateEqOptionQuoteMatrix
def create_eq_option_quote_matrix(exercise_type: str,
                                  underlying_type: str,
                                  as_of_date: datetime,
                                  term_dates: list,
                                  payoff_types: list,
                                  option_prices: list,
                                  option_strikes: list,
                                  underlying: str = ''):
    """
    Create an equity option quote matrix.

    Parameters
    ----------
    exercise_type : str
        The type of option exercise.
    underlying_type : str
        The type of option underlying.
    as_of_date : datetime

    term_dates : list
        List of term dates.
    payoff_types : list
        List of payoff types.
    option_prices : list
        List of option prices.
    option_strikes : list
        List of option strike prices.
    underlying : str, optional
        The identifier for the underlying equity.

    Returns
    -------
    OptionQuoteMatrix
        The created option quote matrix.

    Raises
    ------
    Exception
        If the matrix creation process fails.
    """
    try:
        return create_option_quote_matrix(
            "OQVT_PRICE",
            "OQTT_ABOSULTE_TERM",
            "OQST_ABOSULTE_STRIKE",
            exercise_type,
            underlying_type,
            as_of_date,
            [],
            term_dates,
            payoff_types,
            option_prices,
            option_strikes,
            underlying)

    except Exception as e:
        return str(e)


# EqVolSurfaceBuilder
def eq_vol_surface_builder(as_of_date: datetime,
                           smile_method: str,
                           wing_strike_type: str,
                           lower: float,
                           upper: float,
                           option_quote_matrix,
                           underlying_prices: list,
                           discount_curve,
                           dividend_curve,
                           pricing_settings,
                           building_settings: list,
                           underlying: str):
    """
    Build an equity volatility surface.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the volatility surface.
    smile_method : str
        The smile method to be used.
    wing_strike_type : str
        The type of wing strike.
    lower : float
        The lower bound for the volatility surface.
    upper : float
        The upper bound for the volatility surface.
    option_quote_matrix : OptionQuoteMatrix
        The option quote matrix.
    underlying_prices : list
        List of underlying prices.
    discount_curve : str
        The discount curve.
    dividend_curve : str
        The dividend curve.
    pricing_settings : str
        The pricing settings.
    building_settings : list
        The building settings.
    underlying : str
        The identifier for the underlying equity.

    Returns
    -------
    VolatilitySurface
        The created volatility surface.

    Raises
    ------
    Exception
        If the volatility surface creation process fails.
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
        pb_input = dqCreateProtoEqVolatilitySurfaceBuildingInput(create_date(as_of_date),
                                                                 p_vol_surf_defintion,
                                                                 option_quote_matrix,
                                                                 dqCreateProtoVector(underlying_prices),
                                                                 discount_curve,
                                                                 dividend_curve,
                                                                 p_building_settings,
                                                                 pricing_settings,
                                                                 underlying)
        req_name = "EQ_VOLATILITY_SURFACE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = EqVolatilitySurfaceBuildingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)

        return pb_output.volatility_surface
    except Exception as e:
        return str(e)


def run_eq_pricing(req_name, pb_input):
    pb_output = EqPricingOutput()
    res_msg = process_request(req_name, pb_input)
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output


# EqEuropeanOptionPricer
def eq_european_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price an EQ European option.

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
    EqPricingOutput
        The pricing output.
    """
    pb_input = dqCreateProtoEqEuropeanOptionPricingInput(
        dqCreateProtoEqPricingInput(create_date(pricing_date),
                                    mkt_data_set, pricing_settings, risk_settings,
                                    False, b'', b'', b'', b'',
                                    scn_settings),
        instrument
    )
    req_name = "EQ_EUROPEAN_OPTION_PRICER"
    return run_eq_pricing(req_name, pb_input.SerializeToString())


def eq_american_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price an EQ American option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqAmericanOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_AMERICAN_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_asian_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price an EQ Asian option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqAsianOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_ASIAN_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_digital_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price an EQ Digital option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqDigitalOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_DIGITAL_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_single_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                    scn_settings):
    """
    Price an EQ Single Barrier option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqSingleBarrierOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_SINGLE_BARRIER_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_double_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                    scn_settings):
    """
    Price an EQ Double Barrier option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqDoubleBarrierOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_DOUBLE_BARRIER_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_one_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price an EQ One Touch option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqOneTouchOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_ONE_TOUCH_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_double_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                  scn_settings):
    """
    Price an EQ Double Touch option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqDoubleTouchOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_DOUBLE_TOUCH_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_range_accrual_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                   scn_settings):
    """
    Price an EQ Range Accrual option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqRangeAccrualOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_RANGE_ACCRUAL_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_single_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                      scn_settings):
    """
    Price an EQ Single Shark Fin option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqSingleSharkFinOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_SINGLE_SHARK_FIN_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_double_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                      scn_settings):
    """
    Price an EQ Double Shark Fin option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqDoubleSharkFinOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_DOUBLE_SHARK_FIN_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# EqPingPongOptionPricer
def eq_ping_pong_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price an EQ Ping Pong option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqPingPongOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_PING_PONG_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_airbag_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    """
    Price an EQ Airbag option.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqAirbagOptionPricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_AIRBAG_OPTION_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_snowball_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                          scn_settings):
    """
    Price an EQ Snowball Auto Callable Note.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqSnowballAutoCallableNotePricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_SNOWBALL_AUTOCALLABLE_NOTE_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


def eq_phoenix_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                         scn_settings):
    """
    Price an EQ Phoenix Auto Callable Note.

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
    EqPricingOutput
        The pricing output.
    """
    try:
        pb_input = dqCreateProtoEqPhoenixAutoCallableNotePricingInput(
            dqCreateProtoEqPricingInput(create_date(pricing_date),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "EQ_PHOENIX_AUTOCALLABLE_NOTE_PRICER"
        return run_eq_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# Demo function to show how to use the load_vol_surface_from_file function
def demo_load_vol_surface():
    """
    Demonstrates how to use the load_vol_surface_from_file function to build a volatility surface from a data file.

    Returns
    -------
    VolatilitySurface
        The built equity volatility surface.
    """
    import os

    # Define path to the data file
    file_path = r"D:\Work\Dev\caplib\data\eq_volatility_surface_builder.txt"

    # Call the function to load and parse the data
    vol_surface = load_vol_surface_from_file(file_path)

    return vol_surface
