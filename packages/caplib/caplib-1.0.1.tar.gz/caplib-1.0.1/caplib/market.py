# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 13:00:34 2022

@author: dingq
"""

from caplibproto.dqproto import *

from caplib.staticdata import create_static_data
from caplib.datetime import *

def to_time_series_mode(src):
    '''
    Convert a string to TimeSeries.Mode.
    
    Parameters
    ----------
    src : str
        a string of frequency, i.e. 'TS_FORWARD_MODE'.
    
    Returns
    -------
    None.

    '''
    if src is None:
        return TS_FORWARD_MODE
    if src in ['', 'nan']:
        return TS_FORWARD_MODE
    else:
        return TimeSeries.Mode.DESCRIPTOR.values_by_name[src.upper()].number

def to_underlying_type(src):
    '''
    将字符串转换为 UnderlyingType.

    Parameters
    ----------
    src : str

    Returns
    -------
    UnderlyingType

    '''
    if src is None:
        return SPOT_UNDERLYING_TYPE
    if src in ['', 'nan']:
        return SPOT_UNDERLYING_TYPE
    else:
        return OptionUnderlyingType.DESCRIPTOR.values_by_name[src.upper()].number

def to_exercise_type(src):
    '''
    将字符串转换为 ExerciseType.

    Parameters
    ----------
    src : str

    Returns
    -------
    ExerciseType

    '''
    if src is None:
        return EUROPEAN
    if src in ['', 'nan']:
        return EUROPEAN
    else:
        return ExerciseType.DESCRIPTOR.values_by_name[src.upper()].number


def to_payoff_type(src):
    '''
    将字符串转换为 PayoffType.

    Parameters
    ----------
    src : str

    Returns
    -------
    PayoffType

    '''
    if src is None:
        return CALL
    if src in ['', 'nan']:
        return CALL
    else:
        return PayoffType.DESCRIPTOR.values_by_name[src.upper()].number

def to_payment_type(src):
    '''
    将字符串转换为 PaymentType.

    Parameters
    ----------
    src : str

    Returns
    -------
    PaymentType

    '''
    if src is None:
        return PAY_AT_MATURITY
    if src in ['', 'nan']:
        return PAY_AT_MATURITY
    else:
        return PaymentType.DESCRIPTOR.values_by_name[src.upper()].number
    
def to_instrument_type(src):
    '''
    将字符串转换为 InstrumentType.

    Parameters
    ----------
    src : str

    Returns
    -------
    InstrumentType

    '''
    if src is None:
        return SPOT
    if src in ['', 'nan']:
        return SPOT
    else:
        return InstrumentType.DESCRIPTOR.values_by_name[src.upper()].number

def to_barrier_type(src):
    '''
    将字符串转换为 BarrierType.

    Parameters
    ----------
    src : str

    Returns
    -------
    BarrierType

    '''
    if src is None:
        return DOWN_OUT
    if src in ['', 'nan']:
        return DOWN_OUT
    else:
        return BarrierType.DESCRIPTOR.values_by_name[src.upper()].number
    
def to_performance_type(src):
    '''
    将字符串转换为 PerformanceType.

    Parameters
    ----------
    src : str

    Returns
    -------
    PerformanceType

    '''
    if src is None:
        return RELATIVE_PERFORM_TYPE
    if src in ['', 'nan']:
        return RELATIVE_PERFORM_TYPE
    else:
        return PerformanceType.DESCRIPTOR.values_by_name[src.upper()].number
    
def to_buy_sell_flag(src):
    '''
    将字符串转换为 BuySellFlag.

    Parameters
    ----------
    src : str

    Returns
    -------
    BuySellFlag

    '''
    if src is None:
        return BUY
    if src in ['', 'nan']:
        return BUY
    else:
        return BuySellFlag.DESCRIPTOR.values_by_name[src.upper()].number

def to_settlement_type(src):
    '''
    将字符串转换为 SettlementType.

    Parameters
    ----------
    src : str

    Returns
    -------
    SettlementType

    '''
    if src is None:
        return PHYSICAL_SETTLEMENT
    if src in ['', 'nan']:
        return PHYSICAL_SETTLEMENT
    else:
        return SettlementType.DESCRIPTOR.values_by_name[src.upper()].number
    
# Time Series
def create_time_series(dates,
                       values,
                       mode='TS_FORWARD_MODE',
                       name=''):
    '''
    Create a time series.
    
    Parameters
    ----------
    dates : list
        A list of datetime.The dates are type of Date.
    values : list
        A list of floating numbers.
    mode : TimeSeries.Mode, optional
        Mode indicates the time series is in the date ascending (forward) or descending (backward) order. The default is 'TS_FORWARD_MODE'.
    name : str, optional
        Name of time series given by user. The default is ''.
    
    Returns
    -------
    TimeSeries
        A time series object.
    
    '''
    p_dates = [create_date(d) for d in dates]
    p_values = dqCreateProtoMatrix(len(values), 1, values, Matrix.StorageOrder.ColMajor)
    return dqCreateProtoTimeSeries(p_dates, p_values, to_time_series_mode(mode), name.upper())


# Currency Pair
def to_ccy_pair(src):
    '''
    Create a currency pair. 
    
    Parameters
    ----------
    src : str
        a string of 6 chars, i.e. 'USDCNY', 'usdcny'.
    
    Returns
    -------
    CurrencyPair
        Object of CurrencyPair.
    
    '''
    left = src[0:3]
    right = src[3:6]
    return dqCreateProtoCurrencyPair(dqCreateProtoCurrency(left.upper()),
                                     dqCreateProtoCurrency(right.upper()))


#NotionalExchange
def to_notional_exchange(src):
    if src is None:
        return INVALID_NOTIONAL_EXCHANGE
    
    if src in ['', 'nan']:
        return INVALID_NOTIONAL_EXCHANGE
    else:
        return NotionalExchange.DESCRIPTOR.values_by_name[src.upper()].number
    
#InstrumentStartConvention
def to_instrument_start_convention(src):
    if src is None:
        return SPOTSTART
    
    if src in ['', 'nan']:
        return SPOTSTART
    else:
        return InstrumentStartConvention.DESCRIPTOR.values_by_name[src.upper()].number

#PayReceiveFlag
def to_pay_receive_flag(src):
    if src is None:
        return PAY
    
    if src in ['', 'nan']:
        return PAY
    else:
        return PayReceiveFlag.DESCRIPTOR.values_by_name[src.upper()].number

#NotionalType
def to_notional_type(src):
    if src is None:
        return CONST_NOTIONAL
    
    if src in ['', 'nan']:
        return CONST_NOTIONAL
    else:
        return NotionalType.DESCRIPTOR.values_by_name[src.upper()].number

#StrikeType
def to_strike_type(src):
    if src is None:
        return FIXED_STRIKE
    
    if src in ['', 'nan']:
        return FIXED_STRIKE
    else:
        return StrikeType.DESCRIPTOR.values_by_name[src.upper()].number

#AveragingMethod
def to_averaging_method(src):
    if src is None:
        return ARITHMETIC_AVERAGE_METHOD
    
    if src in ['', 'nan']:
        return ARITHMETIC_AVERAGE_METHOD
    else:
        return AveragingMethod.DESCRIPTOR.values_by_name[src.upper()].number

#EventObservationType
def to_event_observation_type(src):
    if src is None:
        return CONTINUOUS_OBSERVATION_TYPE
    
    if src in ['', 'nan']:
        return CONTINUOUS_OBSERVATION_TYPE
    else:
        return EventObservationType.DESCRIPTOR.values_by_name[src.upper()].number
    
#RiskReversal
def to_risk_reversal(src):
    if src is None:
        return RR_CALL_PUT
    
    if src in ['', 'nan']:
        return RR_CALL_PUT
    else:
        return RiskReversal.DESCRIPTOR.values_by_name[src.upper()].number

def create_fixing_schedule(fixing_dates: list, 
                           fixing_values: list,
                           fixing_weights: list):
    if len(fixing_dates) != len(fixing_values) or len(fixing_dates) != len(fixing_weights):
        raise ValueError("fixing_dates, fixing_values, and fixing_weights must have the same size.")
    
    rows = []
    for i in range(len(fixing_dates)):
        rows.append(dqCreateProtoFixingSchedule_Row(create_date(fixing_dates[i]), fixing_values[i], fixing_weights[i]))    
    return dqCreateProtoFixingSchedule(rows)

def create_foreign_exchange_rate(value,
                                 left_currency,
                                 right_currency):
    """
    创建一个外汇利率对象.

    Parameters
    ----------
    value: float
    base_currency: str
    target_currency: str

    Returns
    -------
    ForeignExchangeRate

    """
    return dqCreateProtoForeignExchangeRate(value,
                                            right_currency,
                                            left_currency)

def create_fx_spot_rate(fx_rate,
                        ref_date,
                        spot_date):
    """
    创建一个外汇即期利率对象.

    Parameters
    ----------
    fx_rate: ForeignExchangeRate
    ref_date: Date
    spot_date: Date

    Returns
    -------
    FxSpotRate

    """
    return dqCreateProtoFxSpotRate(fx_rate,
                                   create_date(ref_date),
                                   create_date(spot_date))

def create_fx_spot_template(inst_name,
                            currency_pair,
                            spot_day_convention,
                            calendars,
                            spot_delay):
    """
    Create a fx spot template object.

    :param inst_name: str
    :param currency_pair: str
    :param spot_day_convention: str
    :param calendars: list
    :param spot_delay: str
    :return: FxSpotTemplate
    """
    p_type = FX_SPOT
    p_currency_pair = to_ccy_pair(currency_pair)
    p_spot_day_convention = to_business_day_convention(spot_day_convention)
    p_spot_delay = to_period(spot_delay)
    pb_data = dqCreateProtoFxSpotTemplate(p_type,
                                          inst_name,
                                          p_currency_pair,
                                          p_spot_day_convention,
                                          calendars,
                                          p_spot_delay)
    pb_data_list = dqCreateProtoFxSpotTemplateList([pb_data])
    create_static_data('SDT_FX_SPOT', pb_data_list.SerializeToString())
    return pb_data

def create_barrier(barrier_type, barrier_value):
    return dqCreateProtoBarrier(to_barrier_type(barrier_type), barrier_value)

#CreateDigitalOption
def create_digital_option(payoff_type,
                          expiry,
                          delivery,
                          strike,
                          cash,
                          asset,
                          nominal,
                          payoff_ccy,
                          underlying_type,
                          underlying_ccy,
                          underlying):
    """
    Create a Digital Option.

    Parameters
    ----------
    payoff_type : str
        Type of the payoff.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    strike : float
        The strike price.
    cash : float
        Cash amount for the option.
    asset : float
        Asset amount for the option.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoDigitalOption
        A protocol buffer object representing the Digital Option.
    """
    return dqCreateProtoDigitalOption(to_payoff_type(payoff_type),
                                    create_date(expiry),
                                    create_date(delivery),
                                    strike,
                                    cash,
                                    asset,
                                    nominal,
                                    underlying,
                                    underlying_ccy,
                                    payoff_ccy,
                                    to_instrument_type(underlying_type))
    
#CreateEuropeanOption
def create_european_option(payoff_type,
                           expiry,
                           delivery,
                           strike,
                           nominal,
                           payoff_ccy,
                           underlying_type,
                           underlying_ccy,
                           underlying):
    """
    Create a European Option.

    Parameters
    ----------
    payoff_type : str
        Type of the payoff.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    strike : float
        The strike price.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    dqproto.EuropeanOption
        A protocol buffer object representing the European Option.
    """

    return dqCreateProtoEuropeanOption(to_payoff_type(payoff_type),
                                       strike,
                                       create_date(delivery),
                                       create_date(expiry),
                                       nominal,
                                       underlying,
                                       underlying_ccy,
                                       payoff_ccy,
                                       to_instrument_type(underlying_type))

#CreateAmericanOption
def create_american_option(payoff_type,
                           expiry,
                           strike,
                           settlement_days,
                           nominal,
                           payoff_ccy,
                           underlying_type,
                           underlying_ccy,
                           underlying):
    """
    Create an American Option.

    Parameters
    ----------
    payoff_type : str
        Type of the payoff.
    expiry : datetime
        Expiry date of the option.
    strike : float
        The strike price of the option.
    settlement_days : int
        Number of days for settlement.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoAmericanOption
        A protocol buffer object representing the American Option.
    """

    return dqCreateProtoAmericanOption(to_payoff_type(payoff_type),
                                       strike,
                                       create_date(expiry),
                                       create_date(expiry),
                                       settlement_days,
                                       nominal,
                                       underlying,
                                       underlying_ccy,
                                       payoff_ccy,
                                       to_instrument_type(underlying_type))
        
#CreateAsianOption
def create_asian_option(payoff_type,
                        expiry,
                        delivery,
                        strike_type,
                        strike,
                        avg_method,
                        obs_type,
                        fixing_schedule,
                        nominal,
                        payoff_ccy,
                        underlying_type,
                        underlying_ccy,
                        underlying):
    """
    Create an Asian Option.

    Parameters
    ----------
    payoff_type : str
        Type of the payoff.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    strike_type : str
        Type of the strike.
    strike : float
        The strike price.
    avg_method : str
        The averaging method.
    obs_type : str
        Type of observation.
    fixing_schedule : list
        Schedule for fixings.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    dqproto.AsianOption
        A protocol buffer object representing the Asian Option.
    """

    return dqCreateProtoAsianOption(to_payoff_type(payoff_type),
                                    to_averaging_method(avg_method),
                                    to_event_observation_type(obs_type),
                                    create_date(expiry),
                                    create_date(delivery),
                                    create_fixing_schedule(fixing_schedule[0], fixing_schedule[1], fixing_schedule[2]),
                                    to_strike_type(strike_type),
                                    strike,
                                    nominal,
                                    underlying,
                                    underlying_ccy,
                                    payoff_ccy,
                                    to_instrument_type(underlying_type))

#CreateOneTouchOption
def create_one_touch_option(expiry,
                            delivery,
                            barrier_type,
                            barrier_value,
                            barrier_obs_type,
                            obs_schedule,
                            payment_type,
                            cash,
                            asset,
                            settlement_days,
                            nominal,
                            payoff_ccy,
                            underlying_type,
                            underlying_ccy,
                            underlying):
    """
    Create a One Touch Option.

    Parameters
    ----------
    expiry : datetime
        The expiry date of the option.
    delivery : datetime
        The delivery date of the option.
    barrier_type : str
        The type of the barrier.
    barrier_value : float
        The value of the barrier.
    barrier_obs_type : str
        The type of barrier observation.
    obs_schedule : list
        The observation schedule for barriers.
    payment_type : str
        The type of payment.
    cash : float
        The cash amount for the option.
    asset : float
        The asset amount for the option.
    settlement_days : int
        The number of days for settlement.
    nominal : float
        The nominal value of the option.
    payoff_ccy : str
        The currency of the payoff.
    underlying_type : str
        The type of the underlying asset.
    underlying_ccy : str
        The currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoOneTouchOption
        A protocol buffer object representing the One Touch Option.
    """
    
    return dqCreateProtoOneTouchOption(asset, cash, create_date(expiry), create_date(delivery), 
                                       create_barrier(barrier_type, barrier_value),
                                       to_payment_type(payment_type),
                                       nominal,
                                       underlying,
                                       settlement_days,
                                       to_event_observation_type(barrier_obs_type),
                                       create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                       underlying_ccy,
                                       payoff_ccy,
                                       to_instrument_type(underlying_type))

#CreateDoubleTouchOption
def create_double_touch_option(expiry,
                               delivery,
                               lower_barrier_type,
                               lower_barrier_value,
                               upper_barrier_type,
                               upper_barrier_value,
                               barrier_obs_type,
                               obs_schedule,
                               payment_type,
                               cash,
                               asset,
                               settlement_days,
                               nominal,
                               payoff_ccy,
                               underlying_type,
                               underlying_ccy,
                               underlying):
    """
    Create a Double Touch Option.

    Parameters
    ----------
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    lower_barrier_type : str
        Type of the lower barrier.
    lower_barrier_value : float
        Value of the lower barrier.
    upper_barrier_type : str
        Type of the upper barrier.
    upper_barrier_value : float
        Value of the upper barrier.
    barrier_obs_type : str
        Type of barrier observation.
    obs_schedule : list
        Observation schedule for barriers.
    payment_type : str
        Type of payment.
    cash : float
        Cash amount for the option.
    asset : float
        Asset amount for the option.
    settlement_days : int
        Number of days for settlement.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoDoubleTouchOption
        A protocol buffer object representing the Double Touch Option.
    """
    
    return dqCreateProtoDoubleTouchOption(asset, cash, create_date(expiry), create_date(delivery),
                                         create_barrier(lower_barrier_type, lower_barrier_value),
                                         create_barrier(upper_barrier_type, upper_barrier_value),
                                         to_payment_type(payment_type),
                                         nominal,
                                         underlying,
                                         settlement_days,
                                         to_event_observation_type(barrier_obs_type),
                                         create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                         underlying_ccy,
                                         payoff_ccy,
                                         to_instrument_type(underlying_type))
#CreateSingleBarrierOption
def create_single_barrier_option(payoff_type,
                                 strike,
                                 expiry,
                                 delivery,
                                 barrier_type,
                                 barrier_value,
                                 barrier_obs_type,
                                 obs_schedule,
                                 payment_type,
                                 cash_rebate,
                                 asset_rebate,
                                 settlement_days,
                                 nominal,
                                 payoff_ccy,
                                 underlying_type,
                                 underlying_ccy,
                                 underlying):
    """
    Create a Single Barrier Option.

    Parameters
    ----------
    payoff_type : str
        Type of the payoff.
    strike : float
        The strike price of the option.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    barrier_type : str
        Type of the barrier.
    barrier_value : float
        Value of the barrier.
    barrier_obs_type : str
        Type of barrier observation.
    obs_schedule : list
        Observation schedule for barriers.
    payment_type : str
        Type of payment.
    cash_rebate : float
        Cash rebate for the barrier.
    asset_rebate : float
        Asset rebate for the barrier.
    settlement_days : int
        Number of days for settlement.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoSingleBarrierOption
        A protocol buffer object representing the Single Barrier Option.
    """

    return dqCreateProtoSingleBarrierOption(to_payoff_type(payoff_type),
                                            strike,
                                            create_date(expiry),
                                            create_date(delivery),
                                            create_barrier(barrier_type, barrier_value),
                                            to_payment_type(payment_type),
                                            cash_rebate,
                                            asset_rebate,
                                            nominal,
                                            underlying,
                                            settlement_days,
                                            to_event_observation_type(barrier_obs_type),
                                            create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                            underlying_ccy,
                                            payoff_ccy,
                                            to_instrument_type(underlying_type))
#CreateDoubleBarrierOption
def create_double_barrier_option(payoff_type,
                                 strike,
                                 expiry,
                                 delivery,
                                 lower_barrier_type,
                                 lower_barrier_value,
                                 upper_barrier_type,
                                 upper_barrier_value,
                                 barrier_obs_type,
                                 obs_schedule,
                                 payment_type,
                                 lower_cash_rebate,
                                 lower_asset_rebate,                                
                                 upper_cash_rebate,                                
                                 upper_asset_rebate,
                                 settlement_days,
                                 nominal,
                                 payoff_ccy,
                                 underlying_type,
                                 underlying_ccy,
                                 underlying):
    """
    Create a Double Barrier Option.

    Parameters
    ----------
    payoff_type : str
        The type of payoff for the option.
    strike : float
        The strike price of the option.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    lower_barrier_type : str
        Type of the lower barrier.
    lower_barrier_value : float
        Value of the lower barrier.
    upper_barrier_type : str
        Type of the upper barrier.
    upper_barrier_value : float
        Value of the upper barrier.
    barrier_obs_type : str
        Type of barrier observation.
    obs_schedule : list
        Schedule for barrier observations.
    payment_type : str
        Type of payment for the option.
    lower_cash_rebate : float
        Cash rebate for breaching the lower barrier.
    lower_asset_rebate : float
        Asset rebate for breaching the lower barrier.
    upper_cash_rebate : float
        Cash rebate for breaching the upper barrier.
    upper_asset_rebate : float
        Asset rebate for breaching the upper barrier.
    settlement_days : int
        Number of days for settlement.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoDoubleBarrierOption
        A protocol buffer object representing the Double Barrier Option.
    """

    return dqCreateProtoDoubleBarrierOption(to_payoff_type(payoff_type),
                                            strike,
                                            create_date(expiry),
                                            create_date(delivery),
                                            create_barrier(lower_barrier_type, lower_barrier_value),
                                            create_barrier(upper_barrier_type, upper_barrier_value),
                                            to_payment_type(payment_type),
                                            lower_cash_rebate, lower_asset_rebate,
                                            upper_cash_rebate, upper_asset_rebate,
                                            nominal,
                                            underlying,
                                            settlement_days,
                                            to_event_observation_type(barrier_obs_type),
                                            create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                            underlying_ccy,
                                            payoff_ccy,
                                            to_instrument_type(underlying_type))
        
#CreateSingleSharkFinOption
def create_single_shark_fin_option(payoff_type,
                                   strike,
                                   expiry,
                                   delivery,
                                   gearing,
                                   performance_type,
                                   barrier_type,
                                   barrier_value,
                                   barrier_obs_type,
                                   obs_schedule,
                                   payment_type,
                                   cash_rebate,
                                   asset_rebate,
                                   settlement_days,
                                   nominal,
                                   payoff_ccy,
                                   underlying_type,
                                   underlying_ccy,
                                   underlying):
    """
    Create a Single Shark Fin Option.

    Parameters
    ----------
    payoff_type : str
        Type of the payoff.
    strike : float
        The strike price.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    gearing : float
        The gearing factor.
    performance_type : str
        Type of the performance.
    barrier_type : str
        Type of the barrier.
    barrier_value : float
        Value of the barrier.
    barrier_obs_type : str
        Type of barrier observation.
    obs_schedule : list
        Observation schedule for barriers.
    payment_type : str
        Type of payment.
    cash_rebate : float
        Cash rebate for the barrier.
    asset_rebate : float
        Asset rebate for the barrier.
    settlement_days : int
        Number of days for settlement.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoSingleSharkFinOption
        A protocol buffer object representing the Single Shark Fin Option.
    """
        
    return dqCreateProtoSingleSharkFinOption(to_payoff_type(payoff_type),
                                             strike,
                                             create_date(expiry),
                                             create_date(delivery),
                                             gearing,
                                             to_performance_type(performance_type),
                                             to_event_observation_type(barrier_obs_type),
                                             create_barrier(barrier_type, barrier_value),
                                             cash_rebate,
                                             asset_rebate,
                                             create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                             nominal,
                                             underlying,
                                             underlying_ccy,
                                             payoff_ccy,
                                             to_instrument_type(underlying_type),
                                             settlement_days,
                                             to_payment_type(payment_type))
    
#CreateDoubleSharkFinOption
def create_double_shark_fin_option(lower_strike,
                                   upper_strike,
                                   expiry,
                                   delivery,
                                   lower_participation,
                                   upper_participation,
                                   performance_type,
                                   lower_barrier,
                                   upper_barrier,
                                   barrier_obs_type,
                                   obs_schedule,
                                   payment_type,
                                   lower_cash_rebate,
                                   lower_asset_rebate,
                                   upper_cash_rebate,
                                   upper_asset_rebate,
                                   settlement_days,
                                   nominal,
                                   payoff_ccy,
                                   underlying_type,
                                   underlying_ccy,
                                   underlying):
    """
    Create a Double Shark Fin Option.

    Parameters
    ----------
    lower_strike : float
        The lower strike price.
    upper_strike : float
        The upper strike price.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    lower_paticipation : float
        The lower participation rate.
    upper_participation : float
        The upper participation rate.
    performance_type : str
        Type of the performance.
    lower_barrier : float
        Value of the lower barrier.
    upper_barrier: float
        Value of the upper barrier.
    barrier_obs_type : str
        Type of barrier observation.
    obs_schedule : list
        Observation schedule for barriers.
    payment_type : str
        Type of payment.
    lower_cash_rebate : float
        Cash rebate for the lower barrier.
    lower_asset_rebate : float
        Asset rebate for the lower barrier.
    upper_cash_rebate : float
        Cash rebate for the upper barrier.
    upper_asset_rebate : float
        Asset rebate for the upper barrier.
    settlement_days : int
        Number of days for settlement.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoDoubleSharkFinOption
        A protocol buffer object representing the Double Shark Fin Option.
    """

    return dqCreateProtoDoubleSharkFinOption(lower_strike, upper_strike, create_date(expiry), create_date(delivery),
                                            lower_participation, upper_participation,
                                            to_event_observation_type(barrier_obs_type),
                                            lower_barrier,
                                            upper_barrier,
                                            lower_cash_rebate, lower_asset_rebate,
                                            upper_cash_rebate, upper_asset_rebate,
                                            create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                            nominal,
                                            underlying,
                                            underlying_ccy,
                                            payoff_ccy,
                                            to_instrument_type(underlying_type),
                                            settlement_days,
                                            to_payment_type(payment_type),
                                            to_performance_type(performance_type))
        
#CreateRangeAccrualOption
def create_range_accrual_option(expiry_date: datetime,
                                delivery_date: datetime,
                                asset: float,
                                cash: float,
                                lower_barrier: float,
                                upper_barrier: float,
                                obs_schedule: list,
                                nominal: float,
                                payoff_ccy: str,
                                underlying_type: str,
                                underlying_ccy: str,
                                underlying: str):
    """
    Create a Range Accrual Option.

    Parameters
    ----------
    expiry_date : datetime
        The expiry date of the option.
    delivery_date : datetime
        The delivery date of the option.
    asset : float
        The asset amount for the option.
    cash : float
        The cash amount for the option.
    lower_barrier : float
        The lower barrier value.
    upper_barrier : float
        The upper barrier value.
    obs_schedule : list
        The observation schedule.
    nominal : float
        The nominal value of the option.
    payoff_ccy : str
        The currency of the payoff.
    underlying_type : str
        The type of the underlying asset.
    underlying_ccy : str
        The currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    dqproto.RangeAccrualOption
        A protocol buffer object representing the Range Accrual Option.
    """


    return dqCreateProtoRangeAccrualOption(create_date(expiry_date),
                                          create_date(delivery_date),
                                          asset, cash,
                                          lower_barrier, upper_barrier,
                                          create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                          nominal, underlying, underlying_ccy, payoff_ccy,
                                          to_instrument_type(underlying_type))
        
#CreateAirBagOption
def create_airbag_option(payoff_type: str, 
                          expiry: datetime,
                          delivery: datetime,
                          lower_strike: float,
                          upper_strike: float,
                          lower_participation: float,
                          upper_participation: float,
                          knock_in_strike: float,
                          barrier_type: str,
                          barrier_value: float,
                          barrier_obs_type: str,
                          obs_schedule: list,                    
                          nominal: float,
                          payoff_ccy: str,
                          underlying_type: str,
                          underlying_ccy: str,
                          underlying: str):
    """
    Create an Air Bag Option.

    Parameters
    ----------
    payoff_type : str
        Type of the payoff.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    lower_strike : float
        The lower strike price.
    upper_strike : float
        The upper strike price.
    lower_participation : float
        The lower participation rate.
    upper_participation : float
        The upper participation rate.
    knock_in_strike : float
        The strike at which the knock-in occurs.
    barrier_type : str
        Type of the barrier.
    barrier_value : float
        Value of the barrier.
    barrier_obs_type : str
        Type of barrier observation.
    obs_schedule : list
        Schedule for observing the barrier.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoAirbagOption
        A protocol buffer object representing the Air Bag Option.
    """

    return dqCreateProtoAirbagOption(to_payoff_type(payoff_type), knock_in_strike, to_event_observation_type(barrier_obs_type),
                                    create_barrier(barrier_type, barrier_value),
                                    lower_participation, upper_participation,
                                    lower_strike, upper_strike,
                                    create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                    create_date(expiry),
                                    create_date(delivery),
                                    nominal, underlying, underlying_ccy, payoff_ccy,
                                    to_instrument_type(underlying_type))
        
#CreatePingPongOption
def create_ping_pong_option(expiry: datetime,
                            delivery: datetime,
                            lower_barrier_type: str,
                            lower_barrier_value: float,
                            upper_barrier_type: str,
                            upper_barrier_value: float,
                            barrier_obs_type: str,
                            obs_schedule: list,
                            payment_type: str,
                            cash: float,
                            asset: float,
                            settlement_days: int,
                            nominal: float,
                            payoff_ccy: str,
                            underlying_type: str,
                            underlying_ccy: str,
                            underlying: str):
    """
    Create a Ping Pong Option.

    Parameters
    ----------
    expiry : datetime
        The expiry date of the option.
    delivery : datetime
        The delivery date of the option.
    lower_barrier_type : str
        Type of the lower barrier.
    lower_barrier_value : float
        Value of the lower barrier.
    upper_barrier_type : str
        Type of the upper barrier.
    upper_barrier_value : float
        Value of the upper barrier.
    barrier_obs_type : str
        Type of barrier observation.
    obs_schedule : list
        Observation schedule for barriers.
    payment_type : str
        Type of payment.
    cash : float
        Cash amount for the option.
    asset : float
        Asset amount for the option.
    settlement_days : int
        Number of days for settlement.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset of the option.

    Returns
    -------
    dqproto.PingPongOption
        A protocol buffer object representing the Ping Pong Option.
    """

    return dqCreateProtoPingPongOption(asset, cash,
                                     create_date(expiry), create_date(delivery),
                                     create_barrier(lower_barrier_type, lower_barrier_value),
                                     create_barrier(upper_barrier_type, upper_barrier_value),
                                     to_event_observation_type(barrier_obs_type),
                                     create_fixing_schedule(obs_schedule[0], obs_schedule[1], obs_schedule[2]),
                                     to_payment_type(payment_type),
                                     settlement_days,
                                     nominal,
                                     underlying, underlying_ccy, payoff_ccy,
                                     to_instrument_type(underlying_type))
        
#CreateCollarOption
def create_collar_option(payoff_type: str,
                            lower_gearing: float,
                            upper_gearing: float,
                            lower_strike: float,
                            upper_strike: float,
                            expiry: datetime,
                            delivery: datetime,
                            nominal: float,
                            payoff_ccy: str,
                            underlying_type: str,
                            underlying_ccy: str,
                            underlying: str):
    """
    Create a Collar Option.

    Parameters
    ----------
    payoff_type : str
        Type of the payoff.
    lower_gearing : float
        The lower gearing factor.
    upper_gearing : float
        The upper gearing factor.
    lower_strike : float
        The lower strike price.
    upper_strike : float
        The upper strike price.
    expiry : datetime
        Expiry date of the option.
    delivery : datetime
        Delivery date of the option.
    nominal : float
        Nominal value of the option.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoCollarOption
        A protocol buffer object representing the Collar Option.
    """

    return dqCreateProtoCollarOption(to_payoff_type(payoff_type), 
                                     lower_gearing,upper_gearing,
                                     lower_strike,upper_strike,
                                     create_date(expiry),create_date(delivery),
                                     nominal,underlying,payoff_ccy,underlying_ccy,
                                     to_instrument_type(underlying_type))
        
#CreatePhoenixAutoCallableNote
def create_phoenix_auto_callable_note(coupon_payoff_type,
    coupon_strike,
    coupon_rate,
    start_date: datetime,
    coupon_dates: list,
    day_count: str,
    knock_out_barrier_type,
    knock_out_barrier_value,
    knock_out_sched: list,
    knock_in_barrier_type: str,
    knock_in_barrier_value: float,
    knock_in_sched: list,
    long_short: str,
    knock_in_payoff_type: str,
    knock_in_payoff_strike: float,
    expiry: datetime,
    delivery: datetime,
    settlement_days: int,
    nominal: float,
    payoff_ccy: str,
    underlying_type: str,
    underlying_ccy: str,
    underlying: str,
):
    """
    Create a Phoenix Auto Callable Note.

    Parameters
    ----------
    coupon_payoff_type : str
        The type of payoff for the coupon.
    coupon_strike : float
        The strike value for the coupon.
    coupon_rate : float
        The rate of the coupon.
    start_date : datetime
        The start date of the note.
    coupon_dates : list
        List of dates when the coupon payments occur.
    day_count : str
        Day count convention used for the note.
    knock_out_barrier_type : str
        Type of barrier for knock-out event.
    knock_out_barrier_value : float
        Value of barrier for knock-out event.
    knock_out_sched : list
        Schedule for knock-out event observations.
    knock_in_barrier_type : str
        Type of barrier for knock-in event.
    knock_in_barrier_value : float
        Value of barrier for knock-in event.
    knock_in_sched : list
        Schedule for knock-in event observations.
    long_short : str
        Indicates if the note is long or short.
    knock_in_payoff_type : str
        The type of payoff if knock-in event occurs.
    knock_in_payoff_strike : float
        The strike value for the knock-in payoff.
    expiry : datetime
        The expiry date of the note.
    delivery : datetime
        The delivery date of the note.
    settlement_days : int
        Number of days for settlement.
    nominal : float
        The nominal value of the note.
    payoff_ccy : str
        Currency of the payoff.
    underlying_type : str
        The type of underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset of the note.

    Returns
    -------
    dqproto.PhoenixAutoCallableNote
        A protocol buffer object representing the Phoenix Auto Callable Note.
    """

    return dqCreateProtoPhoenixAutoCallableNote(to_payoff_type(coupon_payoff_type), coupon_strike, coupon_rate,
                                                create_date(start_date), 
                                                [create_date(d) for d in coupon_dates],
                                                create_barrier(knock_out_barrier_type, knock_out_barrier_value),
                                                create_fixing_schedule(knock_out_sched[0], knock_out_sched[1], knock_out_sched[2]),
                                                create_barrier(knock_in_barrier_type, knock_in_barrier_value),
                                                create_fixing_schedule(knock_in_sched[0], knock_in_sched[1], knock_in_sched[2]),
                                                to_buy_sell_flag(long_short),
                                                to_payoff_type(knock_in_payoff_type),
                                                knock_in_payoff_strike,
                                                create_date(expiry), create_date(delivery),
                                                nominal, underlying, settlement_days, underlying_ccy, payoff_ccy,
                                                to_instrument_type(underlying_type),
                                                to_day_count_convention(day_count))
        
#CreateSnowballAutoCallableNote
def create_snowball_auto_callable_note(
    coupon_rate: float,
    start_date: datetime,
    coupon_dates: list,
    day_count: str,
    knock_out_barrier_type,
    knock_out_barrier_value,
    knock_out_sched: list,
    knock_in_barrier_type: str,
    knock_in_barrier_value: float,
    knock_in_sched: list,
    long_short: str,
    knock_in_payoff_type: str,
    knock_in_payoff_strike: float,
    knock_in_payoff_gearing: float,
    reference_price: float,
    expiry: datetime,
    delivery: datetime,
    settlement_days: int,
    nominal: float,
    payoff_ccy: str,
    underlying_type: str,
    underlying_ccy: str,
    underlying: str
):
    """
    Create a Snowball Auto Callable Note.

    Parameters
    ----------
    coupon_rate : float
        The coupon rate of the note.
    start_date : datetime
        The start date of the note.
    coupon_dates : list
        List of dates when the coupon payments occur.
    day_count : str
        Day count convention used for the note.
    knock_out_barrier_type : str
        Type of barrier for knock-out event.
    knock_out_barrier_value : float
        Value of barrier for knock-out event.
    knock_out_sched : list
        Schedule for knock-out event observations.
    knock_in_barrier_type : str
        Type of barrier for knock-in event.
    knock_in_barrier_value : float
        Value of barrier for knock-in event.
    knock_in_sched : list
        Schedule for knock-in event observations.
    long_short : str
        Indicates if the position is 'LONG' or 'SHORT'.
    knock_in_payoff_type : str
        Type of payoff for knock-in event.
    knock_in_payoff_strike : float
        Strike value for knock-in payoff.
    knock_in_payoff_gearing : float
        Gearing for knock-in payoff.
    reference_price : float
        Reference price for the underlying asset.
    expiry : datetime
        Expiry date of the note.
    delivery : datetime
        Delivery date of the note.
    settlement_days : int
        Number of settlement days for the note.
    nominal : float
        Nominal value of the note.
    payoff_ccy : str
        Payoff currency of the note.
    underlying_type : str
        Type of the underlying asset.
    underlying_ccy : str
        Currency of the underlying asset.
    underlying : str
        The underlying asset.

    Returns
    -------
    ProtoSnowballAutoCallableNote
        A protocol buffer object representing the Snowball Auto Callable Note.
    """

    return dqCreateProtoSnowballAutoCallableNote(coupon_rate, create_date(start_date),
                                                [create_date(d) for d in coupon_dates],
                                                create_barrier(knock_out_barrier_type, knock_out_barrier_value),
                                                create_fixing_schedule(knock_out_sched[0], knock_out_sched[1], knock_out_sched[2]),
                                                create_barrier(knock_in_barrier_type, knock_in_barrier_value),
                                                create_fixing_schedule(knock_in_sched[0], knock_in_sched[1], knock_in_sched[2]),
                                                to_buy_sell_flag(long_short),
                                                to_payoff_type(knock_in_payoff_type),
                                                knock_in_payoff_strike,
                                                create_date(expiry), create_date(delivery),
                                                nominal, underlying, 
                                                knock_in_payoff_gearing, reference_price,
                                                to_day_count_convention(day_count),
                                                settlement_days, underlying_ccy, payoff_ccy,
                                                to_instrument_type(underlying_type))