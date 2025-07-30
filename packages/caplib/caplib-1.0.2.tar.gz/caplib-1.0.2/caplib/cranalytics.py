from datetime import datetime

from caplib.numerics import *
from caplib.market import *
from caplib.datetime import *
from caplib.analytics import *
from caplib.processrequest import process_request


# NumericalFix
def to_numerical_fix(src):
    """
    Convert the source to a numerical fix representation.

    Parameters
    ----------
    src : str or None
        The source string to convert.

    Returns
    -------
    int
        The numerical fix representation.
    """
    if src is None:
        return NONE_FIX

    if src in ['', 'nan']:
        return NONE_FIX
    else:
        return NumericalFix.DESCRIPTOR.values_by_name[src.upper()].number


def to_accrual_bias(src):
    """
    Convert the source to an accrual bias representation.

    Parameters
    ----------
    src : str or None
        The source string to convert.

    Returns
    -------
    int
        The accrual bias representation.
    """
    if src is None:
        return HALFDAYBIAS

    if src in ['', 'nan']:
        return HALFDAYBIAS
    else:
        return AccrualBias.DESCRIPTOR.values_by_name[src.upper()].number


def to_forwards_in_coupon_period(src):
    """
    Convert the source to a forwards in coupon period representation.

    Parameters
    ----------
    src : str or None
        The source string to convert.

    Returns
    -------
    int
        The forwards in coupon period representation.
    """
    if src is None:
        return FLAT

    if src in ['', 'nan']:
        return FLAT
    else:
        return ForwardsInCouponPeriod.DESCRIPTOR.values_by_name[src.upper()].number


def create_cr_risk_settings(ir_curve_settings, cs_curve_settings, theta_settings):
    """
    Create credit risk settings.

    Parameters
    ----------
    ir_curve_settings : object
        Interest rate curve settings.
    cs_curve_settings : object
        Credit spread curve settings.
    theta_settings : object
        Theta settings.

    Returns
    -------
    object
        Credit risk settings.
    """
    settings = dqCreateProtoCrRiskSettings(ir_curve_settings,
                                           cs_curve_settings,
                                           theta_settings)
    return settings


def create_credit_par_curve(as_of_date, currency, name, pillars):
    """
    Create a credit par curve.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the curve.
    currency : str
        The currency of the curve.
    name : str
        The name of the curve.
    pillars : list
        List of tuples representing pillar data.

    Returns
    -------
    object
        The created credit par curve.
    """
    try:
        p_pillars = list()
        for pillar in pillars:
            p_pillars.append(dqCreateProtoCreateCreditParCurveInput_Pillar(str(pillar[0]),
                                                                           to_instrument_type(str(pillar[1])),
                                                                           to_period(str(pillar[2])),
                                                                           float(pillar[3]),
                                                                           to_instrument_start_convention('spotstart')))
        pb_input = dqCreateProtoCreateCreditParCurveInput(create_date(as_of_date),
                                                          currency,
                                                          p_pillars,
                                                          name)
        req_name = "CREATE_CREDIT_PAR_CURVE"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = CreateCreditParCurveOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.par_curve
    except Exception as e:
        return str(e)


def credit_curve_builder(as_of_date, curve_name, par_curve, discount_curve, building_method, calc_jacobian):
    """
    Build a credit curve.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the curve.
    curve_name : str
        The name of the curve.
    par_curve : object
        Par curve for the credit curve.
    discount_curve : object
        Discount curve for the credit curve.
    building_method : str
        Method to build the curve.
    calc_jacobian : bool
        Whether to calculate the Jacobian.

    Returns
    -------
    object
        The built credit curve.
    """
    try:
        pb_input = dqCreateProtoCreditCurveBuildingInput(par_curve,
                                                         curve_name,
                                                         create_date(as_of_date),
                                                         discount_curve,
                                                         building_method)

        req_name = "CREDIT_CURVE_BUILDER"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        pb_output = CreditCurveBuildingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output.credit_curve
    except Exception as e:
        return str(e)


def create_cds_pricing_settings(pricing_currency,
                                include_current_flow,
                                cash_flows,
                                numerical_fix,
                                accrual_bias,
                                fwds_in_cpn_period):
    """
    Create CDS pricing settings.

    Parameters
    ----------
    pricing_currency : str
        The currency for pricing.
    include_current_flow : bool
        Whether to include current flow.
    cash_flows : object
        Cash flows for pricing.
    numerical_fix : str
        Numerical fix setting.
    accrual_bias : str
        Accrual bias setting.
    fwds_in_cpn_period : str
        Forwards in coupon period setting.

    Returns
    -------
    object
        The created CDS pricing settings.
    """
    try:
        model_params = [int(include_current_flow),
                        int(to_numerical_fix(numerical_fix)),
                        int(to_accrual_bias(accrual_bias)),
                        int(to_forwards_in_coupon_period(fwds_in_cpn_period))]
        model_settings = create_model_settings("", model_params)
        settings = create_pricing_settings(
            pricing_currency,
            include_current_flow,
            model_settings,
            'ANALYTICAL',
            create_pde_settings(),
            create_monte_carlo_settings(),
            [],
            cash_flows
        )
        return settings
    except Exception as e:
        return str(e)


def create_cr_mkt_data_set(as_of_date, discount_curve, credit_curve):
    """
    Create credit market data set.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the market data set.
    discount_curve : object
        The discount curve.
    credit_curve : object
        The credit curve.

    Returns
    -------
    object
        The created credit market data set.
    """
    try:
        mkt_data = dqCreateProtoCrMktDataSet(create_date(as_of_date),
                                             discount_curve,
                                             credit_curve)
        return mkt_data
    except Exception as e:
        return str(e)


def credit_default_swap_pricer(instrument,
                               pricing_date,
                               mkt_data_set,
                               pricing_settings,
                               risk_settings):
    """
    Price a credit default swap.

    Parameters
    ----------
    instrument : object
        The credit default swap instrument.
    pricing_date : datetime
        The date for pricing.
    mkt_data_set : object
        Market data set for pricing.
    pricing_settings : object
        Pricing settings for the swap.
    risk_settings : object
        Risk settings for the swap.

    Returns
    -------
    object
        The result of credit default swap pricing.
    """
    try:
        credit_default_swap_pricing_input = dqCreateProtoCreditDefaultSwapPricingInput(create_date(pricing_date),
                                                                                       instrument,
                                                                                       mkt_data_set,
                                                                                       pricing_settings,
                                                                                       risk_settings,
                                                                                       False, b'', b'', b'', b'')
        req_name = "CREDIT_DEFAULT_SWAP_PRICER"
        res_msg = process_request(req_name, credit_default_swap_pricing_input.SerializeToString())
        pb_output = CreditDefaultSwapPricingOutput()
        pb_output.ParseFromString(res_msg)
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)
        return pb_output
    except Exception as e:
        return str(e)