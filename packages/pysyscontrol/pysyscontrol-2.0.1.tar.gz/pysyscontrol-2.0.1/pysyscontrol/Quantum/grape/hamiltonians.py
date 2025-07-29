# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:23:33 2025

@author: Shagedoorn1
"""

import numpy as np

class TwoLevelSystem:
   """
   Two-level quantum system with a drift and control Hamiltonian.
   H(t) = H0 + u(t) * H1
   """
   def __init__(self, delta: float = 1.0, omega: float = 1.0):
       self.delta = delta
       self.omega = omega
       
       self.sigma_x = np.array([[0, 1], [1, 0]], dtype = 'complex')
       self.sigma_z = np.array([[1, 0], [0, -1]], dtype = "complex")
      
   def H0(self):
       return 0.5 * self.delta * self.sigma_z
   
   def H1(self):
       return 0.5 * self.delta * self.sigma_x
   
   def H(self, control: float):
       """
       Full Hamiltonian with given control field u(t)
       """
       return self.H0() + control * self.H1()