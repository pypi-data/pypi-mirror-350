# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 10:19:48 2025

@author: Shagedoorn1
"""

import sympy as sp
import math
sp.init_printing()

class DiffEq:
    """
    A class for handling ordinary differential equations (ODEs).
    This class allows users to enter a differential equation in Lagrange
    notation, the way it would be written on paper, and converts it into a
    symbolic sympy expression.
    
    Note:
        This class only supports non-mixed ODEs.
        If a mixed ODE is required, multiple instances of this class should
        be created.
    """  
    def __init__(self, eq, func, var='t'):
        """
        Initializes the DiffEq class.
        
        Parameters:
            eq (str):
                The differential equation as a string.
                For correct conversion, follow these rules:
                    1. The equation should be enclosed in double quotes.
                    2. Use an asterisk (*) for multiplication.
                    3. For subtraction, use '+-' 
            func (str):
                The name of the function in the differential equation.
                Example: In "y' = 5*y", y is the name.
            var (str):
                The independent variable with respect to which differentiation
                occurs, default t.
        
        Attributes:
            eq:
                The input equation with whitespaces removed
            terms (list):
                A list containing individual terms of the equation.
                Terms are separated by the '+' operator.
            var (str):
                The independent variable.
            t (sympy Symbol):
                Symbolic representation of the independent variable.
            func (str):
                The function name.
            y (sympy Function):
                Symbolic representation of the function dependend on 't'.
            derivatives (list):
                A list indicating the order of derivatives in each term.
                See 'find_derivs()' for details.
            order (int):
                The highest order derivative in the equation
            K (list):
                A list that containing the numerical coefficients of each term.
            function (sympy expression):
                The final converted differential equation as a sympy expression.
        """
        self.eq = eq.replace(" ", "")
        self.terms = self.sort_eq()
        self.var = var
        self.t = sp.Symbol(self.var)
        self.func = func
        self.y = sp.Function(self.func.lower())(self.t)
        self.derivatives = self.find_derivs()
        orders = [i for i in self.derivatives if isinstance(i, int)]
        self.order = max(orders, default=0)
        self.K, self.E = self.find_factors()
        self.function = sp.sympify(sum(self.make_equation())) #Sum and sympify all converted terms for the full expression
    
    def sort_eq(self):
        """
        Splits the equation into individual terms.
        
        The equation is split using the "+" operator.
        
        Returns:
            list:
                A list containing the seperated terms of the equation.
        """
        terms = self.eq.split("+")      #Split at the + operator
        return terms
    
    def find_derivs(self):
        """
        Identifies the order of the differentiation of each term in the
        equation.
        
        Creates a list where each elements represents the derivative order or
        presence of the function in the term.
        
        Returns:
            list:
                A list where each element can be:
                    - A nonzero integer: Represents the order of differentiation.
                    - The string 'A': Indicates the presence of the function
                    name
                    - zero (0): Indicates that the term does not contain the
                    function.
        
        Raises:
            VauleError:
                If a term contains a prime (`'`) but not the function name.
                This suggests an invalid derivative, likely due to a typo.
        
        """
        prims = []
        for n in self.terms:
            m = n.count("'")
            if m != 0 and self.func in n:
                d = m
            elif m != 0 and self.func not in n:
                raise ValueError
            elif m == 0 and self.func in n:
                d = 'A'
            elif m == 0 and self.func not in n:
                d = 0
            prims.append(d)
        return prims
    
    def find_factors(self):
        """
        Extract the numerical factors from each term in the equation.
        
        
        Returns:
            list:
                A list where each element represents the product of numerical
                factors in a corresponding term of the equation.
        
        Details:
            - If a character in a term is not a number, t or y, it is replaced
            with 1 to maintain multiplication consistency.
        """
        fact = []
        exps = []
        for term in self.terms:
            i = term.split('*')
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
                    if char == self.var:
                        sub_l.append(1)
                    else:
                        sub_l.append(1)
            fact.append(sub_l)
            exps.append(exp)
            Ks = [math.prod(sub) for sub in fact]
            es = [math.prod(sub) for sub in exps]
        return Ks, es
    
    def make_equation(self):
        """
        Converts the equation into a symbolic sympy expression.
        
        Returns:
            list:
                A list containing the sympy representation of
                each term in 'self.terms'.
        
        Details:
            -Iterates over 'self.K', 'self.derivatives' and 'self.terms' in
            parallel.
            -Converts each term into a properly formatted sympy expression
            -The final step to forming the full expression
            happens in '__init__'.
        """
        equ = []
        for K, Y, T, E in zip(self.K, self.derivatives, self.terms, self.E):
            if Y == 'A':
                term = K * self.y**E
            elif int(Y) > 0:
                term = K * sp.diff(self.y, self.t, Y)**E
            elif Y == 0:
                term = T
            if (self.func not in T) and (self.var not in T):
                term = T
            equ.append(sp.sympify(term))
        return equ
    
    def isolate(self):
        eq = sp.solve(self.function, sp.diff(self.y, self.t, self.order))[0]
        return sp.lambdify((self.t, self.y), eq)
    
    def initial_conds(self):
        conds = []
        for i in range(self.order):
            c = input(f"Initial value for {i}th oder derivative of {self.func}: ")
            conds.append(c)
        return conds
    
    def __str__(self):
        """
        Returns the converted differential equation as a string.
        
        When an instance of this class is printed, it displays the sympy
        expression of the equation.
        """
        return f'{self.function}'
            
                
if __name__ == '__main__':
    string = "5+t"
    a = DiffEq(string, 'y')
    print(a.function)