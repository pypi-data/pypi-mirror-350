import numpy as np

from caplibproto.dqfxanalyticsservice_pb2 import FxNonDeliverableForwardPricingOutput, FxSwapPricingOutput, \
    FxForwardPricingOutput
from caplibproto.dqproto import dqCreateProtoFxRiskSettings, dqCreateProtoFxMktDataSet, \
    dqCreateProtoFxNonDeliverableForwardPricingInput, dqCreateProtoFxSwapPricingInput, \
    dqCreateProtoFxForwardPricingInput

from caplib.numerics import *
from caplib.market import *
from caplib.datetime import *
from caplib.analytics import *
from caplib.processrequest import process_request


def create_fx_risk_settings(ir_curve_settings,
                            price_settings,
                            vol_settings,
                            price_vol_settings,
                            theta_settings):
    """

    Parameters
    ----------
    ir_curve_settings: IrCurveRiskSettings
    price_settings: PriceRiskSettings
    vol_settings: VolRiskSettings
    price_vol_settings: PriceVolRiskSettings
    theta_settings: ThetaRiskSettings

    Returns
    -------
    FxRiskSettings

    """
    return dqCreateProtoFxRiskSettings(ir_curve_settings,
                                       price_settings,
                                       vol_settings,
                                       price_vol_settings,
                                       theta_settings)


def create_fx_mkt_data_set(as_of_date,
                           domestic_discount_curve,
                           foreign_discount_curve,
                           spot,
                           vol_surf):
    """

    Parameters
    ----------
    as_of_date: Date
    domestic_discount_curve: IrYieldCurve
    foreign_discount_curve: IrYieldCurve
    spot: FxSpotRate
    vol_surf: VolatilitySurface

    Returns
    -------
    FxMktDataSet

    """
    if vol_surf is not None:
        volatility_surface = vol_surf.volatility_surface
    else:
        volatility_surface = create_flat_volatility_surface(as_of_date, 0.0)
    return dqCreateProtoFxMktDataSet(create_date(as_of_date),
                                     domestic_discount_curve,
                                     foreign_discount_curve,
                                     spot,
                                     volatility_surface)


def fx_ndf_pricer(pricing_date,
                  instrument,
                  mkt_data,
                  pricing_settings,
                  risk_settings):
    """

    Parameters
    ----------
    pricing_date: Date
    instrument: FxNonDeliverableForwad
    mkt_data: FxMktDataSet
    pricing_settings: PricingSettings
    risk_settings: FxRiskSettings

    Returns
    -------
    PricingResults

    """
    pb_input = dqCreateProtoFxNonDeliverableForwardPricingInput(create_date(pricing_date),
                                                                instrument,
                                                                mkt_data,
                                                                pricing_settings,
                                                                risk_settings,
                                                                False, b'', b'', b'', b'')
    req_name = "FX_NONDELIVERABLE_FORWARD_PRICER"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxNonDeliverableForwardPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results


def fx_swap_pricer(pricing_date,
                   instrument,
                   mkt_data,
                   pricing_settings,
                   risk_settings):
    """

    Parameters
    ----------
    pricing_date: Date
    instrument: FxSwap
    mkt_data: FxMktDataSet
    pricing_settings: PricingSettings
    risk_settings: FxRiskSettings

    Returns
    -------
    PricingResults

    """
    pb_input = dqCreateProtoFxSwapPricingInput(create_date(pricing_date),
                                               instrument,
                                               mkt_data,
                                               pricing_settings,
                                               risk_settings,
                                               False, b'', b'', b'', b'')
    req_name = 'FX_SWAP_PRICER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxSwapPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results


def fx_forward_pricer(pricing_date,
                      instrument,
                      mkt_data,
                      pricing_settings,
                      risk_settings):
    """

    Parameters
    ----------
    pricing_date: Date
    instrument: FxForward
    mkt_data: FxMktDataSet
    pricing_settings: PricingSettings
    risk_settings: FxRiskSettings

    Returns
    -------
    PricingResults

    """
    pb_input = dqCreateProtoFxForwardPricingInput(create_date(pricing_date),
                                                  instrument,
                                                  mkt_data,
                                                  pricing_settings,
                                                  risk_settings,
                                                  False, b'', b'', b'', b'')
    req_name = 'FX_FORWARD_PRICER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxForwardPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results


