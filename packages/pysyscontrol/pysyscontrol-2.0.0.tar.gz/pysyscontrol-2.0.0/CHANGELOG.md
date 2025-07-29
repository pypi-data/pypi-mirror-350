# Changelog

## [1.1.3] - 2025-03-20
- First correctly functioning release

## [1.2.0] - 2025-03-26
### Added
- Step response
- Nyquist diagram
### Changed
- Added a dark_mode option for the plots

## [1.2.5] - 2025-03-26
### Fixed
- Corrected a typo in pyproject.toml

## [1.3.0] - 2025-04-04
### Added
- Solver class including:
  - Euler
  - Runge Kutta 2
  - Runge Kutta 4
### Changed
- Diffeq now supports exponents.
Also, PySysControl now officially has requirements
## [1.3.1] - 2025-04-06
### Fixed
- Fixed error in DiffEq.find_factors() that incorrectly turned "t" into "t**2"
## [1.4.0] - 2025-04-10
### Added
- PDiffEq. DiffEqs brother for PDEs
## [1.5.0] - 2025-04-16
### Added
- TransferFunction can now compute the closed loop transfer function. Which is used for the nyquist plot
## [2.0.0] - 2025-05-23
### Added
- PDE:
  - TEM: Model Transverse Electro Magnetic Gaussian-Hermite modes
  - WaveFunc: Turn a desired function into a solution of the wave equation and animate it's propagation
  - OneD_WaveFunction: Solve the one dimensional Schrödinger equation for a given potential
- Quantum:
  - GRAPE: Visualize the GRadient Ascend Pulse Engineering algorithm
  - Grover: Use Grovers algorithm to find desired values in a given array or list. (Warning, based on probability, could be wrong). Also can search for maximum and minimum values.
### Changed
- Overhauled the file structure into subpackages:
  - ODE
  - PDE
  - Control
  - Quantum
- The step response in Control/Plotting is now animated to resemble an actual readout from an oscilloscope
## How to update
Run the folowing command to update:
- pip install --upgrade pysyscontrol
