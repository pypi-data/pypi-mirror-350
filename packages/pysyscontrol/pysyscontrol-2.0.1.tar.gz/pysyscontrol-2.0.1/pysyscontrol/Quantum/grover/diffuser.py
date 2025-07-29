# -*- coding: utf-8 -*-
"""
Created on Wed May 14 01:50:34 2025

@author: Shagedoorn1
"""

import numpy as np
from .utils import normalize

def create_uniform_state(n_qubits):
    return normalize(np.ones(n_qubits, dtype=complex))

def diffuser(n_qubits):
    dim = 2 ** n_qubits
    psi = create_uniform_state(dim)
    return 2 * np.outer(psi, psi.conj()) - np.eye(dim)