# CreateFxOptionQuoteMatrix
def create_fx_option_quote_matrix(currency_pair,
                                  as_of_date,
                                  terms,
                                  deltas,
                                  quotes: np.array):
    pb_input = dqCreateProtoCreateFxOptionQuoteMatrixInput(to_ccy_pair(currency_pair),
                                                           create_date(as_of_date),
                                                           terms,
                                                           deltas,
                                                           create_matrix(quotes, False))
    req_name = "CREATE_FX_OPTION_QUOTE_MATRIX"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = CreateFxOptionQuoteMatrixOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.fx_option_quote_matrix


def create_fx_mkt_conventions(atm_type,
                              short_delta_type,
                              long_delta_type,
                              short_delta_cutoff,
                              risk_reversal,
                              smile_quote_type,
                              currency_pair):
    return dqCreateProtoFxMarketConventions(to_atm_type(atm_type),
                                            to_delta_type(short_delta_type),
                                            to_delta_type(long_delta_type),
                                            to_period(short_delta_cutoff),
                                            to_risk_reversal(risk_reversal),
                                            to_smile_quote_type(smile_quote_type),
                                            to_ccy_pair(currency_pair))


# CreateFxVolatilitySurface
def create_fx_volatility_surface(as_of_date,
                                 currency_pair,
                                 term_dates,
                                 strikes: np.array,
                                 vols: np.array,
                                 fx_market_conventions,
                                 vol_surf_definition):
    smile_strikes = list()
    for row in strikes:
        smile_strikes.append(dqCreateProtoVector(row.tolist()))
    smile_vols = list()
    for row in vols:
        smile_vols.append(dqCreateProtoVector(row.tolist()))
    pb_input = dqCreateProtoCreateFxVolatilitySurfaceInput(create_date(as_of_date),
                                                           to_ccy_pair(currency_pair),
                                                           [create_date(d) for d in term_dates],
                                                           smile_strikes, smile_vols,
                                                           vol_surf_definition,
                                                           currency_pair,
                                                           fx_market_conventions)

    req_name = "CREATE_FX_VOLATILITY_SURFACE"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = CreateFxVolatilitySurfaceOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.fx_volatility_surface


# CreateFlatFxVolatilitySurface
def create_flat_fx_volatility_surface(as_of_date: datetime,
                                      currency_pair: str,
                                      vol: float):
    start = as_of_date + timedelta(days=1)
    end = as_of_date + timedelta(days=365.25 * 100)
    term_dates = [start, end]
    strikes = np.array([[1.0e-4, 1.0e4], [1.0e-4, 1.0e4]])
    vols = np.array([[vol, vol], [vol, vol]])

    return create_fx_volatility_surface(as_of_date,
                                        currency_pair,
                                        term_dates,
                                        strikes,
                                        vols,
                                        create_fx_mkt_conventions('Atm_Spot',
                                                                  'Simple_Delta',
                                                                  'Simple_Delta',
                                                                  '1Y',
                                                                  'Rr_Call_Put',
                                                                  'Butterfly_Quote',
                                                                  currency_pair),
                                        create_volatility_surface_definition('Strike_Vol_Smile',
                                                                             'Linear_Smile_Method',
                                                                             'Flat_Extrap',
                                                                             'Linear_In_Variance',
                                                                             'Flat_In_Volatility',
                                                                             'ACT_365_FIXED'))


# FxVolatilitySurfaceBuilder
def fx_volatility_surface_builder(as_of_date,
                                  currency_pair,
                                  fx_market_conventions,
                                  quotes,
                                  fx_spot_rate,
                                  dom_discount_curve,
                                  for_discount_curve,
                                  vol_surf_definitions,
                                  vol_surf_building_settings):
    pb_input = dqCreateProtoFxVolatilitySurfaceBuildingInput(create_date(as_of_date),
                                                             to_ccy_pair(currency_pair),
                                                             fx_market_conventions,
                                                             quotes,
                                                             fx_spot_rate,
                                                             dom_discount_curve,
                                                             for_discount_curve,
                                                             vol_surf_definitions,
                                                             create_vol_surf_build_settings(
                                                                 vol_surf_building_settings[0],
                                                                 vol_surf_building_settings[1]),
                                                             currency_pair
                                                             )
    req_name = "FX_VOLATILITY_SURFACE_BUILDER"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxVolatilitySurfaceBuildingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.fx_volatility_surface


# region RunFxPricing
def run_fx_pricing(req_name, pb_input):
    pb_output = FxPricingOutput()
    res_msg = process_request(req_name, pb_input)
    pb_output = FxPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output


# FxEuropeanOptionPricer
def fx_european_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoFxEuropeanOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_EUROPEAN_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxAmericanOptionPricer
def fx_american_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:

        pb_input = dqCreateProtoFxAmericanOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_AMERICAN_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxAsianOptionPricer
