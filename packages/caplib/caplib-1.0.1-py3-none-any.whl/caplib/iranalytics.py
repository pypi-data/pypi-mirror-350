# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:46:51 2022

@author: dingq
"""

from caplibproto.dqproto import *

from caplib.processrequest import *
from caplib.datetime import *
from caplib.analytics import *


# IR Yield Curve Build Settings:
def create_ir_curve_build_settings(curve_name, discount_curves, forward_curves, use_on_tn_fx_swap=False):
    '''
    Create a settings object for building IR yield curve.

    Parameters
    ----------
    curve_name : str
        DESCRIPTION.
    discount_curves : dict
        DESCRIPTION.
    forward_curves : dict
        DESCRIPTION.
    use_on_tn_fx_swap : bool, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    IrYieldCurveBuildSettings
        DESCRIPTION.

    '''
    p_discount_curves = list()
    for dc in discount_curves:
        p_discount_curve = dqCreateProtoIrYieldCurveBuildSettings_DiscountCurveManager_Curve(dc, discount_curves[dc])
        p_discount_curves.append(p_discount_curve)
    dc_manager = dqCreateProtoIrYieldCurveBuildSettings_DiscountCurveManager(p_discount_curves)
    p_forward_curves = list()
    for fc in forward_curves:
        p_fwd_curve = dqCreateProtoIrYieldCurveBuildSettings_ForwardCurveManager_Curve(fc, forward_curves[fc])
        p_forward_curves.append(p_fwd_curve)
    fc_manager = dqCreateProtoIrYieldCurveBuildSettings_ForwardCurveManager(p_forward_curves)
    return dqCreateProtoIrYieldCurveBuildSettings(curve_name, use_on_tn_fx_swap, dc_manager, fc_manager)


# IR Par Rate Curve
def create_ir_par_rate_curve(as_of_date, currency, curve_name, inst_names, inst_types, inst_terms, factors, quotes):
    '''
    Create an IR par rate curve object.

    Parameters
    ----------
    as_of_date : Date
        DESCRIPTION.
    currency : str
        DESCRIPTION.
    curve_name : str
        DESCRIPTION.
    inst_names : list
        DESCRIPTION.
    inst_types : list
        DESCRIPTION.
    inst_terms : list
        DESCRIPTION.
    factors : list
        DESCRIPTION.
    quotes : list
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    IrParRateCurve
        DESCRIPTION.

    '''
    pb_input = dqCreateProtoCreateIrParRateCurveInput(create_date(as_of_date),
                                                      currency, curve_name,
                                                      inst_names, inst_types, inst_terms, factors, quotes)
    req_name = 'CREATE_IR_PAR_RATE_CURVE'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = CreateIrParRateCurveOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.ir_par_rate_curve


# IR Single Ccy Curve Builder:
def ir_single_ccy_curve_builder(as_of_date, target_curves, build_settings, par_curves,
                                day_count,
                                compounding_type, frequency,
                                other_curves,
                                building_method = 'BOOTSTRAPPING_METHOD',
                                calc_jacobian = False,
                                shift = 1.0e-4,
                                finite_difference_method = 'CENTRAL_DIFFERENCE_METHOD',
                                threading_mode = 'SINGLE_THREADING_MODE'):
    '''
    Build an IR single currency yield curve or two curves simultanesouly.

    Parameters
    ----------
    as_of_date : Date
        DESCRIPTION.
    target_curves : list
        DESCRIPTION.
    build_settings : list
        list of IrYieldCurveBuildSettings.
    par_curves : list
        list of IrParRateCurve.
    day_count : DayCountConvention
        list of .
    compounding_type : CompoundingType
        DESCRIPTION.
    frequency : Frequency
        DESCRIPTION.
    other_curves : list
        DESCRIPTION.
    building_method : IrYieldCurveBuildingMethod
        DESCRIPTION.

    Returns
    -------
    IrYieldCurve
        DESCRIPTION.

    '''
    p_build_settings = list()
    for i in range(len(target_curves)):
        p_build_settings.append(
            dqCreateProtoIrSingleCurrencyCurveBuildingInput_IrYieldCurveBuildSettingsContainer(target_curves[i],
                                                                                               build_settings[i],
                                                                                               par_curves[i],
                                                                                               to_day_count_convention(day_count),
                                                                                               to_compounding_type(compounding_type),
                                                                                               to_frequency(frequency)))
    pb_input = dqCreateProtoIrSingleCurrencyCurveBuildingInput(create_date(as_of_date), p_build_settings, other_curves,
                                                               to_ir_yield_curve_building_method(building_method),
                                                               calc_jacobian,
                                                               shift,
                                                               to_finite_difference_method(finite_difference_method),
                                                               to_threading_mode(threading_mode))
    req_name = 'IR_SINGLE_CURRENCY_CURVE_BUILDER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = IrSingleCurrencyCurveBuildingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.target_curves


# IR Market Data Set:
def create_ir_mkt_data_set(as_of_date,
                           discount_curve,
                           underlyings,
                           forward_curves):
    '''
    Create a set of market data, including discount curve, forward curves.

    Parameters
    ----------
    as_of_date : Date
        DESCRIPTION.
    discount_curve : IrYieldCurve
        DESCRIPTION.
    underlyings : list
        DESCRIPTION.
    forward_curves : list
        list of IrYieldCurve.

    Returns
    -------
    IrMktDataSet
        DESCRIPTION.

    '''
    return dqCreateProtoIrMktDataSet(create_date(as_of_date), discount_curve, underlyings, forward_curves)

#CreateCrossCcyMktDataSet
def create_cross_ccy_mkt_data_set(as_of_date,
                                  base_discount_curve,
                                  xccy_discount_curve,
                                  underlying_interest_rates: list,
                                  underlying_forward_curves: list,
                                  fx_spot_rate):
    return dqCreateProtoIrCrossCcyMktDataSet(create_date(as_of_date),
                                                     base_discount_curve,
                                                     underlying_interest_rates,
                                                     underlying_forward_curves,
                                                     xccy_discount_curve,
                                                     fx_spot_rate)


# IR Risk Settings:
def create_ir_risk_settings(ir_curve_settings,
                            theta_settings):
    '''
    Create a settings object for calculating sensitivities of IR instruments.

    Parameters
    ----------
    ir_curve_settings : IrCurveRiskSettings
        DESCRIPTION.
    theta_settings : ThetaRiskSettings
        DESCRIPTION.

    Returns
    -------
    IrRiskSettings
        DESCRIPTION.

    '''
    return dqCreateProtoIrRiskSettings(ir_curve_settings, theta_settings)


def create_xccy_ir_risk_settings(ir_curve_settings,
                                 fx_settings,
                                 theta_settings):
    return dqCreateProtoXccyIrRiskSettings(ir_curve_settings, theta_settings, fx_settings)

# IR Vanilla Instrument Pricer
def ir_vanilla_instrument_pricer(instrument, pricing_date, mkt_data, pricing_settings, risk_settings):
    '''
    Price an IR flow instrument, i.e. Deposit, FRA, Swap, etc.

    Parameters
    ----------
    instrument : IrVanillaInstrument
        DESCRIPTION.
    pricing_date : Date
        DESCRIPTION.
    mkt_data : IrMktDataSet
        DESCRIPTION.
    pricing_settings : PricingSettings
        DESCRIPTION.
    risk_settings : IrRiskSettings
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    PricingResults
        DESCRIPTION.

    '''
    pb_input = dqCreateProtoIrVanillaInstrumentPricingInput(create_date(pricing_date), instrument, mkt_data, pricing_settings,
                                                            risk_settings,
                                                            False, b'', b'', b'', b'')
    req_name = 'IR_VANILLA_INSTRUMENT_PRICER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = IrVanillaInstrumentPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results


def ir_cross_ccy_curve_builder(as_of_date,
                               target_curves,
                               build_settings,
                               par_curves,
                               day_count,
                               compounding_type,
                               frequency,
                               other_curves,
                               fx_spot,
                               building_method = 'BOOTSTRAPPING_METHOD',
                               calc_jacobian = False,
                               shift = 1.0e-4,
                               finite_difference_method = 'CENTRAL_DIFFERENCE_METHOD',
                               threading_mode = 'SINGLE_THREADING_MODE'):
    """
    Build an IR cross currency yield curve.

    Parameters
    ----------
    as_of_date: Date
    target_curves: List[str]
    build_settings: List[IrYieldCurveBuildSettings]
    par_curves: List[IrParRateCurve]
    day_count: DayCountConvention
    compounding_type: CompoundingType
    frequency: Frequency
    other_curves: List[IrYieldCurve]
    fx_spot: FxSpotRate

    Returns
    -------
    IrYieldCurve

    """
    p_build_settings = list()
    for i in range(len(target_curves)):
        p_build_settings.append(
            dqCreateProtoIrCrossCurrencyCurveBuildingInput_IrYieldCurveBuildSettingsContainer(target_curves[i],
                                                                                              build_settings[i],
                                                                                              par_curves[i],
                                                                                              to_day_count_convention(day_count),
                                                                                              to_compounding_type(compounding_type),
                                                                                              to_frequency(frequency)))
    pb_input = dqCreateProtoIrCrossCurrencyCurveBuildingInput(create_date(as_of_date),
                                                              p_build_settings,
                                                              other_curves,
                                                              fx_spot,
                                                              to_ir_yield_curve_building_method(building_method),
                                                              calc_jacobian,
                                                              shift,
                                                              to_finite_difference_method(finite_difference_method),
                                                              to_threading_mode(threading_mode))
    req_name = 'IR_CROSS_CURRENCY_CURVE_BUILDER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = IrCrossCurrencyCurveBuildingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.target_curves

def cross_currency_swap_pricer(instrument,
                               pricing_date,
                               mkt_data,
                               pricing_settings,
                               risk_settings):
    """
    Price a cross currency swap.

    Parameters
    ----------
    instrument : CrossCurrencySwap
        The cross currency swap instrument.
    pricing_date : datetime
        The date for pricing.
    mkt_data : MarketDataSet
        The market data set for pricing.
    pricing_settings : PricingSettings
        The pricing settings for the swap.
    risk_settings : RiskSettings
        The risk settings for the swap.

    Returns
    -------
    PricingResults
        The result of the cross currency swap pricing.
    """
    pb_input = dqCreateProtoCrossCurrencySwapPricingInput(create_date(pricing_date),
                                                          instrument,
                                                          pricing_settings,
                                                          mkt_data,
                                                          risk_settings,
                                                          False, b'', b'', b'', b'')
    req_name = 'IR_CROSS_CURRENCY_SWAP_PRICER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = CrossCurrencySwapPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results