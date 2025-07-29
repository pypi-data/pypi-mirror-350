# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:22:40 2025

@author: Shagedoorn1
"""

import numpy as np
from scipy.linalg import expm

def evolve(system, psi0, controls, dt):
    """
    Evolve the state psi0 under time-dependent control fields.
    
    Parameters:
        ststem: An object with H(control) method
        psi0: Initial state vector
        controls: Array of control field values over time
        dt: time step
    Returns:
        psi_t: Final state after evolution
        history: List of psi at each time
    """
    psi = psi0.copy()
    history = [psi.copy()]
    
    for u in controls:
        H = system.H(u)
        U = expm(-1j * H * dt)
        psi = U @ psi
        history.append(psi.copy())
        
    return psi, history