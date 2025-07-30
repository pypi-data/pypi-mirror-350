import datetime

from caplibproto import VolSmileType, VolSmileMethod, ExtrapMethod, VolTermInterpMethod, VolTermExtrapMethod, \
    DayCountConvention, VolatilityType, WingStrikeType, PayoffType

from .fi_entity import PricerCurveSetting


class EqDividendCurveBuildInfo:
    def __init__(self, curve_code: str, as_of_date: datetime, underlying: str, underlying_spot_rate: float,
                 discount_curve: [int], expirys: [datetime], strikes: [float], call_prices: [float],
                 put_prices: [float], parse_proto: bool = False):
        '''

        Parameters
        ----------
        curve_code 曲线编码不能空
        as_of_date 日期
        underlying 标的
        underlying_spot_rate 标的即期值
        discount_curve 利率折现曲线
        expirys 到期日,应于行权价、call报价、put报价数量一致
        strikes 行权价
        call_prices call报价
        put_prices put报价
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.curveCode = curve_code
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.underlying = underlying
        self.underlyingSpotRate = underlying_spot_rate
        self.discountCurve = discount_curve
        self.expirys = [d.strftime('%Y-%m-%d') for d in expirys]
        self.strikes = strikes
        self.callPrices = call_prices
        self.putPrices = put_prices
        self.parseProto = parse_proto


class EqOptionQuoteInfo:
    def __init__(self, strike: float, quote: float, pay_off: PayoffType):
        '''

        Parameters
        ----------
        strike 行权价
        quote 报价
        pay_off 收益
        '''
        self.strike = strike
        self.quote = quote
        self.payOff = pay_off


class EqOptionExpiryQuoteInfo:
    def __init__(self, expiry: datetime, option_quotes: [EqOptionQuoteInfo]):
        '''

        Parameters
        ----------
        expiry 到期日
        option_quotes 期权报价
        '''
        self.expiry = expiry.strftime("%Y-%m-%d") if expiry is not None else ''
        self.optionQuotes = option_quotes


class EqDividendVolSurfaceBuildInfo:
    def __init__(self, surface_code: str, as_of_date: datetime, underlying: str, underlying_spot_rate: float,
                 vol_smile_type: VolSmileType, smile_method: VolSmileMethod, smile_extrap_method: ExtrapMethod,
                 time_interp_method: VolTermInterpMethod, time_extrap_method: VolTermExtrapMethod,
                 day_count_convention: DayCountConvention, volatility_type: VolatilityType,
                 wing_strike_type: WingStrikeType, lower_bound: float, upper_bound: float, discount_curve: [int],
                 underlying_dividend_curve: [int], quotes: [EqOptionExpiryQuoteInfo]):
        '''

        Parameters
        ----------
        surface_code 曲面编码
        as_of_date 日期
        underlying 标的
        underlying_spot_rate 标的即期值
        vol_smile_type 波动率曲面类型
        smile_method 微笑模型
        smile_extrap_method 微笑外插方法
        time_interp_method 期限方向内插方法
        time_extrap_method 期限方向外插方法
        day_count_convention 到期时间惯例
        volatility_type 波动率类型
        wing_strike_type wing行权价类型
        lower_bound 上边界行权价
        upper_bound 下边界行权价
        discount_curve 利率折现曲线
        underlying_dividend_curve 标的收益率曲线
        quotes 报价列表
        '''
        self.surfaceCode = surface_code
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.underlying = underlying
        self.underlyingSpotRate = underlying_spot_rate
        self.volSmileType = vol_smile_type
        self.smileMethod = smile_method
        self.smileExtrapMethod = smile_extrap_method
        self.timeInterpMethod = time_interp_method
        self.timeExtrapMethod = time_extrap_method
        self.dayCountConvention = day_count_convention
        self.volatilityType = volatility_type
        self.wingStrikeType = wing_strike_type
        self.lowerBound = lower_bound
        self.upperBound = upper_bound
        self.discountCurveBytes = discount_curve
        self.underlyingDividendCurveBytes = underlying_dividend_curve
        self.quotes = quotes


class EqEuOptionPricingInfo:
    def __init__(self, underlying: str, underlying_price: float, currency: str, as_of_date: datetime, nominal: float,
                 strike: float, delivery: datetime, expiry: datetime, discount_curve: [int], dividend_curve: [int],
                 fx_vol_surface: [int], quanto_discount_curve: [int], quanto_fx_vol_curve: [int],
                 quanto_correlation: float, dv01: PricerCurveSetting, theta: bool, delta: bool, gamma: bool,
                 vega: bool, volga: bool, vanna: bool, parse_proto: bool = False):
        '''

        Parameters
        ----------
        underlying 标的
        underlying_price 标的价格
        currency 货币
        as_of_date 定价时间
        nominal 数量
        strike 行权价
        delivery 交割日期
        expiry 行权日期
        discount_curve 利率折现曲线
        dividend_curve 权益折现曲线
        fx_vol_surface 外汇波动率曲面
        quanto_discount_curve
        quanto_fx_vol_curve
        quanto_correlation
        dv01
        theta
        delta
        gamma
        vega
        volga
        vanna
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.underlying = underlying
        self.underlyingPrice = underlying_price
        self.currency = currency
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.nominal = nominal
        self.strike = strike
        self.deliveryDate = delivery.strftime("%Y-%m-%d") if delivery is not None else ''
        self.expiry = expiry.strftime("%Y-%m-%d") if expiry is not None else ''
        self.discountCurve = discount_curve
        self.dividendCurve = dividend_curve
        self.fxVolSurface = fx_vol_surface
        self.quantoDiscountCurve = quanto_discount_curve
        self.quantoFxVolCurve = quanto_fx_vol_curve
        self.quantoCorrelation = quanto_correlation
        self.dv01 = dv01
        self.theta = theta
        self.fxDelta = delta
        self.fxGamma = gamma
        self.fxVega = vega
        self.fxVolga = volga
        self.fxVanna = vanna
        self.parseProto = parse_proto


