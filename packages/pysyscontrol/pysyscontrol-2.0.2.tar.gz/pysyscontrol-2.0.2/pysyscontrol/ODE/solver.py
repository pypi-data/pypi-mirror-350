# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 16:36:01 2025

@author: Shagedoorn1
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

class Solver:
    """
    A class for numerically solving first order ordinary differential equations.
    
    An ODE is entered as a string in Lagrange notation. The ODE is set to 0 and
    solved for the derivative of y. The result is lambdified and can be
    numerically solved.
    """
    def __init__(self, diff_eq, times, plot=False, dark_mode=False):
        """
        Initialize the solver class.
        
        Arguments:
            diff_eq (DiffEq):
                A DiffEq object, see Diffeq.py for details.
            times (list or tuple):
                A list or tuple with the start and stop time for the numeric
                solution.
            plot (bool):
                When True, a plot is made when the given equation is
                numerically solved, default False.
            dark_mode (bool):
                Only relevant if plot is True. When True, the plot made by the
                numerical solvers is in dark mode.
        Parameters:
            start (float):
                The start time of the numerical solvers.
            stop (float):
                The stop time of the numerical solvers.
            x0 (float):
                The initial condition of the ODE.
                
        """
        self.diff_eq = diff_eq
        self.times = times
        self.start = self.times[0]
        self.stop = self.times[1]
        self.plot = plot
        self.dark_mode = dark_mode
        self.eq = self.diff_eq.isolate()
        self.x0 = self.diff_eq.initial_conds()[0]
        self.time = [self.start]
        self.fig_size = (10,15)
        if self.dark_mode:
            self.line_width = 3
            self.color = 'magenta'
            self.font_size = 18
        else:
            self.line_width = 1.5
            self.color = 'black'
            self.font_size = 12
            
    
    def euler(self, n=200):
        """
        Solves the given ODE with the Euler method.
        
        Arguments:
            n (int):
                The amount of time steps over which the ODE is solved.
                Default 200.
        Returns:
            x (numpy array):
                An array containing the first order solution of the equation.
        """
        n = int(n)
        dt = (self.stop - self.start) / n
        x = np.zeros(n + 1)
        x[0] = self.x0
        t = self.start
        for i in range(1, n+1):
            x[i] = x[i-1] + dt * self.eq(t, x[i-1])
            t += dt
            self.time.append(t)
        if self.dark_mode:
            plt.style.use("dark_background")
        else:
            plt.style.use('default')
        if self.plot:
            plt.figure(figsize = self.fig_size)
            plt.title(f"${sp.latex(self.diff_eq.function)}$ = 0", fontsize = self.font_size)
            plt.plot(
                self.time,
                x,
                linewidth = self.line_width,
                label = "Euler",
                color = self.color,
                )
            plt.grid()
            plt.legend()
            plt.show()
        return x
    
    def RK2(self, n=200):
        """
        Solves the given ODE with the Runge Kutta 2 method.
        
        Arguments:
            n (int):
                The amount of time steps over which the ODE is solved.
                Default 200.
        Returns:
            x (numpy array):
                An array containing the second order solution of the equation.
        """
        dt = (self.stop - self.start) / n
        x = np.zeros(n + 1)
        x[0] = self.x0
        t = self.start
        for i in range(1, n+1):
            k1 = dt * self.eq(t, x[i-1])
            k2 = dt * self.eq(t + 0.5 * dt, x[i-1] + 0.5 * k1)
            x[i] = x[i-1] + k2
            t += dt
            self.time.append(t)
        if self.dark_mode:
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        if self.plot:
            plt.figure(figsize = self.fig_size)
            plt.title(f"${sp.latex(self.diff_eq.function)}$ = 0", fontsize = self.font_size)
            plt.plot(
                self.time,
                x,
                linewidth = self.line_width,
                label = "Runge Kutta 2",
                color = self.color,
                )
            plt.grid()
            plt.legend()
            plt.show()
        return x
        
    def RK4(self, n=200):
        """
        Solves the given ODE with the Runge Kutta 4 method.
        
        Arguments:
            n (int):
                The amount of time steps over which the ODE is solved.
                Default 200.
        Returns:
            x (numpy array):
                An array containing the fourth order solution of the equation.
        """
        dt = (self.stop - self.start) / n
        x = np.zeros(n + 1)
        x[0] = self.x0
        t = self.start
        for i in range(1, n+1):
            k1 = dt * self.eq(t, x[i-1])
            k2 = dt * self.eq(t + 0.5 * dt, x[i-1] + 0.5 * k1)
            k3 = dt * self.eq(t + 0.5 * dt, x[i-1] + 0.5 * k2)
            k4 = dt * self.eq(t + dt, x[i-1] + k3)
            x[i] = x[i-1] + (1/6) * (k1 + 2 * k2 + 2 * k3 + k4)
            t += dt
            self.time.append(t)
        if self.dark_mode:
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        if self.plot:
            plt.figure(figsize = self.fig_size)
            plt.title(f"${sp.latex(self.diff_eq.function)}$ = 0", fontsize = self.font_size)
            plt.plot(
                self.time,
                x,
                linewidth = self.line_width,
                label = "Runge Kutta 4",
                color = self.color,
                )
            plt.grid()
            plt.legend()
            plt.show()
        return x
        
if __name__ == "__main__":
    from ..Diffeq import DiffEq
    string = "y'+y"
    D = DiffEq(string, 'y')
    Solve = Solver(D, [0, 2], plot = True, dark_mode = True)
    #Solve.euler(10)
    #Solve.RK2(10)
    Solve.RK4(10)