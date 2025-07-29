# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 18:58:04 2025

@author: SHagedoorn1
"""
import sympy as sp
from ..Diffeq import DiffEq
from numpy import zeros
sp.init_printing()

class LaplaceHandler:
    """
    A class for correctly computing the laplace transform of a differentail equation.
    
    This class properly handles the transformation of an ordinary differential
    equation (ODE) into the Laplace domain, ensuring the correct handling of
    functions and initial conditions.
    """
    def __init__(self, equation, name, var='t'):
        """
        Initializes the LaplaceHandler class.
        
        Parameters:
            equation (str):
                The differential equation to be transformed
            name:
                The name of the function in the equation, commonly 'y'
            var:
                The independent variable of the equation, default 't'
        
        Attributes:
            t (sympy Symbol):
                The independent variable before transforming
            s (sympy Symbol):
                The complex-valued laplace variable
            name (sympy Function):
                The function to be transformed
            lap_name (sympy Function):
                The name of the laplace-transformed function,
                capitalized version of 'name'.
            function (DiffEq object):
                A symbolic expression of the input equation (see Diffeq.py)
            equation:
                The differential equation converted to a sympy expression.
            initial_conds (numpy array):
                Initial conditions of the differential equations.
                In control theory, these are assumed to be zero, meaning the
                system is at rest before the input signal is applied.
            laplace_transform (sympy expression):
                The laplace transformed version of the input equation
        """
        self.t = sp.Symbol(var.lower())
        self.s = sp.Symbol('s')
        
        self.name = sp.Function(name.lower())
        self.lap_name = sp.Function(name.upper())
        self.function = DiffEq(equation, name, var)
        self.equation = self.function.function
        
        if self.function.order == 0:
            self.initial_conds = [0]
        else:
            self.initial_conds = zeros(self.function.order)
        self.laplace_transform = self.transform()
    
    def transform(self):
        """
        This transforms the given equation into the Laplace domain.
        
        This function applies the Laplace transform to the input equation using
        sympy's built in functions, while ensuring correct handling of initial
        conditions and function substitution.
        
        Returns:
            sympy expression:
                The Laplace-transformed equation.
        """
        transformed = sp.laplace_transform(self.equation, self.t, self.s, noconds=True)
        transformed = sp.laplace_correspondence(transformed, {self.name: self.lap_name})
        transformed = sp.laplace_initial_conds(transformed, self.t, {self.name: self.initial_conds})
        return transformed
    
    def __str__(self):
        """
        Returns the Laplace-transformed equation as a formatted string.
        
        When an instance of this class is printed, the transformed equation is
        displayed in a readable format
        """
        sp.pretty_print(f"{self.laplace_transform}")
        return ""
if __name__ == '__main__':
    string = "y'''+y''+y'+y+sin(t)"
    a = LaplaceHandler(string, 'y')
    print(a)