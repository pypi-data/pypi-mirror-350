# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:46:51 2022

@author: dingq
"""

from caplib.analytics import *


# BondQuoteType
def to_bond_quote_type(src):
    '''
    将字符串转换为 BondQuoteType

    Parameters
    ----------
    src : str
        表示债券报价类型的字符串，如‘YIELD_TO_MATURITY’.

    Returns
    -------
    BondQuoteType

    '''
    if src is None:
        return YIELD_TO_MATURITY
    if src in ['', 'nan']:
        return YIELD_TO_MATURITY
    else:
        return BondQuoteType.DESCRIPTOR.values_by_name[src.upper()].number


# Bond Yield Curve Build Settings:
def create_bond_curve_build_settings(curve_name, curve_type,
                                     interp_method, extrap_method):
    '''


    Parameters
    ----------
    curve_name : str
        DESCRIPTION.
    curve_type : str, IrYieldCurveType
        DESCRIPTION.
    interp_method : str, InterpMethod
        DESCRIPTION.
    extrap_method : str, ExtrapMethod
        DESCRIPTION.
    Returns
    -------
    BondYieldCurveBuildSettings
        DESCRIPTION.

    '''
    p_build_settings = dqCreateProtoBondYieldCurveBuildSettings(curve_name.upper(),
                                                                to_ir_yield_curve_type(curve_type),
                                                                to_interp_method(interp_method),
                                                                to_extrap_method(extrap_method))
    return p_build_settings


# Bond Par Curve
def create_bond_par_curve(as_of_date, currency, inst_names, quotes, quote_type, curve_name):
    '''


    Parameters
    ----------
    as_of_date : Date
        DESCRIPTION.
    currency : str
        DESCRIPTION.
    inst_names : list
        DESCRIPTION.
    quotes : list
        DESCRIPTION.
    quote_type : BondQuoteType
        DESCRIPTION.
    curve_name : str
        DESCRIPTION.

    Returns
    -------
    BondParCurve
        DESCRIPTION.

    '''
    p_pillars = list()
    for i in range(len(inst_names)):
        pb_pillar = dqCreateProtoCreateBondParCurveInput_Pillar(inst_names[i].upper(), quotes[i])
        p_pillars.append(pb_pillar)

    pb_input = dqCreateProtoCreateBondParCurveInput(create_date(as_of_date),
                                                    currency.upper(),
                                                    p_pillars,
                                                    to_bond_quote_type(quote_type),
                                                    curve_name.upper())
    req_name = 'CREATE_BOND_PAR_CURVE'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = CreateBondParCurveOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.bond_par_curve


# Bond Yield Curve Builder:
def build_bond_yield_curve(build_settings,
                           curve_name,
                           as_of_date,
                           par_curve,
                           day_count='ACT_365_FIXED',
                           compounding_type='CONTINUOUS_COMPOUNDING',
                           freq='ANNUAL',
                           build_method='BOOTSTRAPPING_METHOD',
                           calc_jacobian=False,
                           fwd_curve=None):
    '''


    Parameters
    ----------
    build_settings : BondYieldCurveBuildSettings
        DESCRIPTION.
    curve_name : str
        DESCRIPTION.
    as_of_date : Date
        DESCRIPTION.
    par_curve : BondParCurve
        DESCRIPTION.
    day_count : DayCountConvention, optional
        DESCRIPTION. The default is ACT_365_FIXED.
    compounding_type : CompoundingType, optional
        DESCRIPTION. The default is CONTINUOUS_COMPOUNDING.
    freq : Frequency, optional
        DESCRIPTION. The default is ANNUAL.
    fwd_curve : IrYieldCurve, optional
        Forward curve for floating index. The default is None.
    build_method : IrYieldCurveBuildingMethod, optional
        DESCRIPTION. The default is BOOTSTRAPPING_METHOD.
    calc_jacobian : bool, optional
        DESCRIPTION. The default is False.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    IrYieldCurve
        DESCRIPTION.

    '''
    pb_settings_container = dqCreateProtoBondYieldCurveBuildSettingsContainer(curve_name.upper(),
                                                                              build_settings,
                                                                              par_curve,
                                                                              to_day_count_convention(day_count),
                                                                              to_compounding_type(compounding_type),
                                                                              to_frequency(freq))
    if fwd_curve is None:
        fwd_curve = create_flat_ir_yield_curve(as_of_date, par_curve.currency, 0.0)
    pb_input = dqCreateProtoBondYieldCurveBuildingInput(create_date(as_of_date),
                                                        [pb_settings_container],
                                                        fwd_curve,
                                                        to_ir_yield_curve_building_method(build_method),
                                                        calc_jacobian)

    req_name = 'BOND_YIELD_CURVE_BUILDER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = BondYieldCurveBuildingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.ir_yield_curve


# Build Bond Credit Spread Curve:
def build_bond_sprd_curve(build_settings,
                          curve_name,
                          as_of_date,
                          par_curve,
                          discount_curve,
                          build_method=BOOTSTRAPPING_METHOD,
                          calc_jacobian=False,
                          fwd_curve=None):
    '''


    Parameters
    ----------
    build_settings : BondYieldCurveBuildSettings
        DESCRIPTION.
    curve_name : TYPE
        DESCRIPTION.
    as_of_date : TYPE
        DESCRIPTION.
    par_curve : BondParCurve
        DESCRIPTION.
    discount_curve : IrYieldCurve
        DESCRIPTION.
    fwd_curve : IrYieldCurve, optional
        Forward curve for floating index. The default is None.
    build_method : IrYieldCurveBuildingMethod, optional
        DESCRIPTION. The default is BOOTSTRAPPING_METHOD.
    calc_jacobian : bool, optional
        DESCRIPTION. The default is False.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    CreditCurve
        DESCRIPTION.

    '''
    if fwd_curve is None:
        fwd_curve = create_flat_ir_yield_curve(as_of_date, par_curve.currency, 0.0)
    pb_input = dqCreateProtoBondCreditSpreadCurveBuildingInput(create_date(as_of_date),
                                                               par_curve, discount_curve, fwd_curve,
                                                               curve_name,
                                                               to_ir_yield_curve_building_method(build_method),
                                                               calc_jacobian)

    req_name = 'BOND_CREDIT_SPREAD_CURVE_BUILDER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = BondCreditSpreadCurveBuildingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.credit_sprd_curve


# IR Market Data Set:
def create_fi_mkt_data_set(as_of_date,
                           discount_curve,
                           credit_sprd_curve,
                           forward_curve,
                           underlying_discount_curve,
                           underlying_income_curve):
    '''


    Parameters
    ----------
    as_of_date : Date
        DESCRIPTION.
    discount_curve : IrYieldCurve
        DESCRIPTION.
    credit_sprd_curve : CreditCurve
        DESCRIPTION.
    forward_curve : IrYieldCurve
        DESCRIPTION.
    underlying_discount_curve : IrYieldCurve
        DESCRIPTION.
    underlying_income_curve : IrYieldCurve
        DESCRIPTION.

    Returns
    -------
    IrMktDataSet
        DESCRIPTION.

    '''
    return dqCreateProtoFiMktDataSet(create_date(as_of_date),
                                     discount_curve,
                                     credit_sprd_curve,
                                     forward_curve,
                                     underlying_discount_curve,
                                     underlying_income_curve)


# FI Risk Settings:
def create_fi_risk_settings(ir_curve_settings,
                            cs_curve_settings,
                            theta_settings):
    '''


    Parameters
    ----------
    ir_curve_settings : IrCurveRiskSettings
        DESCRIPTION.
    cs_curve_settings : CreditCurveRiskSettings
        DESCRIPTION.
    theta_settings : ThetaRiskSettings
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return dqCreateProtoFiRiskSettings(ir_curve_settings,
                                       cs_curve_settings,
                                       theta_settings)


# Vanilla Bond Pricer
def vanilla_bond_pricer(instrument, pricing_date, mkt_data, pricing_settings, risk_settings):
    '''


    Parameters
    ----------
    instrument : VanillaBond
        DESCRIPTION.
    pricing_date : Date
        DESCRIPTION.
    mkt_data : FiMktDataSet
        DESCRIPTION.
    pricing_settings : PricingSettings
        DESCRIPTION.
    risk_settings : FiRiskSettings
        DESCRIPTION.

    Returns
    -------
    PricingResults
        DESCRIPTION.

    '''
    pb_input = dqCreateProtoVanillaBondPricingInput(create_date(pricing_date), instrument, mkt_data, pricing_settings,
                                                    risk_settings,
                                                    False, b'', b'', b'', b'')
    req_name = 'VANILLA_BOND_PRICER'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = VanillaBondPricingOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.results


# Yield to Maturity calculator
def yield_to_maturity_calculator(calculation_date, compounding_type, bond, forward_curve, price, price_type, frequency):
    '''


    Parameters
    ----------
    calculation_date : Date
        DESCRIPTION.
    compounding_type : CompoundingType
        DESCRIPTION.
    bond : VanillaBond
        DESCRIPTION.
    forward_curve : IrYieldCurve
        DESCRIPTION.
    price : float
        DESCRIPTION.
    price_type : BondQuoteType
        DESCRIPTION.
    frequency : Frequency
        DESCRIPTION.

    Returns
    -------
    float
        DESCRIPTION.

    '''
    if forward_curve is None:
        forward_curve = create_flat_ir_yield_curve(calculation_date, bond.leg.interest_rate_leg.leg_definition.currency,
                                                   0.0)

    pb_input = dqCreateProtoYieldToMaturityCalculationInput(create_date(calculation_date),
                                                            to_compounding_type(compounding_type),
                                                            bond, forward_curve, price,
                                                            to_bond_quote_type(price_type), to_frequency(frequency))

    req_name = 'YIELD_TO_MATURITY_CALCULATOR'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = YieldToMaturityCalculationOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.yield_to_maturity


# Par Rate calculator
def fixed_cpn_bond_par_rate_calculator(calculation_date, bond, bond_yield_curve, bond_sprd_curve):
    '''


    Parameters
    ----------
    calculation_date : datetime
        DESCRIPTION.
    bond : VanillaBond
        DESCRIPTION.
    bond_yield_curve : IrYieldCurve
        DESCRIPTION.
    bond_sprd_curve : CreditCurve
        DESCRIPTION.

    Returns
    -------
    float
        DESCRIPTION.

    '''
    if bond_yield_curve is None:
        raise Exception('Empty bond yield curve!')
    if bond_sprd_curve is None:
        credit_sprd_curve = create_flat_credit_curve(calculation_date, 0.0)
    else:
        credit_sprd_curve = bond_sprd_curve

    mkt_data = create_fi_mkt_data_set(calculation_date,
                                      bond_yield_curve,
                                      credit_sprd_curve,
                                      bond_yield_curve,
                                      bond_yield_curve,
                                      bond_yield_curve)

    pb_input = dqCreateProtoFixedCpnBondParRateCalculationInput(create_date(calculation_date), bond, mkt_data)

    req_name = 'FIXED_CPN_BOND_PAR_RATE_CALCULATOR'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FixedCpnBondParRateCalculationOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.par_rate