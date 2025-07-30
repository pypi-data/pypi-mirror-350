# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:47:50 2022

@author: dingq
"""
import pandas as pd
import datetime as dt

from caplibproto.dqproto import *

from caplib.processrequest import * 
from caplib.datetime import *
from caplib.market import *

#BrokenRateCalculationMethod
def to_brokend_rate_calculation_method(src):
    '''
    Convert a string to BrokenRateCalculationMethod.
    
    Parameters
    ----------
    src : str
        a string of brokend rate calculation method, i.e. 'CURRENT'.
    
    Returns
    -------
    BrokenRateCalculationMethod       

    '''
    if src is None:
        return INVALID_BROKEN_RATE_CALCULATION_METHOD
    if src in ['', 'nan']:
        return INVALID_BROKEN_RATE_CALCULATION_METHOD
    else:
        return BrokenRateCalculationMethod.DESCRIPTOR.values_by_name[src.upper()].number

#InterestRateLegType
def to_interest_rate_leg_type(src):
    '''
    Convert a string to InterestRateLegType.
    
    Parameters
    ----------
    src : str
        a string of interest rate leg type, i.e. 'FIXED_LEG'.
    
    Returns
    -------
    InterestRateLegType       

    '''
    if src is None:
        return INVALID_INTEREST_RATE_LEG_TYPE
    if src in ['', 'nan']:
        return INVALID_INTEREST_RATE_LEG_TYPE
    else:
        return InterestRateLegType.DESCRIPTOR.values_by_name[src.upper()].number

#InterestCalculationMethod
def to_interest_calculation_method(src):
    '''
    Convert a string to InterestCalculationMethod.
    
    Parameters
    ----------
    src : str
        a string of interest calculation method, i.e. 'SIMPLE'.
    
    Returns
    -------
    InterestCalculationMethod       

    '''
    if src is None:
        return INVALID_INTEREST_CALCULATION_METHOD
    if src in ['', 'nan']:
        return INVALID_INTEREST_CALCULATION_METHOD
    else:
        return InterestCalculationMethod.DESCRIPTOR.values_by_name[src.upper()].number

#PaymentDiscountMethod
def to_payment_discount_method(src):
    if src is None:
        return NO_DISCOUNT
    
    if src in ['', 'nan']:
        return NO_DISCOUNT
    else:
        return PaymentDiscountMethod.DESCRIPTOR.values_by_name[src.upper()].number
    
#InterestRateCalculationMethod
def to_interest_rate_calculation_method(src):
    '''
    Convert a string to InterestRateCalculationMethod.
    
    Parameters
    ----------
    src : str
        a string of interest rate calculation method, i.e. 'STANDARD'.
    
    Returns
    -------
    InterestRateCalculationMethod       

    '''
    if src is None:
        return INVALID_INTEREST_RATE_CALCULATION_METHOD
    if src in ['', 'nan']:
        return INVALID_INTEREST_RATE_CALCULATION_METHOD
    else:
        return InterestRateCalculationMethod.DESCRIPTOR.values_by_name[src.upper()].number

#InterestScheduleType
def to_interest_schedule_type(src):
    '''
    Convert a string to InterestScheduleType.
    
    Parameters
    ----------
    src : str
        a string of interest calculation schedule, i.e. 'INTEREST_CALCULATION_SCHEDULE'.
    
    Returns
    -------
    InterestScheduleType       

    '''
    if src is None:
        return INVALID_INTEREST_SCHEDULE_TYPE
    if src in ['', 'nan']:
        return INVALID_INTEREST_SCHEDULE_TYPE
    else:
        return InterestScheduleType.DESCRIPTOR.values_by_name[src.upper()].number

#InterestRateIndexType
def to_interest_rate_index_type(src):
    '''
    Convert a string to InterestRateIndexType.
    
    Parameters
    ----------
    src : str
        a string of interest rate index type, i.e. 'IBOR_INDEX'.
    
    Returns
    -------
    InterestRateIndexType       

    '''
    if src is None:
        return INVALID_INTEREST_RATE_INDEX_TYPE
    if src in ['', 'nan']:
        return INVALID_INTEREST_RATE_INDEX_TYPE
    else:
        return InterestRateIndexType.DESCRIPTOR.values_by_name[src.upper()].number

#IborIndexType
def to_ibor_index_type(src):
    '''
    Convert a string to IborIndexType.
    
    Parameters
    ----------
    src : str
        a string of IBOR index type, i.e. 'STANDARD_IBOR_INDEX'.
    
    Returns
    -------
    IborIndexType       

    '''
    if src is None:
        return STANDARD_IBOR_INDEX
    if src in ['', 'nan']:
        return STANDARD_IBOR_INDEX
    else:
        return IborIndexType.DESCRIPTOR.values_by_name[src.upper()].number
    
#IBOR Index
def create_ibor_index(index_name, 
                      index_tenor, 
                      index_ccy, 
                      calendar_list, 
                      start_delay, 
                      day_count = 'ACT_360', 
                      interest_day_convention = 'MODIFIED_FOLLOWING', 
                      date_roll_convention = 'INVALID_DATE_ROLL_CONVENTION',
                      ibor_type = 'STANDARD_IBOR_INDEX'):
    '''
    Create an Ibor Index object and store it in the object cache.
    
    Parameters
    ----------
    index_name : str
        DESCRIPTION.
    index_tenor : str
        DESCRIPTION.
    index_ccy : str
        DESCRIPTION.
    calendar_list : list of str
        DESCRIPTION.
    start_delay : int, optional
        DESCRIPTION. 
    day_count : DayCountConvention, optional
        DESCRIPTION. The default is 'ACT_360'.
    interest_day_convention : BusinessDayConvention, optional
        DESCRIPTION. The default is 'MODIFIED_FOLLOWING'.
    date_roll_convention : DateRollConvention, optional
        DESCRIPTION. The default is 'INVALID_DATE_ROLL_CONVENTION'.
    ibor_type : IborIndexType, optional
        DESCRIPTION. The default is 'STANDARD_IBOR_INDEX'.

    Returns
    -------
    boolean
        DESCRIPTION.

    '''
    pb_data = dqCreateProtoIborIndex(IBOR_INDEX,
                                     index_name.upper(),  
                                     to_period(index_tenor), 
                                     index_ccy.upper(), 
                                     create_period(start_delay, 'DAYS'), 
                                     calendar_list, 
                                     to_day_count_convention(day_count), 
                                     to_business_day_convention(interest_day_convention), 
                                     to_date_roll_convention(date_roll_convention), 
                                     to_ibor_index_type(ibor_type))        
    pb_data_list = dqCreateProtoIborIndexList([pb_data])
    return create_static_data('SDT_IBOR_INDEX', pb_data_list.SerializeToString())

#Interest Leg Definition:
def create_leg_definition(leg_type, currency, day_count, ref_index, payment_discount_method, rate_calc_method,                          
                          notional_exchange, spread, fx_convert, fx_reset,
                          calendar, freq, interest_day_convention, stub_policy, broken_period_type,
                          pay_day_offset, pay_day_convention,
                          fixing_calendars, fixing_freq, fixing_day_convention, fixing_mode, fixing_day_offset):
    '''
    Create an object of InterestRateLegDefinition.

    Parameters
    ----------
    leg_type : InterestRateLegType
        DESCRIPTION.
    currency : str
        DESCRIPTION.
    day_count : DayCountConvention
        DESCRIPTION.
    ref_index : str
        DESCRIPTION.
    payment_discount_method : PaymentDiscountMethod
        DESCRIPTION.
    rate_calc_method : InterestRateCalculationMethod
        DESCRIPTION.
    notional_exchange : NotionalExchange
        DESCRIPTION.
    spread : bool
        DESCRIPTION.
    fx_convert : bool
        DESCRIPTION.
    fx_reset : bool
        DESCRIPTION.
    calendar : str
        DESCRIPTION.
    freq : Frequency
        DESCRIPTION.
    interest_day_convention : BusinessDayConvention
        DESCRIPTION.
    stub_policy : StubPolicy
        DESCRIPTION.
    broken_period_type : BrokenPeriodType
        DESCRIPTION.
    pay_day_offset : int
        DESCRIPTION.
    pay_day_convention : BusinessDayConvention
        DESCRIPTION.
    fixing_calendars : list
        DESCRIPTION.
    fixing_freq : Frequency
        DESCRIPTION.
    fixing_day_convention : BusinessDayConvention
        DESCRIPTION.
    fixing_mode : DateGenerationMode
        DESCRIPTION.
    fixing_day_offset : int
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    InterestRateLegDefinition
        DESCRIPTION.

    '''    
    if leg_type == '':
        raise ValueError('create_leg_definition: empty leg_type')
        
    if currency == '':
        raise ValueError('create_leg_definition: empty currency')
    
    if day_count == '':
        raise ValueError('create_leg_definition: empty day_count')
    
    p_freq = to_frequency(freq)
    p_interest_day_convention = to_business_day_convention(interest_day_convention)
    p_stub_policy = to_stub_policy(stub_policy)
    p_broken_period_type = to_broken_period_type(broken_period_type)
    interest_calculation_schedule_definition = dqCreateProtoInterestRateLegScheduleDefinition_InterestCaculationScheduleDefinition(ABSOLUTE_NORMAL,
                                                                                                                                   INVALID_INTEREST_SCHEDULE_TYPE,
                                                                                                                                   [calendar], 
                                                                                                                                   p_freq, 
                                                                                                                                   p_interest_day_convention, 
                                                                                                                                   p_stub_policy, p_broken_period_type,
                                                                                                                                   INVALID_DATE_ROLL_CONVENTION,
                                                                                                                                   INVALID_RELATIVE_SCHEDULE_GENERATION_MODE)
    p_pay_day_convention = to_business_day_convention(pay_day_convention)
    
    interest_payment_schedule_definition = dqCreateProtoInterestRateLegScheduleDefinition_InterestPaymentScheduleDefinition(RELATIVE_TO_SCHEDULE,
                                                                                                                            INTEREST_CALCULATION_SCHEDULE,
                                                                                                                            [calendar], p_freq, p_pay_day_convention, IN_ARREAR, 1, create_period(pay_day_offset, 'DAYS'),                                                                                                                                
                                                                                                                            BACKWARD_WITHOUT_BROKEN)
    p_fixing_freq = to_frequency(fixing_freq)
    p_fixing_day_convention = to_business_day_convention(fixing_day_convention)
    p_fixing_mode = to_date_gen_mode(fixing_mode)    
    interest_rate_fixing_schedule_definition = dqCreateProtoInterestRateLegScheduleDefinition_InterestRateFixingScheduleDefinition(RELATIVE_TO_SCHEDULE,
                                                                                                                                   INTEREST_CALCULATION_SCHEDULE,
                                                                                                                                   fixing_calendars, 
                                                                                                                                   p_fixing_freq, p_fixing_day_convention, p_fixing_mode, 1, create_period(fixing_day_offset, 'DAYS'),
                                                                                                                                   BACKWARD_WITHOUT_BROKEN)
    
    schedule_definition = dqCreateProtoInterestRateLegScheduleDefinition(interest_calculation_schedule_definition,
                                                                         interest_payment_schedule_definition,
                                                                         interest_rate_fixing_schedule_definition)
    
    p_leg_type = to_interest_rate_leg_type(leg_type)
    p_day_count = to_day_count_convention(day_count)
    p_payment_discount_method = to_payment_discount_method(payment_discount_method)
    p_rate_calc_method = to_interest_rate_calculation_method(rate_calc_method)
    p_notional_exchange = to_notional_exchange(notional_exchange)
    leg_definition = dqCreateProtoInterestRateLegDefinition(p_leg_type, currency.upper(), p_day_count, 
                                                            ref_index.upper(), p_payment_discount_method, SIMPLE, 
                                                            p_rate_calc_method, CURRENT,
                                                            p_notional_exchange, spread, fx_convert, fx_reset, schedule_definition)    
    return leg_definition


#Definition for a fixed leg:
def create_fixed_leg_definition(currency, calendar, freq, day_count = 'ACT_365_FIXED', 
                                interest_day_convention = 'MODIFIED_FOLLOWING', stub_policy = 'INITIAL', broken_period_type = 'LONG',
                                pay_day_offset = 0, pay_day_convention = 'MODIFIED_FOLLOWING', notional_exchange = 'INVALID_NOTIONAL_EXCHANGE'):
    '''
    Create an object of type InterestRateLegDefinition for fixed leg.

    Parameters
    ----------
    currency : str
        DESCRIPTION.
    calendar : str
        DESCRIPTION.
    freq : Frequency
        DESCRIPTION.
    day_count : DayCountConvention, optional
        DESCRIPTION. The default is ACT_365_FIXED.
    interest_day_convention : BusinessDayConvention, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    stub_policy : StubPolicy, optional
        DESCRIPTION. The default is INITIAL.
    broken_period_type : BrokenPeriodType, optional
        DESCRIPTION. The default is LONG.
    pay_day_offset : Period, optional
        DESCRIPTION. The default is Period(0, DAYS).
    pay_day_convention : BusinessDayConvention, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    notional_exchange : NotionalExchange, optional
        DESCRIPTION. The default is INVALID_NOTIONAL_EXCHANGE.

    Returns
    -------
    InterestRateLegDefinition
        DESCRIPTION.

    '''   
    
    return create_leg_definition('FIXED_LEG', currency, day_count, '', 'NO_DISCOUNT', 'STANDARD',                          
                                notional_exchange, False, False, False,
                                calendar, freq, interest_day_convention, stub_policy, broken_period_type,
                                pay_day_offset, pay_day_convention,
                                [], 'INVALID_FREQUENCY', 'INVALID_BUSINESS_DAY_CONVENTION', 'INVALID_DATE_GENERATION_MODE', 0)

#Definition for a floating leg:
def create_floating_leg_definition(currency, ref_index, calendar, fixing_calendars, freq, fixing_freq, day_count = 'ACT_360',  
                                   payment_discount_method = 'NO_DISCOUNT', rate_calc_method = 'STANDARD', spread = False,
                                   interest_day_convention = 'MODIFIED_FOLLOWING', stub_policy = 'INITIAL', broken_period_type = 'LONG',
                                   pay_day_offset = 0, pay_day_convention = 'MODIFIED_FOLLOWING',
                                   fixing_day_convention = 'MODIFIED_PRECEDING', fixing_mode ='IN_ADVANCE', fixing_day_offset = -2,                          
                                   notional_exchange = 'INVALID_NOTIONAL_EXCHANGE'):
    '''
    Create an object of type InterestRateLegDefinition for floating leg.

    Parameters
    ----------
    currency : str
        DESCRIPTION.
    ref_index : str
        DESCRIPTION.
    calendar : str
        DESCRIPTION.
    fixing_calendars : list
        DESCRIPTION.
    freq : Frequency
        DESCRIPTION.
    fixing_freq : TYPE
        DESCRIPTION.
    day_count : TYPE, optional
        DESCRIPTION. The default is 'ACT_360'.
    payment_discount_method : TYPE, optional
        DESCRIPTION. The default is 'NO_DISCOUNT'.
    rate_calc_method : TYPE, optional
        DESCRIPTION. The default is 'STANDARD'.
    spread : TYPE, optional
        DESCRIPTION. The default is False.
    interest_day_convention : TYPE, optional
        DESCRIPTION. The default is 'MODIFIED_FOLLOWING'.
    stub_policy : TYPE, optional
        DESCRIPTION. The default is 'INITIAL'.
    broken_period_type : TYPE, optional
        DESCRIPTION. The default is 'LONG'.
    pay_day_offset : TYPE, optional
        DESCRIPTION. The default is '0d'.
    pay_day_convention : TYPE, optional
        DESCRIPTION. The default is 'MODIFIED_FOLLOWING'.
    fixing_day_convention : TYPE, optional
        DESCRIPTION. The default is 'MODIFIED_PRECEDING'.
    fixing_mode : TYPE, optional
        DESCRIPTION. The default is 'IN_ADVANCE'.
    fixing_day_offset : TYPE, optional
        DESCRIPTION. The default is '-2d'.
    notional_exchange : TYPE, optional
        DESCRIPTION. The default is ''.

    Returns
    -------
    InterestRateLegDefinition
        DESCRIPTION.

    '''    
    return create_leg_definition('FLOATING_LEG', currency, day_count, ref_index, payment_discount_method, rate_calc_method,                          
                                 notional_exchange, spread, False, False,
                                 calendar, freq, interest_day_convention, stub_policy, broken_period_type,
                                 pay_day_offset, pay_day_convention,
                                 fixing_calendars, fixing_freq, fixing_day_convention, fixing_mode, fixing_day_offset)

#IR Deposit Template:
def create_depo_template(inst_name, currency, calendar, start_delay = 1, 
                         day_count = 'ACT_360', interest_day_convention = 'MODIFIED_FOLLOWING', 
                         pay_day_offset = 0, pay_day_convention = 'MODIFIED_FOLLOWING',
                         start_convention = 'SPOTSTART'):
    '''
    Create an object of InterestRateInstrumentTemplate for Deposit instrument.

    Parameters
    ----------
    inst_name : TYPE
        DESCRIPTION.
    currency : TYPE
        DESCRIPTION.
    calendar : TYPE
        DESCRIPTION.
    start_delay : TYPE, optional
        DESCRIPTION. The default is Period(1, DAYS).
    day_count : TYPE, optional
        DESCRIPTION. The default is ACT_360.
    interest_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    pay_day_offset : TYPE, optional
        DESCRIPTION. The default is Period(0, DAYS).
    pay_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    start_convention : TYPE, optional
        DESCRIPTION. The default is SPOTSTART.

    Returns
    -------
    InterestRateInstrumentTemplate
        DESCRIPTION.

    '''    
    leg_definition = create_fixed_leg_definition(currency, calendar, 'ONCE', day_count, 
                                                 interest_day_convention, 'INITIAL', 'LONG',
                                                 pay_day_offset, pay_day_convention, 'INITIAL_FINAL_EXCHANGE')
    p_leg_definition = [leg_definition]
    p_start_convention = to_instrument_start_convention(start_convention)
    pb_data = dqCreateProtoInterestRateInstrumentTemplate(DEPOSIT, inst_name.upper(), create_period(start_delay, 'DAYS'), 
                                                          p_leg_definition, p_start_convention)
    pb_data_list = dqCreateProtoInterestRateInstrumentTemplateList([pb_data])
    create_static_data('SDT_IR_VANILLA_INSTRUMENT', pb_data_list.SerializeToString())    
    return pb_data_list.interest_rate_instrument_template[0]

#FRA Template:
def create_fra_template(inst_name, ref_index, currency, calendar, fixing_calendars, freq,   
                        day_count = 'ACT_360', payment_discount_method = 'DISCOUNT_AT_FLOATING_RATE', 
                        interest_day_convention= 'MODIFIED_FOLLOWING', pay_day_offset = 0, pay_day_convention= 'MODIFIED_FOLLOWING',
                        fixing_day_convention = 'MODIFIED_PRECEDING', fixing_day_offset = -1):
    '''
    Create an object of InterestRateInstrumentTemplate for FRA instrument.

    Parameters
    ----------
    inst_name : TYPE
        DESCRIPTION.
    ref_index : TYPE
        DESCRIPTION.
    currency : TYPE
        DESCRIPTION.
    calendar : TYPE
        DESCRIPTION.
    fixing_calendars : TYPE
        DESCRIPTION.
    freq : TYPE
        DESCRIPTION.
    day_count : TYPE, optional
        DESCRIPTION. The default is ACT_360.
    payment_discount_method : TYPE, optional
        DESCRIPTION. The default is DISCOUNT_AT_FLOATING_RATE.
    interest_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    pay_day_offset : TYPE, optional
        DESCRIPTION. The default is Period(0, DAYS).
    pay_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    fixing_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_PRECEDING.
    fixing_day_offset : TYPE, optional
        DESCRIPTION. The default is Period(-1, DAYS).

    Returns
    -------
    InterestRateInstrumentTemplate
        DESCRIPTION.

    '''
    leg_definition = create_floating_leg_definition(currency, ref_index, calendar, fixing_calendars, freq, freq, day_count,  
                                                    payment_discount_method, 'STANDARD', True,
                                                    interest_day_convention, 'INITIAL', 'LONG',
                                                    pay_day_offset, pay_day_convention,
                                                    fixing_day_convention, 'IN_ADVANCE', fixing_day_offset,                          
                                                    'INITIAL_FINAL_EXCHANGE')
    p_leg_definition = [leg_definition]
    pb_data = dqCreateProtoInterestRateInstrumentTemplate(FORWARD_RATE_AGREEMENT, inst_name.upper(), create_period(0, 'DAYS'), 
                                                          p_leg_definition, SPOTSTART)
    pb_data_list = dqCreateProtoInterestRateInstrumentTemplateList([pb_data])
    create_static_data('SDT_IR_VANILLA_INSTRUMENT', pb_data_list.SerializeToString())    
    return pb_data_list.interest_rate_instrument_template[0]

#IR Vanilla Swap Template
def create_ir_vanilla_swap_template(inst_name, start_delay, 
                                    leg1_definition,
                                    leg2_definition,
                                    start_convention):
    '''
    Create an object of InterestRateInstrumentTemplate for vanilla swap instrument.

    Parameters
    ----------
    inst_name : TYPE
        DESCRIPTION.
    start_delay : int
        DESCRIPTION.
    leg1_definition : TYPE
        DESCRIPTION.
    leg2_definition : TYPE
        DESCRIPTION.
    start_convention : TYPE
        DESCRIPTION.

    Returns
    -------
    InterestRateInstrumentTemplate
        DESCRIPTION.

    '''     
    p_leg_definition = [leg1_definition, leg2_definition]
    p_start_convention = to_instrument_start_convention(start_convention)
    pb_data = dqCreateProtoInterestRateInstrumentTemplate(IR_VANILLA_SWAP, inst_name.upper(), create_period(start_delay, 'DAYS'), 
                                                          p_leg_definition, p_start_convention)
    pb_data_list = dqCreateProtoInterestRateInstrumentTemplateList([pb_data])
    create_static_data('SDT_IR_VANILLA_INSTRUMENT', pb_data_list.SerializeToString())    
    return pb_data_list.interest_rate_instrument_template[0]

#Leg Fixings
def create_leg_fixings(fixings):
    '''
    Create an object of LegFixings.

    Parameters
    ----------
    fixings : TYPE
        DESCRIPTION.

    Returns
    -------
    LegFixings
        DESCRIPTION.

    '''    
    p_leg_fixings_maps = list()
    for i in range(len(fixings)):        
        p_leg_fixings_maps.append(dqCreateProtoTimeSeriesMap(fixings[i][0].upper(), fixings[i][1])) 
    p_leg_fixings = dqCreateProtoLegFixings(p_leg_fixings_maps)    
    return p_leg_fixings

#IR Vanilla Instrument
def build_ir_vanilla_instrument(pay_rec, cpn_rate, spread, start_date, maturity, inst_template, nominal, leg_fixings):
    '''
    Build an IR vanilla instrument object.

    Parameters
    ----------
    pay_rec : PayReceiveFlag
        DESCRIPTION.
    cpn_rate : TYPE
        DESCRIPTION.
    spread : TYPE
        DESCRIPTION.
    start_date : TYPE
        DESCRIPTION.
    maturity : TYPE
        DESCRIPTION.
    inst_template : TYPE
        DESCRIPTION.
    nominal : TYPE
        DESCRIPTION.
    leg_fixings : TYPE
        DESCRIPTION.

    Returns
    -------
    IrVanillaInstrument
        DESCRIPTION.

    '''    
    p_pay_rec = to_pay_receive_flag(pay_rec)
    pb_input = dqCreateProtoBuildIrVanillaInstrumentInput(create_date(start_date), create_date(maturity), 
                                                          p_pay_rec, cpn_rate, spread, 
                                                          nominal, 1.0, 
                                                          inst_template, leg_fixings)    
    req_name = 'BUILD_IR_VANILLA_INSTRUMENT'
    res_msg = process_request(req_name, pb_input.SerializeToString())        
    pb_output = BuildIrVanillaInstrumentOutput()
    pb_output.ParseFromString(res_msg)            
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)   
    return pb_output.inst 

#IR Depo
def build_depo(pay_rec, rate, start_date, maturity, inst_template, nominal = 1.0):
    '''
    Build a Deposit object.

    Parameters
    ----------
    pay_rec : TYPE
        DESCRIPTION.
    rate : TYPE
        DESCRIPTION.
    start_date : TYPE
        DESCRIPTION.
    maturity : TYPE
        DESCRIPTION.
    inst_template : TYPE
        DESCRIPTION.
    nominal : TYPE, optional
        DESCRIPTION. The default is 1.0.

    Returns
    -------
    IrVanillaInstrument
        DESCRIPTION.

    '''    
    leg_fixings = create_leg_fixings([['', create_time_series([], [])]])
    return build_ir_vanilla_instrument(pay_rec, rate, 0.0, start_date, maturity, inst_template, nominal, leg_fixings)

#FRA
def build_fra(pay_rec, rate, start_date, maturity, inst_template, leg_fixings, nominal = 1.0):
    '''
    Build an FRA object.

    Parameters
    ----------
    pay_rec : TYPE
        DESCRIPTION.
    rate : TYPE
        DESCRIPTION.
    start_date : TYPE
        DESCRIPTION.
    maturity : TYPE
        DESCRIPTION.
    inst_template : TYPE
        DESCRIPTION.
    leg_fixings : TYPE
        DESCRIPTION.
    nominal : TYPE, optional
        DESCRIPTION. The default is 1.0.

    Returns
    -------
    IrVanillaInstrument
        DESCRIPTION.

    '''    
    return build_ir_vanilla_instrument(pay_rec, 0.0, -rate, start_date, maturity, inst_template, nominal, leg_fixings)

def print_cash_flow_sched(cash_flow_schedule):
    '''
    Print an object of CashFlowSchedule as pandas.DataFrame

    Parameters
    ----------
    cash_flow_schedule : CashFlowSchedule
        DESCRIPTION.

    Returns
    -------
    pandas.DataFrame.

    '''
    pay_dates = list()
    start_dates = list()
    end_dates=list()
    fixing_dates = list()
    for i in range(len(cash_flow_schedule.data)):
        tmp = cash_flow_schedule.data[i]
        pay = tmp.payment_date
        start = tmp.interest_schedule.data[0].start_date
        end = tmp.interest_schedule.data[0].end_date
        fixing = tmp.interest_schedule.data[0].fixing_date
        pay_dates.append(dt.datetime(pay.year, pay.month, pay.day).strftime('%Y-%m-%d'))
        start_dates.append(dt.datetime(start.year, start.month, start.day).strftime('%Y-%m-%d'))
        end_dates.append(dt.datetime(end.year, end.month, end.day).strftime('%Y-%m-%d'))
        fixing_dates.append(dt.datetime(fixing.year, fixing.month, fixing.day).strftime('%Y-%m-%d'))
    df = pd.DataFrame(columns=['pay', 'start', 'end', 'fixing']) 
    df['pay'] = pay_dates
    df['start'] = start_dates
    df['end'] = end_dates
    df['fixing'] = fixing_dates
    return df