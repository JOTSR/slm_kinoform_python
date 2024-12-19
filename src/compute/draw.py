import numpy as np
from scipy.special import hermite
import math 

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

#fonction calcul RMS 

def RMS(F_mn,K_mn,area):
    rms = (np.mean((np.abs(np.fft.fft(F_mn) - np.fft.fft(K_mn)) ** 2)/area/255))
    return np.sqrt(rms)


#fonction calcul de l'efficacité  

def efficiency (F_mn,K_mn,p,q,w):
    C= 2**(p+q)*math.factorial(p)*math.factorial(q)*np.pi*w**2/2
    A = (1/C)*np.sum(K_mn*F_mn)
    eff=A**2*np.sum(F_mn**2)/np.sum(K_mn**2)
    return eff

#fonction d'applatissment des arrays d'arrays

def flatten(xss):
    return [x for xs in xss for x in xs]
