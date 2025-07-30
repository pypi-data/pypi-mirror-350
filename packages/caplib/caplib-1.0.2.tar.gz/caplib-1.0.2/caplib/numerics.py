# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:23:20 2022

@author: dingq
"""
import numpy as np

from caplibproto.dqproto import *
from caplibproto.dqnumerics_pb2 import *

#InterpMethod
def to_interp_method(src):
    '''
    Convert a string to InterpMethod.
    
    Parameters
    ----------
    src : str
        a string of interpolation method, i.e. 'LINEAR_INTERP'.
    
    Returns
    -------
    InterpMethod       

    '''
    if src is None:
        return LINEAR_INTERP
    if src in ['', 'nan']:
        return LINEAR_INTERP
    else:
        return InterpMethod.DESCRIPTOR.values_by_name[src.upper()].number
    
#ExtrapMethod
def to_extrap_method(src):
    '''
    Convert a string to ExtrapMethod.
    
    Parameters
    ----------
    src : str
        a string of extrapolation method, i.e. 'FLAT_EXTRAP'.
    
    Returns
    -------
    ExtrapMethod       

    '''
    if src is None:
        return FLAT_EXTRAP
    if src in ['', 'nan']:
        return FLAT_EXTRAP
    else:
        return ExtrapMethod.DESCRIPTOR.values_by_name[src.upper()].number
    
#UniformRandomNumberType
def to_uniform_random_number_type(src):
    '''
    Convert a string to UniformRandomNumberType.
    
    Parameters
    ----------
    src : str
        a string of uniform random number type, i.e. 'SOBOL_NUMBER'.
    
    Returns
    -------
    UniformRandomNumberType       

    '''
    if src is None:
        return SOBOL_NUMBER
    if src in ['', 'nan']:
        return SOBOL_NUMBER
    else:
        return UniformRandomNumberType.DESCRIPTOR.values_by_name[src.upper()].number
    
#GaussianNumberMethod
def to_gaussian_number_method(src):
    '''
    Convert a string to GaussianNumberMethod.
    
    Parameters
    ----------
    src : str
        a string of Gaussian number method, i.e. 'INVERSE_CUMULATIVE_METHOD'.
    
    Returns
    -------
    GaussianNumberMethod       

    '''
    if src is None:
        return INVERSE_CUMULATIVE_METHOD
    if src in ['', 'nan']:
        return INVERSE_CUMULATIVE_METHOD
    else:
        return GaussianNumberMethod.DESCRIPTOR.values_by_name[src.upper()].number
    
#WienerProcessBuildMethod
def to_wiener_process_build_method(src):
    '''
    Convert a string to WienerProcessBuildMethod.
    
    Parameters
    ----------
    src : str
        a string of weiner process build method, i.e. 'BROWNIAN_BRIDGE_METHOD'.
    
    Returns
    -------
    WienerProcessBuildMethod       

    '''
    if src is None:
        return BROWNIAN_BRIDGE_METHOD
    if src in ['', 'nan']:
        return BROWNIAN_BRIDGE_METHOD
    else:
        return WienerProcessBuildMethod.DESCRIPTOR.values_by_name[src.upper()].number
    
#GridType
def to_grid_type(src):
    '''
    Convert a string to GridType.
    
    Parameters
    ----------
    src : str
        a string of grid type, i.e. 'UNIFORM_GRID'.

    Returns
    -------
    GridType       

    '''
    if src is None:
        return UNIFORM_GRID
    if src in ['', 'nan']:
        return UNIFORM_GRID
    else:
        return GridType.DESCRIPTOR.values_by_name[src.upper()].number
    
#PdeSettings.MinMaxType
def to_pde_min_max_type(src):
    '''
    Convert a string to PdeSettings.MinMaxType.
    
    Parameters
    ----------
    src : str
        a string of PdeSettings.MinMaxType, i.e. 'MMT_NUM_STDEVS'.

    Returns
    -------
    GridType       

    '''
    if src is None:
        return PdeSettings.MinMaxType.MMT_NUM_STDEVS
    if src in ['', 'nan']:
        return PdeSettings.MinMaxType.MMT_NUM_STDEVS
    else:
        return PdeSettings.MinMaxType.DESCRIPTOR.values_by_name[src.upper()].number

def create_matrix(data: np.array, col_major = True):
    num_rows = data.shape[0]
    num_cols = data.shape[1]
    data_list = data.reshape(data.size).tolist()
    if col_major:
        return dqCreateProtoMatrix(num_rows, num_cols, data_list, Matrix.StorageOrder.ColMajor)    
    else:
        return dqCreateProtoMatrix(num_rows, num_cols, data_list, Matrix.StorageOrder.RowMajor)  