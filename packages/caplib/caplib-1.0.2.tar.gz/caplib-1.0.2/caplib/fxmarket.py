# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 13:27:58 2022

@author: dingq
"""
from caplib.market import *
from caplib.datetime import *
from caplib.staticdata import *

# FX Forward Template
def create_fx_forward_template(inst_name,
                               fixing_offset,
                               currency_pair,
                               delivery_day_convention,
                               fixing_day_convention,
                               calendars):
    """
    Create a fx forward template object.

    Parameters
    ----------
    inst_name: str
    fixing_offset: str
    currency_pair: str
    delivery_day_convention: str
    fixing_day_convention: str
    calendars: list

    Returns
    -------
    FxForwardTemplate

    """
    p_type = FX_FORWARD
    p_currency_pair = to_ccy_pair(currency_pair)
    p_delivery_day_convention = to_business_day_convention(delivery_day_convention)
    p_fixing_offset = to_period(fixing_offset)
    p_fixing_day_convention = to_business_day_convention(fixing_day_convention)

    pb_data = dqCreateProtoFxForwardTemplate(p_type,
                                             inst_name,
                                             p_fixing_offset,
                                             p_currency_pair,
                                             p_delivery_day_convention,
                                             p_fixing_day_convention,
                                             calendars)

    pb_data_list = dqCreateProtoFxForwardTemplateList([pb_data])
    create_static_data('SDT_FX_FORWARD', pb_data_list.SerializeToString())
    return pb_data


# FX Swap Template
def create_fx_swap_template(inst_name,
                            start_convention,
                            currency_pair,
                            calendars,
                            start_day_convention,
                            end_day_convention,
                            fixing_offset,
                            fixing_day_convention):
    """
    Create a fx swap template object.

    Parameters
    ----------
    inst_name: str
    start_convention: str
    currency_pair: str
    calendars: list
    start_day_convention: str
    end_day_convention: str
    fixing_offset: str
    fixing_day_convetion: BusinessDayConvention

    Returns
    -------
    FxSwapTemplate

    """

    p_type = FX_SWAP
    p_start_convention = to_instrument_start_convention(start_convention) 
    p_currency_pair = to_ccy_pair(currency_pair)
    p_start_day_convention = to_business_day_convention(start_day_convention)
    p_end_day_convention = to_business_day_convention(end_day_convention)
    p_fixing_offset = to_period(fixing_offset)
    p_fixing_day_convention = to_business_day_convention(fixing_day_convention)
    pb_data = dqCreateProtoFxSwapTemplate(p_type,
                                          inst_name,
                                          p_start_convention,
                                          p_currency_pair,
                                          calendars,
                                          p_start_day_convention,
                                          p_end_day_convention,
                                          p_fixing_offset,
                                          p_fixing_day_convention)
    pb_data_list = dqCreateProtoFxSwapTemplateList([pb_data])
    create_static_data('SDT_FX_SWAP', pb_data_list.SerializeToString())
    return pb_data


# FX Ndf Template
def create_fx_ndf_template(inst_name,
                           fixing_offset,
                           currency_pair,
                           delivery_day_convention,
                           fixing_day_convention,
                           calendars,
                           settlement_currency):
    """
    Create a fx ndf template object.

    Parameters
    ----------
    inst_name: str
    fixing_offset: str
    currency_pair: str
    delivery_day_convention: str
    fixing_day_convention: str
    calendars: list
    settlement_currency: str

    Returns
    -------
    FxNdfTemplate

    """
    p_type = FX_NON_DELIVERABLE_FORWARD
    p_fixing_offset = to_period(fixing_offset)
    p_currency_pair = to_ccy_pair(currency_pair)
    p_delivery_day_convention = to_business_day_convention(delivery_day_convention)    
    p_fixing_day_convention = to_business_day_convention(fixing_day_convention)
    pb_data = dqCreateProtoFxNdfTemplate(p_type,
                                         inst_name,
                                         p_fixing_offset,
                                         p_currency_pair,
                                         p_delivery_day_convention,
                                         p_fixing_day_convention,
                                         calendars,
                                         settlement_currency)

    pb_data_list = dqCreateProtoFxNdfTemplateList([pb_data])
    create_static_data('SDT_FX_NDF', pb_data_list.SerializeToString())
    return pb_data


# FX Non Deliverable Forwad
def create_fx_non_deliverable_forwad(buy_currency,
                                     buy_amount,
                                     sell_currency,
                                     sell_amount,
                                     delivery_date,
                                     expiry_date,
                                     settlement_currency):
    """
    Create a fx non deliverable forwad instrument object.

    Parameters
    ----------
    buy_currency: str
    buy_amount: float
    sell_currency: str
    sell_amount: float
    delivery_date: Date
    expiry_date: Date
    settlement_currency: str

    Returns
    -------
    FxNonDeliverableForwad

    """
    return dqCreateProtoFxNonDeliverableForward(buy_currency,
                                                               buy_amount,
                                                               sell_currency,
                                                               sell_amount,
                                                               create_date(delivery_date),
                                                               create_date(expiry_date),
                                                               settlement_currency)

# FX Swap
def create_fx_swap(near_buy_currency,
                   near_buy_amount,
                   near_sell_currency,
                   near_sell_amount,
                   near_delivery_date,
                   near_expiry_date,
                   far_buy_currency,
                   far_buy_amount,
                   far_sell_currency,
                   far_sell_amount,
                   far_delivery_date,
                   far_expiry_date
                   ):
    """
    Create a fx swap instrument object.

    Parameters
    ----------
    near_buy_currency: str
    near_buy_amount: float
    near_sell_currency: str
    near_sell_amount: float
    near_delivery_date: Date
    near_expiry_date: Date
    far_buy_currency: str
    far_buy_amount: float
    far_sell_currency: str
    far_sell_amount: float
    far_delivery_date: Date
    far_expiry_date: Date

    Returns
    -------
    FxSwap

    """
    return dqCreateProtoFxSwap(near_buy_currency,
                                              near_buy_amount,
                                              near_sell_currency,
                                              near_sell_amount,
                                              create_date(near_delivery_date),
                                              create_date(near_expiry_date),
                                              far_buy_currency,
                                              far_buy_amount,
                                              far_sell_currency,
                                              far_sell_amount,
                                              create_date(far_delivery_date),
                                              create_date(far_expiry_date)
                                              )

# FX Forward
def create_fx_forward(buy_currency,
                      buy_amount,
                      sell_currency,
                      sell_amount,
                      delivery,
                      expiry):
    """
    Create a fx forward instrument object.

    Parameters
    ----------
    buy_currency: str
    buy_amount: float
    sell_currency: str
    sell_amount: float
    delivery: Date
    expiry: Date

    Returns
    -------
    FxForward

    """
    return dqCreateProtoFxForward(buy_currency,
                                  buy_amount,
                                  sell_currency,
                                  sell_amount,
                                  create_date(delivery),
                                  create_date(expiry))

#FxSpotDateCalculator
def fx_spot_date_calculator(calculation_date: datetime, 
                            currency_pair: str):
    
    pb_input = dqCreateProtoFxSpotDateCalculationInput(create_date(calculation_date),
                                                       to_ccy_pair(currency_pair))
    req_name = 'FX_SPOT_DATE_CALCULATOR'
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxSpotDateCalculationOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return datetime(pb_output.spot_date.year, pb_output.spot_date.month, pb_output.spot_date.day)

#FxOptionDateCalculator
def fx_option_date_calculator(calculation_date: datetime,
                                 currency_pair: str,
                                 term: str,
                                 business_day_convention: str,
                                 mode: str = ""):
    pb_input = dqCreateProtoFxOptionDateCalculationInput(create_date(calculation_date),
                                                       to_ccy_pair(currency_pair),
                                                       to_period(term),
                                                       to_business_day_convention(business_day_convention))
        
    req_name = "FX_OPTION_DATE_CALCULATOR"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    pb_output = FxOptionDateCalculationOutput()
    pb_output.ParseFromString(res_msg)
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return datetime(pb_output.spot_date.year, pb_output.spot_date.month, pb_output.spot_date.day)