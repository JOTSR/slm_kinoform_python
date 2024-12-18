import numpy as np
from scipy.special import hermite

def grating(wx, wy):
    Max = 2 * np.pi
    two_pi = 2 * np.pi
    Cx = (256 / wx) * (Max / two_pi)
    Cy = (256 / wy) * (Max / two_pi)
    return lambda x, y: ((x % wx) * Cx + (y % wy) * Cy) % 256

def kinoform(p, q, w):
    H_p = hermite(p)
    H_q = hermite(q)
    factor = np.sqrt(2) / w
    w2 = w ** 2
    return lambda x, y: 127 if H_p(x * factor) * H_q(y * factor) * np.exp(-(x ** 2 + y ** 2) / w2) > 0 else 0

def rect(a, b):
    def pixels(x, y):
        if x < -a / 2 or y < -b / 2:
            return 0
        if x > a / 2 or y > b / 2:
            return 0
        return 1
    return pixels


