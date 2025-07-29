# -*- coding: utf-8 -*-
"""
Created on Tue May 13 15:23:40 2025

@author: Shagedoorn1
"""

import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter

class BlochSphere:
    
    def __init__(self):
        self.fig = plt.figure(figsize=(8,8))
        self.ax = self.fig.add_subplot(111, projection = "3d")
        self._setup_axes()
        self._draw_bloch_sphere()
    
    def _setup_axes(self):     
        lims = [-1.2, 1.2]
        self.ax.set_xlim(lims)
        self.ax.set_ylim(lims)
        self.ax.set_zlim(lims)
        
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
    
    def _draw_bloch_sphere(self):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax.plot_surface(x, y, z, color="lightblue", alpha=0.3)
    def state_to_bloch(self, state):
        x = 2 * np.real(state[0] * np.conj(state[1]))
        y = 2 * np.imag(state[0] * np.conj(state[1]))
        z = np.real(np.abs(state[0])**2 - np.abs(state[1])**2)
        return x, y, z
    
    def plot_vector(self, bloch_coords, color='r', label=''):
        x, y, z = bloch_coords
        return self.ax.quiver(0, 0, 0, x, y, z, color=color, arrow_length_ratio=0.1, label=label)
    
    def clear_vectors(self):
        for artist in self.ax.collections + self.ax.lines:
            artist.remove()
        
        
class BlochCircle:
    
    def __init__(self,):
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Z")
        self.ax.set_title("2D Bloch Circle (X-Z plane)")
    def _setup_axes(self):     
        lims = [-1.2, 1.2]
        self.ax.set_xlim(lims)
        self.ax.set_ylim(lims)
        
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
    def _draw_bloch_sphere(self):
        x = np.linspace(-1, 1, 1000)
        y = np.sqrt(1-x**2)
        plt.plot(x, y, color="Black")
        plt.plot(x,-y, color="Black")
        
    def state_to_bloch(self, state):
        x = 2 * np.real(state[0] * np.conj(state[1]))
        z = np.real(np.abs(state[0])**2 - np.abs(state[1])**2)
        return x, z

    def plot_vector(self, vec, color='r', label=''):
        x, z = vec
        self.ax.quiver(0, 0, x, z, angles='xy', scale_units='xy', scale=1, color=color, label=label)
    def clear_vectors(self):
        for artist in self.ax.collections + self.ax.lines:
            artist.remove()

def animate_bloch_evolution(system, psi0, target, controls, dt, steps, dimension=3):
    """
    Animates the quantum state evolution on the Bloch sphere or circle.
    system: Quantum system object with H(control) method
    psi0: Initial state vector
    controls: Array of control field values over time
    dt: Time step
    steps: Number of steps in the evolution
    """
    if dimension == 3:
        bloch = BlochSphere()
    elif dimension == 2:
        bloch = BlochCircle()
    else:
        raise ValueError("Dimension must be 2 or 3")
    
    # Time evolution: evolve the state for each control field
    psi = psi0
    states = [psi.copy()]
    
    for u in controls:
        H = system.H(u)
        U = expm(-1j * H * dt)  # Time evolution operator
        psi = U @ psi
        states.append(psi)
    
    bloch_vectors = [bloch.state_to_bloch(state) for state in states]
    initial_vec = bloch.state_to_bloch(psi0)
    final_vec = bloch.state_to_bloch(target)
    
    def update(frame):
        bloch.ax.cla()
        bloch._setup_axes()
        bloch._draw_bloch_sphere()
        
        bloch.plot_vector(initial_vec, color='black', label=r"$|\psi_0\rangle$")
        bloch.plot_vector(final_vec, color='blue', label=r'$|\psi_{target}\rangle$')
        
        bloch.plot_vector(bloch_vectors[frame], color='red', label=r"$|\psi\rangle$")
        bloch.ax.grid()
        bloch.ax.legend()
        
        
    ani = FuncAnimation(bloch.fig, update, frames=steps, interval=50, repeat=False)
    plt.show()
    ani.save("grape_alg.gif",writer=PillowWriter(fps=20))
    return ani