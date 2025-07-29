# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 09:04:02 2025

@author: SHagedoorn1
"""
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .transfer_function import TransferFunction
def bode_plot(transfer_function, omega_range=np.logspace(-1, 6, 1000), dark_mode=False):
    """
    Generate and display the Bode plot of the given system.
    
    A Bode plot consists of 2 subplots:
        1 magnitude (in decibels) vs frequency (in radians per second)
        2 phase (in degrees) vs frequency (in radians per second)
    
    Parameters:
        transfer_function (TransferFunction):
            A TransferFunction object, see transfer_function.py for details
        omega_range (numpy array):
            A range of frequencies for which the Bode plot is computed,
            default from 10^-1 to 10^6, with 1000 points.
        dark_mode (bool):
            When True, changes the color of the background and lines
            to dark mode. Default False.
    """
    magnitude, phase = transfer_function.calc_magnitude_and_phase(omega_range)
    fig_size = (10, 6)
    if dark_mode:
        plt.style.use("dark_background")
        line_width = 3
        font_size = 18
    else:
        line_width = 1.5
        font_size = 12
    
    plt.figure(figsize = fig_size)
    plt.subplot(2, 1, 1)
    plt.semilogx(omega_range, magnitude, linewidth=line_width, color='cyan' if dark_mode else 'black')
    plt.title("Bode plot", fontsize = font_size)
    plt.ylabel("Magnitude (dB)", fontsize = font_size)
    plt.axhline(linewidth=1, color='white' if dark_mode else 'black')
    plt.grid(True, which='both', linestyle="--", linewidth=0.7, color="gray" if dark_mode else 'black')
    
    plt.subplot(2, 1, 2)
    plt.semilogx(omega_range, phase, linewidth = line_width, color='magenta' if dark_mode else 'black')
    plt.ylabel("phase (deg)", fontsize = font_size)
    plt.xlabel("Frequency (rad/s)", fontsize = font_size)
    plt.axhline(linewidth=1, color='white' if dark_mode else 'black')
    plt.axhline(y=-90, linewidth=2, color='white' if dark_mode else 'black', linestyle="--")
    plt.grid(True, which="both", linestyle="--", linewidth=0.7, color='gray' if dark_mode else 'black')

def pz_map(transfer_function, dark_mode=False):
    """
    Generate and display the Pole-Zero map of the given system.
    
    The map shows the poles and zeros of the transfer function in the complex
    plane
        - Poles are marked with an "X"
        - Zeros are marked with an "O"
    
    Parameters:
        transfer_function (TransferFunction):
            The transfer_function object that represents the system,
            see transfer_function.py for details.
        dark_mode (bool):
            When True, changes the color of the background and lines
            to dark mode. Default False.
    
    """
    fig_size = (10, 6)
    poles = transfer_function.poles
    zeros = transfer_function.zeros
    i = 0
    j = 0
    reals = []
    comps = []
    if dark_mode:
        plt.style.use('dark_background')
        color = 'magenta'
        h_color = 'gray'
        g_color = 'white'
        font_size = 18
    else:
        color = 'black'
        h_color = 'black'
        g_color = 'black'
        font_size = 12
    plt.figure(figsize=fig_size)
    plt.title("Pole-Zero map")
    plt.scatter(
        [sp.re(p) for p in poles],
        [sp.im(p) for p in poles],
        marker = 'x',
        s = 500,
        color = color,
        label = 'poles')
    while i < len(zeros):
        reals.append(sp.re(zeros[i]))
        comps.append(sp.im(zeros[i]))
        i += 1
    plt.scatter(
        [sp.re(z) for z in zeros],
        [sp.im(z) for z in zeros],
        marker = "o",
        s = 500,
        edgecolors = color,
        facecolors = 'none',
        label = 'zeros')
    while j < len(poles):
        reals.append(sp.re(poles[j]))
        comps.append(sp.im(poles[j]))
        j += 1
    plt.xlim([float(min(reals)) - 1, float(max(reals)) + 1])
    plt.ylim([float(min(comps))-1, float(max(comps)) + 1])
    plt.axhline(linewidth=2, color=h_color)
    plt.axvline(linewidth=2, color=h_color)
    plt.xlabel(r"$\lambda$ re(s)", fontsize=font_size)
    plt.ylabel(r"$j \omega$ im(s)", fontsize=font_size)
    plt.legend(prop={'size': 15})
    plt.grid(True, which='both', linestyle="--", linewidth=0.7, color=g_color)
    plt.show()
    
def step_response(transfer_function, dark_mode=False):
    """
    Generate and animate the step response of the given system.
    
    The step response represents how a system reacts through time after a unit
    step signal is applied. A unit step has value 0 when t < 0 and
    value 1 when t > 0
    
    Parameters:
        transfer_function (TransferFunction):
            A TransferFunction object, see transfer_function.py for details
        dark_mode (bool):
            When True, changes the color of the background and lines
            to dark mode. Default False.
    Returns:
        anim:
            Animation, return statement is necessary to prevent the animation
            from being garbage collected.
    """
    fig_size = (10, 6)

    if dark_mode:
        plt.style.use('dark_background')
        l_color1 = 'magenta'
        l_color2 = 'pink'
        h_color = 'gray'
        g_color = 'white'
        font_size = 18
    else:
        plt.style.use("default")
        l_color1 = 'black'
        l_color2 = 'red'
        h_color = 'black'
        g_color = 'black'
        font_size = 12
    
    step_in, step_out = transfer_function.step_response()
    
    t = np.linspace(-1, 10, 1000)               #Start before step, end after stabilization
    
    step_in_num = np.array([float(step_in.subs(transfer_function.var, x).evalf()) for x in t])
    step_out_num = np.array([float(step_out.subs(transfer_function.var, x).evalf()) for x in t])
    
    fig, ax = plt.subplots(figsize=fig_size)
    fig.canvas.draw()
    
    ax.set_xlim((t[0], t[-1]))
    ax.set_ylim((float(min(step_out_num))-0.1,float(np.max(step_out_num))+0.1))
    
    ax.axhline(0, linewidth = 2, color = h_color)
    ax.axvline(0, linewidth = 2, color = h_color)
    
    ax.set_xlabel('$time$ [s]', fontsize = font_size)
    ax.set_ylabel('$y(t)$', fontsize = font_size)
    
    ax.grid(True, which='both', linestyle="--", linewidth=0.7, color=g_color)
    
    line_in, = ax.plot([], [], color = l_color1, linewidth = 3, label = '$y_{in}$')
    line_out, = ax.plot([], [], color = l_color2, linewidth = 3, label = '$y_{out}$')
    ax.legend(prop={'size': 15})
    
    def update(frame):
        line_in.set_data(t[:frame], step_in_num[:frame])
        line_out.set_data(t[:frame], step_out_num[:frame])
        return line_in, line_out
    
    anim = FuncAnimation(fig, update, frames=len(t), interval=10, blit=True, repeat = False)
    plt.show()
    return anim

def Nyquist(transfer_function, dark_mode=False):
    """
    Generate and display the Nyquist diagram of the closed loop transfer function of the given system.
    
    The Nyquist diagram is a graphic representation of the systems frequency
    response, plotted in the complex plane. It is used to determine the systems
    stability and performance.
    
    Parameters:
        transfer_function (TransferFunction):
            A TransferFunction object, see transfer_function.py for details
        dark_mode (bool):
            When True, changes the color of the background and lines
            to dark mode. Default False.
    """
    if dark_mode:
        plt.style.use('dark_background')
        l_color = 'magenta'
        h_color = 'gray'
        g_color = 'white'
        font_size = 18
    else:
        l_color = 'black'
        h_color = 'black'
        g_color = 'black'
        font_size = 12
    
    #Make sure to be in the Fourier domain
    if transfer_function.domain:
        transfer_function.switch_domain()
    func = sp.lambdify(transfer_function.w, transfer_function.close_loop(), 'numpy')
    
    omega_pos = np.logspace(-2, 5, 5000)
    omega_neg = -omega_pos[::-1]
    
    func_pos = func(omega_pos)
    func_neg = func(omega_neg)              #Account for negative frequencies
    
    func_vals = np.concatenate((func_neg, func_pos))
    
    func_re = np.real(func_vals)
    func_im = np.imag(func_vals)
    
    plt.plot(func_re, func_im, color=l_color, linewidth = 3)
    
    plt.axhline(linewidth=2, color=h_color)
    plt.axvline(linewidth=2, color=h_color)
    
    plt.xlabel("$re(H)$", fontsize=font_size)
    plt.ylabel("$im(H)$", fontsize=font_size)
    
    plt.grid(True, which='both', linestyle="--", linewidth=0.7, color=g_color)
    
    plt.show()
    

if __name__ == "__main__":
    string1 = "y''+y'+y"
    string2 = "x'+x"
    o_range = np.logspace(-1,3,1000)
    Trans = TransferFunction(string1, string2)
    #bode_plot(Trans, np.logspace(-1,3,1000), True)
    #pz_map(Trans, True)
    #a = step_response(Trans, dark_mode=False)
    Nyquist(Trans, True)