import numpy as np

def softmin(a, b, alpha):
    """
    Smooth approximation of min(a, b) using softmin function.

    Parameters:
        a (float): first value
        b (float): second value
        alpha (float): smoothness parameter (larger alpha -> closer to min)

    Returns:
        float: softmin(a, b)
    """
    ea = np.exp(-alpha * a)
    eb = np.exp(-alpha * b)
    return (a * ea + b * eb) / (ea + eb)
