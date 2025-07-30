"""lkfit - a Python library for fitting.

This module contains plotting routines for polynomial fitting.

Copyright 2015-2022 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

from lkcom.standard_func import poly_2


def fit_poly_2(X=None, Y=None, plot=False, plot_fit=False, color=None):
    if len(X) < 3:
        raise ValueError("Insufficient number of points to fit a poly-2")
    if color is None:
        color = 'r'

    popt, pcov = optimize.curve_fit(poly_2, X, Y, p0=[-1, 0, 0])

    if(plot):
        plt.plot(X, Y, '.')

    if(plot or plot_fit):
        X_fit = np.linspace(min(X), max(X), 1000)
        plt.plot(X_fit, poly_2(X_fit, popt[0], popt[1], popt[2]),
                 c=color, ls='-')
        plt.draw()

    return [popt, pcov]


def get_poly_2_max_x(k):
    return -k[1]/(2*k[0])
