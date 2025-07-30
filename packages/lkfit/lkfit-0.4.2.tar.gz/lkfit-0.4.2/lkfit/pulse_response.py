"""lkfit - a Python library for fitting

Copyright 2015-2024 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import numpy as np

def estimate_pulse_response(xarr, yarr):
    """Estimate pulse response with rise and fall times.

    The function estimates maximum amplitude, the x value at maximum amplitude,
    and the rise and fall times at 1/e.
    """
    ymax = np.max(yarr)
    ymax_ind = np.argmax(yarr)
    x0 = xarr[ymax_ind]

    # Interpolation only works for monotonically increasing data, so must clip
    # the date before one sample before max. No -1 is needed.
    xrise = np.interp(ymax*np.exp(-1), yarr[:ymax_ind], xarr[:ymax_ind])

    # Data must be flipped for interpolation to work on the falling edge. Here
    # +1 is required to go one sample after the maximum. This way the ambiguous
    # max point is not used neither for the rising nor the falling edge.
    # Note that the interpolation time is correct because the xarr is flipped
    # as well.
    xfall = np.interp(ymax*np.exp(-1), np.flipud(yarr[ymax_ind+1:]),
                      np.flipud(xarr[ymax_ind+1:]))

    # xrise and xfall times are absolute in the x axis. To get lifetimes we
    # count rise and fall from the maximum value time.
    tau0 = x0 - xrise
    tau1 = xfall - x0

    return {'ymax': ymax, 'x0': x0, 'tau0': tau0, 'tau1': tau1,
            'xrise': xrise, 'xfall': xfall}
