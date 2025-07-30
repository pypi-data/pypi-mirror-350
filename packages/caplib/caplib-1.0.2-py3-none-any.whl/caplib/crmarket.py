
from caplib.market import *
from caplib.datetime import *
from caplib.staticdata import *

def to_credit_protection_type(src):
    '''
    将字符串转换为 CreditProtectionType.

    Parameters
    ----------
    src : str

    Returns
    -------
    CreditProtectionType

    '''
    if src is None:
        return PAY_PROTECTION_AT_DEFAULT
    if src in ['', 'nan']:
        return PAY_PROTECTION_AT_DEFAULT
    else:
        return CreditProtectionType.DESCRIPTOR.values_by_name[src.upper()].number
    
def to_credit_premium_type(src):
    '''
    将字符串转换为 CreditPremiumType.

    Parameters
    ----------
    src : str

    Returns
    -------
    CreditPremiumType

    '''
    if src is None:
        return PAY_PREMIUM_AT_DEFAULT
    if src in ['', 'nan']:
        return PAY_PREMIUM_AT_DEFAULT
    else:
        return CreditPremiumType.DESCRIPTOR.values_by_name[src.upper()].number
    
#CreateCdsTemplate
def create_cds_template(inst_name, 
                        start_delay, 
                        settlement_type, 
                        reference_price, 
                        leverage, 
                        credit_protection_type, 
                        recovery_rate, 
                        credit_premium_type, 
                        day_count, 
                        frequency, 
                        business_day_convention, 
                        calendars, 
                        rebate_accrual):
    try:
        inst_template = dqCreateProtoCreditInstrumentTemplate(inst_name,
                                                              to_instrument_type('credit_default_swap'),
                                                              to_instrument_start_convention('spotstart'),
                                                              to_period(start_delay),
                                                              to_settlement_type(settlement_type),
                                                              reference_price,
                                                              leverage,
                                                              to_credit_protection_type(credit_protection_type),
                                                              recovery_rate,
                                                              to_credit_premium_type(credit_premium_type),
                                                              to_day_count_convention(day_count),
                                                              to_frequency(frequency),
                                                              to_business_day_convention(business_day_convention),
                                                              calendars,
                                                              rebate_accrual)
        pb_data_list = dqCreateProtoCreditInstrumentTemplateList([inst_template])  
        create_static_data('SDT_CREDIT_INSTRUMENT', pb_data_list.SerializeToString())
        return inst_template
    except Exception as e:
        return e.__str__()

#BuildCreditDefaultSwap
def build_credit_default_swap(nominal,
                                 currency,
                                 issue_date,
                                 maturity,
                                 protection_leg_pay_receive,
                                 protection_leg_settlement_type,
                                 protection_leg_reference_price,
                                 protection_leg_leverage,
                                 credit_protection_type,
                                 protection_leg_recovery_rate,
                                 coupon_rate,
                                 credit_premium_type,
                                 day_count_convention,
                                 frequency,
                                 business_day_convention,
                                 calendars,
                                 upfront_rate,
                                 rebate_accrual):
    try:
        build_credit_default_swap_input = dqCreateProtoBuildCreditDefaultSwapInput(dqCreateProtoNotional(currency, nominal),
                                                                                   create_date(issue_date),
                                                                                   create_date(maturity),
                                                                                   to_pay_receive_flag(protection_leg_pay_receive),
                                                                                   to_settlement_type(protection_leg_settlement_type),
                                                                                   protection_leg_reference_price,
                                                                                   protection_leg_leverage,
                                                                                   to_credit_protection_type(credit_protection_type),
                                                                                   protection_leg_recovery_rate,
                                                                                   coupon_rate,
                                                                                   to_credit_premium_type(credit_premium_type),
                                                                                   to_day_count_convention(day_count_convention),
                                                                                   to_frequency(frequency),
                                                                                   to_business_day_convention(business_day_convention),
                                                                                   calendars,
                                                                                   upfront_rate,
                                                                                   rebate_accrual)
        req_name = "BUILD_CREDIT_DEFAULT_SWAP"
        res_msg = process_request(req_name, build_credit_default_swap_input.SerializeToString())
        pb_output = BuildCreditDefaultSwapOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.credit_default_swap
    except Exception as e:
        return str(e)