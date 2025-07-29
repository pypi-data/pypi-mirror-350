# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 10:53:55 2025

@author: Shagedoorn1
"""
import sympy as sp
import numpy as np
import cmath
from sympy import I
from .laplace_handler import LaplaceHandler
from ..Diffeq import DiffEq


class TransferFunction:
    """
    A class that calculates the transfer function of a control system from its
    governing ordinary differential equations, ODEs.
    
    Two ODEs should be provided one for the input signal and one
    for the output signal. These are laplace transformed and set equal to eachother.
    
    The transfer function H(s) is defined as the ratio:
        H(s) = Y(s) / X(s)
    
    If a more readable version of the equations is desired, omit print 
    statements and directly evaluate the required value in the editor or
    console.
    """
    
    def __init__(self, equation_out, equation_in, name_out='y', name_in='x', var='t'):
        """
        Initializes the TransferFunction class.
        
        Parameters:
            equation_out (str):
                The ODE representing the output signal
            equation_in (str):
                The ODE representing the input signal
            name_out (str):
                The name of the output function, default y
            name_in (str):
                The name of the input function, defaulte x
            var (str):
                The independent variable of the ODEs, default t
        
        Attributes:
            laplace_transform_out (sympy expression):
                The laplace transform of the output equation
            laplace_transform_in (sympy expression):
                The laplace transform of the input equation
            transfer_func (sympy expression):
                The calculated transfer function H(s)
            num (sympy expression):
                This is the numerator of the transfer function
            den (sympy expression):
                The denominator of the transfer functions
            zeros (list):
                The zeros of the transfer function, these are the roots of the
                numerator
            poles (list):
                The poles of the transfer function, these are the roots of the
                denominator
            
        """
        
        #Initalize string equations
        self.equation_out = equation_out
        self.equation_in = equation_in
        
        #Initialize function names
        self.name_out = name_out
        self.name_in = name_in
        
        #Initialize variable
        self.var = var
        
        #Initialize Laplace transforms
        self.lap_out = LaplaceHandler(self.equation_out, self.name_out, self.var)
        self.lap_in = LaplaceHandler(self.equation_in, self.name_in, self.var)
        
        #Initialize symbols and functions
        self.y = self.lap_out.name
        self.x = self.lap_in.name
        self.t = sp.Symbol(self.var)
        self.s = sp.Symbol('s')
        self.w = sp.Symbol('w')
        
        #Initialize Laplace functions
        self.Y = sp.Function(self.name_out.upper())(self.s)
        self.X = sp.Function(self.name_in.upper())(self.s)
        self.H = sp.Function('H')
        
        #Initialize laplace domain
        self.domain = True
        
        #Convert string equations
        self.out_func = DiffEq(self.equation_out, self.name_out, self.var).function
        self.in_func = DiffEq(self.equation_in, self.name_in, self.var).function
        
        #Compute Laplace transforms
        self.laplace_transform_out = self.lap_out.laplace_transform
        self.laplace_transform_in = self.lap_in.laplace_transform
        
        #Initialize transfer function
        self.transfer_func = self.compute_h()
        
        
        #Initialize poles and zeros
        self.num, self.den = sp.fraction(self.transfer_func)
        self.zeros, self.poles = self.compute_zeros_and_poles()
    
    def compute_h(self, print_eq=False):
        """
        Computes the transfer function H(s).
        
        This function subtracts the Laplace transformed equations from each
        other, sets the result equal to zero and solves for Y(s).
        Finally, H(s) is computed by dividing by X(s)
        
        Parameters:
            print_eq (bool):
                If True, prints the equation before solving, default False.
        Returns:
            Hs (sympy expression):
                The transfer function H(s).
        """
        eq = self.laplace_transform_out - self.laplace_transform_in
        if print_eq:
            sp.pprint(f"{eq} = 0")
        H = sp.solve(eq, self.Y)[0] #remove list
        Hs = H/self.X
        return Hs
    
    def compute_zeros_and_poles(self):
        """
        Computes the zeros and poles of the transfer function.
        
        Zeros are found by setting the numerator equal to 0, poles are found
        by setting the denominator equal to 0.
        
        Returns:
            list:
                zeros
                poles
        """
        zeros = sp.solve(self.num)
        poles = sp.solve(self.den)
        return zeros, poles
    
    def switch_domain(self):
        """
        Switches the domain of the transfer function between Laplace (s-domain)
        and Fourier (w-domain).
        
        Replace s with jw, Laplace-to-Fourier,
        or w with -js, Fourier-to-Laplace
        Returns:
            Sympy expression:
                The transfer function in the switched domain.
        """
        if self.domain:
            self.transfer_func = self.transfer_func.subs(self.s, (I*self.w)) #Laplace to Fourier
        elif not self.domain:
            self.transfer_func = self.transfer_func.subs((self.w), -I*self.s) #Fourier to Laplace
        self.domain = not self.domain
        return self.transfer_func
    
    def transfer_function_numeric(self):
        """
        Converts the symbolic transfer function into a numeric function.
        
        Ensures the function is in the Fourier domain before numeric substitution
        
        Returns:
            Function:
                A function that evaluates the transfer function at specified
                values of omega.
        """
        if self.domain: #Make sure to be in Fourier domain
            self.switch_domain()
        
        def H_numeric(omega):
            transfer_func = self.transfer_func.subs(self.w, omega) #Substitute w for numbers
            return transfer_func
        return H_numeric
    
    def calc_magnitude_and_phase(self, omega_range = np.logspace(-1,6,1000)):
        """
        Calculates the magnitude and phase of the transfer function over a
        given range of frequencies.
        
        The magnitude is expressed in decibels using:
            magnitude = 20 * log10(|H(jw)|)
        
        The phase is expressed in degrees using:
            phase = arctan(re(H)/im(H) * (180/pi))
        
        Parameter:
            omega_range:
                A range of frequencies, in rad/s, over which the magnitude and
                phase are computed.
                Default is logarithmically spaced range from 10^-1 to 10^6 with
                1000 points.
        
        Returns:
            lists:
                magnitude: The magnitude response in decibels
                phase: The phase response in degrees
        """
        H_numeric = self.transfer_function_numeric()
        
        magnitude = []
        phase = []
        
        for omega in omega_range:
            H = H_numeric(omega)
            magnitude.append(20 * np.log10(float(abs(H))))
            phase.append(cmath.phase(H) * (180/np.pi))
        return magnitude, phase
    
    def step_response(self):
        """
        Computes the step response of the system.
        
        Returns:
            y_in:
                The sympy expression for the input signal,
                this is the step function.
            y_out:
                The sympy expression for the output signal, this is calculated
                by multiplying the transfer function with the laplace transform
                of the input signal.
        """
        if not self.domain:
            self.switch_domain()
        
        lap_step_in = 1/self.s                           #Laplace transform of stepresponse input
        lap_step_out = self.transfer_func * lap_step_in       #Laplace transform of stepresponse output
        
        y_in = sp.inverse_laplace_transform(lap_step_in, self.s, self.t)
        y_out = sp.inverse_laplace_transform(lap_step_out, self.s, self.t)
        return y_in, y_out
    def close_loop(self):
        closed = self.transfer_func / (1 + self.transfer_func)
        return closed
    
    def __str__(self):
        """
        Returns a formatted string representation of the system.
        
        Displays the systems differential equation, its Laplace transform and
        the transfer function.
        """
        return f"ODE: {self.out_func} = {self.in_func} \n Laplace transform: {self.laplace_transform_out} = {self.laplace_transform_in} \n H(s) = {self.transfer_func}"

if __name__ == '__main__':
    string1 = "y''+1*y'+y"
    string2 = "x+x'"
        
    Trans = TransferFunction(string1, string2)
    print(Trans.transfer_func)