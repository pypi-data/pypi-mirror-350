# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:22:37 2025

@author: Shagedoorn1
"""

import numpy as np
from .pulse_solvers import evolve
from .fidelity import fidelity

class GRAPESolver:
    """
    A solver using the GRAPE (Gradient Ascent Pulse Engineering) algorithm for
    quantum control optimization.
    
    This class optimizes a control pulse sequence to evolve a quantum state
    from an initial state to a desired target state with high fidelity.
    
    Parameters:
        system : object
        A quantum system object that provides a method `H(control)` to return the Hamiltonian
        for a given control value.
    psi0 : numpy array
        The initial quantum state vector (normalized).
    psi_target : numpy array
        The desired target state vector (normalized).
    T : float, optional
        Total evolution time. Default is 10.
    steps : int, optional
        Number of time steps in the control sequence. Default is 1000.
    lr : float, optional
        Learning rate for gradient ascent. Default is 0.1.
    
    Attributes:
        controls : np.ndarray
        Array of control amplitudes to be optimized.
    dt : float
        Time step size (T / steps).
    """
    def __init__(self, system, psi0, psi_target, T = 10, steps = 1000, lr = 0.1):
        self.system = system
        self.psi0 = psi0
        self.psi_target = psi_target
        self.T = T
        self.N = steps
        self.dt = T / steps
        self.lr = lr
        self.controls = np.random.randn(self.N) * 0.1
        
    def optimize(self, iterations = 100):
        """
        Run the GRAPE optimization loop.
        
        Parameters:
            iterations: int
                Number of optimization iterations
        
        Returns:
            self.controls: numpy array:
                Optimized control field array
        """
        for i in range(iterations):
            f, grad = self._compute_fidelity_and_gradient()
            self.controls += self.lr * grad
            if i % 10 ==0:
                print(f"Iter {i:3d}: Fidelity = {f:.6f}")
        return self.controls
    
    def _compute_fidelity_and_gradient(self, epsilon=1e-5):
        """
        Computes the fidelity and its gradient with respect to the control fields
        using finite difference approximation.

        Parameters:
            epsilon : float
                Perturbation size for numerical gradient computation.

        Returns:
            fidelity : float
                Fidelity between final and target state.
            gradient : numpy array
                Gradient of fidelity with respect to control amplitudes.
        """
        psi_final, _ = evolve(self.system, self.psi0, self.controls, self.dt)
        f0 = fidelity(psi_final, self.psi_target)
        
        grad = np.zeros_like(self.controls)
        for i in range(len(self.controls)):
            controls_eps = self.controls.copy()
            controls_eps[i] += epsilon
            psi_eps, _ = evolve(self.system, self.psi0, controls_eps, self.dt)
            f_eps = fidelity(psi_eps, self.psi_target)
            grad[i] = (f_eps - f0) / epsilon
        return f0, grad
    
    def psi_final(self):
        """
        Compute the final state of the system
        """
        psi, _ = evolve(self.system, self.psi0, self.controls, self.dt)
        return psi