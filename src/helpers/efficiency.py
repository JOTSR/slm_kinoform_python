#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:14:19 2024

@author: baraille
"""
import numpy as np 

          
def efficiency_calcul(app): 
      P, Q = app.hg_frame.get_values() 
      W = app.waist_frame.get_value() 
      try: 
          p, q, w = int(P), int(Q), int(W)
          K_mm = np.fft.ftt(app.canvas1.image)
          F_mm =np.fft.fft( app.canvas2.image)
          area = 1980 * 1020
          rms = RMS(F_mm,K_mm,area)
          E = efficiency(F_mm, K_mm, p, q, w)
          
          app.label_Eff.text = str(E)
          app.Label_RMS.text = str(rms)
      except ValueError:
          print("Please enter valid numerical values for the coefficients and parameters.")
          