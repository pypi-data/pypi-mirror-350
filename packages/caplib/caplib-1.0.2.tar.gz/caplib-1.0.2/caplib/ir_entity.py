import datetime
from enum import Enum

from caplibproto import IrYieldCurveType, InterpMethod, ZERO_RATE, LINEAR_INTERP, ExtrapMethod, FLAT_EXTRAP, \
    DayCountConvention, ACT_365_FIXED, CompoundingType, CONTINUOUS_COMPOUNDING, Frequency, ANNUAL, \
    IrYieldCurveBuildingMethod, BOOTSTRAPPING_METHOD, InstrumentType, InterestRateIndexType, BusinessDayConvention, \
    IborIndexType, InterestRateLegType, InterestRateCalculationMethod, NotionalExchange, StubPolicy, BrokenPeriodType, \
    DateGenerationMode
from .fx_entity import FxInfo
from .fi_entity import PricerCurveSetting


class InterestRateLegInfo:
    def __init__(self, leg_type: InterestRateLegType, start_delay: int, day_count_convention: DayCountConvention,
                 ref_rate: str, rate_calc_method: InterestRateCalculationMethod, notional_exchange: NotionalExchange,
                 spread: bool, fx_convert: bool, fx_reset: bool, calendars: [str], frequency: Frequency,
                 interest_day_convention: BusinessDayConvention, stub_policy: StubPolicy,
                 broken_period_type: BrokenPeriodType, pay_day_convention: BusinessDayConvention, pay_day_offset: int,
                 fixing_calendars: [str], fixing_frequency: Frequency, fixing_day_convention: BusinessDayConvention,
                 fixing_mode: DateGenerationMode, fixing_day_offset: int, currency: str):
        '''

        Parameters
        ----------
        leg_type 腿类型
        start_delay 起息日调整天数
        day_count_convention 计息基准惯例
        ref_rate 基准利率
        rate_calc_method 利率计算方法
        notional_exchange 本金交换
        spread 是否息差腿
        fx_convert 是否汇率转换
        fx_reset 是否汇率重置
        calendars 日历
        frequency  计息频率
        interest_day_convention 计息日调整惯例
        stub_policy 残段位置
        broken_period_type 残段类型
        pay_day_convention 支付日调整惯例
        pay_day_offset 支付日调整天数
        fixing_calendars 利率重置日历
        fixing_frequency 利率重置频率
        fixing_day_convention 利率重置日调整惯例
        fixing_mode 利率重置模式
        fixing_day_offset 利率重置日调整天数
        currency 货币
        '''
        self.legType = leg_type
        self.startDelay = start_delay
        self.dayCountConvention = day_count_convention
        self.refRate = ref_rate
        self.rateCalcMethod = rate_calc_method
        self.notionalExchange = notional_exchange
        self.spread = spread
        self.fxConvert = fx_convert
        self.fxReset = fx_reset
        self.calendar = ','.join(calendars) if len(calendars) > 0 else None
        self.frequency = frequency
        self.interestDayConvention = interest_day_convention
        self.stubPolicy = stub_policy
        self.brokenPeriodType = broken_period_type
        self.payDayConvention = pay_day_convention
        self.payDayOffset = pay_day_offset
        self.fixingCalendars = ','.join(fixing_calendars) if len(fixing_calendars) > 0 else None
        self.fixingFrequency = fixing_frequency
        self.fixingDayConvention = fixing_day_convention
        self.fixingMode = fixing_mode
        self.fixingDayOffset = fixing_day_offset
        self.currency = currency


class IrInfo:
    def __init__(self, inst_code: str, type: InstrumentType, term: str, legs: [InterestRateLegInfo]):
        '''

        Parameters
        ----------
        inst_code 利率编码
        type 类型
        term 期限
        legs 腿信息
        '''
        self.code = inst_code
        self.type = type
        self.term = term
        self.legs = legs


class IrQuoteInfo:
    def __init__(self, inst_code: str, type: InstrumentType, term: str, factor: float, quote: float):
        '''

        Parameters
        ----------
        inst_code 产品编码
        type 产品类型
        term 产品期限
        factor 报价因子
        quote 报价
        '''
        self.instCode = inst_code
        self.type = type
        self.term = term
        self.factor = factor
        self.quote = quote


class IborInfo:
    def __init__(self, inst_code: str, ir_index_type: InterestRateIndexType, term: str, currency: str, start_delay: int,
                 calendars: [str], day_count_convention: DayCountConvention,
                 interest_day_convention: BusinessDayConvention,
                 ibor_index_type: IborIndexType):
        '''

        Parameters
        ----------
        inst_code 基准利率编码
        ir_index_type 利率类型
        term 期限
        currency 货币
        start_delay 起息日调整天数
        calendars 日历
        day_count_convention 计息基准惯例
        interest_day_convention 计息日调整惯例
        ibor_index_type 基准利率类型
        '''
        self.code = inst_code
        self.irIndexType = ir_index_type
        self.tenor = term
        self.currency = currency
        self.startDelay = start_delay
        self.calendar = ','.join(calendars) if len(calendars) > 0 else None
        self.dayCountConvention = day_count_convention
        self.interestDayConvention = interest_day_convention
        self.iborIndexType = ibor_index_type


