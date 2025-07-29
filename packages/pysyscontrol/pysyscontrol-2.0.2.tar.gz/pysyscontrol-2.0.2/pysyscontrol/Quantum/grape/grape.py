# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:48:59 2025

@author: Shagedoorn1
"""

import numpy as np
from .hamiltonians import TwoLevelSystem
from .optimizers import GRAPESolver
from .bloch import animate_bloch_evolution
from .utils import normalize

class GRAPE:
    """
    High-level wrapper for running the GRAPE (Gradient Ascent Pulse Engineering)
    algorithm on a two-level quantum system.

    This class handles system setup, automatic initialization of a random initial
    state, optimization toward a target state, and optional Bloch sphere animation.

    Parameters:
    target : numpy array
        The desired target state vector (2D complex vector, normalized or unnormalized).
    iterations : int
        Number of optimization steps (also used as time discretization points).
    delta : float, optional
        Energy level detuning of the two-level system. Default is 1.0.
    omega : float, optional
        Control strength (e.g., Rabi frequency). Default is 1.0.
    T : float, optional
        Total evolution time. Default is 10.
    lr : float, optional
        Learning rate for the GRAPE optimizer. Default is 0.5.

    Attributes:
    sys : TwoLevelSystem
        The quantum system under control.
    psi0 : numpy array
        The randomly initialized and normalized starting state.
    target : numpy array
        The normalized target state.
    solver : GRAPESolver
        The low-level solver instance performing the optimization.
    """
    def __init__(self, target, iterations, delta=1.0, omega=1.0, T = 10, lr = 0.5):
        self.sys = TwoLevelSystem(delta=delta, omega = omega)
       
        psi0 = np.array([np.random.randn(), np.random.randn()], dtype="complex")
        self.psi0 = normalize(psi0)
        self.target = normalize(target)
        
        self.T = T
        self.lr = lr
        
        self.solver = GRAPESolver(system=self.sys, psi0=self.psi0, psi_target=self.target, T=self.T, steps=iterations, lr=self.lr)
        self.solver.optimize(iterations = iterations)
        
    def animate(self, dimensions=2):
        """
        Visualizes the quantum state evolution using a 2D or 3D Bloch-circle/sphere animation.

        This helps illustrate how the optimized control pulses evolve the
        quantum state from the initial state to the target state.
        """
        self._ani = animate_bloch_evolution(system=self.sys, psi0=self.psi0, target=target, controls=self.solver.controls, dt=self.solver.dt, steps=self.solver.N, dimension=dimensions)

if __name__ == "__main__":
    target = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype='complex')
    grape = GRAPE(target=target, iterations=50)
    grape.animate()