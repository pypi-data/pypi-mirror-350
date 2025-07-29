# -*- coding: utf-8 -*-
"""
Created on Wed May 14 01:50:35 2025

@author: Shagedoorn1
"""

import numpy as np

def mark_single_state(n_qubits, index):
    dim = 2 ** n_qubits
    O = np.eye(dim, dtype=complex)
    O[index, index] = -1
    return O

def mark_multiple_states(n_qubits, indices):
    dim = 2 ** n_qubits
    O = np.eye(dim, dtype=complex)
    for idx in indices:
        O[idx, idx] = -1
    return O