# -*- coding: utf-8 -*-
"""
Created on Wed May 14 01:51:44 2025

@author: Shagedoorn1
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_probabilities(state, title="Grover State Amplitudes"):
    probs = np.abs(state) ** 2
    n_states = len(probs)
    states = [f"|{i:0{int(np.log2(n_states))}b}⟩" for i in range(n_states)]
    
    plt.figure(figsize=(10, 5))
    plt.bar(states, probs, color='skyblue')
    plt.title(title)
    plt.ylabel("Probability")
    plt.xlabel("Basis state")
    plt.ylim(0, 1)
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.show()