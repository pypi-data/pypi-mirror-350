import datetime

from caplibproto import SettlementType, CreditProtectionType, CreditPremiumType, DayCountConvention, Frequency, \
    BusinessDayConvention, IrYieldCurveBuildingMethod, PayReceiveFlag

from .fi_entity import PricerCurveSetting


class CrInfo:
    def __init__(self, inst_code: str, start_delay: int, settlement_type: SettlementType, ref_price: float,
                 leverage: float, credit_protection_type: CreditProtectionType, recovery_rate: float,
                 credit_premium_type: CreditPremiumType, day_count_convention: DayCountConvention,
                 frequency: Frequency, calendars: [str], interest_day_convention: BusinessDayConvention,
                 rebate_accrual: bool):
        '''

        Parameters
        ----------
        inst_code 产品编码
        start_delay 起息日调整天数
        settlement_type 交割类型
        ref_price 参考价格
        leverage 杠杆
        credit_protection_type 信用保护类型
        recovery_rate 回收率
        credit_premium_type 信用金类型
        day_count_convention 计息基准惯例
        frequency 计息频率
        calendars 日历
        interest_day_convention 计息日调整惯例
        rebate_accrual 是否返利累计
        '''
        self.instCode = inst_code
        self.startDelay = start_delay
        self.settlementType = settlement_type
        self.refPrice = ref_price
        self.leverage = leverage
        self.creditProtectionType = credit_protection_type
        self.recoveryRate = recovery_rate
        self.creditPremiumType = credit_premium_type
        self.dayCountConvention = day_count_convention
        self.frequency = frequency
        self.calendar = ','.join(calendars) if len(calendars) > 0 else ''
        self.interestDayConvention = interest_day_convention
        self.rebateAccrual = rebate_accrual


class CrQuoteInfo:
    def __init__(self, cr_info: CrInfo, quote: float, term: str):
        '''

        Parameters
        ----------
        cr_info 信用信息
        quote 报价
        term 期限
        '''
        self.crInfo = cr_info
        self.quote = quote
        self.term = term


class CrCurveBuildInfo:
    def __init__(self, curve_code: str, as_of_date: datetime, currency: str, cr_quotes: [CrQuoteInfo],
                 discount_curve: [int], ir_yield_curve_building_method: IrYieldCurveBuildingMethod,
                 parse_proto: bool = False):
        '''

        Parameters
        ----------
        curve_code 曲线编码
        as_of_date 日期
        currency 货币
        cr_quotes 报价列表
        discount_curve 收益率折现曲线
        ir_yield_curve_building_method 构建方法
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.curveCode = curve_code
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.currency = currency
        self.crQuotes = cr_quotes
        self.discountCurve = discount_curve
        self.irYieldCurveBuildingMethod = ir_yield_curve_building_method
        self.parseProto = parse_proto


class CrPricingInfo:
    def __init__(self, cr_info: CrInfo, nominal: float, issue_date: datetime, maturity: datetime, as_of_date: datetime,
                 leg_pay_receive: PayReceiveFlag, coupon_rate: float, upfront_rate: float, currency: str,
                 discount_curve: [int], credit_curve: [int], dv01: PricerCurveSetting, cs01: PricerCurveSetting,
                 theta: bool, parse_proto: bool = False):
        '''
        Parameters
        ----------
        cr_info 信用信息
        nominal 数量
        issue_date 发行日期
        maturity 到期日期
        as_of_date 定价时间
        leg_pay_receive 腿支付类型
        coupon_rate 票面利率
        upfront_rate 预付利率
        currency 货币
        discount_curve 利率折现曲线
        credit_curve 信用曲线
        dv01
        cs01
        theta
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.crInfo = cr_info
        self.nominal = nominal
        self.issueDate = issue_date.strftime("%Y-%m-%d") if issue_date is not None else ''
        self.maturity = maturity.strftime("%Y-%m-%d") if maturity is not None else ''
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.legPayReceive = leg_pay_receive
        self.couponRate = coupon_rate
        self.upfrontRate = upfront_rate
        self.currency = currency
        self.discountCurve = discount_curve
        self.creditCurve = credit_curve
        self.dv01 = dv01
        self.cs01 = cs01
        self.theta = theta
        self.parseProto = parse_proto