class CurveUsage(Enum):
    DISCOUNT_CURVE = 1
    FORWARD_CURVE = 2
    FX_SPOT_RATE = 3


class IrCurveRefInfo:
    def __init__(self, assignee: str, curve_code: str, curve: [int], quote: float, fx_spot: FxInfo,
                 curve_usage: CurveUsage):
        '''

        Parameters
        ----------
        assignee 分配标的
        curve_code 曲线编码
        curve 对应曲线编码的曲线,曲线用途为DISCOUNT_CURVE FORWARD_CURVE 时必填
        quote 报价，曲线用途为FX_SPOT_RATE是必填
        fx_spot 外汇即期信息，曲线用途为FX_SPOT_RATE是必填
        curve_usage 曲线用途
        '''
        self.assignee = assignee
        self.curveCode = curve_code
        self.curve = curve
        self.quote = quote
        self.fxSpot = fx_spot
        self.curveUsage = curve_usage


class IrYieldCurveBuildInfo:
    def __init__(self, curve_code: str, as_of_date: datetime, ir_quotes: [IrQuoteInfo], ref_curves: [IrCurveRefInfo],
                 ibor_list: [IborInfo], fx_list: [FxInfo], ir_list: [IrInfo], currency: str = 'CNY',
                 ir_yield_curve_type: IrYieldCurveType = ZERO_RATE,
                 interp_method: InterpMethod = LINEAR_INTERP, extrap_method: ExtrapMethod = FLAT_EXTRAP,
                 day_count_convention: DayCountConvention = ACT_365_FIXED,
                 compounding_type: CompoundingType = CONTINUOUS_COMPOUNDING, frequency: Frequency = ANNUAL,
                 ir_yield_curve_building_method: IrYieldCurveBuildingMethod = BOOTSTRAPPING_METHOD,
                 calc_jacobian: bool = False, parse_proto: bool = False):
        '''

        Parameters
        ----------
        curve_code  曲线编码
        as_of_date  日期
        ir_quotes 利率报价列表
        ref_curves  曲线依赖
        ibor_list  基准利率列表
        fx_list  外汇列表
        ir_list  利率列表
        currency  货币
        ir_yield_curve_type  曲线类型
        interp_method  内插方法
        extrap_method  外插方法
        day_count_convention  计息惯例
        compounding_type  复利类型
        frequency  复利频率
        ir_yield_curve_building_method  构建方法
        calc_jacobian  是否计算雅可比
        parse_proto  是否解析二进制，false时返回结果只有二进制
        '''
        self.curveCode = curve_code
        self.date = as_of_date.strftime("%Y-%m-%d") if as_of_date is not None else ''
        self.currency = currency
        self.irYieldCurveType = ir_yield_curve_type
        self.interpMethod = interp_method
        self.extrapMethod = extrap_method
        self.dayCountConvention = day_count_convention
        self.compoundingType = compounding_type
        self.frequency = frequency
        self.irYieldCurveBuildingMethod = ir_yield_curve_building_method
        self.calcJacobian = calc_jacobian
        self.irQuotes = ir_quotes
        self.refList = ref_curves
        self.parseProto = parse_proto
        self.iborList = ibor_list
        self.fxList = fx_list
        self.irList = ir_list


class IrTradeInfo:
    def __init__(self, ir_info: IrInfo, start: datetime, maturity: datetime, nominal: float, rate: float,
                 spread: float = 0):
        '''

        Parameters
        ----------
        ir_info 利率信息
        start 起息日
        maturity 到期日
        nominal 本金
        rate 利率
        spread 基差
        '''
        self.irInfo = ir_info
        self.start = start.strftime("%Y-%m-%d") if start is not None else ''
        self.maturity = maturity.strftime("%Y-%m-%d") if maturity is not None else ''
        self.nominal = nominal
        self.rate = rate
        self.spread = spread


class IrPricingInfo:
    def __init__(self, ir_trade: IrTradeInfo, pricing_date: datetime, discount_curve: [int], forward_curve: [[int]],
                 dv01: PricerCurveSetting, theta: bool, parse_proto: bool = False):
        '''

        Parameters
        ----------
        ir_trade 利率交易信息
        pricing_date 定价时间
        discount_curve 折现曲线
        forward_curve 远期曲线
        dv01
        theta
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.irTrade = ir_trade
        self.pricingDate = pricing_date.strftime("%Y-%m-%d %H:%M:%S") if pricing_date is not None else ''
        self.discountCurve = discount_curve
        self.forwardCurve = forward_curve
        self.dv01 = dv01
        self.theta = theta
        self.parseProto = parse_proto
