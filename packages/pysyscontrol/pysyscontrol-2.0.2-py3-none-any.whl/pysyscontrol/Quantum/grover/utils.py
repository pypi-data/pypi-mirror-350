# -*- coding: utf-8 -*-
"""
Created on Wed May 14 01:01:58 2025

@author: Shagedoorn1
"""

import numpy as np

def normalize(u):
    """
    If you need full documentation on this then you have no idea what we are doing.
    Fine
    Parameter:
        u (numpy array):
            Array which is to be normalized
    
    Returns:
        u (numpy array):
            Normalized array. An array is normalised when it has length of one. This is achieved by dividing the array by it's length.
    """
    return u / np.linalg.norm(u)