# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:23:48 2025

@author: Shagedoorn1
"""

import numpy as np

def fidelity(psi_final, psi_target):
    """
    Computes state overlap fidelity. This is defined as the square of the dot product of the state and target state.
    F = ⟨ψtarget|ψ⟩^2
    """
    
    return np.abs(np.vdot(psi_target, psi_final))**2