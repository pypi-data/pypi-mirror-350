import datetime

from caplibproto import InstrumentType, BusinessDayConvention, VolSmileType, VolSmileMethod, ExtrapMethod, \
    VolTermInterpMethod, VolTermExtrapMethod, DayCountConvention, VolatilityType, WingStrikeType, AtmType, DeltaType, \
    PayoffType

from python.caplib.caplib.fi_entity import PricerCurveSetting


class FxInfo:
    def __init__(self, currency_pair: str, type: InstrumentType, base_ccy: str, quote_ccy: str, start_delay: int,
                 delivery_day_convention: BusinessDayConvention, calendars: [str], delivery_currency: str):
        '''

        Parameters
        ----------
        currency_pair 货币对
        type 类型
        base_ccy 基础货币
        quote_ccy 报价货币
        start_delay 调整天数
        delivery_day_convention  交割日调整惯例
        calendars 日历
        delivery_currency 交割货币
        '''
        self.currencyPair = currency_pair
        self.type = type
        self.baseCcy = base_ccy
        self.quoteCcy = quote_ccy
        self.startDelay = start_delay
        self.deliveryDayConvention = delivery_day_convention
        self.calendars = ','.join(calendars) if len(calendars) > 0 else None
        self.deliveryCurrency = delivery_currency


class FxVolSurfaceTermQuoteInfo:
    def __init__(self, inst_code: str, term: str, strike: str, pay_off: PayoffType, quote: float):
        '''

        Parameters
        ----------
        inst_code 产品编码
        term 期限
        strike 行权价
        pay_off 收益
        quote 报价
        '''
        self.instCode = inst_code
        self.term = term
        self.strike = strike
        self.payOff = pay_off
        self.quote = quote


class FxVolSurfaceBuildInfo:
    def __init__(self, surface_code: str, as_of_date: datetime, fx_spot: FxInfo, fx_spot_quote: float,
                 vol_smile_type: VolSmileType, smile_method: VolSmileMethod, smile_extrap_method: ExtrapMethod,
                 time_interp_method: VolTermInterpMethod, time_extrap_method: VolTermExtrapMethod,
                 day_count_convention: DayCountConvention, volatility_type: VolatilityType,
                 wing_strike_type: WingStrikeType, lower_bound: float, upper_bound: float, quote_discount_curve: [int],
                 base_discount_curve: [int], atm_type: AtmType, short_delta: DeltaType, long_delta: DeltaType,
                 delta_cutoff: str, vol_surface_term_quotes: [FxVolSurfaceTermQuoteInfo]):
        '''

        Parameters
        ----------
        surface_code 曲面编码
        as_of_date 日期
        fx_spot 外汇即期
        fx_spot_quote 外汇即期报价
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
        quote_discount_curve 报价货币折现曲线
        base_discount_curve 基础货币折现曲线
        atm_type ATM类型
        short_delta 短期delta类型
        long_delta 长期delta类型
        delta_cutoff delta分割时间
        vol_surface_term_quotes 期限报价
        '''
        self.surfaceCode = surface_code
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.fxSpot = fx_spot
        self.fxSpotQuote = fx_spot_quote
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
        self.quoteDiscountCurve = quote_discount_curve
        self.baseDiscountCurve = base_discount_curve
        self.atmType = atm_type
        self.shortDelta = short_delta
        self.longDelta = long_delta
        self.deltaCutoff = delta_cutoff
        self.terms = vol_surface_term_quotes


