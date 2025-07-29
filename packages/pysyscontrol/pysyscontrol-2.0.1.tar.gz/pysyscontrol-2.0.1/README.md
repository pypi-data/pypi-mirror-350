# PySysControl
![PySysControl Logo](https://raw.githubusercontent.com/Shagedoorn1/PySysControl/main/Logo_svg.svg)

A python package to analyse control systems down from the governing differential equation.
The classes allow for the equations to be entered easily and intuitively. 

Guidelines for entering a differential equation:
  Use double quotes, Lagrange notation uses single quotes for derivatives
  For multiplication use an asterisk
  For subtraction use +-, as in 5+-3. (There is a mathematical reason why this is more correct than 5-3, but that's beside the point)
The above guidelines are also listed in the documentation.

The laplace_handler transforms the given equation from whatever domain it is defined on, which it is assumed to be the time-domain,
to the complex valued s-domain.

The transfer_function class converts the given differential equations to a transfer function in the s-domain, which can be switched to the w-domain.

The functions in plotting generate plots based on the given system. The available plots are the Bode plot, the Pole Zero Map, the Step response and the Nyquist plot. Dark mode is also available for the plots. 

The changelog of this package can be found in the github repository:
https://github.com/Shagedoorn1/PySysControl