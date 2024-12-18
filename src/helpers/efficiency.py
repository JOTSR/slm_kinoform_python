#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:14:19 2024

@author: baraille
"""
import numpy as np 
import src.compute as comp
from src.compute.draw import flatten
from src.helpers.ploting import create_saved_plot
from src.helpers.camera import imagecool
          
def efficiency_calcul(app): 
    P, Q = app.hg_frame.get_values()
    WX, WY = app.grating_frame.get_values()
    A, B = app.rect_frame.get_values()
    W = app.waist_frame.get_value()
      
    
    try: 
        p, q, wx, wy, a, b, w = int(P), int(Q), int(WX), int(WY), int(A), int(B), int(W)
        K_mn = flatten(create_saved_plot(p, q, w, wx, wy, a, b))
        F_mn = flatten(imagecool)
        area = 1980 * 1020
        rms = comp.RMS(F_mn,K_mn,area)
        E = comp.efficiency(F_mn, K_mn, p, q, w)
          
        app.label_Eff.text = str(E)
        app.Label_RMS.text = str(rms)
        
        def get_values_E(app):
            return app.E.get()
    except ValueError:
        print("Please enter valid numerical values for the coefficients and parameters.")
          