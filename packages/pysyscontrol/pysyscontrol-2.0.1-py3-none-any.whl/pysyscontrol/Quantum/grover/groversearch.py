# -*- coding: utf-8 -*-
"""
Created on Fri May 16 12:10:16 2025

@author: Shagedoorn1
"""

import numpy as np
from .oracle import mark_multiple_states
from .diffuser import diffuser
from .grover_solver import grover_iteration

class GroverSearch:
    def __init__(self, data, target=None, iterations=None):
        self.original_data = np.array(data)
        self.original_length = len(self.original_data)

        
        self.N = 1 << (self.original_length - 1).bit_length()
        dummy_value = None
        pad_length = self.N - self.original_length
        if pad_length > 0:
            
            if self.original_data.dtype.kind in {'i','u','f'}:
                if self.original_data.dtype.kind == 'f':
                    dummy_value = np.nan
                else:
                    dummy_value = np.iinfo(self.original_data.dtype).max + 1
            else:
                dummy_value = object()
                
            self.data = np.concatenate([self.original_data, np.full(pad_length, dummy_value)])
        else:
            self.data = self.original_data.copy()

        self.n_qubits = int(np.log2(self.N))
        self.target = target
        self.target0 = target
        self.iterations = iterations or int(np.floor(np.pi / 4 * np.sqrt(self.N)))

    def _create_uniform_state(self):
        dim = 2 ** self.n_qubits
        state = np.ones(dim, dtype=complex) / np.sqrt(dim)
        return state

    def _get_indices_for_target(self):
        if self.target is None:
            raise ValueError("Target must be specified")

        indices = [i for i, val in enumerate(self.data) if val == self.target]
        if not indices:
            raise ValueError("Target not found in data")
        return indices

    def run(self, verbose=False):

        indices = self._get_indices_for_target()
        state = self._create_uniform_state()

        O = mark_multiple_states(self.n_qubits, indices)
        D = diffuser(self.n_qubits)

        for i in range(self.iterations):
            state = grover_iteration(state, O, D)
            if verbose:
                prob = np.abs(state[indices[0]]) ** 2
                print(f"Iter {i+1}: prob @ index {indices[0]} = {prob:.4f}")

        probabilities = np.abs(state) ** 2
        probabilities /= probabilities.sum()

        # Exclude padded indices when sampling
        valid_indices = list(range(self.original_length))
        probs_valid = probabilities[:self.original_length]
        probs_valid /= probs_valid.sum()

        chosen_index = np.random.choice(valid_indices, p=probs_valid)
        chosen_value = self.data[chosen_index]

        if verbose:
            print(f"Chosen index: {chosen_index}, value: {chosen_value}, prob: {probs_valid[chosen_index]:.4f}")

        return chosen_value, probs_valid
    def set_target(self, target):
        self.target = target
        self.oracle = mark_multiple_states(self.n_qubits,
                                           [i for i, val in enumerate(self.data) if val == target])
    def reset_target(self):
        self.target = self.target0
        self.orable = mark_multiple_states(self.n_qubits,
                                           [i for i, val in enumerate(self.data) if val == self.target])
    def grover_max(self):
        self.set_target(np.max(self.data))
        g_max,_ = self.run()
        return g_max
    
    def grover_min(self):
        self.set_target(np.min(self.data))
        g_min, _ = self.run()
        return g_min
    
    def search(self, target):
        self.set_target(target)
        g, _ = self.run()
        return g
    
    def search_given_target(self):
        self.reset_target()
        g, _ = self.run()
        return g
    
if __name__ == "__main__":
    data = np.array([10, 5, 30,4])  # length not power of two
    target = 5

    grover = GroverSearch(data, target, iterations=None)
    g_max = grover.grover_max()
    g_min = grover.grover_min()
    g = grover.search_given_target()
    print(g_max)
    print(g_min)
    print(g)