def fx_asian_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoFxAsianOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_ASIAN_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxDigitalOptionPricer
def fx_digital_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoFxDigitalOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_DIGITAL_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxSingleBarrierOptionPricer
def fx_single_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                    scn_settings):
    try:
        pb_input = dqCreateProtoFxSingleBarrierOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_SINGLE_BARRIER_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxDoubleBarrierOptionPricer
def fx_double_barrier_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                    scn_settings):
    try:
        pb_input = dqCreateProtoFxDoubleBarrierOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_DOUBLE_BARRIER_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxOneTouchOptionPricer
def fx_one_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoFxOneTouchOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_ONE_TOUCH_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxDoubleTouchOptionPricer
def fx_double_touch_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                  scn_settings):
    try:
        pb_input = dqCreateProtoFxDoubleTouchOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_DOUBLE_TOUCH_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxRangeAccrualOptionPricer
def fx_range_accrual_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                   scn_settings):
    try:
        pb_input = dqCreateProtoFxRangeAccrualOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_RANGE_ACCRUAL_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxSingleSharkFinOptionPricer
def fx_single_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                      scn_settings):
    try:
        pb_input = dqCreateProtoFxSingleSharkFinOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_SINGLE_SHARK_FIN_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxDoubleSharkFinOptionPricer
def fx_double_shark_fin_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                      scn_settings):
    try:
        pb_input = dqCreateProtoFxDoubleSharkFinOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_DOUBLE_SHARK_FIN_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxPingPongOptionPricer
def fx_ping_pong_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoFxPingPongOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_PING_PONG_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxAirbagOptionPricer
def fx_airbag_option_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings, scn_settings):
    try:
        pb_input = dqCreateProtoFxAirbagOptionPricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_AIRBAG_OPTION_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxSnowballAutoCallableNotePricer
def fx_snowball_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                          scn_settings):
    try:
        pb_input = dqCreateProtoFxSnowballAutoCallableNotePricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_SNOWBALL_AUTOCALLABLE_NOTE_PRICER"
        return run_fx_pricing(req_name, pb_input.SerializeToString())
    except Exception as e:
        return str(e)


# FxPhoenixAutoCallableNotePricer
def fx_phoenix_auto_callable_note_pricer(instrument, pricing_date, mkt_data_set, pricing_settings, risk_settings,
                                         scn_settings):
    try:
        pb_input = dqCreateProtoFxPhoenixAutoCallableNotePricingInput(
            dqCreateProtoFxPricingInput(create_date(pricing_date), to_ccy_pair(instrument.underlying),
                                        mkt_data_set, pricing_settings, risk_settings,
                                        False, b'', b'', b'', b'', b'',
                                        scn_settings),
            instrument)
        req_name = "FX_PHOENIX_AUTOCALLABLE_NOTE_PRICER"
    except Exception as e:
        return str(e)


# FxDeltaToStrikeCalculator
def fx_delta_to_strike_calculator(delta_type, delta, expiry_date, vol_surf, fx_spot_rate, domestic_discount_curve,
                                  foreign_discount_curve):
    try:
        option_type = 'Call'
        if delta < 0:
            option_type = 'Put'
        pb_input = dqCreateProtoFxDeltaToStrikeCalculationInput(to_delta_type(delta_type),
                                                                delta,
                                                                to_payoff_type(option_type),
                                                                create_date(expiry_date),
                                                                fx_spot_rate,
                                                                domestic_discount_curve,
                                                                foreign_discount_curve,
                                                                vol_surf)

        req_name = "FX_DELTA_TO_STRIKE_CALCULATOR"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = FxDeltaToStrikeCalculationOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.strike
    except Exception as e:
        return str(e)


# FxAtmStrikeCalculator
def fx_atm_strike_calculator(atm_type, expiry_date, vol_surface, fx_spot_rate, domestic_discount_curve,
                             foreign_discount_curve):
    try:
        pb_input = dqCreateProtoFxAtmStrikeCalculationInput(to_atm_type(atm_type),
                                                            create_date(expiry_date),
                                                            fx_spot_rate,
                                                            domestic_discount_curve,
                                                            foreign_discount_curve,
                                                            vol_surface)

        req_name = "FX_ATM_STRIKE_CALCULATOR"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = FxAtmStrikeCalculationOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.strike

    except Exception as e:
        return str(e)


# GetFxVolatility
def get_fx_volatility(fx_vol_surf, terms, strike):
    try:
        return get_volatility(fx_vol_surf.volatility_surface, terms, strike)
    except Exception as e:
        return str(e)