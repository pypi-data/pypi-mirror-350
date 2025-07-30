'''
实体对象,对应http接口
'''
import datetime
from enum import Enum

from caplibproto import DayCountConvention, ACT_ACT_ISDA, BusinessDayConvention, FOLLOWING, StubPolicy, INITIAL, \
    BrokenPeriodType, LONG, Frequency, DateGenerationMode, VanillaBondType, CONST_NOTIONAL, BondQuoteType, \
    YIELD_TO_MATURITY, IrYieldCurveBuildingMethod, BOOTSTRAPPING_METHOD, IrYieldCurveType, ZERO_RATE, InterpMethod, \
    LINEAR_INTERP, FLAT_EXTRAP, ExtrapMethod, ACT_365_FIXED, CONTINUOUS_COMPOUNDING, CompoundingType, ANNUAL, \
    DISCRETE_COMPOUNDING


class BondTemplateInfo:
    def __init__(self, frequency: str,
                 currency: str = 'CNY',
                 settlement_days: int = 1,
                 day_count_convention: DayCountConvention = ACT_ACT_ISDA,
                 calendar: str = 'CFETS',
                 interest_day_convention: BusinessDayConvention = FOLLOWING,
                 pay_day_offset: int = 0,
                 pay_day_convention: BusinessDayConvention = FOLLOWING,
                 stub_policy: StubPolicy = INITIAL,
                 broken_period_type: BrokenPeriodType = LONG,
                 ref_index: str = '',
                 fixing_calendars: [str] = [],
                 fixing_frequency: Frequency = None,
                 fixing_day_convention: BusinessDayConvention = None,
                 fixing_mode: DateGenerationMode = None,
                 fixing_day_offset: int = 0,
                 excoupon_period: str = '0D', excoupon_calendar: str = '',
                 excoupon_day_convention: BusinessDayConvention = None,
                 excoupon_eom: bool = False):
        '''
        债券模板实体
        Parameters
        ----------
        currency 货币
        settlement_days 交割日调整天数
        frequency 付息频率
        day_count_convention 计息基准惯例
        calendar 日历
        interest_day_convention 计息日调整惯例
        pay_day_offset 支付日调整天数
        pay_day_convention 支付日调整惯例
        stub_policy 残段位置
        broken_period_type 残段类型
        ref_index 基准利率
        fixing_calendars 利率重装日历
        fixingFrequency 利率重置频率
        fixing_day_convention 利率重置日调整惯例
        fixing_mode 利率重置模式
        fixing_day_offset 利率重置天数
        excoupon_period 除息期
        excouponCalendar 除息期日历
        excoupon_day_convention 除息日调整惯例
        excouponEom 除息日是否末月
        '''
        self.currency = currency
        self.settlementDays = settlement_days
        self.frequency = frequency
        self.dayCountConvention = day_count_convention
        self.calendar = calendar
        self.interestDayConvention = interest_day_convention
        self.payDayOffset = pay_day_offset
        self.payDayConvention = pay_day_convention
        self.stubPolicy = stub_policy
        self.brokenPeriodType = broken_period_type
        self.refIndex = ref_index
        self.fixingCalendars = ','.join(fixing_calendars) if len(fixing_calendars) > 0 else ''
        self.fixingFrequency = fixing_frequency
        self.fixingDayConvention = fixing_day_convention
        self.fixingMode = fixing_mode
        self.fixingDayOffset = fixing_day_offset
        self.excouponPeriod = excoupon_period
        self.excouponCalendar = excoupon_calendar
        self.excouponDayConvention = excoupon_day_convention
        self.excouponEom = excoupon_eom


class BondInfo:
    def __init__(self, inst_code: str, inst_type: VanillaBondType, issue_date: datetime, start_date: datetime,
                 maturity: str,
                 maturity_date: datetime, issue_price: float, coupon_rate: float, nominal: float,
                 template: BondTemplateInfo, recovery_rate: float = 0.0, is_std_bond: bool = False):
        '''
        债券信息实体
        Parameters
        ----------
        inst_code 债券编码
        inst_type 产品类型
        issue_date 发行日
        start_date 起息日
        maturity 发行期限
        maturity_date 到期日
        issue_price 发行价格
        coupon_rate 票面利率
        nominal 本金
        template 债券模板
        recovery_rate 恢复率
        isStdBond 是否标准债
        '''
        self.instCode = inst_code
        self.instType = inst_type
        self.issueDate = issue_date.strftime("%Y-%m-%d") if issue_date is not None else ''
        self.startDate = start_date.strftime("%Y-%m-%d") if start_date is not None else ''
        self.maturity = maturity
        self.maturityDate = maturity_date.strftime("%Y-%m-%d") if maturity_date is not None else ''
        self.issuePrice = issue_price
        self.couponRate = coupon_rate
        self.nominal = nominal
        self.template = template
        self.recoveryRate = recovery_rate
        self.isStdBond = is_std_bond
        self.notionalType = CONST_NOTIONAL


class BondCnpCalculatorInfo:
    def __init__(self, bond_info: BondInfo, as_of_date: datetime, discount_curve: [int], credit_curve: [int],
                 nominal: float = 100.0):
        '''
        标准债票面利率计算信息
        Parameters
        ----------
        bond_info 债券信息
        as_of_date 时间
        discount_curve 折现曲线
        credit_curve 信用利差曲线
        nominal 本金
        '''
        self.bondInfo = bond_info
        self.date = as_of_date.strftime("%Y-%m-%d") if as_of_date is not None else ''
        self.discountCurve = discount_curve
        self.creditCurve = credit_curve
        self.nominal = nominal


