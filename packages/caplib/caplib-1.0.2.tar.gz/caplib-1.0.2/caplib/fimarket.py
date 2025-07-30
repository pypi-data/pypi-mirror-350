# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:47:50 2022

@author: dingq
"""
from caplibproto.dqdatetime_pb2 import ACT_365_FIXED, INVALID_FREQUENCY, INVALID_BUSINESS_DAY_CONVENTION, ANNUAL, \
    MODIFIED_FOLLOWING, INITIAL, LONG, INVALID_DATE_GENERATION_MODE, DAYS
from caplibproto.dqfimarket_pb2 import FIXED_COUPON_BOND, VanillaBondType, FLOATING_COUPON_BOND, ZERO_COUPON_BOND
from caplibproto.dqfimarketservice_pb2 import BuildVanillaBondOutput
from caplibproto.dqirmarket_pb2 import FIXED_LEG, STANDARD, FLOATING_LEG
from caplibproto.dqmarket_pb2 import NO_DISCOUNT, INITIAL_FINAL_EXCHANGE
from caplibproto.dqstaticdataservice_pb2 import SDT_VANILLA_BOND

from caplib.irmarket import *
from caplib.datetime import create_period

def to_vanilla_bond_type(src):
    '''
    Convert a string to VanillaBondType.
    
    Parameters
    ----------
    src : str
        a string of vanilla bond type, i.e. 'FIXED_COUPON_BOND'.

    Returns
    -------
    VanillaBondType       

    '''
    if src is None:
        return FIXED_COUPON_BOND
    if src in ['', 'nan']:
        return FIXED_COUPON_BOND
    else:
        return VanillaBondType.DESCRIPTOR.values_by_name[src.upper()].number
	
#Vanilla Bond Template
def create_vanilla_bond_template(inst_name, bond_type, issue_date, settlement_days, start_date, maturity,
                                 rate, currency, issue_price,                                 
                                 day_count,
                                 calendar, frequency, interest_day_convention, stub_policy, broken_period_type,
                                 pay_day_offset, pay_day_convention,
                                 ref_index,  
                                 fixing_calendars, fixing_freq, fixing_day_convention, fixing_mode, fixing_day_offset,
                                 ex_cpn_period, ex_cpn_calendar, ex_cpn_day_convention, ex_cpn_eom, 
                                 notional_type = 'CONST_NOTIONAL',
                                 recovery_rate = 0.0):
    '''
    Create a vanilla bond template object and store in the object cache.

    Parameters
    ----------
    inst_name : str
        DESCRIPTION.
    bond_type : VanillaBondType
        DESCRIPTION.
    issue_date : Date
        DESCRIPTION.
    settlement_days : int
        DESCRIPTION.
    start_date : Date
        DESCRIPTION.
    maturity : Period
        DESCRIPTION.
    rate : float
        DESCRIPTION.
    currency : str
        DESCRIPTION.
    issue_price : float
        DESCRIPTION.
    day_count : DayCountConvention
        DESCRIPTION.
    calendar : str
        DESCRIPTION.
    frequency : Frequency
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
    ref_index : str
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
    ex_cpn_period : Period
        DESCRIPTION.
    ex_cpn_calendar : str
        DESCRIPTION.
    ex_cpn_day_convention : BusinessDayConvention
        DESCRIPTION.
    ex_cpn_eom : bool
        DESCRIPTION.
    notional_type : NotionalType
        DESCRIPTION.
    recovery_rate : float
        DESCRIPTION.

    Returns
    -------
    VanillaBondTemplate
        DESCRIPTION.

    '''  
    p_bond_type = to_vanilla_bond_type(bond_type)
    if (p_bond_type==FLOATING_COUPON_BOND):
        leg_type = 'FLOATING_LEG'
    else:
        leg_type = 'FIXED_LEG'
        
    p_leg_definition = create_leg_definition(leg_type, currency, day_count, 
                                             ref_index, 'NO_DISCOUNT', 'STANDARD', 'INITIAL_FINAL_EXCHANGE', False, False, False,
                                             calendar, frequency, interest_day_convention, stub_policy, broken_period_type,
                                             pay_day_offset, pay_day_convention,
                                             fixing_calendars, fixing_freq, fixing_day_convention, fixing_mode, fixing_day_offset)
    
    p_ex_cpn_day_convention = to_business_day_convention(ex_cpn_day_convention)  
    p_notional_type = to_notional_type(notional_type)
    p_template = dqCreateProtoVanillaBondTemplate(inst_name.upper(), p_bond_type, 
                                                  settlement_days, p_leg_definition, 
                                                  to_period(ex_cpn_period), ex_cpn_calendar, 
                                                  p_ex_cpn_day_convention, ex_cpn_eom, 
                                                  create_date(issue_date), rate, to_period(maturity), issue_price, create_date(start_date),
                                                  p_notional_type,
                                                  recovery_rate)
    
    p_template_list = dqCreateProtoVanillaBondTemplateList([p_template])    
    create_static_data('SDT_VANILLA_BOND', p_template_list.SerializeToString())    
    return p_template

#Vanilla Bond Template
def create_zero_cpn_bond_template(inst_name, issue_date, settlement_days, start_date, maturity,
                                  currency, issue_price,                                 
                                  calendar, day_count = 'ACT_365_FIXED', pay_day_convention = 'MODIFIED_FOLLOWING',
                                  recovery_rate = 0.0):
    '''
    Create a zero coupon bond template object and store in the object cache.

    Parameters
    ----------
    inst_name : TYPE
        DESCRIPTION.
    issue_date : TYPE
        DESCRIPTION.
    settlement_days : TYPE
        DESCRIPTION.
    maturity : TYPE
        DESCRIPTION.
    currency : TYPE
        DESCRIPTION.
    issue_price : TYPE
        DESCRIPTION.
    calendar : TYPE
        DESCRIPTION.
    day_count : TYPE, optional
        DESCRIPTION. The default is ACT_365_FIXED.
    pay_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    '''
    @args:        
        inst_name: string
        settlement_days: integer
        maturity: string, dqproto.Period
        currency: string
        issue_price: float
        calendar: string
        day_count: string, dqproto.DayCountConvention        
        pay_day_convention: string, dqproto.BusinessDayConvention        
    @return:
        dqproto.VanillaBondTemplate
    '''
    return create_vanilla_bond_template(inst_name, 'ZERO_COUPON_BOND', issue_date, settlement_days, start_date, maturity,
                                        0.0, currency, issue_price,                                 
                                        day_count,
                                        calendar, 'ANNUAL', 'MODIFIED_FOLLOWING', 'INITIAL', 'LONG', 0, pay_day_convention,
                                        '', 
                                        [], 'INVALID_FREQUENCY', 'INVALID_BUSINESS_DAY_CONVENTION', 'INVALID_DATE_GENERATION_MODE', 0,
                                        '0D', '', 'INVALID_BUSINESS_DAY_CONVENTION', False,
                                        'CONST_NOTIONAL',
                                        recovery_rate)

#Fixed Cpn Bond Template
def create_fixed_cpn_bond_template(inst_name, issue_date, settlement_days, start_date, maturity,
                                   rate, currency, calendar, frequency = 'ANNUAL',                              
                                   day_count = 'ACT_365_FIXED', issue_price = 100.0,    
                                   interest_day_convention = 'MODIFIED_FOLLOWING', stub_policy ='INITIAL', broken_period_type = 'LONG',
                                   pay_day_offset = 0, pay_day_convention='MODIFIED_FOLLOWING',
                                   ex_cpn_period = '0D', ex_cpn_calendar='', ex_cpn_day_convention='INVALID_BUSINESS_DAY_CONVENTION', ex_cpn_eom=False,
                                   notional_type = 'CONST_NOTIONAL',
                                   recovery_rate = 0.0):
    '''
    Create a fixed coupon bond template object and store in the object cache.

    Parameters
    ----------
    inst_name : TYPE
        DESCRIPTION.
    issue_date : TYPE
        DESCRIPTION.
    settlement_days : TYPE
        DESCRIPTION.
    maturity : TYPE
        DESCRIPTION.
    rate : TYPE
        DESCRIPTION.
    currency : TYPE
        DESCRIPTION.
    calendar : TYPE
        DESCRIPTION.
    frequency : TYPE, optional
        DESCRIPTION. The default is ANNUAL.
    day_count : TYPE, optional
        DESCRIPTION. The default is ACT_365_FIXED.
    issue_price : TYPE, optional
        DESCRIPTION. The default is 100.0.
    interest_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    stub_policy : TYPE, optional
        DESCRIPTION. The default is INITIAL.
    broken_period_type : TYPE, optional
        DESCRIPTION. The default is LONG.
    pay_day_offset : TYPE, optional
        DESCRIPTION. The default is Period(0, DAYS).
    pay_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    ex_cpn_period : TYPE, optional
        DESCRIPTION. The default is Period(0, DAYS).
    ex_cpn_calendar : TYPE, optional
        DESCRIPTION. The default is ''.
    ex_cpn_day_convention : TYPE, optional
        DESCRIPTION. The default is INVALID_BUSINESS_DAY_CONVENTION.
    ex_cpn_eom : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    VanillaBondTemplate
        DESCRIPTION.

    '''    
    return create_vanilla_bond_template(inst_name, 'FIXED_COUPON_BOND', issue_date, settlement_days, start_date, maturity,
                                        rate, currency, issue_price,                                 
                                        day_count,
                                        calendar, frequency, interest_day_convention, stub_policy, broken_period_type,
                                        pay_day_offset, pay_day_convention,
                                        '', 
                                        [], 'INVALID_FREQUENCY', 'INVALID_BUSINESS_DAY_CONVENTION', 'INVALID_DATE_GENERATION_MODE', 0,
                                        ex_cpn_period, ex_cpn_calendar, ex_cpn_day_convention, ex_cpn_eom,
                                        notional_type,
                                        recovery_rate)
    
# Standard Bond Template:
def create_std_bond_template(inst_name, bond_type, issue_date, settlement_days, maturity,
                             currency,                               
                             day_count,
                             calendar, frequency, interest_day_convention, stub_policy, broken_period_type,
                             pay_day_offset, pay_day_convention,
                             rate = 1.0,
                             issue_price = 100.0,      
                             ref_index = '',  
                             fixing_calendars = [], fixing_freq = 'INVALID_FREQUENCY', fixing_day_convention = 'INVALID_BUSINESS_DAY_CONVENTION', 
                             fixing_mode = 'INVALID_DATE_GENERATION_MODE', fixing_day_offset = 0,
                             recovery_rate = 0.0):
    '''
    Create a standard bond template object and store in the object cache.

    Parameters
    ----------
    inst_name : TYPE
        DESCRIPTION.
    bond_type : TYPE
        DESCRIPTION.
    issue_date : datetime
        DESCRIPTION.
    settlement_days : TYPE
        DESCRIPTION.
    maturity : TYPE
        DESCRIPTION.
    currency : TYPE
        DESCRIPTION.
    day_count : TYPE
        DESCRIPTION.
    calendar : TYPE
        DESCRIPTION.
    frequency : TYPE
        DESCRIPTION.
    interest_day_convention : TYPE
        DESCRIPTION.
    stub_policy : TYPE
        DESCRIPTION.
    broken_period_type : TYPE
        DESCRIPTION.
    pay_day_offset : TYPE
        DESCRIPTION.
    pay_day_convention : TYPE
        DESCRIPTION.
    ref_index : TYPE, optional
        DESCRIPTION. The default is ''.
    fixing_calendars : TYPE, optional
        DESCRIPTION. The default is [].
    fixing_freq : TYPE, optional
        DESCRIPTION. The default is INVALID_FREQUENCY.
    fixing_day_convention : TYPE, optional
        DESCRIPTION. The default is INVALID_BUSINESS_DAY_CONVENTION.
    fixing_mode : TYPE, optional
        DESCRIPTION. The default is INVALID_DATE_GENERATION_MODE.
    fixing_day_offset : TYPE, optional
        DESCRIPTION. The default is Period(0, DAYS).

    Returns
    -------
    VanillaBondTemplate
        DESCRIPTION.

    '''    
    return create_vanilla_bond_template(inst_name, bond_type, issue_date, settlement_days, create_date(None), maturity,
                                        rate, currency, issue_price,                                 
                                        day_count,
                                        calendar, frequency, interest_day_convention, stub_policy, broken_period_type,
                                        pay_day_offset, pay_day_convention,
                                        ref_index,  
                                        fixing_calendars, fixing_freq, fixing_day_convention, fixing_mode, fixing_day_offset,
                                        '0D', '', 'INVALID_BUSINESS_DAY_CONVENTION', False,
                                        'CONST_NOTIONAL',
                                        recovery_rate)

# Standard Zero Coupon Bond Template:
def create_std_zero_cpn_bond_template(inst_name, issue_date, maturity, currency, calendar,                                       
                                      issue_price,   
                                      settlement_days = 1, 
                                      day_count = 'ACT_365_FIXED',
                                      pay_day_convention = 'MODIFIED_FOLLOWING',
                                      recovery_rate = 0.0):
    '''
    Create a standard zero coupon bond template object and store in the object cache.

    Parameters
    ----------
    inst_name : TYPE
        DESCRIPTION.
    maturity : TYPE
        DESCRIPTION.
    currency : TYPE
        DESCRIPTION.
    calendar : TYPE
        DESCRIPTION.
    settlement_days : TYPE, optional
        DESCRIPTION. The default is 1.
    day_count : TYPE, optional
        DESCRIPTION. The default is ACT_365_FIXED.
    pay_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.

    Returns
    -------
    VanillaBondTemplate
        DESCRIPTION.

    '''
    
    return create_std_bond_template(inst_name, 'ZERO_COUPON_BOND', issue_date, settlement_days, maturity,
                                    currency,                          
                                    day_count,
                                    calendar, 'ANNUAL', pay_day_convention, 'INITIAL', 'LONG',
                                    0, pay_day_convention,
                                    0.0,
                                    issue_price,    
                                    '', 
                                    [], 'INVALID_FREQUENCY', 'INVALID_BUSINESS_DAY_CONVENTION', 'INVALID_DATE_GENERATION_MODE', 0,
                                    recovery_rate)
    
# Standard Fixed Coupon Bond Template:
def create_std_fixed_cpn_bond_template(inst_name, issue_date, maturity,
                                       currency, calendar, 
                                       rate = 1.0,
                                       issue_price = 100.0,    
                                       settlement_days = 1, 
                                       day_count = 'ACT_365_FIXED',
                                       frequency = 'ANNUAL', 
                                       interest_day_convention = 'MODIFIED_FOLLOWING', 
                                       stub_policy = 'INITIAL', 
                                       broken_period_type = 'LONG',
                                       pay_day_offset = 0, 
                                       pay_day_convention = 'MODIFIED_FOLLOWING',
                                       recovery_rate = 0.0):
    '''
    Create a standard fixed coupon bond template object and store in the object cache.

    Parameters
    ----------
    inst_name : TYPE
        DESCRIPTION.
    maturity : TYPE
        DESCRIPTION.
    currency : TYPE
        DESCRIPTION.
    calendar : TYPE
        DESCRIPTION.
    settlement_days : TYPE, optional
        DESCRIPTION. The default is 1.
    day_count : TYPE, optional
        DESCRIPTION. The default is ACT_365_FIXED.
    frequency : TYPE, optional
        DESCRIPTION. The default is ANNUAL.
    interest_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.
    stub_policy : TYPE, optional
        DESCRIPTION. The default is INITIAL.
    broken_period_type : TYPE, optional
        DESCRIPTION. The default is LONG.
    pay_day_offset : TYPE, optional
        DESCRIPTION. The default is Period(0, DAYS).
    pay_day_convention : TYPE, optional
        DESCRIPTION. The default is MODIFIED_FOLLOWING.

    Returns
    -------
    VanillaBondTemplate
        DESCRIPTION.

    '''    
    return create_std_bond_template(inst_name, 'FIXED_COUPON_BOND', issue_date, settlement_days, maturity,
                                    currency,                       
                                    day_count,
                                    calendar, frequency, interest_day_convention, stub_policy, broken_period_type,
                                    pay_day_offset, pay_day_convention, rate, issue_price,
                                    '', 
                                    [], 'INVALID_FREQUENCY', 'INVALID_BUSINESS_DAY_CONVENTION', 'INVALID_DATE_GENERATION_MODE', 0,
                                    recovery_rate)
    
#Vanilla Bond 
def build_vanilla_bond(nominal, vanilla_bond_template, fixings):
    '''
    Build a vanilla bond instrument object.

    Parameters
    ----------
    nominal : TYPE
        DESCRIPTION.
    vanilla_bond_template : TYPE
        DESCRIPTION.
    fixings : TYPE
        DESCRIPTION.

    Returns
    -------
    VanillaBond
        DESCRIPTION.

    '''    
    pb_input = dqCreateProtoBuildVanillaBondInput(nominal, vanilla_bond_template, fixings)
    req_name = 'BUILD_VANILLA_BOND'
    res_msg = process_request(req_name, pb_input.SerializeToString())        
    pb_output = BuildVanillaBondOutput()
    pb_output.ParseFromString(res_msg)        
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)       
    return pb_output.instrument 

#Zero Cpn Bond 
def build_zero_cpn_bond(nominal, zero_cpn_bond_template):
    '''
    Build a zero coupon bond instrument object.    

    Parameters
    ----------
    nominal : float
        DESCRIPTION.
    zero_cpn_bond_template : VanillaBondTemplate
        DESCRIPTION.

    Returns
    -------
    VanillaBond
        DESCRIPTION.

    '''    
    return build_vanilla_bond(nominal, zero_cpn_bond_template, create_time_series([], []))

#Fixed Cpn Bond 
def build_fixed_cpn_bond(nominal, fixed_cpn_bond_template):
    '''
    Build a fixed coupon bond instrument object.

    Parameters
    ----------
    nominal : float
        DESCRIPTION.
    fixed_cpn_bond_template : VanillaBondTemplate
        DESCRIPTION.

    Returns
    -------
    VanillaBond
        DESCRIPTION.

    '''    
    return build_vanilla_bond(nominal, fixed_cpn_bond_template, create_time_series([], []))