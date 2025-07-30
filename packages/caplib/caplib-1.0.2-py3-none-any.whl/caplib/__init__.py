#! /usr/bin/env python
# coding=utf-8

from .analytics import create_ir_curve_risk_settings, create_credit_curve_risk_settings, create_theta_risk_settings
from .analytics import create_ir_yield_curve, create_flat_ir_yield_curve, create_credit_curve, create_flat_credit_curve
from .analytics import create_ir_yield_curve_from_binary, create_credit_curve_from_binary
from .analytics import create_model_settings, create_pde_settings, create_monte_carlo_settings, create_pricing_settings, \
    create_model_free_pricing_settings
from .analytics import create_price_risk_settings, create_vol_risk_settings, create_price_vol_risk_settings
from .analytics import create_volatility_surface_definition, create_volatility_smile, create_volatility_surface
from .analytics import print_term_structure_curve
from .cmanalytics import cm_european_option_pricer, cm_american_option_pricer, cm_asian_option_pricer, \
    cm_digital_option_pricer, cm_single_barrier_option_pricer, cm_double_barrier_option_pricer
from .cmanalytics import cm_one_touch_option_pricer, cm_double_touch_option_pricer, cm_range_accrual_option_pricer, \
    cm_single_shark_fin_option_pricer, cm_double_shark_fin_option_pricer, cm_ping_pong_option_pricer, \
    cm_airbag_option_pricer
from .cmanalytics import cm_snowball_auto_callable_note_pricer, cm_phoenix_auto_callable_note_pricer
from .cmanalytics import create_cm_option_quote_matrix, cm_vol_surface_builder
from .cmanalytics import create_cm_risk_settings, create_cm_mkt_data_set
from .cmanalytics import create_pm_par_rate_curve, pm_yield_curve_builder, create_pm_mkt_conventions, \
    create_pm_option_quote_matrix, pm_vol_surface_builder
from .cmmarket import create_pm_cash_template
from .cranalytics import create_cr_risk_settings, create_credit_par_curve, credit_curve_builder, \
    create_cds_pricing_settings, create_cr_mkt_data_set, credit_default_swap_pricer
from .crmarket import create_cds_template, build_credit_default_swap
from .datetime import create_date, create_period, create_calendar, year_frac_calculator, simple_year_frac_calculator, \
    date_generator
from .eqanalytics import create_eq_risk_settings, create_eq_mkt_data_set
from .eqanalytics import eq_european_option_pricer, eq_american_option_pricer, eq_asian_option_pricer, \
    eq_digital_option_pricer, eq_single_barrier_option_pricer, eq_double_barrier_option_pricer
from .eqanalytics import eq_one_touch_option_pricer, eq_double_touch_option_pricer, eq_range_accrual_option_pricer, \
    eq_single_shark_fin_option_pricer, eq_double_shark_fin_option_pricer, eq_ping_pong_option_pricer, \
    eq_airbag_option_pricer
from .eqanalytics import eq_snowball_auto_callable_note_pricer, eq_phoenix_auto_callable_note_pricer
from .fianalytics import create_bond_curve_build_settings, create_bond_par_curve, build_bond_yield_curve, \
    build_bond_sprd_curve
from .fianalytics import create_fi_mkt_data_set, create_fi_risk_settings, vanilla_bond_pricer
from .fianalytics import yield_to_maturity_calculator, fixed_cpn_bond_par_rate_calculator
from .fimarket import build_vanilla_bond, build_zero_cpn_bond, build_fixed_cpn_bond
from .fimarket import create_std_bond_template, create_std_zero_cpn_bond_template, create_std_fixed_cpn_bond_template
from .fimarket import create_vanilla_bond_template, create_zero_cpn_bond_template, create_fixed_cpn_bond_template
from .fxanalytics import create_fx_risk_settings, create_fx_mkt_data_set
from .fxanalytics import fx_european_option_pricer, fx_american_option_pricer, fx_asian_option_pricer, \
    fx_digital_option_pricer, fx_single_barrier_option_pricer, fx_double_barrier_option_pricer
from .fxanalytics import fx_ndf_pricer, fx_swap_pricer, fx_forward_pricer
from .fxanalytics import fx_one_touch_option_pricer, fx_double_touch_option_pricer, fx_range_accrual_option_pricer, \
    fx_single_shark_fin_option_pricer, fx_double_shark_fin_option_pricer, fx_ping_pong_option_pricer, \
    fx_airbag_option_pricer
from .fxanalytics import fx_snowball_auto_callable_note_pricer, fx_phoenix_auto_callable_note_pricer
from .fxmarket import create_fx_forward_template, create_fx_swap_template, create_fx_ndf_template
from .fxmarket import create_fx_non_deliverable_forwad, create_fx_swap, create_fx_forward
from .fxmarket import fx_spot_date_calculator, fx_option_date_calculator
from .http_request import post_no_token, save_token
from .iranalytics import create_ir_curve_build_settings, create_ir_par_rate_curve, ir_single_ccy_curve_builder, \
    ir_cross_ccy_curve_builder
from .iranalytics import create_ir_mkt_data_set, create_ir_risk_settings, ir_vanilla_instrument_pricer
from .irmarket import create_depo_template, create_fra_template, create_ir_vanilla_swap_template
from .irmarket import create_ibor_index, create_leg_definition, create_fixed_leg_definition, \
    create_floating_leg_definition
from .irmarket import create_leg_fixings, build_ir_vanilla_instrument, build_depo, build_fra
from .irmarket import print_cash_flow_sched
from .market import create_european_option, create_american_option, create_asian_option, create_digital_option
from .market import create_foreign_exchange_rate, create_fx_spot_rate
from .market import create_fx_spot_template
from .market import create_one_touch_option, create_double_touch_option, create_single_barrier_option, \
    create_double_barrier_option, create_single_shark_fin_option, create_double_shark_fin_option
from .market import create_range_accrual_option, create_airbag_option, create_ping_pong_option, create_collar_option, \
    create_phoenix_auto_callable_note, create_snowball_auto_callable_note
from .market import create_time_series

# from .mktrisk import calculate_risk_factor_change, simulate_risk_factor, calculate_expected_shortfall, calculate_value_at_risk
