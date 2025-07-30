# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:25:51 2022

@author: dingq
"""

import pandas as pd
from datetime import datetime, timedelta

from caplibproto.dqnumerics_pb2 import *
from caplibproto.dqdatetime_pb2 import *
from caplibproto.dqanalytics_pb2 import *

from caplib.numerics import *
from caplib.datetime import *
from caplib.market import *
from caplib.utility import num_to_bytes 

# CompoundingType
def to_compounding_type(src):
    '''
    将字符串转换为 CompoundingType类型.
    
    Parameters
    ----------
    src : str
        表示复利类型的字符串，如‘CONTINUOUS_COMPOUNDING’.

    Returns
    -------
    CompoundingType       

    '''
    if src is None:
        return CONTINUOUS_COMPOUNDING
    if src in ['', 'nan']:
        return CONTINUOUS_COMPOUNDING
    else:
        return CompoundingType.DESCRIPTOR.values_by_name[src.upper()].number

# PricingModelName
def to_pricing_model_name(src):
    '''
    将字符串转换为 PricingModelName 类型.
    
    Parameters
    ----------
    src : str
        表示定价模型的字符串，如‘BLACK_SCHOLES_MERTON’.

    Returns
    -------
    PricingModelName       

    '''
    if src is None:
        return BLACK_SCHOLES_MERTON
    if src in ['', 'nan']:
        return BLACK_SCHOLES_MERTON
    else:
        return PricingModelName.DESCRIPTOR.values_by_name[src.upper()].number

# PricingMethodName
def to_pricing_method_name(src):
    '''
    将字符串转换为 PricingMethodName 类型.

    Parameters
    ----------
    src : str
        表示定价方法类型的字符串，如‘ANALYTICAL’.

    Returns
    -------
    PricingMethodName       

    '''
    if src is None:
        return ANALYTICAL
    if src in ['', 'nan']:
        return ANALYTICAL
    else:
        return PricingMethodName.DESCRIPTOR.values_by_name[src.upper()].number

# FiniteDifferenceMethod
def to_finite_difference_method(src):
    '''
    将字符串转换为 FiniteDifferenceMethod 类型.
    
    Parameters
    ----------
    src : str
        表示差分方法类型的字符串，如‘CENTRAL_DIFFERENCE_METHOD’.

    Returns
    -------
    FiniteDifferenceMethod       

    '''
    if src is None:
        return CENTRAL_DIFFERENCE_METHOD
    if src in ['', 'nan']:
        return CENTRAL_DIFFERENCE_METHOD
    else:
        return FiniteDifferenceMethod.DESCRIPTOR.values_by_name[src.upper()].number

# ThreadingMode
def to_threading_mode(src):
    '''
    将字符串转换为 ThreadingMode 类型.
    
    Parameters
    ----------
    src : str
        表示线程模式的字符串，如‘SINGLE_THREADING_MODE’.

    Returns
    -------
    ThreadingMode       

    '''
    if src is None:
        return SINGLE_THREADING_MODE
    if src in ['', 'nan']:
        return SINGLE_THREADING_MODE
    else:
        return ThreadingMode.DESCRIPTOR.values_by_name[src.upper()].number

# RiskGranularity
def to_risk_granularity(src):
    '''
    将字符串转换为 RiskGranularity 类型.
    
    Parameters
    ----------
    src : str
        表示风险颗粒度模式的字符串，如‘TOTAL_RISK’.

    Returns
    -------
    RiskGranularity       

    '''
    if src is None:
        return TOTAL_RISK
    if src in ['', 'nan']:
        return TOTAL_RISK
    else:
        return RiskGranularity.DESCRIPTOR.values_by_name[src.upper()].number

# IrYieldCurveBuildingMethod
def to_ir_yield_curve_building_method(src):
    '''
    将字符串转换为 IrYieldCurveBuildingMethod 类型.

    Parameters
    ----------
    src : str
        表示收益率曲线构建类型的字符串，如‘BOOTSTRAPPING_METHOD’.

    Returns
    -------
    IrYieldCurveBuildingMethod

    '''
    if src is None:
        return BOOTSTRAPPING_METHOD
    if src in ['', 'nan']:
        return BOOTSTRAPPING_METHOD
    else:
        return IrYieldCurveBuildingMethod.DESCRIPTOR.values_by_name[src.upper()].number

# IrYieldCurveType
def to_ir_yield_curve_type(src):
    '''
    将字符串转换为 IrYieldCurveType.

    Parameters
    ----------
    src : str
        表示收益率曲线类型的字符串，如‘ZERO_RATE’.

    Returns
    -------
    IrYieldCurveType

    '''
    if src is None:
        return ZERO_RATE
    if src in ['', 'nan']:
        return ZERO_RATE
    else:
        return IrYieldCurveType.DESCRIPTOR.values_by_name[src.upper()].number
  
# DividendType
def to_dividend_type(src):
    '''
    将字符串转换为 DividendType.

    Parameters
    ----------
    src : str

    Returns
    -------
    DividendType

    '''
    if src is None:
        return CONTINUOUS_DIVIDEND
    if src in ['', 'nan']:
        return CONTINUOUS_DIVIDEND
    else:
        return DividendType.DESCRIPTOR.values_by_name[src.upper()].number
    
def to_option_quote_value_type(src):
    '''
    将字符串转换为 OptionQuoteValueType.

    Parameters
    ----------
    src : str

    Returns
    -------
    OptionQuoteValueType

    '''
    if src is None:
        return OQVT_PRICE
    if src in ['', 'nan']:
        return OQVT_PRICE
    else:
        return OptionQuoteValueType.DESCRIPTOR.values_by_name[src.upper()].number
                      
def to_option_quote_term_type(src):
    '''
    将字符串转换为 OptionQuoteTermType.

    Parameters
    ----------
    src : str

    Returns
    -------
    OptionQuoteTermType

    '''
    if src is None:
        return OQTT_ABOSULTE_TERM
    if src in ['', 'nan']:
        return OQTT_ABOSULTE_TERM
    else:
        return OptionQuoteTermType.DESCRIPTOR.values_by_name[src.upper()].number

def to_option_quote_strike_type(src):
    '''
    将字符串转换为 OptionQuoteStrikeType.

    Parameters
    ----------
    src : str

    Returns
    -------
    OptionQuoteStrikeType

    '''
    if src is None:
        return OQST_ABOSULTE_STRIKE
    if src in ['', 'nan']:
        return OQST_ABOSULTE_STRIKE
    else:
        return OptionQuoteStrikeType.DESCRIPTOR.values_by_name[src.upper()].number

def to_option_underlying_type(src):
    '''
    将字符串转换为 OptionUnderlyingType.

    Parameters
    ----------
    src : str

    Returns
    -------
    OptionUnderlyingType

    '''
    if src is None:
        return SPOT_UNDERLYING_TYPE
    if src in ['', 'nan']:
        return SPOT_UNDERLYING_TYPE
    else:
        return OptionUnderlyingType.DESCRIPTOR.values_by_name[src.upper()].number

def to_smile_quote_type(src):
    '''
    将字符串转换为SmileQuoteType类型.

    Parameters
    ----------
    src : str
        a string of vol smile type, i.e. 'STRIKE_VOL_SMILE'.

    Returns
    -------
    SmileQuoteType

    '''
    if src is None:
        return BUTTERFLY_QUOTE
    if src in ['', 'nan']:
        return BUTTERFLY_QUOTE
    else:
        return SmileQuoteType.DESCRIPTOR.values_by_name[src.upper()].number
    
def to_vol_smile_type(src):
    '''
    将字符串转换为VolSmileType类型.

    Parameters
    ----------
    src : str
        a string of vol smile type, i.e. 'STRIKE_VOL_SMILE'.

    Returns
    -------
    VolSmileType

    '''
    if src is None:
        return STRIKE_VOL_SMILE
    if src in ['', 'nan']:
        return STRIKE_VOL_SMILE
    else:
        return VolSmileType.DESCRIPTOR.values_by_name[src.upper()].number

def to_vol_smile_method(src):
    '''
    将字符串转换为VolSmileMethod类型.

    Parameters
    ----------
    src : str
        a string of vol smile method, i.e. 'LINEAR_SMILE_METHOD'.

    Returns
    -------
    VolSmileMethod

    '''
    if src is None:
        return LINEAR_SMILE_METHOD
    if src in ['', 'nan']:
        return LINEAR_SMILE_METHOD
    else:
        return VolSmileMethod.DESCRIPTOR.values_by_name[src.upper()].number

# VolTermInterpMethod
def to_vol_term_time_interp_method(src):
    '''
    Convert a string to VolTermInterpMethod.

    Parameters
    ----------
    src : str
        A string representing the vol term interpolation method.

    Returns
    -------
    VolTermInterpMethod
    '''
    if src is None:
        return LINEAR_IN_VARIANCE
    
    if src in ['', 'nan']:
        return LINEAR_IN_VARIANCE
    else:
        return VolTermInterpMethod.DESCRIPTOR.values_by_name[src.upper()].number

# VolTermExtrapMethod 
def to_vol_termtime_extrap_method(src):
    '''
    Convert a string to VolTermExtrapMethod.

    Parameters
    ----------
    src : str
        A string representing the vol term extrapolation method.

    Returns
    -------
    VolTermExtrapMethod
    '''
    if src is None:
        return FLAT_IN_VOLATILITY
    
    if src in ['', 'nan']:
        return FLAT_IN_VOLATILITY
    else:
        return VolTermExtrapMethod.DESCRIPTOR.values_by_name[src.upper()].number

# VolatilityType 
def to_volatility_type(src):
    '''
    Convert a string to VolatilityType.

    Parameters
    ----------
    src : str
        A string representing the volatility type.

    Returns
    -------
    VolatilityType
    '''
    if src is None:
        return LOG_NORMAL_VOL_TYPE
    
    if src in ['', 'nan']:
        return LOG_NORMAL_VOL_TYPE
    else:
        return VolatilityType.DESCRIPTOR.values_by_name[src.upper()].number

# WingStrikeType 
def to_wing_strike_type(src):
    '''
    Convert a string to WingStrikeType.

    Parameters
    ----------
    src : str
        A string representing the wing strike type.

    Returns
    -------
    WingStrikeType
    '''
    if src is None:
        return DELTA
    
    if src in ['', 'nan']:
        return DELTA
    else:
        return WingStrikeType.DESCRIPTOR.values_by_name[src.upper()].number

# AtmType 
def to_atm_type(src):
    '''
    Convert a string to AtmType.

    Parameters
    ----------
    src : str
        A string representing the ATM type.

    Returns
    -------
    AtmType
    '''
    if src is None:
        return ATM_FORWARD
    
    if src in ['', 'nan']:
        return ATM_FORWARD
    else:
        return AtmType.DESCRIPTOR.values_by_name[src.upper()].number

# DeltaType 
def to_delta_type(src):
    '''
    Convert a string to DeltaType.

    Parameters
    ----------
    src : str
        A string representing the delta type.

    Returns
    -------
    DeltaType
    '''
    if src is None:
        return PIPS_SPOT_DELTA
    
    if src in ['', 'nan']:
        return PIPS_SPOT_DELTA
    else:
        return DeltaType.DESCRIPTOR.values_by_name[src.upper()].number

def to_scn_analysis_type(src):
    '''
    Convert a string to ScnAnalysisType.

    Parameters
    ----------
    src : str
        A string representing the scenario analysis type.

    Returns
    -------
    ScnAnalysisType
    '''
    if src is None:
        return NO_SCN_ANALYSIS
    
    if src in ['', 'nan']:
        return NO_SCN_ANALYSIS
    else:
        return ScnAnalysisType.DESCRIPTOR.values_by_name[src.upper()].number
    
# Pricing Model Settings
def create_model_settings(model_name: str,
                          constant_params=[0.0],
                          time_homogeneous_model_params=[],
                          underlying='',
                          model_calibrated=False):
    '''
    创建定价模型的参数设置对象.
    
    Parameters
    ----------
    model_name : str
        模型名称，查看可支持的模型:'PricingModelName'.
    constant_params : list, optional
        非时间函数的模型参数值，如Displaced Black模型中的Displacement参数.
    time_homogeneous_model_params : list, optional
        期限结构的模型参数值,如Hull-White利率模型中的期限结构波动率P参数.
    underlying : str, optional
        模型所对应的标的资产名称，如货币对‘USDCNY’， 沪深300指数等.
    model_calibrated : bool, optional
        标识模型参数是否已校验，默认值为否.

    Returns
    -------
    PricingModelSettings
        定价模型的Parameters设置对象
    '''
    return dqCreateProtoPricingModelSettings(to_pricing_model_name(model_name),
                                             constant_params,
                                             time_homogeneous_model_params,
                                             underlying,
                                             model_calibrated)

# PDE Settings
def create_pde_settings(t_size=50,
                        x_size=100, x_min=-4.0, x_max=4.0, x_min_max_type='MMT_NUM_STDEVS',
                        x_density=1.0, x_grid_type='UNIFORM_GRID', x_interp_method='LINEAR_INTERP',
                        y_size=3, y_min=-4.0, y_max=4.0, y_min_max_type='MMT_NUM_STDEVS',
                        y_density=1.0, y_grid_type='UNIFORM_GRID', y_interp_method='LINEAR_INTERP',
                        z_size=3, z_min=-4.0, z_max=4.0, z_min_max_type='MMT_NUM_STDEVS',
                        z_density=1.0, z_grid_type='UNIFORM_GRID', z_interp_method='LINEAR_INTERP'):
    '''
    创建PDE数值解法需要的参数设置对象.
    
    Parameters
    ----------
    t_size : int, optional
        时间网格的点数尺寸，默认值为50.
    x_size : int, optional
        空间第一维度网格的点数尺寸，默认值为100.
    x_min : float, optional
        空间第一维度网格的下边界值，可以为绝对值或标准差数，默认值为4个标准差.
    x_max : float, optional
        空间第一维度网格的上边界值，可以为绝对值或标准差数，默认值为4个标准差.
    x_min_max_type : PdeSettings.MinMaxType, optional
        空间第一维度网格的边界值类型，可以为绝对值或标准差类型，默认值为标准差 MMT_NUM_STDEVS.
    x_density : float, optional
        空间第一维度网格的密度Parameters，这是针对非均匀网格的时候。默认值为1.0.
    x_grid_type : GridType, optional
        空间第一维度网格的类型，分为均匀网格和非均匀网格。默认值为1.0.
    x_interp_method : InterpMethod, optional
        空间第一维度网格使用的插值方法，默认为线性插值（LINEAR_INTERP）.
    y_size : int, optional
        Size of 2nd dimension spatial grid. The default is 3.
    y_min : float, optional
        Lower boundary of 2nd dimension spatial grid and it can be either an absolute boundary value or standard devidation. The default is -4.0.
    y_max : float, optional
        Upper boundary of 2nd dimension spatial grid and it can be either an absolute boundary value or standard devidation. The default is 4.0.
    y_min_max_type : PdeSettings.MinMaxType, optional
        The boundary value type for 2nd dimension spatial grid. The default is 'MMT_NUM_STDEVS'.
    y_density : float, optional
        The density of 2nd dimension spatial grid when the grid is non-uniform. The default is 1.0.
    y_grid_type : GridType, optional
        The type of 2nd dimension spatial grid. The default is 'UNIFORM_GRID'.
    y_interp_method : InterpMethod, optional
        The interpolation method for 2nd dimension spatial grid. The default is 'LINEAR_INTERP'.
    z_size : int, optional
        Size of 3rd dimension spatial grid. The default is 3.
    z_min : float, optional
        Lower boundary of 3rd dimension spatial grid and it can be either an absolute boundary value or standard devidation. The default is -4.0.
    z_max : float, optional
        Upper boundary of 3rd dimension spatial grid and it can be either an absolute boundary value or standard devidation. The default is 4.0.
    z_min_max_type : PdeSettings.MinMaxType, optional
        The boundary value type for 3rd dimension spatial grid. The default is 'MMT_NUM_STDEVS'.
    z_density : float, optional
        The density of 3rd dimension spatial grid when the grid is non-uniform. The default is 1.0.
    z_grid_type : GridType, optional
        The type of 3rd dimension spatial grid. The default is 'UNIFORM_GRID'.
    z_interp_method : InterpMethod, optional
        The interpolation method for 3rd dimension spatial grid. The default is 'LINEAR_INTERP'.

    Returns
    -------
    PdeSettings
        PDE数值解法需要的参数设置对象
    '''
    return dqCreateProtoPdeSettings(t_size,
                                    x_size, x_min, x_max, to_pde_min_max_type(x_min_max_type),
                                    y_size, y_min, y_max, to_pde_min_max_type(y_min_max_type),
                                    z_size, z_min, z_max, to_pde_min_max_type(z_min_max_type),
                                    x_density, y_density, z_density,
                                    to_grid_type(x_grid_type),
                                    to_grid_type(y_grid_type),
                                    to_grid_type(z_grid_type),
                                    to_interp_method(x_interp_method),
                                    to_interp_method(y_interp_method),
                                    to_interp_method(z_interp_method))

# Monte Carlo Settings
def create_monte_carlo_settings(num_simulations=1024,
                                uniform_number_type='SOBOL_NUMBER',
                                seed=1024,
                                wiener_process_build_method='BROWNIAN_BRIDGE_METHOD',
                                gaussian_number_method='INVERSE_CUMULATIVE_METHOD',
                                use_antithetic=False,
                                num_steps=1):
    '''
    创建蒙特卡洛仿真需要的参数设置对象.

    Parameters
    ----------
    num_simulations : int, optional
        蒙特卡洛仿真次数，默认值为1024.
    uniform_number_type : UniformRandomNumberType, optional
        均匀分布随机数类型，默认值为Sobol随机数（SOBOL_NUMBER）.
    seed : int, optional
        产生均匀分布随机数需要的种子值，默认为1024.
    wiener_process_build_method : WienerProcessBuildMethod, optional
        构建布朗运动过程的方法，默认为布朗桥方法（BROWNIAN_BRIDGE_METHOD）.
    gaussian_number_method : GaussianNumberMethod, optional
        根据均匀分布随机数生成正态分布随机数的方法，默认为INVERSE_CUMULATIVE_METHOD.
    use_antithetic : bool, optional
        设置是否使用Antithetic的方差减少方法，默认为否（False）.
    num_steps : int, optional
        设置在创建布朗运动过程中每个时间区间中所需的额外步长，默认为1.

    Returns
    -------
    MonteCarloSettings    
        蒙特卡洛仿真需要的参数设置对象.
    '''
    return dqCreateProtoMonteCarloSettings(num_simulations,
                                           to_uniform_random_number_type(uniform_number_type),
                                           seed,
                                           to_wiener_process_build_method(wiener_process_build_method),
                                           to_gaussian_number_method(gaussian_number_method),
                                           use_antithetic,
                                           num_steps)

# Pricing Settings:
def create_pricing_settings(pricing_currency,
                            inc_current,
                            model_settings,
                            pricing_method,
                            pde_settings,
                            mc_settings,
                            specific_pricing_requests=[],
                            cash_flows=False):
    '''
    创建产品定价所需的参数设置，包括模型参数，定价方法，PDE数值解法参数，蒙特卡洛参数，以及用户指定指标.
    
    Parameters
    ----------
    pricing_currency: str, optional
        产品定价所指定的货币.
    inc_current : bool
        设置是否将当前的现金流计入产品现值中.
    model_settings : PricingModelSettings
        设置定价模型参数.
    pricing_method : str
        指定定价方法，如解析解或其它数值解法.
    pde_settings : PdeSettings
        设置PDE数值解法参数，如果定价方法为PDE.
    mc_settings : MonteCarloSettings
        设置蒙特卡洛仿真参数，如果定价方法为蒙特卡洛.
    specific_pricing_requests : list, optional
        设置针对特定产品的计算指标，如对于债券，有到期收益率，全价，净价等， 默认为空.
    cash_flows: bool, optional
    
    Returns
    -------
    PricingSettings
        产品定价所需的参数设置.
    '''
    return dqCreateProtoPricingSettings(pricing_currency,
                                        inc_current,
                                        pde_settings,
                                        mc_settings,
                                        model_settings,
                                        to_pricing_method_name(pricing_method),
                                        specific_pricing_requests,
                                        cash_flows)

# Default Pricing Settings:
def create_model_free_pricing_settings(pricing_currency='',
                                       inc_current=True,
                                       specific_pricing_requests=[],
                                       cash_flows=False):
    '''
    创建无需模型的产品定价所需的参数设置.
    
    Parameters
    ----------
    pricing_currency: str, optional
        Currency specified for instrument pricing.
    inc_current : bool, optional
        设置是否将当前的现金流计入产品现值中， 默认为是（True） .
    specific_pricing_requests : list, optional
        设置针对特定产品的计算指标，如对于债券，有到期收益率，全价，净价等， 默认为空.
    cash_flows: bool, optional

    Returns
    -------
    PricingSettings
        产品定价所需的参数设置.

    '''
    return create_pricing_settings(pricing_currency,
                                   inc_current,
                                   create_model_settings(''),
                                   'ANALYTICAL',
                                   create_pde_settings(),
                                   create_monte_carlo_settings(),
                                   specific_pricing_requests,
                                   cash_flows)

# IR Curve Risk Settings:
def create_ir_curve_risk_settings(delta=False,
                                  gamma=False,
                                  curvature=False,
                                  shift=1.0e-4,
                                  curvature_shift=5.0e-3,
                                  method='CENTRAL_DIFFERENCE_METHOD',
                                  granularity='TOTAL_RISK',
                                  scaling_factor=1.0e-4,
                                  threading_mode='SINGLE_THREADING_MODE'):
    '''
    创建计算利率收益率曲线敏感度的风险参数设置.
    
    Parameters
    ----------
    delta : bool, optional
        设置是否计算曲线Delta（DV01），默认为否.
    gamma : bool, optional
        设置是否计算曲线Gamma，默认为否.
    curvature : bool, optional
        设置是否计算曲线Curvature,根据FRTB定义，默认为否.
    shift : float, optional
        计算曲线Delta和Gamma时的扰动大小，默认为1基点.
    curvature_shift : float, optional
        计算曲线Curvature的扰动大小，默认为50基点.
    method : FiniteDifferenceMethod, optional
        计算曲线Delta的差分方法，默认为中央差分法（CENTRAL_DIFFERENCE_METHOD）.
    granularity : RiskGranularity, optional
        设置计算曲线Delta和Gamma的颗粒度，默认为整体平移（TOTAL_RISK）.
    scaling_factor : float, optional
        将百分比型的敏感度转换成实际的价格变化绝对值的因子值，默认为1基点.
    threading_mode : ThreadingMode, optional
        计算敏感度时的线程模式，可以设为单线程和多线程两种，默认为单线程.

    Returns
    -------
    IrCurveRiskSettings
        计算利率收益率曲线敏感度的风险参数设置对象.
    '''
    return dqCreateProtoIrCurveRiskSettings(delta, gamma, curvature, shift, curvature_shift,
                                            to_finite_difference_method(method),
                                            to_risk_granularity(granularity),
                                            scaling_factor,
                                            to_threading_mode(threading_mode))

# Credit Curve Risk Settings:
def create_credit_curve_risk_settings(delta=False,
                                      gamma=False,
                                      shift=1.0e-4,
                                      method='CENTRAL_DIFFERENCE_METHOD',
                                      granularity='TOTAL_RISK',
                                      scaling_factor=1.0e-4,
                                      threading_mode='SINGLE_THREADING_MODE'):
    '''
    创建计算信用曲线敏感度需要的风险参数设置.
    
    Parameters
    ----------
    delta : bool, optional
        设置是否计算曲线Delta（CS01），默认为否.
    gamma : bool, optional
        设置是否计算曲线Gamma，默认为否
    shift : float, optional
        计算曲线Delta和Gamma时的扰动大小，默认为1基点.
    method : FiniteDifferenceMethod, optional
        计算曲线Delta的差分方法，默认为中央差分法（CENTRAL_DIFFERENCE_METHOD）.
    granularity : RiskGranularity, optional
        设置计算曲线Delta和Gamma的颗粒度，默认为整体平移（TOTAL_RISK）.
    scaling_factor : float, optional
        将百分比型的敏感度转换成实际的价格变化绝对值的因子值，默认为1基点.
    threading_mode : ThreadingMode, optional
        计算敏感度时的线程模式，可以设为单线程和多线程两种，默认为单线程.

    Returns
    -------
    CreditCurveRiskSettings
        计算信用曲线敏感度需要的风险参数设置对象.

    '''
    return dqCreateProtoCreditCurveRiskSettings(delta, gamma, shift,
                                                to_finite_difference_method(method),
                                                to_risk_granularity(granularity),
                                                scaling_factor,
                                                to_threading_mode(threading_mode))

#CreateDividendCurveRiskSettings
def create_dividend_curve_risk_settings(delta=False, 
                                        gamma=False, 
                                        shift=1.0e-4, 
                                        method="CENTRAL_DIFFERENCE_METHOD", 
                                        granularity="TOTAL_RISK", 
                                        scaling_factor=1.0e-4, 
                                        threading_mode="SINGLE_THREADING_MODE"):
    """
    Creates risk settings for dividend curve sensitivity calculations.
    
    Parameters
    ----------
    delta : bool, optional
        Specifies whether to calculate the curve Delta. Default is False.
    gamma : bool, optional
        Specifies whether to calculate the curve Gamma. Default is False.
    shift : float, optional
        The perturbation size for Delta and Gamma calculations. Default is 1.0e-4.
    method : FiniteDifferenceMethod, optional
        The finite difference method used for Delta calculation. Default is "CENTRAL_DIFFERENCE_METHOD".
    granularity : RiskGranularity, optional
        The granularity for Delta and Gamma calculations. Default is "TOTAL_RISK".
    scaling_factor : float, optional
        Factor to convert percentage sensitivity to absolute price change. Default is 1.0e-4.
    threading_mode : ThreadingMode, optional
        The threading mode for sensitivity calculations. Default is "SINGLE_THREADING_MODE".
    
    Returns
    -------
    DividendCurveRiskSettings
        An object representing the risk settings for dividend curve sensitivity calculations.
    """
    settings = dqCreateProtoDividendCurveRiskSettings(delta, gamma, shift, 
                                                      to_finite_difference_method(method), 
                                                      to_risk_granularity(granularity), 
                                                      scaling_factor, 
                                                      to_threading_mode(threading_mode))
    return settings

# Theta Risk Settings:
def create_theta_risk_settings(theta=False, shift=1, scaling_factor=1. / 365.):
    '''
    创建计算Theta的参数设置.
    
    Parameters
    ----------
    theta : bool, optional
        设置是否计算Theta，默认为否.
    shift : int, optional
        计算曲线Delta和Gamma时的扰动大小，默认为1天.
    scaling_factor : float, optional
        将百分比型的敏感度转换成实际的价格变化绝对值的因子值，默认为1./365.

    Returns
    -------
    ThetaRiskSettings
        计算Theta的参数设置对象.

    '''
    return dqCreateProtoThetaRiskSettings(theta, shift, scaling_factor)

def create_scn_analysis_settings(scn_analysis_type: str, 
                                 min_underlying_price: float, 
                                 max_underlying_price: float, 
                                 num_price_scns: int,
                                 price_scn_gen_type: int,
                                 min_vol: float, 
                                 max_vol: float,
                                 num_vol_scns: int, 
                                 vol_scn_gen_type=0,
                                 threading_mode='SINGLE_THREADING_MODE'):
    """
    Create scenario analysis settings.

    Parameters
    ----------
    scn_analysis_type : str
        Type of scenario analysis.
    min_underlying_price : float
        Minimum underlying price for price scenario generation.
    max_underlying_price : float
        Maximum underlying price for price scenario generation.
    num_price_scns : int
        Number of price scenarios to generate.
    price_scn_gen_type : int
        Type of price scenario generation.
    min_vol : float
        Minimum volatility for volatility scenario generation.
    max_vol : float
        Maximum volatility for volatility scenario generation.
    num_vol_scns : int
        Number of volatility scenarios to generate.
    vol_scn_gen_type : int, optional
        Type of volatility scenario generation. Default is 0.
    threading_mode : str, optional
        The threading mode for scenario analysis. Default is 'SINGLE_THREADING_MODE'.

    Returns
    -------
    ScnAnalysisSettings
        An object representing the scenario analysis settings.
    """
    price_scn_settings = dqCreateProtoScnSettings(min_underlying_price, max_underlying_price, num_price_scns, price_scn_gen_type)
    vol_scn_settings = dqCreateProtoScnSettings(min_vol, max_vol, num_vol_scns, vol_scn_gen_type)
    return dqCreateProtoScnAnalysisSettings(to_scn_analysis_type(scn_analysis_type), price_scn_settings, vol_scn_settings, to_threading_mode(threading_mode))

def create_asset_yield_curve(as_of_date, 
                             curve_dates, 
                             curve_values, 
                             interp_method="", 
                             extrap_method="", 
                             day_count="", 
                             compounding_type="", 
                             pillar_names=None, 
                             curve_name=""):
    """
    Create an asset yield curve.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the curve.
    curve_dates : list
        A list of dates for the yield curve.
    curve_values : list
        A list of yield values corresponding to each date.
    interp_method : str, optional
        The interpolation method to use for the curve.
    extrap_method : str, optional
        The extrapolation method to use for the curve.
    day_count : str, optional
        The day count convention.
    compounding_type : str, optional
        The compounding type.
    pillar_names : list, optional
        Names of the pillar dates.
    curve_name : str, optional
        The name of the curve.

    Returns
    -------
    AssetYieldCurve
        The constructed asset yield curve object.
    """

    pillar_dates = [create_date(d) for d in curve_dates]
    p_ts_curve = dqCreateProtoTermStructureCurve(create_date(as_of_date),
                                                 to_day_count_convention(day_count),
                                                 pillar_dates, 
                                                 pillar_names,
                                                 dqCreateProtoVector(curve_values),
                                                 to_interp_method(interp_method),
                                                 to_extrap_method(extrap_method),
                                                 curve_name)
    asset_yield_curve = dqCreateProtoAssetYieldCurve(p_ts_curve,
                                                    to_compounding_type(compounding_type))
    
    return asset_yield_curve

# IR Yield Curve:
def create_ir_yield_curve(as_of_date,
                          currency,
                          term_dates,
                          zero_rates,
                          day_count='ACT_365_FIXED',
                          interp_method='LINEAR_INTERP',
                          extrap_method='FLAT_EXTRAP',
                          compounding_type='CONTINUOUS_COMPOUNDING',
                          frequency='ANNUAL',
                          jacobian=[0.0],
                          curve_name='',
                          pillar_names=['']):
    '''
    创建利率收益率曲线.
    
    Parameters
    ----------
    as_of_date : datetime
        利率收益率曲线的参考日期
    currency : str
        利率收益率曲线的参考货币.
    term_dates : list of datetime
        一组递增的日期，并且每个日期必须在参考日期之后.
    zero_rates : list
        一组零息利率值，对应上面的一组日期.
    day_count : str, optional
        计息区间惯例，默认为ACT_365_FIXED.
    interp_method : str, optional
        曲线零息利率的插值方法，默认为线性插值.
    extrap_method : str, optional
        曲线零息利率的外插方法，默认为平推.
    compounding_type : str, optional
        计算折现率使用的复利类型，默认为连续复利.
    frequency : Frequency, optional
        当复利为离散型时，计算折现率使用的频率参数.
    jacobian : list, optional
        市场行情曲线对零息曲线的Jacobian矩阵，默认为单值为0的列表.
    curve_name : str, optional
        创建曲线时用户给定的曲线名称，默认为空.
    pillar_names : list, optional
        曲线每个关键期限点的名称，如['1M', '3M'].

    Returns
    -------
    IrYieldCurve
        利率收益率曲线对象.
    '''    
    pillar_dates = [create_date(d) for d in term_dates]
    p_ts_curve = dqCreateProtoTermStructureCurve(create_date(as_of_date),
                                                 to_day_count_convention(day_count),
                                                 pillar_dates, pillar_names, dqCreateProtoVector(zero_rates),
                                                 to_interp_method(interp_method),
                                                 to_extrap_method(extrap_method),
                                                 curve_name)
    p_asset_curve = dqCreateProtoAssetYieldCurve(p_ts_curve,
                                                 to_compounding_type(compounding_type))
    p_mat = dqCreateProtoMatrix(len(jacobian), 1,
                                jacobian,
                                Matrix.StorageOrder.ColMajor)
    p_jacobian = dqCreateProtoIrYieldCurve_Jacobian(curve_name, p_mat)
    
    zero_curve = dqCreateProtoIrYieldCurve(IrYieldCurveType.ZERO_RATE,
                                           p_asset_curve,
                                           currency,
                                           to_frequency(frequency),
                                           [p_jacobian])
    return zero_curve

# Flat IR Yield Curve
def create_flat_ir_yield_curve(as_of_date,
                               currency,
                               rate):
    '''
    创建一条水平利率收益率曲线.
    
    Parameters
    ----------
    as_of_date : datetime
        利率收益率曲线的参考日期.
    currency : str
        利率收益率曲线的参考货币.
    rate : float
        曲线收益率水平.

    Returns
    -------
    IrYieldCurve
        利率收益率曲线对象.
    '''
    start = as_of_date + timedelta(days=1)
    end = as_of_date + timedelta(days=365.25 * 100)
    term_dates = [start, end]
    rates = [rate] * 2
    return create_ir_yield_curve(as_of_date, currency, term_dates, rates)

# Credit Curve:
def create_credit_curve(as_of_date,
                        term_dates,
                        hazard_rates,
                        day_count='ACT_365_FIXED',
                        interp_method='LINEAR_INTERP',
                        extrap_method='FLAT_EXTRAP',
                        curve_name='',
                        pillar_names=['']):
    '''
    创建一条信用利差曲线.
    
    Parameters
    ----------
    as_of_date : Date
        信用利差曲线的参考日期.
    term_dates : list
        一组递增的日期，并且每个日期必须在参考日期之后.
    hazard_rates : list
        一组风险率，对应上面的一组日期.
    day_count : DayCountConvention, optional
        计息区间惯例，默认为ACT_365_FIXED.
    interp_method : InterpMethod, optional
        曲线插值方法，默认为线性插值.
    extrap_method : ExtrapMethod, optional
        曲线外插方法，默认为平推.
    curve_name : str, optional
        创建曲线时用户给定的曲线名称，默认为空.
    pillar_names : list, optional
        曲线每个关键期限点的名称，如['1M', '3M'].

    Returns
    -------
    CreditCurve
        信用利差曲线对象.

    '''
    pillar_dates = [create_date(d) for d in term_dates]
    p_ts_curve = dqCreateProtoTermStructureCurve(create_date(as_of_date),
                                                 to_day_count_convention(day_count),
                                                 pillar_dates, pillar_names, dqCreateProtoVector(hazard_rates),
                                                 to_interp_method(interp_method),
                                                 to_extrap_method(extrap_method),
                                                 curve_name)

    cs_curve = dqCreateProtoCreditCurve(p_ts_curve, dqCreateProtoVector(hazard_rates))
    return cs_curve

# Flat Credit Curve
def create_flat_credit_curve(as_of_date,
                             hazard_rate):
    '''
    创建一条水平风险率的信用曲线.
    
    Parameters
    ----------
    as_of_date : Date
        信用利差曲线的参考日期.
    hazard_rate : float
        曲线风险率水平.

    Returns
    -------
    CreditCurve.
        信用利差曲线对象.

    '''
    start = as_of_date + timedelta(days=1)
    end = as_of_date + timedelta(days=365.25 * 100)
    term_dates = [start, end]
    hazard_rates = [hazard_rate] * 2
    return create_credit_curve(as_of_date, term_dates, hazard_rates)

#CreateDividendCurve
def create_dividend_curve(
    as_of_date: datetime,
    pillar_dates,
    pillar_values,
    dividend_type,
    interp_method,
    extrap_method,
    day_count,
    yield_start_date: datetime,
    pillar_names=None,
    curve_name=""
):
    """
    Create a dividend curve using specified parameters.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the dividend curve.
    pillar_dates : list
        A list of dates for the dividend curve.
    pillar_values : list
        A list of dividend values corresponding to each date.
    dividend_type : str
        The type of dividend.
    interp_method : str
        The interpolation method to use for the curve.
    extrap_method : str
        The extrapolation method to use for the curve.
    day_count : str
        The day count convention.
    yield_start_date : datetime
        The start date for yield calculations.
    pillar_names : list, optional
        Names of the pillar dates.
    curve_name : str, optional
        The name of the curve.

    Returns
    -------
    DividendCurve
        The constructed dividend curve object.
    """
    asset_yield_curve = create_asset_yield_curve(
        as_of_date, pillar_dates, pillar_values,
        interp_method, extrap_method, day_count, "", pillar_names, curve_name)
    
    dividend_curve = dqCreateProtoDividendCurve(asset_yield_curve, 
                                                create_date(yield_start_date), 
                                                to_dividend_type(dividend_type))
    return dividend_curve

def create_flat_dividend_curve(
    as_of_date: datetime,
    dividend: float = 0.0,
    curve_name: str = ""
):
    """
    Create a flat dividend curve with constant dividend.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the flat dividend curve.
    dividend : float, optional
        The constant dividend value. Default is 0.0.
    curve_name : str, optional
        The name of the curve.

    Returns
    -------
    DividendCurve
        The constructed flat dividend curve object.
    """
    start = as_of_date + timedelta(days=1)
    end = as_of_date + timedelta(days=365.25 * 100)
    term_dates = [start, end]
    dividends = [dividend] * 2
    return create_dividend_curve(
        as_of_date, 
        term_dates, dividends, 
        "", "", "", "", as_of_date, None, curve_name)

def print_term_structure_curve(curve):
    '''
    将任意期限结构曲线以pandas.DataFrame的结构展示

    Parameters
    ----------
    curve : TermStructuredCurve
        一条期限结构曲线
    
    Returns
    -------
    pandas.DataFrame

    '''
    curve_dates = list()
    curve_values = list()
    for i in range(len(curve.pillar_date)):
        p_date = curve.pillar_date[i]
        curve_dates.append(dt.datetime(p_date.year, p_date.month, p_date.day).strftime('%Y-%m-%d'))
        curve_values.append(curve.pillar_values.data[i])
    df = pd.DataFrame(columns=['Date', 'Value'])
    df['Date'] = curve_dates
    df['Value'] = curve_values
    return df
   
def create_volatility_surface_definition(vol_smile_type,
                                         smile_method,
                                         smile_extrap_method,
                                         time_interp_method,
                                         time_extrap_method,
                                         day_count_convention,
                                         vol_type,
                                         wing_strike_type,
                                         lower,
                                         upper):
    """
    创建一个 volatility surface definition 对象.

    Parameters
    ----------
    vol_smile_type: str, VolSmileType
    smile_method: str, VolSmileMethod
    smile_extrap_method: str, ExtrapMethod
    time_interp_method: str, VolTermInterpMethod
    time_extrap_method: str, VolTermExtrapMethod
    day_count_convention: str, DayCountConvention
    vol_type: str, VolatilityType
    wing_strike_type: str, WingStrikeType
    lower: float
    upper: float

    Returns
    -------
    VolatilitySurfaceDefinition

    """
    return dqCreateProtoVolatilitySurfaceDefinition(to_vol_smile_type(vol_smile_type),
                                                    to_vol_smile_method(smile_method),
                                                    to_extrap_method(smile_extrap_method),
                                                    to_vol_term_time_interp_method(time_interp_method),
                                                    to_vol_termtime_extrap_method(time_extrap_method),
                                                    to_day_count_convention(day_count_convention),
                                                    to_volatility_type(vol_type),
                                                    to_wing_strike_type(wing_strike_type),
                                                    lower,
                                                    upper)

def create_volatility_smile(vol_smile_type,
                            reference_date,
                            strikes,
                            vols,
                            smile_method,
                            extrap_method,
                            term,
                            model_params,
                            auxilary_params,
                            lower,
                            upper):
    """
    创建一个波动率微笑对象.

    Parameters
    ----------
    vol_smile_type: str, VolSmileType
    reference_date: datetime
    lower: float
    upper: float
    curve: Curve
    smile_method: str, VolSmileMethod
    term: float

    Returns
    -------
    VolatilitySmile

    """    
    return dqCreateProtoVolatilitySmile(to_vol_smile_type(vol_smile_type),                                        
                                        create_date(reference_date),
                                        lower,
                                        upper,
                                        dqCreateProtoVector(strikes),
                                        dqCreateProtoVector(vols),                                        
                                        to_vol_smile_method(smile_method),
                                        term,
                                        dqCreateProtoVector(model_params),
                                        dqCreateProtoVector(auxilary_params),
                                        to_extrap_method(extrap_method))

def create_yield_curve(as_of_date,
                       term_dates,
                       zero_rates,
                       day_count=ACT_365_FIXED,
                       interp_method=LINEAR_INTERP,
                       extrap_method=FLAT_EXTRAP,
                       curve_name=''):
    '''
    创建一个收益率曲线.

    Parameters
    ----------
    as_of_date : Date
        Reference date for the IR yield curve.
    term_dates : list
        A list of dates in ascending order. The dates must be in the future relative to the reference date.
    zero_rates : list
        A list of zero rates correspoding to the dates.
    day_count : DayCountConvention, optional
        Day count convention. The default is 'ACT_365_FIXED'.
    interp_method : InterpMethod, optional
        Interpolation method for the curve zero rates. The default is 'LINEAR_INTERP'.
    extrap_method : ExtrapMethod, optional
        Extrapolation method for the curve zero rates. The default is 'FLAT_EXTRAP'.
    curve_name : str, optional
        Curve name given by the user. The default is ''.

    Returns
    -------
    Curve

    '''
    size = len(term_dates)

    terms = [0.0] * size
    for i in range(size):
        terms[i] = year_frac_calculator(as_of_date, term_dates[i], day_count, as_of_date, term_dates[i], term_dates[i])

    p_interpolator = dqCreateProtoInterpolator1D(interp_method,
                                                 extrap_method,
                                                 size,
                                                 dqCreateProtoVector(terms),
                                                 dqCreateProtoVector(zero_rates),
                                                 dqCreateProtoVector([]), dqCreateProtoVector([]))
    return dqCreateProtoCurve(p_interpolator, curve_name)

def create_volatility_surface(definition,
                              reference_date,
                              vol_smiles,
                              term_dates,
                              name=""):
    """
    创建一个波动率曲面.

    Parameters
    ----------
    definition: VolatilitySurfaceDefinition
    reference_date: Date
    vol_smiles: list
    term_dates: Date
    terms: Vector
    name: str

    Returns
    -------
    VolatilitySurface

    """
    vol_dates = [create_date(d) for d in term_dates]
    return dqCreateProtoVolatilitySurface(definition,
                                          create_date(reference_date),
                                          vol_smiles,
                                          vol_dates,
                                          name)

#CreateVolCurve
def create_vol_curve(
    as_of_date: datetime,
    terms: list,
    vols: list,
    interp_method: str = "",
    extrap_method: str = "",
    day_count: str = "",
    pillar_names=None,
    underlying: str = ""
):
    """
    Create a volatility curve.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the volatility curve.
    terms : list
        A list of term dates for the volatility curve.
    vols : list
        A list of volatility values corresponding to each term date.
    interp_method : str, optional
        Interpolation method to use for the curve.
    extrap_method : str, optional
        Extrapolation method to use for the curve.
    day_count : str, optional
        Day count convention.
    pillar_names : list, optional
        Names of the pillars.
    underlying : str, optional
        The underlying asset.

    Returns
    -------
    VolatilityCurve
        The constructed volatility curve object.
    """
    if len(terms) != len(vols):
        raise Exception("pillar dates and values must have the same size!")
    pillar_dates = [create_date(d) for d in terms]
    vol_curve = dqCreateProtoVolatilityCurve(create_date(as_of_date),
                                             to_day_count_convention(day_count),
                                             pillar_dates,
                                             pillar_names,
                                             dqCreateProtoVector(vols),
                                             to_interp_method(interp_method),
                                             to_extrap_method(extrap_method),
                                             underlying)
    return vol_curve


def create_flat_vol_curve(
    as_of_date: datetime,
    vol: float = 0.0,
    underlying: str = ""
):
    """
    Create a flat volatility curve with constant volatility.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the volatility curve.
    vol : float, optional
        The constant volatility value. Default is 0.0.
    underlying : str, optional
        The underlying asset.

    Returns
    -------
    VolatilityCurve
        The constructed flat volatility curve object.
    """
    start = as_of_date + timedelta(days=1)
    end = as_of_date + timedelta(days=365.25 * 100)
    terms = [start, end]
    vols = [vol] * 2
    return create_vol_curve(
        as_of_date, 
        terms, 
        vols, 
        "", "", "", None, underlying)


def create_option_quote_matrix(
    quote_value_type: str,
    quote_term_type: str,
    quote_strike_type: str,
    exercise_type: str,
    option_underlying_type: str,
    as_of_date: datetime,
    terms: list,
    term_dates: list,
    payoff_types: list,
    values: list,
    strikes: list,
    asset_name: str = ""
):
    """
    Create an option quote matrix.

    Parameters
    ----------
    quote_value_type : str
        The type of quote value.
    quote_term_type : str
        The type of quote term.
    quote_strike_type : str
        The type of quote strike.
    exercise_type : str
        The type of option exercise.
    option_underlying_type : str
        The type of option underlying.
    as_of_date : datetime
        The reference date for the option matrix.
    terms : list
        List of terms for the quotes.
    term_dates : list
        List of term dates corresponding to the quotes.
    payoff_types : list
        List of payoff types for the options.
    values : list
        List of quote values.
    strikes : list
        List of strike prices.
    asset_name : str, optional
        The name of the asset.

    Returns
    -------
    OptionQuoteMatrix
        The constructed option quote matrix object.
    """
    p_quote_smiles = list()
    for i in range(len(values)):
        p_quotes = list()
        for j in range(len(values[i])):
            p_quote = dqCreateProtoOptionQuote(to_payoff_type(payoff_types[i][j]), values[i][j], strikes[i][j])
            p_quotes.append(p_quote)
        if quote_term_type.upper() == "OQTT_RELATIVE_TERM":
            p_quote_smile = dqCreateProtoOptionQuoteVector(to_period(terms[i]), 
                                                        create_date(None),
                                                        p_quotes,
                                                        to_period('0d'), 
                                                        create_date(None))
        else:
            p_quote_smile = dqCreateProtoOptionQuoteVector(to_period('0d'), 
                                                        create_date(term_dates[i]),
                                                        p_quotes,
                                                        to_period('0d'), 
                                                        create_date(None))
        p_quote_smiles.append(p_quote_smile)
    
    return dqCreateProtoOptionQuoteMatrix(to_option_quote_value_type(quote_value_type), 
                                          to_option_quote_term_type(quote_term_type),
                                          to_option_quote_strike_type(quote_strike_type),
                                          to_exercise_type(exercise_type),
                                          to_option_underlying_type(option_underlying_type),
                                          create_date(as_of_date),
                                          p_quote_smiles,
                                          asset_name)

def create_proxy_option_quote_matrix(
        underlying: str,
        ref_vol_surface: VolatilitySurface,
        ref_underlying_price: float,
        underlying_price: float
        ):
    """
    Create a proxy option quote matrix.

    Parameters
    ----------
    underlying : str
        The underlying asset.
    ref_vol_surface : VolatilitySurface
        The reference volatility surface.
    ref_underlying_price : float
        The reference underlying price.
    underlying_price : float
        The current underlying price.

    Returns
    -------
    OptionQuoteMatrix
        The constructed proxy option quote matrix object.

    Raises
    ------
    Exception
        If the operation fails.
    """
    
    try:
        pb_input = dqCreateProtoCreateProxyOptionQuoteMatrixInput(underlying, ref_vol_surface, ref_underlying_price, underlying_price)
        req_name = "CREATE_PROXY_OPTION_QUOTE_MATRIX"
        res_msg = process_request(req_name, pb_input.SerializeToString())
        if res_msg is None:
            raise Exception('CREATE_PROXY_OPTION_QUOTE_MATRIX ProcessRequest: failed!')
        
        pb_output = CreateProxyOptionQuoteMatrixOutput()
        pb_output.ParseFromString(res_msg) 
        if pb_output.success == False:
            raise Exception(pb_output.err_msg)            
        return pb_output.option_quote_matrix        
    except Exception as e:
        return str(e)   

def create_flat_volatility_surface(as_of_date: datetime,
                                   vol: float,
                                   underlying: str = ""):
    """
    Create a flat volatility surface with constant volatility.

    Parameters
    ----------
    as_of_date : datetime
        The reference date for the volatility surface.
    vol : float
        The constant volatility value.
    underlying : str, optional
        The underlying asset.

    Returns
    -------
    VolatilitySurface
        The constructed flat volatility surface object.
    """
    start = as_of_date + timedelta(days=1)
    end = as_of_date + timedelta(days=365.25 * 100)
    term_dates = [start, end]

    strikes = [1.0e-4, 1.0e4]
    vols = [vol, vol]
    lower = 1.0e-4
    upper = 1.0e4

    vol_smiles = list()
    vol_smiles.append(create_volatility_smile('',
                            as_of_date,
                            strikes,
                            vols,
                            '',
                            '',
                            1./365,
                            [],
                            [],
                            lower,
                            upper))
    vol_smiles.append(create_volatility_smile('',
                            as_of_date,
                            strikes,
                            vols,
                            '',
                            '',
                            100.,
                            [],
                            [],
                            lower,
                            upper))
    
    return create_volatility_surface(create_volatility_surface_definition("", "", "", "", "", "", "", "", 0, 1),
                              as_of_date,
                              vol_smiles,
                              term_dates,
                              underlying)

def create_vol_surf_build_settings(ith_param_fixed: int, ith_param: float):
    """
    Create a volatility surface build settings object.

    Parameters
    ----------
    ith_param_fixed : int
        The index of the parameter that is fixed.
    ith_param : float
        The value of the ith parameter.

    Returns
    -------
    VolatilitySurfaceBuildSettings
        The settings object for building a volatility surface.
    """
    return dqCreateProtoVolatilitySurfaceBuildSettings(ith_param_fixed, ith_param)

def create_price_risk_settings(delta=False,
                               gamma=False,
                               curvature=False,
                               shift=1.0e-4,
                               curvature_shift=5.0e-3,
                               method='CENTRAL_DIFFERENCE_METHOD',
                               scaling_factor=1.0e-4,
                               threading_mode='SINGLE_THREADING_MODE'):
    """

    Parameters
    ----------
    delta : bool, optional
        Flag for indicating whether to calculate the curve delta (DV01). The default is False.
    gamma : bool, optional
        Flag for indicating whether to calculate the curve gamma. The default is False.
    curvature : bool, optional
        Flag for indicating whether to calculate the curve curvature，as defined in FRTB. The default is False.
    shift : float, optional
        The shift size for the curve delta and gamma calculation. The default is 1.0e-4.
    curvature_shift : float, optional
        The shift size for the curvature calculation. The default is 5.0e-3.
    method : FiniteDifferenceMethod, optional
        The finite difference method for the curve delta calculation. The default is 'CENTRAL_DIFFERENCE_METHOD'.
    scaling_factor : float, optional
        The scaling factor for calculating USD amount sensitivity. The default is 1.0e-4.
    threading_mode : ThreadingMode, optional
        The threading mode in the calculation of sensitivities. Two modes are single and multi threading. The default is 'SINGLE_THREADING_MODE'.

    Returns
    -------
    PriceRiskSettings

    """
    return dqCreateProtoPriceRiskSettings(delta,
                                          gamma,
                                          curvature,
                                          shift,
                                          curvature_shift,
                                          to_finite_difference_method(method),
                                          scaling_factor,
                                          to_threading_mode(threading_mode))

def create_vol_risk_settings(vega=False,
                             volga=False,
                             shift=1.0e-4,
                             method='CENTRAL_DIFFERENCE_METHOD',
                             granularity='TOTAL_RISK',
                             scaling_factor=1.0e-4,
                             threading_mode='SINGLE_THREADING_MODE'):
    """
    Create volatility risk settings.

    Parameters
    ----------
    vega : bool, optional
        Flag for indicating whether to calculate the vega risk. The default is False.
    volga : bool, optional
        Flag for indicating whether to calculate the volga risk. The default is False.
    shift : float, optional
        The shift size for the vega and volga calculation. The default is 1.0e-4.
    method : FiniteDifferenceMethod, optional
        The finite difference method for the vega calculation. The default is 'CENTRAL_DIFFERENCE_METHOD'.
    granularity : RiskGranularity, optional
        The granularity for the vega and volga calculations. The default is 'TOTAL_RISK'.
    scaling_factor : float, optional
        Factor to convert percentage sensitivity to absolute price change. The default is 1.0e-4.
    threading_mode : ThreadingMode, optional
        The threading mode for sensitivity calculations. The default is 'SINGLE_THREADING_MODE'.

    Returns
    -------
    VolRiskSettings
        An object representing the risk settings for volatility calculations.
    """

    return dqCreateProtoVolRiskSettings(vega,
                                        volga,
                                        shift,
                                        to_finite_difference_method(method),
                                        to_risk_granularity(granularity),
                                        scaling_factor,
                                        to_threading_mode(threading_mode))

def create_price_vol_risk_settings(vanna=False,
                                   price_shift=1.0e-4,
                                   vol_shift=1.0e-4,
                                   method='CENTRAL_DIFFERENCE_METHOD',
                                   granularity='TOTAL_RISK',
                                   price_scaling_factor=1.0e-4,
                                   vol_scaling_factor=1.0e-4,
                                   threading_mode='SINGLE_THREADING_MODE'):
    """
    Create risk settings for price and volatility sensitivity calculations.

    Parameters
    ----------
    vanna : bool, optional
        Flag for indicating whether to calculate vanna risk. The default is False.
    price_shift : float, optional
        The shift size for the price calculation. The default is 1.0e-4.
    vol_shift : float, optional
        The shift size for the volatility calculation. The default is 1.0e-4.
    method : FiniteDifferenceMethod, optional
        The finite difference method for the calculation. The default is 'CENTRAL_DIFFERENCE_METHOD'.
    granularity : RiskGranularity, optional
        The granularity for the calculations. The default is 'TOTAL_RISK'.
    price_scaling_factor : float, optional
        Factor to convert price percentage sensitivity to absolute change. The default is 1.0e-4.
    vol_scaling_factor : float, optional
        Factor to convert volatility percentage sensitivity to absolute change. The default is 1.0e-4.
    threading_mode : ThreadingMode, optional
        The threading mode for the calculations. The default is 'SINGLE_THREADING_MODE'.

    Returns
    -------
    PriceVolRiskSettings
        An object representing the risk settings for price and volatility sensitivity calculations.
    """

    return dqCreateProtoPriceVolRiskSettings(vanna,
                                             price_shift,
                                             vol_shift,
                                             to_finite_difference_method(method),
                                             to_risk_granularity(granularity),
                                             price_scaling_factor,
                                             vol_scaling_factor,
                                             to_threading_mode(threading_mode))

def create_ir_yield_curve_from_binary(data: list):
    """
    Create an IrYieldCurve object from a list of binary data.

    Parameters:
    -----------
    data : list
        A list containing the serialized data of an IrYieldCurve.

    Returns:
    --------
    IrYieldCurve
        An IrYieldCurve object parsed from the input data.
    """
    # Convert the list of data to bytes
    _bytes = num_to_bytes(data)
    
    # Create an empty IrYieldCurve object
    curve = IrYieldCurve()
    
    # Parse the bytes into the IrYieldCurve object
    curve.ParseFromString(_bytes)
    
    return curve

def create_credit_curve_from_binary(data: list):
    """
    Create a CreditCurve object from a list of binary data.

    Parameters:
    -----------
    data : list
        A list containing the serialized data of a CreditCurve.

    Returns:
    --------
    CreditCurve
        A CreditCurve object parsed from the input data.
    """
    # Convert the list of data to bytes
    _bytes = num_to_bytes(data)
    
    # Create an empty CreditCurve object
    curve = CreditCurve()
    
    # Parse the bytes into the CreditCurve object
    curve.ParseFromString(_bytes)
    
    return curve

#GetDiscountFactor
def get_discount_factor(ir_curve, dates: list):
    """
    Calculate the discount factors for given interest rate curve and dates.

    Parameters
    ----------
    ir_curve : object
        The interest rate curve.
    dates : list
        List of dates for which to calculate the discount factors.

    Returns
    -------
    list
        Discount factors corresponding to the input dates.
    """
    terms_dates = [create_date(d) for d in dates]
    pb_input = dqCreateProtoGetDiscountFactorInput(terms_dates, ir_curve)
    req_name = "DISCOUNT_FACTOR_CALCULATOR"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    if res_msg is None:
        raise Exception('DISCOUNT_FACTOR_CALCULATOR ProcessRequest: failed!')
    pb_output = GetDiscountFactorOutput()
    pb_output.ParseFromString(res_msg)
    return pb_output.discount_factors


def get_zero_rate(ir_curve, dates):
    """
    Calculate the zero rates for given interest rate curve and dates.

    Parameters
    ----------
    ir_curve : object
        The interest rate curve.
    dates : list
        List of dates for which to calculate the zero rates.

    Returns
    -------
    list
        Zero rates corresponding to the input dates.
    """
    terms_dates = [create_date(d) for d in dates]
    pb_input = dqCreateProtoGetZeroRateInput(terms_dates, ir_curve)
    req_name = "ZERO_RATE_CALCULATOR"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    if res_msg is None:
        raise Exception('ZERO_RATE_CALCULATOR ProcessRequest: failed!')
    pb_output = GetZeroRateOutput()
    pb_output.ParseFromString(res_msg)
    return pb_output.zero_rate


def get_fwd_rate(ir_curve, dates, tenor: float):
    """
    Calculate the forward rates for given interest rate curve, dates, and tenor.

    Parameters
    ----------
    ir_curve : object
        The interest rate curve.
    dates : list
        List of dates for which to calculate the forward rates.
    tenor : float
        The tenor for which to calculate the forward rates.

    Returns
    -------
    list
        Forward rates corresponding to the input dates and tenor.
    """
    terms_dates = [create_date(d) for d in dates]
    pb_input = dqCreateProtoGetFwdRateInput(terms_dates, ir_curve, tenor)
    req_name = "FWD_RATE_CALCULATOR"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    if res_msg is None:
        raise Exception('FWD_RATE_CALCULATOR ProcessRequest: failed!')
    pb_output = GetFwdRateOutput()
    pb_output.ParseFromString(res_msg)
    return pb_output.fwd_rates


def get_survival_probability(cr_curve, dates):
    """
    Calculate the survival probabilities for given credit risk curve and dates.

    Parameters
    ----------
    cr_curve : object
        The credit risk curve.
    dates : list
        List of dates for which to calculate the survival probabilities.

    Returns
    -------
    list
        Survival probabilities corresponding to the input dates.
    """
    terms_dates = [create_date(d) for d in dates]
    pb_input = dqCreateProtoGetSurvivalProbabilityInput(terms_dates, cr_curve)
    req_name = "SURVIVAL_PROBABILITY_CALCULATOR"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    if res_msg is None:
        raise Exception('SURVIVAL_PROBABILITY_CALCULATOR ProcessRequest: failed!')
    pb_output = GetSurvivalProbabilityOutput()
    pb_output.ParseFromString(res_msg)
    return pb_output.survival_probabilities


def get_credit_spread(cr_curve, dates):
    """
    Calculate the credit spreads for given credit risk curve and dates.

    Parameters
    ----------
    cr_curve : object
        The credit risk curve.
    dates : list
        List of dates for which to calculate the credit spreads.

    Returns
    -------
    list
        Credit spreads corresponding to the input dates.
    """
    terms_dates = [create_date(d) for d in dates]
    pb_input = dqCreateProtoGetCreditSpreadInput(terms_dates, cr_curve)
    req_name = "CREDIT_SPREAD_CALCULATOR"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    if res_msg is None:
        raise Exception('CREDIT_SPREAD_CALCULATOR ProcessRequest: failed!')
    pb_output = GetCreditSpreadOutput()
    pb_output.ParseFromString(res_msg)
    return pb_output.credit_spreads


def get_volatility(vol_surface, term_dates, strikes):
    """
    Calculate the volatilities for given volatility surface, term dates, and strikes.

    Parameters
    ----------
    vol_surface : object
        The volatility surface.
    term_dates : list
        List of term dates for which to calculate the volatilities.
    strikes : list
        List of strikes for which to calculate the volatilities.

    Returns
    -------
    list
        Volatilities corresponding to the input term dates and strikes.
    """
    terms = [create_date(d) for d in term_dates]
    pb_input = dqCreateProtoGetVolatilityInput(vol_surface, terms, dqCreateProtoVector(strikes))
    req_name = "GET_VOLATILITY"
    res_msg = process_request(req_name, pb_input.SerializeToString())
    if res_msg is None:
        raise Exception('GET_VOLATILITY ProcessRequest: failed!')
    pb_output = GetVolatilityOutput()
    pb_output.ParseFromString(res_msg)
    return pb_output.volatility
