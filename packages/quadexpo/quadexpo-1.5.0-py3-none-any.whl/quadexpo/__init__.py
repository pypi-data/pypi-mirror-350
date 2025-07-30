import numpy as np
from scipy.integrate import quad

def quadexpo_function(a, b, c, k, x_min, x_max):
    def integrand(x):
        return a*x**2 + b*x + c * np.exp(-k*x)
    result, _ = quad(integrand, x_min, x_max)
    return result
