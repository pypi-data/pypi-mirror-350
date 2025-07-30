"""lkfit - a Python library for fitting.

This module contains various data processing routines.

Copyright 2015-2022 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import numpy as np
from scipy.ndimage.filters import uniform_filter1d


def find_peaks(arr, thr=0.1, win_sz=100):
    """Find peaks in noisy data by low-pass filtering."""
    arr = uniform_filter1d(arr, win_sz)
    peak_list = []
    while True:
        if np.max(arr) < thr:
            return peak_list
        ind = np.argmax(arr)
        peak_list.append(ind)
        arr[int(ind - win_sz):int(ind + win_sz)] = 0
