# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 14:47:26 2022

@author: dingq
"""
from caplibproto.dqproto import *

from caplib.processrequest import * 

#Calculate Change of Risk Factors
def calculate_risk_factor_change(risk_factor_values, change_type):
    '''
    Calculate the change of risk factor from one time to the other.

    Parameters
    ----------
    risk_factor_values : TYPE
        DESCRIPTION.
    change_type : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    p_type = RiskFactorChangeType.DESCRIPTOR.values_by_name[change_type.upper()].number 
    p_samples = list(risk_factor_values)
    pb_input = dqCreateProtoRiskFactorChangeCalculationInput(p_type, p_samples)
    req_name = 'RISK_FACTOR_CHANGE_CALCULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString())
    pb_output = RiskFactorChangeCalculationOutput()
    pb_output.ParseFromString(res_msg)        
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)   
    return pb_output.result

#Simulate Risk Factors
def simulate_risk_factor(risk_factor_changes, change_type, base):
    '''
    Simulate scenarios for a risk factor given its historical changes and current value.

    Parameters
    ----------
    risk_factor_changes : TYPE
        DESCRIPTION.
    change_type : TYPE
        DESCRIPTION.
    base : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    p_type = RiskFactorChangeType.DESCRIPTOR.values_by_name[change_type.upper()].number 
    p_changes = dqCreateProtoVector(risk_factor_changes)
    p_base = float(base)
    pb_input = dqCreateProtoRiskFactorSimulationInput(p_type, p_changes, p_base)    
    req_name = 'RISK_FACTOR_SIMULATOR'
    res_msg = ProcessRequest(req_name, pb_input.SerializeToString()) 
    pb_output = RiskFactorSimulationOutput()
    pb_output.ParseFromString(res_msg)           
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)
    return pb_output.result
   

#dqCalculateInstrumentRawReturns:
def calculate_inst_raw_returns(settings, inst_price_series):
    '''
    @args:
        1. settings: dqproto.InstrumentReturnSettings
        2. inst_price_series: dqproto.TimeSeries
    @return:
        dqproto.InstrumentStatisticsSeries
    '''
    try:
        pb_input = dqCreateProtoCalculateInstrumentRawReturnsInput(settings, inst_price_series)
        
        res_msg = ProcessRequest("CALCULATE_INSTRUMENT_RAW_RETURNS", pb_input.SerializeToString())
        pb_output = CalculateInstrumentRawReturnsOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.raw_returns_series
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
#dqCalculateInstrumentCleansedReturns:
def calculate_inst_cleansed_returns(settings, inst_quote_series, inst_listed_date, proxy_return_series):
    '''
    @args:
        1. settings: dqproto.InstrumentCleansedReturnSettings
        2. inst_quote_series: dqproto.TimeSeries
        3. inst_listed_date: dqproto.Date
        4. proxy_return_series: dqproto.InstrumentStatisticsSeries
    @return:
        dqproto.InstrumentStatisticsSeries
    '''
    try:
        pb_input = dqCreateProtoCalculateInstrumentCleansedReturnsInput(settings, inst_quote_series, inst_listed_date, proxy_return_series)
        
        res_msg = ProcessRequest("CALCULATE_INSTRUMENT_CLEANSED_RETURNS", pb_input.SerializeToString())
        pb_output = CalculateInstrumentCleansedReturnsOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.cleansed_returns_series
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
      
#dqGenerateHsScenarios:
def generate_hist_sim_scenarios(settings, inst_quote_series, inst_listed_date, proxy_return_series):
    '''
    @args:
        1. settings: dqproto.HsScnGenSettings 
        2. inst_return_series: dqproto.InstrumentStatisticsSeries 
        3. risk_factor_name: string
        4. as_of_date: dqproto.Date
    @return:
        dqproto.Scenario
    '''
    try:
        pb_input = dqCreateProtoGenerateFhsScenariosInput(inst_return_series, risk_factor_name, settings, as_of_date)
        
        res_msg = ProcessRequest("GENERATE_HS_SCENARIOS", pb_input.SerializeToString())
        pb_output = GenerateFhsScenariosOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.scenarios
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))  

#dqIdentifyStressedDates:
def identify_stress_dates(settings, benchmark_return_series, as_of_date):
    '''
    @args:
       1. settings: dqproto.StressedScnGenSettings
       2. benchmark_return_series: dqproto.InstrumentStatisticsSeries
       3. as_of_date: dqproto.Date
    @return:
        dqproto.Scenario
    '''
    try:
        pb_input = dqCreateProtoIdentifyStressDatesInput(benchmark_return_series, settings, as_of_date)
        
        res_msg = ProcessRequest("IDENTIFY_STRESSED_DATES", pb_input.SerializeToString())
        pb_output = IdentifyStressDatesOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.stress_dates
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
        
#dqGenerateStressedScenearios:
def generate_stressed_scenarios(settings, inst_return_series, risk_factor_name, stress_dates, as_of_date):
    '''
    @args:
       1. inst_return_series: dqproto.InstrumentStatisticsSeries
        2. risk_factor_name: string
        3. p_settings: dqproto.StressedScnGenSettings
        4. stress_dates: dqproto.Date
        5. as_of_date: dqproto.Date
    @return:
        dqproto.Scenario
    '''
    try:
        pb_input = dqCreateProtoGenerateStressScenariosInput(inst_return_series, risk_factor_name, settings, stress_dates, as_of_date)
        
        res_msg = ProcessRequest("GENERATE_STRESSED_SCENARIOS", pb_input.SerializeToString())
        pb_output = GenerateStressScenariosOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.scenarios
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))  
       
        
#dqCreateTradingPosition:
def create_trading_position(buy_sell, norminal, inst_name, tier):
    '''
    @args:
        1. buy_sell: dqproto.BuySellFlag
        2. norminal: double
        3. inst_name: string
        4. tier: dqproto.InstrumentTier
    @return:
        dqproto.TradingPosition
    '''
    try:
        return dqCreateProtoTradingPosition(buy_sell, norminal, inst_name, tier)
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
#dqCreatePortfolio:
def create_portfolio(portfolio_id, trading_positions):
    '''
    @args:
        1. portfolio_id: string
        2. trading_positions: list of dqproto.TradingPosition
    @return:
        dqproto.Portfolio
    '''
    try:
        return dqCreateProtoPortfolio(portfolio_id, trading_positions)
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))
        
        
#dqCalculateProfitLossDistribution:
def calculate_profit_loss_distribution(portfolio, scenarios):
    '''
    @args:
      1. portfolio: dqproto.Portfolio
      2. scenarios: dqproto.Scenario
    @return:
        dqproto.Vector
    '''
    try:
        pb_input = dqCreateProtoCalculateProfitLossInput(portfolio, scenarios)
        
        res_msg = ProcessRequest("CALCULATE_PROFIT_LOSS_DISTRIBUTION", pb_input.SerializeToString())
        pb_output = CalculateProfitLossOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.profit_loss_samples
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
 
#dqCalculateValueAtRisk:
def calculate_value_at_risk(profit_loss_samples, probability, antithetic):
    '''
    @args:
      1. profit_loss_samples: dqproto.Vector
      2. probability: double
      3. antithetic: bool
    @return:
        dqproto.CalculateValueAtRiskOutput
    '''
    try:
        pb_input = dqCreateProtoCalculateValueAtRiskInput(profit_loss_samples, probability, antithetic)
        
        res_msg = ProcessRequest("CALCULATE_VALUE_AT_RISK", pb_input.SerializeToString())
        pb_output = CalculateValueAtRiskOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
        
#dqCalculateExpectedShortfall:
def calculate_expected_short_fall(profit_loss_samples, probability, antithetic):
    '''
    @args:
      1. profit_loss_samples: dqproto.Vector
      2. probability: double
      3. antithetic: bool
    @return:
        dqproto.CalculateExpectedShortfallOutput
    '''
    try:
        pb_input = dqCreateProtoCalculateExpectedShortfallInput(profit_loss_samples, probability, antithetic)
        
        res_msg = ProcessRequest("CALCULATE_EXPECTED_SHORT_FALL", pb_input.SerializeToString())
        pb_output = CalculateExpectedShortfallOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
        
#dqCalculateTierPInitialMargin:
def calculate_tier_p_initial_margin(settings, portfolio, portfolio_hs_profit_loss_samples, position_hs_profit_loss_samples, portfolio_stressed_profit_loss_samples, position_stressed_profit_loss_samples):
    '''
    @args:
        1. settings: dqproto.TierPInitialMarginSettings
        2. portfolio: dqproto.Portfolio
        3. portfolio_hs_profit_loss_samples: dqproto.Vector
        4. position_hs_profit_loss_samples: list of dqproto.Vector
        5. portfolio_stressed_profit_loss_samples: dqproto.Vector
        6. position_stressed_profit_loss_samples: list of dqproto.Vector
    @return:
        dqproto.CalculateTierPInitialMarginOutput
    '''
    try:
        pb_input = dqCreateProtoCalculateTierPInitialMarginInput(settings, 
                                                                 portfolio, 
                                                                 portfolio_hs_profit_loss_samples, 
                                                                 position_hs_profit_loss_samples, 
                                                                 portfolio_stressed_profit_loss_samples, 
                                                                 position_stressed_profit_loss_samples)
        
        res_msg = ProcessRequest("CALCULATE_TIER_P_INITIAL_MARGIN", pb_input.SerializeToString())
        pb_output = CalculateTierPInitialMarginOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 


#dqCalculateTierNInitialMarginRate:
def calculate_tier_n_initial_margin_rate(settings, reference_date, benchmark_1, benchmark_2):
    '''
    @args:
        1. settings: dqproto.TierNInitialMarginSettings
        2. reference_date: dqproto.Date
        3. benchmark_1: dqproto.InstrumentStatisticsSeries
        4. benchmark_2: dqproto.InstrumentStatisticsSeries
    @return:
        double
    '''
    try:
        pb_input = dqCreateProtoCalculateTierNInitialMarginRateInput(settings, 
                                                                 reference_date, 
                                                                 benchmark_1, 
                                                                 benchmark_2)
        
        res_msg = ProcessRequest("CALCULATE_TIER_N_INITIAL_MARGIN_RATE", pb_input.SerializeToString())
        pb_output = CalculateTierNInitialMarginRateOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.flat_margin_rate
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))         

        
#dqCalculateTierNInitialMargin:
def calculate_tier_n_initial_margin(portfolio, margin_rate):
    '''
    @args:
        portfolio: dqproto.Portfolio
        margin_rate: double
    @return:
        double
    '''
    try:
        pb_input = dqCreateProtoCalculateTierNInitialMarginInput(portfolio, margin_rate)
        res_msg = ProcessRequest("CALCULATE_TIER_N_INITIAL_MARGIN", pb_input.SerializeToString())
        pb_output = CalculateTierNInitialMarginOutput()
        pb_output.ParseFromString(res_msg)
        return pb_output.margin
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e))

        
#dqCalculateTotalInitialMargin:
def calculate_total_initial_margin(p_initial_margins, n_initial_margin, round_up_value):
    '''
    @args:
        1. p_initial_margins: double
        2. n_initial_margin: double
        3. round_up_value: int32
    @return:
        double
    '''
    try:
        pb_input = dqCreateProtoCalculateTotalInitialMarginInput(p_initial_margins, 
                                                                 n_initial_margin, 
                                                                 round_up_value)
        
        res_msg = ProcessRequest("CALCULATE_TOTAL_INITIAL_MARGIN", pb_input.SerializeToString())
        pb_output = CalculateTotalInitialMarginOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
        
        
#dqRunDataCleansingEngine:
def run_data_cleansing_engine(settings, index_series, inst_quote_series):
    '''
    @args:
        1. settings: dqproto.RiskFactorDataCleansingSettings
        2. index_series: dqproto.TimeSeries
        3. inst_quote_series: dqproto.InstrumentQuoteSeries
    @return:
        double
    '''
    try:
        index_cleansed_return_manager = "IndexCleansedReturnManager"
        inst_raw_return_manager = "InstrumentRawReturnManager"
        inst_raw_return_series = "InstrumentRawReturnSeries"
        all_cleansed_return_series = "AllCleansedReturnSeries"
        pb_input = dqCreateProtoRunRiskFactorDataCleansingEngineInput(settings, 
                                                                      index_series, 
                                                                      inst_quote_series,
                                                                      index_cleansed_return_manager,
                                                                      inst_raw_return_manager,
                                                                      inst_raw_return_series,
                                                                      all_cleansed_return_series)
        
        res_msg = ProcessRequest("RISK_FACTOR_DATA_CLEANSING_ENGINE", pb_input.SerializeToString())
        pb_output = RunRiskFactorDataCleansingEngineOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output.success
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
        

#dqRunInitialMarginEngine:
def run_initial_margin_engine(im_settings, hs_scn_gen_settings, stressed_scn_gen_settings, portfolios, use_arbitrary_scenario,hs_scenarios,stressed_scenarios):
    '''
    @args:
        1. im_settings: dqproto.InitialMarginSettings
        2. hs_scn_gen_settings: dqproto.HsScnGenSettings
        3. stressed_scn_gen_settings: dqproto.StressedScnGenSettings
        4. portfolios: dqproto.Portfolio
        5. use_scenario: bool
        6. hs_scenarios: dqproto.Scenario
        7. stressed_scenarios: dqproto.Scenario
        8. aod: dqproto.Date
    @return:
        dqproto.RunInitialMarginEngineOutput
    '''
    try:
        index_cleansed_return_manager = "IndexCleansedReturnManager"
        all_cleansed_return_series = "AllCleansedReturnSeries"
        
        pb_input = dqCreateProtoRunInitialMarginEngineInput(aod, 
                                                            im_settings, 
                                                            hs_scn_gen_settings,
                                                            stressed_scn_gen_settings,
                                                            portfolios,
                                                            all_cleansed_return_series,
                                                            index_cleansed_return_manager,
                                                            use_arbitrary_scenario,
                                                            hs_scenarios,
                                                            stressed_scenarios,
                                                            HYPOPORTFOLIO)
        
        res_msg = ProcessRequest("INITIAL_MARGIN_ENGINE", pb_input.SerializeToString())
        pb_output = RunInitialMarginEngineOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
    

#dqRunInitialMarginBacktestingEngine:
def run_initial_margin_backtesting_engine(im_settings, hs_scn_gen_settings, stressed_scn_gen_settings, portfolios, cleansed_return_data, raw_return_data, schedule, name, tag):
    '''
    @args:
        1. im_settings: dqproto.InitialMarginSettings
        2. hs_scn_gen_settings: dqproto.HsScnGenSettings
        3. stressed_scn_gen_settings: dqproto.StressedScnGenSettings        
        4. portfolio: dqproto.Portfolio
        5. cleansed_return_data: dqproto.InstrumentStatisticsSeries
        6. raw_return_data: dqproto.InstrumentStatisticsSeries
        7. schedule: dqproto.Schedule
        8. name: string
        9. tag: string
    @return:
        dqproto.RunInitialMarginBacktestingOutput
    '''
    try:
                
        pb_input = dqCreateProtoRunInitialMarginBacktestingInput(schedule, 
                                                                 portfolios, 
                                                                 raw_return_data, 
                                                                 cleansed_return_data, 
                                                                 im_settings, 
                                                                 hs_scn_gen_settings, 
                                                                 stressed_scn_gen_settings, 
                                                                 name, tag)
        
        res_msg = ProcessRequest("RUN_INITIAL_MARGIN_BACKTESTING", pb_input.SerializeToString())
        pb_output = RunInitialMarginBacktestingOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 
        
        
#dqGetIMBacktestingResult:
def get_im_backtesting_result(initial_margin_backtesting_engine, portfolio, instrument, backtesting_date, option):
    '''
    @args:
        1. initial_margin_backtesting_engine: string
        2. portfolio: string
        3. instrument: string
        4. backtesting_date: dqproto.Date
        5. option: string
    @return:
        dqproto.GetInitialMarginBacktestingResultOutput
    '''
    try:
        #dqCreateProtoSchedule(size, data, frist_period, last_period)
        pb_input = dqCreateProtoGetInitialMarginBacktestingResultInput(initial_margin_backtesting_engine, 
                                                                       portfolio, 
                                                                       instrument, 
                                                                       backtesting_date, 
                                                                       option)
        
        res_msg = ProcessRequest("GET_INITIAL_MARGIN_BACKTESTING_RESULT", pb_input.SerializeToString())
        pb_output = GetInitialMarginBacktestingResultOutput()
        pb_output.ParseFromString(res_msg)
        
        return pb_output
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print(str(e)) 