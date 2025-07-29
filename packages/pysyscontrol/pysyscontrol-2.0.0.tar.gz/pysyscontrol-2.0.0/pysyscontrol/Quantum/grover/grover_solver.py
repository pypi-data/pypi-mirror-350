# -*- coding: utf-8 -*-
"""
Created on Wed May 14 01:51:34 2025

@author: Shagedoorn1
"""

import numpy as np
from .diffuser import diffuser
from .oracle import mark_single_state, mark_multiple_states
from .visualize import plot_probabilities

def normalize(state):
    return state / np.linalg.norm(state)

def create_uniform_state(n_qubits):
    return normalize(np.ones(n_qubits, dtype=complex))

def grover_iteration(state, O, D):
    return D @ (O @ state)

def grover_search(n_qubits, marked_index, iterations=None, verbose=False):
    state = create_uniform_state(n_qubits)
    O = mark_single_state(n_qubits, marked_index)
    D = diffuser(n_qubits)

    if iterations is None:
        iterations = int(np.floor(np.pi / 4 * np.sqrt(2 ** n_qubits)))

    for i in range(iterations):
        final_state = grover_iteration(state, O, D)
        if verbose:
            probs = np.abs(state) ** 2
            print(f"Iteration {i+1}: Prob = {probs[marked_index]:.4f} at index {marked_index}")
    probs = np.abs(state)**2
    print("\nFinal probabilities:")
    print(np.round(np.abs(state)**2, 4))
    plot_probabilities(probs)
    return state

def grover_search_array(data, target, iterations=None, verbose=False):
    N = len(data)
    indices = [i for i, val in enumerate(data) if val==target]
    
    if not indices:
        raise ValueError("Target not found in data")
    
    
    state = create_uniform_state(N)
    O = mark_multiple_states(int(np.log2(N)), indices)
    D = diffuser(int(np.log2(N)))
    
    if iterations == None:
        iterations = int(np.floor(np.pi / 4 * np.sqrt(N)))
    
    for i in range(iterations):
        state = grover_iteration(state, O, D)
        if verbose:
            prob = np.abs(state[indices[0]]) ** 2
            print(f"Iter {i+1}: prob @ index {indices[0]} = {prob:.4f}")
    probabilities = np.abs(state) ** 2
    probabilities /= probabilities.sum()
    
    chosen_index = np.random.choice(N, p=probabilities)
    
    if verbose:
        print(f"Chosen index sampled from distribution: {chosen_index} with prob {probabilities[chosen_index]:.4f}")
        
    return data[chosen_index], probabilities

if __name__ == "__main__":
    data = np.arange(0, 16)
    target = 3
    print(f"Target = {target}\n")
    chosen_value, probs = grover_search_array(data, target, verbose=False)
    ind = np.where(data == chosen_value)[0][0]
    print(f"Value chosen by Grover search: {chosen_value}\n")
    print(f"Probability of chosen value: {probs[ind]:.2%}\n")
    print(f"Correct: {target == chosen_value}")