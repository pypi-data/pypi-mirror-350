from caplib.market import *
from caplib.datetime import *
from caplib.staticdata import *

def create_pm_cash_template(inst_name: str, 
                            start_delay: int, 
                            delivery_day_convention: str, 
                            calendars: list, 
                            day_count: str):
    """
    Create a PM cash template.

    Parameters
    ----------
    inst_name : str
        The name of the instrument.
    start_delay : int
        The start delay in days.
    delivery_day_convention : str
        The delivery day convention.
    calendars : list
        List of calendars.
    day_count : str
        The day count convention.

    Returns
    -------
    PmCashTemplate
        The created PM cash template.
    """
    try:
        inst_template_list = PmCashTemplateList()
        inst_template = dqCreateProtoPmCashTemplate(inst_name,
                                                    start_delay,
                                                    to_business_day_convention(delivery_day_convention),
                                                    calendars,
                                                    to_day_count_convention(day_count))
        
        pb_data_list = dqCreateProtoPmCashTemplateList([inst_template])  
        create_static_data('SDT_PM_CASH', pb_data_list.SerializeToString())
        return inst_template
    except Exception as e:
        return str(e)