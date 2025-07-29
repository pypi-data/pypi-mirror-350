# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 17:18:16 2025

@author: Shagedoorn1
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
sp.init_printing()

class WaveFunc:
    """
    A class to represent a 1 dimensional wave function.
    It is initially defined as a variable and can be shaped into the
    desired wave function using arithmetic operations.
    
    A function is a wave function if it is a solution of the wave
    equation:
        ∂²f     ∂²f
        ___ = v²___
        ∂t²     ∂x²
    Any function f(p), where p=x-vt, is a solution of this equation.
    
    This class 'becomes' a function f(x) through arithmetic operations
    and becomes a wave
    """
    def __init__(self, var, v):
        """
        Initialize the wave function.
        
        Parameters:
            var (string):
                The name of the spatial dimension. Defaults to x
            v (int):
                The velocity of the wave.
        Attributes:
            self.x (sp.Symbol):
                The symbolic version of the var parameter
            self.expr (sp.Symbol):
                The body of the function f(x). This is modified through
                arithmetic operations.
            self.t (sp.Symbol):
                The symbol for the time dimension
        """
        self.var = var
        self.x = sp.Symbol(self.var)
        self.expr = self.x
        self.t = sp.Symbol("t")
        self.v = v
    
    def __iadd__(self, other):
        self.expr +=  other
        return self
    
    def __isub__(self, other):
        self.expr -= other
        return self
    
    def __imul__(self, other):
        self.expr *= other
        return self
    
    def __itruediv__(self, other):
        self.expr /= other
        return self
    
    def __add__(self, other):
        new = WaveFunc(self.var, self.v)
        new.expr = self.expr + other
        return new
    
    def __sub__(self, other):
        new = WaveFunc(self.var, self.v)
        new.expr = self.expr - other
        return new
    
    def __mul__(self, other):
        new = WaveFunc(self.var, self.v)
        new.expr = self.expr * other
        return new
    
    def __truediv__(self, other):
        new = WaveFunc(self.var, self.v)
        new.expr = self.expr / other
        return new
    
    @property
    def wav(self):
        """
        Turn the given function into a wave function with the substitution
        x -> x - vt
        Returns:
            wave (property):
                Wave function form of the function
        """
        wav = self.expr.subs(self.x, self.x - self.v*self.t)
        return wav
    
    def animate(self, dark_mode = False):
        """
        Animate the propegation of the wave.
        
        Parameters:
            dark_mode (bool):
                Make the plot in dark mode
        Returns:
            ani (animation):
                This prevents the animation from being garbage
                collected before it renders.
        """
        if dark_mode:
            plt.style.use("dark_background")
            width = 5
            l_color="magenta"
        else:
            plt.style.use("default")
            width = 2
            l_color="black"
        w_func = sp.lambdify([self.x,self.t],self.wav, modules=["numpy"])
        
        space = np.linspace(-1, 1, 200)
        time = np.linspace(-1,1,200)
        mesh_x, mesh_t = np.meshgrid(space, time)
        values = w_func(mesh_x, mesh_t)
        
        y_min, y_max = np.min(values), np.max(values)
        
        fig, ax = plt.subplots(figsize=(8,8))
        line, = ax.plot([], [], lw=width, color=l_color)
        ax.set_xlim(space[0], space[-1])
        ax.set_ylim(y_min - 0.1, y_max + 0.1)  # adjust as needed
        ax.set_title("Wave Propagation")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$f(x, t)$")
        ax.grid()

        # Init function
        def init():
            line.set_data([], [])
            return line,

        # Animation function
        def animate(i):
            y = w_func(space, time[i])
            line.set_data(space, y)
            return line,
        
        interval = max(1, int(100 / abs(self.v)))
        ani = FuncAnimation(
            fig, animate, frames=len(time), init_func=init,
                            blit=True, interval=interval
            )  # interval in milliseconds
        plt.show()
        return ani
if __name__ == "__main__":
    x = sp.Symbol("x")
    wave = WaveFunc("x", 3)
    
    wave *= sp.exp(-x**2)
    wave /= x
    ani =wave.animate(dark_mode=True)