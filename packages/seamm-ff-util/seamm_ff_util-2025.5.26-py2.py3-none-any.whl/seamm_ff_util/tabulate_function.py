# -*- coding: utf-8 -*-

"""Functions for creating the input for LAMMPS tabulated potentials."""
import numpy as np

import sympy


def tabulate_angle(equation, values, derivative=None, step=0.2):
    """Return the angle, energy and force on a grid of points.

    Some angle terms might go to inifinity at precisely 0.0 degrees, so if the values
    include 'zero-shift' the first angle is set to that value during the calculation,
    but reset to 0.0 in the returned angles.

    Parameters
    ----------
    equation : str
        The symbolic equation as a string.
    values : {str: int or float}
        The values of the constants in the equation, indexex by the name
    derivative : str = None
        The equation for the derivative. If None, it will be derived if possible
    step : float = 0.2
        The step to us for the angle grid, in degrees.
    """
    npts = int(180 / step) + 1
    thetas = np.linspace(0, 180, num=npts)
    if "zero-shift" in values:
        thetas[0] += values.pop("zero-shift")

    symbols = [sympy.symbols(key) for key in values.keys()]
    Theta = sympy.symbols("Theta")
    symbols.append(Theta)
    eqn = sympy.parse_expr(equation)
    E = sympy.lambdify(symbols, eqn, "numpy")

    Es = E(**values, Theta=np.radians(thetas))
    if derivative is None:
        deqn = sympy.diff(eqn, Theta)
    else:
        deqn = sympy.parse_expr(derivative)
    dE = sympy.lambdify(symbols, deqn, "numpy")
    dEs = dE(**values, Theta=np.radians(thetas))

    # Undo any shift
    thetas[0] = 0.0

    # Note angle is degrees. dE is naturally in radians, so convert to degrees
    # Yeah ... it looks like we are converting to radians but that is correct!
    # need to divide by degrees/radian which means multiplying by radians.
    return thetas.tolist(), Es.tolist(), np.radians(dEs).tolist()