class EqAmericanOptionPricingInfo:
    def __init__(self, underlying: str, underlying_price: float, currency: str, as_of_date: datetime, nominal: float,
                 strike: float, settlement_days: int, expiry: datetime, discount_curve: [int], dividend_curve: [int],
                 fx_vol_surface: [int], quanto_discount_curve: [int], quanto_fx_vol_curve: [int],
                 quanto_correlation: float, dv01: PricerCurveSetting, theta: bool, delta: bool, gamma: bool,
                 vega: bool, volga: bool, vanna: bool, parse_proto: bool = False):
        '''

        Parameters
        ----------
        underlying 标的
        underlying_price 标的价格
        currency 货币
        as_of_date 定价时间
        nominal 数量
        strike 行权价
        settlement_days 结算日调整天数
        expiry 行权日期
        discount_curve 利率折现曲线
        dividend_curve 权益折现曲线
        fx_vol_surface 外汇波动率曲面
        quanto_discount_curve
        quanto_fx_vol_curve
        quanto_correlation
        dv01
        theta
        delta
        gamma
        vega
        volga
        vanna
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.underlying = underlying
        self.underlyingPrice = underlying_price
        self.currency = currency
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.nominal = nominal
        self.strike = strike
        self.settlementDays = settlement_days
        self.expiry = expiry.strftime("%Y-%m-%d") if expiry is not None else ''
        self.discountCurve = discount_curve
        self.dividendCurve = dividend_curve
        self.fxVolSurface = fx_vol_surface
        self.quantoDiscountCurve = quanto_discount_curve
        self.quantoFxVolCurve = quanto_fx_vol_curve
        self.quantoCorrelation = quanto_correlation
        self.dv01 = dv01
        self.theta = theta
        self.fxDelta = delta
        self.fxGamma = gamma
        self.fxVega = vega
        self.fxVolga = volga
        self.fxVanna = vanna
        self.parseProto = parse_proto
