# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 10:58:43 2025

@author: 23066776
"""

import sympy as sp
import math
sp.init_printing()

class PDiffEq:
    """
    A class for handling partial differential equations (PDEs).
    This class allows users to enter a PDE in "extended" lagrange notation.
    This class assumes a function:
        y(t, x)
    The extended lagrange notation goes as follows:
        ∂y/∂t = f'
        ∂y/∂x = f.
        ∂2y/∂t2 = f''
        ∂2y/∂x2 = f..
        ∂2y/∂t∂x = f'.
    """
    def __init__(self, eq, name="y", var1="t", var2="x"):
        """
        Initializes the PDiffEq class.
        
        Parameters:
            eq (str):
                The equation which is to be converted.
            name (str):
                The name of the function in the equation.
            var1 (str):
                The first variable of the function.
            var2 (str):
                The second variable of the function.
        
        Attributes:
            eq:
                The input equation with whitespaces removed
            terms (list):
                A list containing individual terms of the equation.
                Terms are separated by the '+' operator.
            var1 (str):
                The first independent variable.
            var2 (str):
                The second independent variable
            t (sympy Symbol):
                Symbolic representation of the first independent variable.
            x (sympy Symbol):
                Symbolic representation of the second independent variable.
            name (str):
                The function name.
            y (sympy Function):
                Symbolic representation of the function dependend on 't'.
            tprims (list):
                A list indicating the order of derivatives to the first 
                variable in each term.
                See 'find_derivs()' for details.
            xprims (list):
                A list indicating the order of derivatives to the second 
                variable in each term.
            K (list):
                A list that contains the numerical coefficients of each term.
            E (list):
                A list that contains the numerical exponents of each term.
            function (sympy expression):
                The final converted differential equation as a sympy expression.
        """
        self.eq = eq.replace(" ", "")
        
        self.var1 = var1.lower()
        self.var2 = var2.lower()
        self.name = name.lower()
        
        self.t = sp.Symbol(var1)
        self.x = sp.Symbol(var2)
        self.y = sp.Function(self.name)(self.t, self.x)
        
        self.terms = self.eq.split("+")
        
        self.tprims, self.xprims = self.find_derivs()
        
        self.K, self.E = self.find_factors()
        
        self.equ = self.make_equation()
        self.function = sum(self.equ)
    
    def find_derivs(self):
        """
        A function to find the derivatives to the variables in the given
        equation.
        Returns:
            tprims (list):
                A list containing the derivatives to t for each term.
            xprims (list):
                A list containing the derivatives to x for each term.
        """
        tprims = []
        xprims = []
        
        for term in self.terms:
            tcount = term.count("'")
            xcount = term.count(".")
            
            if (self.name in term):
                if tcount != 0 or xcount != 0:
                    tval = tcount if tcount != 0 else "A"
                    xval = xcount if xcount != 0 else "A"
                else:
                    tval = xval = "A"
                    
            else:
                if tcount != 0 or xcount != 0:
                    raise ValueError
                tval = xval = 0
            tprims.append(tval)
            xprims.append(xval)
        return tprims, xprims
    
    def find_factors(self):
        """
        Find the numerical factors and exponents of each term in the equation.
        
        Returns:
            Ks (list):
                A list with the numerical factor of each term.
            es (list):
                A list with the numerical exponent of each term
        """
        fact = []
        exps = []
        for term in self.terms:
            i = term.split("*")
            sub_l = []
            exp = []
            for char in i:
                if "^" in char:
                    j = char.split("^")
                    for m in j:
                        try:
                            e = int(m)
                            exp.append(e)
                        except ValueError:
                            exp.append(1)
                try:
                    f = int(char)
                    sub_l.append(f)
                except ValueError:
                    if "-" in char:
                        sub_l.append(-1)
                    else:
                        sub_l.append(1)
            fact.append(sub_l)
            exps.append(exp)
            Ks = [math.prod(sub) for sub in fact]
            es = [math.prod(sub) for sub in exps]
        return Ks, es
    
    def make_equation(self):
        """
        Build the PDE from the derivatives, factors and exponents.
        """
        equ = []
        for K, Yt, Yx, T, E in zip(self.K, self.tprims, self.xprims, self.terms, self.E):
            if Yt == "A" and Yx == "A":
                term = K * self.y**E
            elif (Yt != "A" and Yt > 0) and (Yx != "A"and Yx > 0):
                term = K * sp.diff(self.y, self.t, Yt, self.x, Yx)**E
            elif (Yt != "A" and Yt > 0) or (Yx != "A" and Yx > 0):
                term = K * sp.diff(self.y, self.t, Yt if (Yt != "A" and Yt > 0) else 0, self.x, Yx if (Yx != "A" and Yx > 0) else 0)
            else:
                term = sp.sympify(T)
            equ.append(term)
        return equ

if __name__ == "__main__":
    sting = "y.'+y'+y.+3*t+y"
    a = PDiffEq(sting)
    a.function