class FxNdfPricingInfo:
    def __init__(self, inst_code: str, fx_ndf_info: FxInfo, as_of_date: datetime, rate: float, buy_size: float,
                 sell_size: float, delivery_date: datetime, dome_curve: [int], foreign_curve: [int],
                 dv01: PricerCurveSetting, theta: bool, fx_delta: bool, parse_proto: bool = False):
        '''

        Parameters
        ----------
        inst_code 产品编码
        fx_ndf_info 外汇不可交割远期信息
        as_of_date 时间
        rate 汇率
        buy_size 买入数量
        sell_size 卖出数量
        delivery_date 交割日期
        dome_curve 报价货币利率折现曲线
        foreign_curve 基础货币利率折现曲线
        dv01
        theta
        fx_delta  fx delta
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.instCode = inst_code
        self.fxNdfInfo = fx_ndf_info
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.rate = rate
        self.buySize = buy_size
        self.sellSize = sell_size
        self.deliveryDate = delivery_date.strftime("%Y-%m-%d") if delivery_date is not None else ''
        self.domeCurve = dome_curve
        self.foreignCurve = foreign_curve
        self.dv01 = dv01
        self.theta = theta
        self.fxDelta = fx_delta
        self.parseProto = parse_proto


class FxSwapPricingInfo:
    def __init__(self, inst_code: str, fx_swap_info: FxInfo, as_of_date: datetime, rate: float, near_buy_size: float,
                 near_sell_size: float, near_delivery_date: datetime, far_buy_size: float, far_sell_size: float,
                 far_delivery_date: datetime, dome_curve: [int], foreign_curve: [int],
                 dv01: PricerCurveSetting, theta: bool, fx_delta: bool, parse_proto: bool = False):
        '''

        Parameters
        ----------
        inst_code 产品编码
        fx_swap_info 外汇掉期信息
        as_of_date 时间
        rate 汇率
        near_buy_size 近端买入数量
        near_sell_size 近端卖出数量
        near_delivery_date 交割日期
        far_buy_size 远端买入数量
        far_sell_size 远端卖出数量
        far_delivery_date 远端交割日期
        dome_curve 报价货币利率折现曲线
        foreign_curve 基础货币利率折现曲线
        dv01
        theta
        fx_delta  fx delta
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.instCode = inst_code
        self.fxSwapInfo = fx_swap_info
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.rate = rate
        self.nearBuySize = near_buy_size
        self.nearSellSize = near_sell_size
        self.nearDeliveryDate = near_delivery_date.strftime("%Y-%m-%d") if near_delivery_date is not None else ''
        self.farBuySize = far_buy_size
        self.farSellSize = far_sell_size
        self.farDeliveryDate = far_delivery_date.strftime("%Y-%m-%d") if far_delivery_date is not None else ''
        self.domeCurve = dome_curve
        self.foreignCurve = foreign_curve
        self.dv01 = dv01
        self.theta = theta
        self.fxDelta = fx_delta
        self.parseProto = parse_proto


class FxForwardPricingInfo:
    def __init__(self, inst_code: str, fx_forward_info: FxInfo, as_of_date: datetime, rate: float, buy_size: float,
                 sell_size: float, delivery_date: datetime, dome_curve: [int], foreign_curve: [int],
                 dv01: PricerCurveSetting, theta: bool, fx_delta: bool, parse_proto: bool = False):
        '''

        Parameters
        ----------
        inst_code 产品编码
        fx_forward_info 外汇远期信息
        as_of_date 时间
        rate 汇率
        buy_size 买入数量
        sell_size 卖出数量
        delivery_date 交割日期
        dome_curve 报价货币利率折现曲线
        foreign_curve 基础货币利率折现曲线
        dv01
        theta
        fx_delta  fx delta
        parse_proto 是否解析二进制，false时返回结果只有二进制
        '''
        self.instCode = inst_code
        self.fxForwardInfo = fx_forward_info
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.rate = rate
        self.buySize = buy_size
        self.sellSize = sell_size
        self.deliveryDate = delivery_date.strftime("%Y-%m-%d") if delivery_date is not None else ''
        self.domeCurve = dome_curve
        self.foreignCurve = foreign_curve
        self.dv01 = dv01
        self.theta = theta
        self.fxDelta = fx_delta
        self.parseProto = parse_proto


