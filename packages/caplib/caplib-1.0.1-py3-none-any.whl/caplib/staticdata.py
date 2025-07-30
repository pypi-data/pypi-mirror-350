# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 11:26:50 2022

@author: dingq
"""

from caplibproto.dqproto import *
from caplibproto.dqstaticdataservice_pb2 import CreateStaticDataOutput, StaticDataType, INVALID_STATIC_DATA_TYPE #StaticDataType

from caplib.processrequest import * 

def to_static_data_type(src):
    '''
    Convert a string to StaticDataType.
    
    Parameters
    ----------
    src : str
        a string of static data type, i.e. 'SDT_IBOR_INDEX'.
    
    Returns
    -------
    Frequency       

    '''
    if src is None:
        return INVALID_STATIC_DATA_TYPE
    if src in ['', 'nan']:
        return INVALID_STATIC_DATA_TYPE
    else:
        return StaticDataType.DESCRIPTOR.values_by_name[src.upper()].number
    
#Static Data
def create_static_data(data_type, pb_data):
    '''
    Create static data object and send to dqlib object cache.
    
    Parameters
    ----------
    data_type : str
        Type of static data, i.e. 'SDT_IBOR_INDEX' for IBOR INDEX.
    pb_data : bytes
        Static data in bytes.
    
    Returns
    -------
    bool
        Indicates whether it is successful or not.
    
    '''    
    pb_input = dqCreateProtoCreateStaticDataInput(to_static_data_type(data_type), 
                                                  pb_data)        
    req_name = 'CREATE_STATIC_DATA'
    res_msg = process_request(req_name, pb_input.SerializeToString())   
    pb_output = CreateStaticDataOutput()
    pb_output.ParseFromString(res_msg)        
    if pb_output.success == False:
        raise Exception(pb_output.err_msg)       
    return pb_output.success