class BondQuoteInfo:
    def __init__(self, bond_info: BondInfo, quote: float):
        '''
        债券报价信息
        Parameters
        ----------
        bond_info 债券信息
        quote 债券报价/或到期收益率
        '''
        self.bondInfo = bond_info
        self.quote = quote


class PricerCurveSetting(Enum):
    NO = 1
    PAR = 2
    ZERO = 3
    BUCKET_PAR = 4
    BUCKET_ZERO = 5


class BondPricingInfo:
    def __init__(self, bond_info: BondInfo, as_of_date: datetime, discount_curve: [int], credit_curve: [int],
                 forward_curve: [int], dv01: PricerCurveSetting, cs01: PricerCurveSetting, theta: bool,
                 nominal: float = 100.0,parse_proto:bool=False):
        '''
        债券估值/定价信息
        Parameters
        ----------
        bond_info 债券信息
        as_of_date 时间
        discount_curve 折现曲线
        credit_curve 信用利差曲线
        forward_curve 远期曲线
        dv01
        cs01
        theta
        nominal 本金
        parse_proto 是否解析二进制 false时返回结果只有二进制
        '''
        self.bondInfo = bond_info
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.discountCurve = discount_curve
        self.creditCurve = credit_curve
        self.forwardCurve = forward_curve
        self.dv01 = dv01
        self.cs01 = cs01
        self.theta = theta
        self.nominal = nominal
        self.parseProto = parse_proto


class BondSprdCurveBuildInfo:
    def __init__(self, curve_code: str, as_of_date: datetime, bond_quotes: [BondQuoteInfo], currency: str,
                 base_curve: [int], forward_curve: [int],
                 quote_type: BondQuoteType = YIELD_TO_MATURITY,
                 ir_yield_curve_building_method: IrYieldCurveBuildingMethod = BOOTSTRAPPING_METHOD,
                 calc_jacobian: bool = False,
                 parse_proto: bool = False
                 ):
        '''
        构建债券信用利差曲线信息
        Parameters
        ----------
        curve_code 曲线编码
        as_of_date 日期
        bond_quotes 债券报价列表
        currency 货币
        base_curve 基准利率曲线
        forward_curve 远期利率曲线
        quote_type 报价类型
        ir_yield_curve_building_method 构建方法
        calc_jacobian  是否计算雅可比
        parse_proto 是否解析二进制 false时返回结果只有二进制
        '''
        self.code = curve_code
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.bondQuotes = bond_quotes
        self.currency = currency
        self.baseCurve = base_curve
        self.forwardCurve = forward_curve
        self.quoteType = quote_type
        self.irYieldCurveBuildingMethod = ir_yield_curve_building_method
        self.calcJacobian = calc_jacobian
        self.parseProto = parse_proto


class BondYieldCurveBuildInfo:
    def __init__(self, curve_code: str, as_of_date: datetime, bond_quotes: [BondQuoteInfo], currency: str,
                 ir_yield_curve_type: IrYieldCurveType = ZERO_RATE,
                 quote_type: BondQuoteType = YIELD_TO_MATURITY,
                 interp_method: InterpMethod = LINEAR_INTERP,
                 extrap_method: ExtrapMethod = FLAT_EXTRAP,
                 day_count_convention: DayCountConvention = ACT_365_FIXED,
                 compounding_type: CompoundingType = CONTINUOUS_COMPOUNDING,
                 frequency: Frequency = ANNUAL,
                 ir_yield_curve_building_method: IrYieldCurveBuildingMethod = BOOTSTRAPPING_METHOD,
                 calc_jacobian: bool = False,
                 parse_proto: bool = False):
        '''
        收益率曲线构建方法
        Parameters
        ----------
        curve_code  曲线编码
        as_of_date 日期
        bond_quotes 债券报价列表
        currency 货币
        ir_yield_curve_type 插值对象
        quote_type 报价类型
        interp_method 内插方法
        extrap_method 外插方法
        day_count_convention 计息惯例
        compounding_type 复利类型
        frequency 复利频率
        ir_yield_curve_building_method 构建方法
        calc_jacobian 是否计算雅可比
        parse_proto 是否解析二进制 false时返回结果只有二进制
        '''
        self.curveCode = curve_code
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.currency = currency
        self.irYieldCurveType = ir_yield_curve_type
        self.quoteType = quote_type
        self.interpMethod = interp_method
        self.extrapMethod = extrap_method
        self.dayCountConvention = day_count_convention
        self.compoundingType = compounding_type
        self.frequency = frequency
        self.irYieldCurveBuildingMethod = ir_yield_curve_building_method
        self.calcJacobian = calc_jacobian
        self.bondQuotes = bond_quotes
        self.parseProto = parse_proto


class BondYtmCalculationInfo:
    def __init__(self, bond_info: BondInfo, as_of_date: datetime, prices: [float],
                 quote_type: BondQuoteType, compounding_type: CompoundingType = DISCRETE_COMPOUNDING,
                 forward_curve: [int] = [], nominal: float = 100.0):
        '''
        计算债券到期收益率信息
        Parameters
        ----------
        bond_info  债券信息
        as_of_date 时间
        prices 价格列表
        quote_type 报价类型
        compounding_type 复利类型
        forward_curve 远期曲线
        nominal 本金
        '''
        self.bondInfo = bond_info
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.compoundingType = compounding_type
        self.forwardCurve = forward_curve
        self.nominal = nominal
        self.prices = prices
        self.priceType = quote_type