class FxEuOptionPricingInfo:
    def __init__(self, inst_code: str, fx_spot_info: FxInfo, as_of_date: datetime, rate: float, nominal: float,
                 strike: float, delivery_date: datetime, expiry: datetime, dome_curve: [int], foreign_curve: [int],
                 fx_vol_surface: [int], dv01: PricerCurveSetting, theta: bool, fx_delta: bool, fx_gamma: bool,
                 fx_vega: bool, fx_volga: bool, fx_vanna: bool, parse_proto: bool = False):
        '''
        
        Parameters
        ----------
        inst_code 产品编码
        fx_spot_info 外汇即期信息
        as_of_date 定价时间
        rate 汇率
        nominal 数量
        strike 行权价
        delivery_date 交割日期
        expiry 行权日期
        dome_curve 报价货币利率折现曲线
        foreign_curve 基础货币利率折现曲线
        fx_vol_surface 波动率曲面
        dv01
        theta
        fx_delta  fx delta
        fx_gamma  fx gamma
        fx_vega  fx vega
        fx_volga  fx volga
        fx_vanna  fx vanna
        parse_proto  是否解析二进制，false时返回结果只有二进制
        '''
        self.instCode = inst_code
        self.fxSpotInfo = fx_spot_info
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.rate = rate
        self.nominal = nominal
        self.strike = strike
        self.deliveryDate = delivery_date.strftime("%Y-%m-%d") if delivery_date is not None else ''
        self.expiry = expiry.strftime("%Y-%m-%d") if expiry is not None else ''
        self.domeCurve = dome_curve
        self.foreignCurve = foreign_curve
        self.fxVolSurface = fx_vol_surface
        self.dv01 = dv01
        self.theta = theta
        self.fxDelta = fx_delta
        self.fxGamma = fx_gamma
        self.fxVega = fx_vega
        self.fxVolga = fx_volga
        self.fxVanna = fx_vanna
        self.parseProto = parse_proto


class FxAmericanOptionPricingInfo:
    def __init__(self, inst_code: str, fx_spot_info: FxInfo, as_of_date: datetime, rate: float, nominal: float,
                 strike: float, delivery_date: datetime, expiry: datetime, settlement_days: int, dome_curve: [int],
                 foreign_curve: [int], fx_vol_surface: [int], dv01: PricerCurveSetting, theta: bool, fx_delta: bool,
                 fx_gamma: bool, fx_vega: bool, fx_volga: bool, fx_vanna: bool, parse_proto: bool = False):
        '''

        Parameters
        ----------
        inst_code 产品编码
        fx_spot_info 外汇即期信息
        as_of_date 定价时间
        rate 汇率
        nominal 数量
        strike 行权价
        delivery_date 交割日期
        expiry 行权日期
        settlement_days 结算日调整天数
        dome_curve 报价货币利率折现曲线
        foreign_curve 基础货币利率折现曲线
        fx_vol_surface 波动率曲面
        dv01
        theta
        fx_delta  fx delta
        fx_gamma  fx gamma
        fx_vega  fx vega
        fx_volga  fx volga
        fx_vanna  fx vanna
        parse_proto  是否解析二进制，false时返回结果只有二进制
        '''
        self.instCode = inst_code
        self.fxSpotInfo = fx_spot_info
        self.date = as_of_date.strftime("%Y-%m-%d %H:%M:%S") if as_of_date is not None else ''
        self.rate = rate
        self.nominal = nominal
        self.strike = strike
        self.deliveryDate = delivery_date.strftime("%Y-%m-%d") if delivery_date is not None else ''
        self.expiry = expiry.strftime("%Y-%m-%d") if expiry is not None else ''
        self.settlementDays = settlement_days
        self.domeCurve = dome_curve
        self.foreignCurve = foreign_curve
        self.fxVolSurface = fx_vol_surface
        self.dv01 = dv01
        self.theta = theta
        self.fxDelta = fx_delta
        self.fxGamma = fx_gamma
        self.fxVega = fx_vega
        self.fxVolga = fx_volga
        self.fxVanna = fx_vanna
        self.parseProto = parse_proto
