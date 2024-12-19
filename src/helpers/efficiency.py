#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:14:19 2024

@author: baraille
"""
import numpy as np
import src.compute as comp
from src.compute.draw import flatten
from src.compute.draw import RMS
from src.compute.draw import efficiency
from src.helpers.ploting import create_plot

E = None


def resize_array(array, width, height):
    resized = []

    for h in range(0, height):
        row = []
        for w in range(0, width):
            row.append(array[h][w])
        resized.append(row)
    return resized


def efficiency_calcul(app):
    P, Q = app.hg_frame.get_values()
    WX, WY = app.grating_frame.get_values()
    A, B = app.rect_frame.get_values()
    W = app.waist_frame.get_value()

    try:
        p, q, wx, wy, a, b, w = int(P), int(Q), int(WX), int(WY), int(A), int(
            B), int(W)
        image_width = len(app.photo_latest[0])
        image_height = len(app.photo_latest)
        K_mn = create_plot(p, q, w, wx, wy, a, b)
        K_mn = resize_array(K_mn, image_width, image_height)
        K_mn = flatten(K_mn)
        F_mn = flatten(app.photo_latest)
        F_mn = [pixel[0]
                for pixel in F_mn]  # image is in rgb, only use one component
        area = image_width * image_height
        rms = RMS(F_mn, K_mn, area)
        E = efficiency(F_mn, K_mn, p, q, w)
        app.label_Eff.text = str(E)
        app.label_RMS.text = str(rms)

    except ValueError:
        print(
            "Please enter valid numerical values for the coefficients and parameters."
        )
