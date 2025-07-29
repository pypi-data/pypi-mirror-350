import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

class OneD_WaveFunction:
    """
    A class to represent a one dimensional quantum wave function.
    
    This class allows the user to define a potential energy function,
    compute eigenstates of the corresponding Hamiltonian using
    imaginary time evolution, and visualize the energy levels and
    wavefunctions.
    """
    def __init__(self, V_expr=None, x_max=5, N_grid=1000, hbar=1, m=1):
        """
        Initialize the one dimensional wave function.
        
        Parameters:
            V_expr (optional sp.Expression):
                The symbolic expression for the potential energy V(x).
                If None, defaults to a harmonic oscillator potential:
                            1      2
                    V(x) =  _ m * x
                            2
            x_max (optional float):
                Half the width of the spatial domain
            N_grid (optional int):
                The number of grid points
            hbar (optional float):
                Reduced Plancks constant (defaults to 1)
            m (optional float):
                particle mass (defaults to 1)
        """
        self.hbar = hbar
        self.m = m
        
        self.x_symb = sp.Symbol("x")        
        self.x = np.linspace(-x_max, x_max, N_grid)
        self.dx = self.x[1] - self.x[0]
        
        if V_expr is None:
            V_expr = 0.5 * m * self.x_symb**2
        
        self.V_expr = V_expr
        self.V_func = sp.lambdify(self.x_symb, V_expr, modules='numpy')
        self.V = self.V_func(self.x)
        
        self.states = []
        self.energies = []
        
        self.normalize = lambda psi: psi / (np.linalg.norm(psi) * np.sqrt(self.dx))
    
    def expected_energy(self, psi):
        """
        Calculate the expected energy for a given wavefunction.
        
        Parameters:
            psi (numpy array):
                A normalized wavefunction defined on the spatial grid.
                
            Returns:
                float:
                    The the expected energy value: ⟨ψ|H|ψ⟩
        """
        lap = -0.5 * (psi[:-2] - 2 * psi[1:-1] + psi[2:]) / self.dx**2
        T = np.sum(psi[1:-1] * lap) * self.dx
        V = np.sum(self.V[1:-1] * psi[1:-1]**2) * self.dx
        return T + V
    
    def orthogonalize(self, psi):
        """
        Orthogonalize the wavefunction against all previously computed states.
        
        Parameters:
            psi (numpy array):
                The wavefunction to be orthogonalized
        Returns:
            psi (numpy array):
                The orthogonalized wavefunction
        """
        for phi in self.states:
            psi -= np.sum(psi * phi) * self.dx * phi
        return psi
    
    def compute_states(self, N_levels=4, max_iter=10000, tol=1e-6):
        """
        Compute the lowest N energy eigenstates using imaginary time
        evolution.
        
        Parameters:
            N_levels (optional int):
                Number of eigenstates to compute
            max_iter (optional int):
                The maximum number of itterations before convergence
            tol (optional float):
                The convegence tolerance allowed for energy states.
        """
        self.states = []
        self.energies = []
        
        for n in range(N_levels):
            psi = np.exp(-self.x**2 / 2) * np.polynomial.hermite.hermval(self.x, [0]*n + [1])
            psi = self.normalize(psi)
            E = 0.5 + n
            
            for it in range(max_iter):
                lap = np.zeros_like(psi)
                lap[1:-1] = (psi[:-2] - 2*psi[1:-1] + psi[2:]) / self.dx**2
                psi_new = psi + self.dx**2 * ((self.V - E) * psi + 0.5 * lap)
                
                psi_new = self.orthogonalize(psi_new)
                psi_new = self.normalize(psi_new)
                
                E_new = self.expected_energy(psi_new)
                
                if abs(E_new - E) < tol:
                    print(f"Level {n} converged: E = {E_new:.6f} (in {it} iterations)")
                    self.states.append(psi_new.copy())
                    self.energies.append(E_new)
                    break

                # Sanity check: abort if energy goes off scale
                if E_new > 1000 or np.isnan(E_new):
                    print(f"Level {n} diverged or unstable (E = {E_new:.2e})")
                    break

                psi = psi_new
                E = E_new
            else:
                print(f"Level {n} did not converge after {max_iter} iterations.")
    
    def plot_states(self):
        """
        Plot all computed eigenstates and the potential energy curve
        
        Each state ψₙ(x) is vertically offset by its corresponding energy Eₙ
        """
        for n, (psi, E) in enumerate(zip(self.states, self.energies)):
            plt.plot(self.x, psi + E, label=f"n={n}, E={E:.3f}")
        plt.plot(self.x, self.V, 'k--', label=f"$V(x) = {sp.latex(self.V_expr)}$")
        plt.title("Eigenstates")
        plt.xlabel("x")
        plt.ylabel(r"$\psi(x) + E$")
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def get_state(self, n):
        """
        Retrieve the nth computed eigenstate and energy
        
        Parameters:
            n (int):
                Quantum number (index of the state to retrieve)
        
        Returns:
            x (numpy array):
                The spatial grid
            psi (numpy array):
                The nth wavefunction ψₙ(x)
            E (float):
                The energy Eₙ of the nth eigenstate
        """
        if n < len(self.states):
            return self.x, self.states[n], self.energies[n]
        else:
            raise IndexError("Requested quantum number exceeds computed levels.")
if __name__ == "__main__":
    x = sp.Symbol('x')
    V_expr = 0.5*x**2
    osc = OneD_WaveFunction(V_expr=V_expr, x_max=5)
    osc.compute_states(N_levels=4)
    osc.plot_states()
