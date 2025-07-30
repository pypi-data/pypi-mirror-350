"""lkfit - a Python library for fitting.

This module contains gaussian fitting and plotting routines.

Copyright 2015-2025 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize
from scipy.ndimage.measurements import center_of_mass

from lkcom.util import find_closest, extend_range, get_color
from lkcom.standard_func import gaussian_1D, gaussian_1D_arglist, \
    plot_gaussian_1D_arglist, gaussian_2D, gaussian_2D_lambda, gaussian_2D_rot_lambda
from lkcom.plot import add_y_marker, plot_ellipse

from skimage.morphology import area_opening
from skimage.measure import label, regionprops


def fit_gaussian_1d(
        X, Y, fixed_a=None, fixed_y0=None, plot=False,
        y_scale='lin', main_axes=None, res_axes=None, y_axis_pos='left',
        center_z_axis_in_plot=False, xlim=None, show_y_zero_marker=True,
        plot_residuals=False, plot_fwhm=False, xlabel=None, ylabel=None):
    """Fit data to a 1D gaussian."""
    try:
        num_plot_pts = 1000
        if X is None:
            X = np.arange(Y.size)

        y0_g = np.min(Y)
        c_g = X[np.argmax(Y)]
        A_g = np.max(Y) - y0_g

        c_ind = find_closest(Y, A_g + y0_g)

        if c_ind > 1 and c_ind < len(Y)-1:
            w1_ind = find_closest(Y[0:c_ind], A_g/2 + y0_g)
            w2_ind = find_closest(Y[c_ind:-1], A_g/2 + y0_g) + c_ind
            w_g = abs(X[w2_ind] - X[w1_ind])
        else:
            w_g = (np.max(X) - np.min(X))/3
    except Exception:
        print("Fitting failed")
        fit_result = None

    try:
        if fixed_a is not None:
            if fixed_y0 is not None:
                def fit_func(x, w, c):
                    return gaussian_1D(x, A=fixed_a, w=w, c=c, y0=fixed_y0)
                p0 = [w_g, c_g]
            else:
                def fit_func(x, w, c, y0):
                    return gaussian_1D(x, A=fixed_a, w=w, c=c, y0=y0)
                p0 = [w_g, c_g, y0_g]
        else:
            if fixed_y0 is not None:
                def fit_func(x, w, c):
                    return gaussian_1D(x, A, w, c, y0=fixed_y0)
                p0 = [A_g, w_g, c_g]
            else:
                def fit_func(x, A, w, c, y0):
                    return gaussian_1D(x, A, w, c, y0)
                p0 = [A_g, w_g, c_g, y0_g]

        fit_result = optimize.curve_fit(fit_func, X, Y, p0=p0)[0]

        if fixed_a is not None:
            fit_result = np.append(fixed_a, fit_result)
        if fixed_y0 is not None:
            fit_result = np.append(fit_result, fixed_y0)
    except Exception as excpt:
        print("Fitting failed", excpt)
        plot = False
        fit_result = None

    if plot is True and fit_result is not None:
        if center_z_axis_in_plot:
            X = X - fit_result[2]
            fit_result[2] = 0

        if plot_residuals:
            res = Y - gaussian_1D_arglist(fit_result, X)
            if main_axes is None:
                grid = plt.GridSpec(5, 1, wspace=0.1, hspace=0.1)
                main_axes = plt.subplot(grid[0:4, :])
                res_axes = plt.subplot(grid[4, :])
        else:
            if main_axes is None:
                main_axes = plt.gca()

        if xlim is None:
            xlim = [np.min(X), np.max(X)]

        plt.sca(main_axes)
        if y_axis_pos == 'right':
            main_axes.yaxis.set_label_position("right")
            main_axes.yaxis.tick_right()

        if y_scale == 'lin':
            plt.ylim(extend_range([np.min(Y), np.max(Y)], 0.1))
            if show_y_zero_marker:
                add_y_marker(0, xlim=xlim, ls='-')
            plt.plot(X, Y, '.-', c=get_color('db'))
        elif y_scale == 'log':
            plt.semilogy(X, Y, '.-', c=get_color('db'))
        X_fit = np.linspace(min(X), max(X), num_plot_pts)

        plot_gaussian_1D_arglist(fit_result, X=X_fit, c=get_color('dr'))

        if plot_fwhm:
            w = fit_result[1]
            A = fit_result[0]
            y0 = fit_result[3]
            plt.draw()
            xl = plt.xlim()
            x_span = xl[1] - xl[0]
            plt.text(w/2+x_span*0.02, A/2+y0, '{:.2f} um'.format(w))

        if ylabel is not None:
            plt.ylabel(ylabel)

        plt.xlim(xlim)
        plt.grid('on')

        if plot_residuals:
            plt.tick_params(axis="x", which="both", bottom=False, top=False)
            plt.sca(res_axes)
            add_y_marker(0, xlim=xlim, ls='-')
            plt.plot(X, res, c=get_color('db'))
            plt.grid('on')
            plt.xlim(xlim)

        if xlabel is not None:
            plt.xlabel(xlabel)

    return fit_result


def plot_gaussian_1d_profile(X, A, width_txt_fmt="{:.2f}", xlim=None):
    """Fit and plot a 1D gaussian."""
    fr = fit_gaussian_1d(X, A, plot=True)
    if xlim is not None:
        plt.xlim(xlim)

    profile_amp = fr[0]
    profile_w = np.abs(fr[1])
    profile_c = fr[2]
    width_txt = width_txt_fmt.format(profile_w)
    plt.text(profile_c + profile_w, profile_amp/2, width_txt)

def est_gaussian_2p_par(
        data, roi_center_ref=None, roi_sz_ref=None, background_level=None,
        **kwargs):
    """Estimate 2D Gaussian parameters for fitting.

    Amplitude is taken as the maximum value of the data. Center is estimated by
    removing background to keep just the bright spots, then performing image
    opening with an area threshold of 9 pixels and taking the centroid of the
    remaining nonzero pixel region with the largest area. Width is then
    estimated from X and Y profiles through the center area.

    Center estimation is quite sensitive to spurious pixel values and image
    background. Specular reflections from screw heads and various edges seem to
    be particularly problematic as the main beam intensity goes down. If
    approximate beam center position and the ROI area where the beam should be
    located are known, e.g. from an image with a bright beam when scanning
    wavelength or intensity, the center and ROI diameter can be provided as
    roi center_ref and roi_sz_ref. Center estimation should then be robust
    against background interference.
    """
    A = data.max()

    # Remove background
    if background_level is None:
        br = int(data.shape[0]/5)
        bc = int(data.shape[1]/5)
        background_sample = data[0:br, 0:bc]
        background_mean = np.mean(data[0:br, 0:bc])
        background_max = np.max(data[0:br, 0:bc])
        background_std = np.std(data[0:br, 0:bc])
        background_level = background_mean + background_std*3

    if background_level > A:
        RuntimeWarning("Background level is above the maximum amplitude, " +
                       "fitting may be difficult.")

    # Suppress background
    data_b = data.copy()
    data_b[data_b < background_level] = 0

    X, Y = np.indices(data.shape)

    # The image might contain spurious bright areas that should be ignored when
    # estimating the center position. If the ROI center is not given, use
    # center of the image. If the ROI diameter is not given, use 50% of the
    # image.
    if roi_center_ref is not None:
        roi_center = roi_center_ref
    else:
        roi_center = np.array(data.shape)/2

    if roi_sz_ref is not None:
        roi_sz = roi_sz_ref
    else:
        roi_sz = np.min(data.shape)/2

    roi_sz = int(roi_sz)
    roi_ofs = (np.array(roi_center) - roi_sz/2).astype(int)

    roi = data[roi_ofs[0]:roi_ofs[0]+roi_sz,
               roi_ofs[1]:roi_ofs[1]+roi_sz]

    # Remove salt noise before thresholding
    roi = area_opening(roi, 9)

    # Threshold at three sigma above mean
    roi_mask = roi > np.mean(roi) + np.std(roi)*3

    # Remove small areas after thresholding
    roi_mask = area_opening(roi_mask, 9)

    rprops = regionprops(label(roi_mask))

    areas = []
    for rprop in rprops:
        if rprop.eccentricity < 0.8:
            areas.append(rprop.area)
        else:
            areas.append(0)

    if len(areas) > 0:
        [cy, cx] = rprops[np.argmax(areas)].centroid

        # Shift centroid from ROI coordinates to image coordinates
        cy += roi_ofs[0]
        cx += roi_ofs[1]
    else:
        if np.sum(roi_mask) > 0:
            print("Failed to isolate data center, trying ROI center of mass")
            [cy, cx] = center_of_mass(roi_mask)
            cy += roi_ofs[0]
            cx += roi_ofs[1]
        else:
            print("ROI contains no above-background data, trying global center"
                  " of mass")
            [cy, cx] = center_of_mass(data_b)


    # Find maximum xy position
    #[cy, cx] = np.unravel_index(np.argmax(data_b, axis=None), data_b.shape)
    # cx = (X*data_b).sum()/total
    # cy = (Y*data_b).sum()/total

    # Get profiles at maximum xy position
    col = row = np.nan
    if not np.isnan(cy):
        col = data[int(cy), :]
    if not np.isnan(cx):
        row = data[:, int(cx)]

    sx = sy = None
    if np.isnan(col).all() or np.isnan(row).all():
        print("Could not find center point profile")
    elif col.sum() == 0 or row.sum() == 0:
        print("One of the profiles is all zeros, cannot estimate std. dev.")
    else:
        # Estimate by Gaussian fitting, this should always work. Fitter returns
        # FWHM, need to convert to sigma.
        fit_result = fit_gaussian_1d(np.arange(len(col)), col)
        if fit_result is not None:
            sx = fit_result[1]/np.sqrt(8*np.log(2))

        fit_result = fit_gaussian_1d(np.arange(len(row)), row)
        if fit_result is not None:
            sy = fit_result[1]/np.sqrt(8*np.log(2))

        # Estimate the width of the gaussian by by using a weighted std. dev.
        # where the data is the pixel index centered on the maximum
        # and the weights are the profile pixel values witht the background
        # subtracted
        # sy = DescrStatsW(np.arange(col.size)-cx, weights=col, ddof=0).std
        # sx = DescrStatsW(np.arange(row.size)-cy, weights=row, ddof=0).std

        # TODO: figured why the following old method worked for square pinhole
        # scan images
        # sx = np.sqrt(np.abs((np.arange(col.size)-cy)**2*col).sum()/col.sum())
        # sy = np.sqrt(np.abs((np.arange(row.size)-cx)**2*row).sum()/row.sum())

    # If profile std. dev. cannot be estimated, assume it is half the range
    if sx is None:
        sx = (np.max(X) - np.min(X))/2

    if sy is None:
        sy = (np.max(Y) - np.min(Y))/2

    return [A, cy, cx, sy, sx, 0]


def fit_gaussian_2d(
        data, X=None, Y=None, fit_rotation=False, pxsz=1,
        return_fwhm=False, return_xy_order=False, w_txt_fmt="%.2f", plot=False,
        plot_width=None, suptitle_str=None, pause_on_plot=False, crop_area=None,
        crop_to_fit_region=False, square_crop=True, dbg_plot=False,
        with_sz_ellipse=False,
        use_physical_scale_for_images=False, **kwargs):
    """Fit a 2D gaussian.

    Args:
        data (2D array): Data to fit to.
        X (1D array): X axis values at which the data is sampled.
        Y (1D array): Y axis values at which the data is sampled.
        fit_rotation (bool): Fit with a rotating Gaussian.
        pxsz (int): Physical array pixel size in microns.
        return_fwhm (bool): Return width as FWHM if true, otherwise return
            sigma.
        return_xy_order (bool): Return center position and width in xy order if
            true, otherwise return in row-major ij order.
        w_txt_fmt (str): Gaussian width reporting text format.
        plot (bool): Make a fit result figure.
        plot_width (bool): Show width in the plot.
        suptitle_str (str): String to add to the suptitle of the plot.
        pause_on_plot (bool): Pause when plotting is completed before
            returning.
        crop_area (4-tuple): Area to crop the image to (left, top, right,
            bottom).
        crop_to_fit_region (bool): Crop the image to an area centered around
            the fit center position.
        square_crop (bool): Make the crop area square.
        use_physical_scale_for_images (bool): Use micrometers instead of pixels
            when cropping.

    Returns:
        Fit parameter array: [A, c1, c2, w1, w2, y0, theta]
        1 and 2 are x and y if return_xy_order is True, otherwise 1 and 2 are
        i and j. w is FWHM if return_fwhm is true, otherwise it is sigma.
    """
    if dbg_plot:
        plot = True
        with_sz_ellipse = True

    if crop_to_fit_region:
        guess_p = est_gaussian_2p_par(data, **kwargs)

    if kwargs.get('roi_sz_ref'):
        roi_sz = kwargs.get('roi_sz_ref')
        roi_center = kwargs.get('roi_center_ref')
        crop_area = np.array([roi_center[1] - roi_sz/2, roi_center[1] + roi_sz/2, roi_center[0] - roi_sz/2, roi_center[0] + roi_sz/2]).astype(int)

    crop_ofs = (0, 0)
    X = np.arange(0, data.shape[1])*pxsz
    Y = np.arange(0, data.shape[0])*pxsz
    if crop_area is not None or crop_to_fit_region:
        if crop_area is not None:
            # TODO: verify crop extent
            crop_x_from = crop_area[0]
            crop_x_to = crop_area[1]
            crop_y_from = crop_area[2]
            crop_y_to = crop_area[3]
        elif crop_to_fit_region:
            if square_crop:
                crop_sz = 3*np.mean(guess_p[3:5])
                crop_x_from = int(np.floor(guess_p[2] - crop_sz))
                crop_y_from = int(np.floor(guess_p[1] - crop_sz))
                crop_x_to = int(np.ceil(guess_p[2] + crop_sz))
                crop_y_to = int(np.ceil(guess_p[1] + crop_sz))
            else:
                crop_x_from = int(np.floor(guess_p[2] - 3*guess_p[4]))
                crop_y_from = int(np.floor(guess_p[1] - 3*guess_p[3]))
                crop_x_to = int(np.ceil(guess_p[2] + 3*guess_p[4]))
                crop_y_to = int(np.ceil(guess_p[1] + 3*guess_p[3]))

        crop_ofs = (crop_y_from, crop_x_from)
        if crop_to_fit_region:
            guess_p[1:3] = np.subtract(guess_p[1:3], crop_ofs)

        if crop_x_from < 0:
            crop_x_from = 0
        if crop_y_from < 0:
            crop_y_from = 0
        if crop_x_to > data.shape[1]:
            crop_x_to = data.shape[1]
        if crop_y_to > data.shape[0]:
            crop_y_to = data.shape[0]
        I_orig = data
        data = data[crop_y_from:crop_y_to, crop_x_from:crop_x_to]
        Y_crop = Y[crop_y_from:crop_y_to]
        X_crop = X[crop_x_from:crop_x_to]

        guess_p = est_gaussian_2p_par(data)
    else:
        X_crop = X
        Y_crop = Y
        guess_p = est_gaussian_2p_par(data)

    plot_guess = False
    if plot_guess:
        plt.imshow(gaussian_2D(
            data.shape, A=guess_p[0], c=guess_p[1:3], sigma=guess_p[3:5],
            y0=guess_p[5]))
        if plot_width is not None:
            plt.xlim(plot_width[0] + guess_p[1])
            plt.ylim(plot_width[1] + guess_p[2])
        plt.show()

    def errorfunction(p):
        return np.ravel(gaussian_2D_lambda(*p)(*np.indices(data.shape))
                        - data)

    # Debug plot: data and guess before fitting:
    # plt.clf(); plt.subplot(1, 2, 1); plt.imshow(data); plt.subplot(1, 2, 2); plt.imshow(gaussian_2D_lambda(*guess_p)(*np.indices(data.shape))); plt.show()

    p, success = optimize.leastsq(errorfunction, guess_p)

    # Debug plot: data, guess and result after fitting
    # plt.clf(); plt.subplot(1, 3, 1); plt.imshow(data); plt.subplot(1, 3, 2); plt.imshow(gaussian_2D_lambda(*guess_p)(*np.indices(data.shape))); plt.subplot(1, 3, 3); plt.imshow(gaussian_2D_lambda(*p)(*np.indices(data.shape))); plt.show()

    if fit_rotation:
        def errorfunction(p):
            return np.ravel(gaussian_2D_rot_lambda(*p)(*np.indices(data.shape))
                     - data)

        p, success = optimize.leastsq(errorfunction, np.append(p, 0))

    A = p[0]
    cy = p[1]
    cx = p[2]
    sy = p[3]*pxsz
    if sy < 0:
        p[3] = -p[3]
        sy = p[3]*pxsz
    sx = p[4]*pxsz
    if sx < 0:
        p[4] = -p[4]
        sx = p[4]*pxsz
    y0 = p[5]

    # Check whether the fit center is at least 2*sigma away from the edges
    # TODO: Would be good to also return these warnings and a fit unreliable
    #   flag. This can be done when the output type dict and not an array.
    if cx < 2*sx:
        print("WARNING: Fit center is too close to the left edge")
    if cx > data.shape[1] - 2*sx:
        print("WARNING: Fit center is too close to the right edge")
    if cy < 2*sy:
        print("WARNING: Fit center is too close to the top edge")
    if cy > data.shape[0] - 2*sy:
        print("WARNING: Fit center is too close to the bottom edge")

    # Center values in the true camera coordinate frame
    cx_true = cx + crop_ofs[1]
    cy_true = cy + crop_ofs[0]
    cy_um = cy_true*pxsz
    cx_um = cx_true*pxsz

    if fit_rotation:
        theta = p[6]
        # Unwind theta angle. The Gaussian rotation period is 180 deg.
        # Subtract a whole number of periods leaving a negative or positive
        # final theta value, whose magnitude is less than pi.
        theta -= np.sign(theta)*np.round(np.abs(theta/np.pi))*np.pi
        theta_deg = theta/np.pi*180
    else:
        theta = 0

    wx = sx*np.sqrt(8*np.log(2))
    wy = sy*np.sqrt(8*np.log(2))

    if plot:
        print("2D gaussian fit parameters:")
        print("\tA = {:.3f}".format(A))
        print("\tC X = {:.3f}".format(cx_um))
        print("\tC Y =  {:.3f}".format(cy_um))
        print("\tFWHM X  {:.3f}".format(wx))
        print("\tFWHM Y  {:.3f}".format(wy))
        print("\ty0 =  {:.3f}".format(y0))
        if fit_rotation:
            print("\ttheta =  {:.2f} deg".format(theta_deg))

        plt.clf()
        if plot_width is not None:
            profile_xlim = [cx_um - plot_width[0]/2, cx_um + plot_width[0]/2]
            profile_ylim = [cy_um - plot_width[1]/2, cy_um + plot_width[1]/2]
        else:
            profile_xlim = [np.min(X_crop), np.max(X_crop)]
            profile_ylim = [np.min(Y_crop), np.max(Y_crop)]

        if use_physical_scale_for_images:
            extent = [crop_ofs[1]*pxsz, (data.shape[1]+crop_ofs[1])*pxsz,
                      crop_ofs[0]*pxsz, (data.shape[0]+crop_ofs[0])*pxsz]
            center_point = [cx_um, cy_um]
            image_xlim = profile_xlim
            image_ylim = profile_ylim
        else:
            extent = None
            center_point = [cx, cy]
            if plot_width is not None:
                image_xlim = [cx - plot_width[0]/pxsz/2,
                              cx + plot_width[0]/pxsz/2]
                image_ylim = [cy - plot_width[1]/pxsz/2,
                              cy + plot_width[1]/pxsz/2]
            else:
                image_xlim = [cx - np.min(X_crop), cx + np.min(X_crop)]
                image_ylim = [cy - np.min(Y_crop), cy + np.min(Y_crop)]

        plt.subplot(2, 2, 1)
        plt.imshow(data, extent=extent)
        plt.plot(center_point[0], center_point[1], '*r')
        if plot_width is not None:
            plt.xlim(image_xlim)
            plt.ylim(image_ylim)
        plt.title("Data")

        if with_sz_ellipse:
            plot_ellipse([cx, cy], [2*wx, 2*wy], 0, c='w')

        plt.subplot(2, 2, 2)
        # TODO: No idea why theta needs to have the opposite sign here for the
        # orientation to look correct
        If = gaussian_2D(data.shape, A=p[0], c=p[1:3], sigma=[p[4], p[3]],
                         y0=p[5], theta=-theta)
        plt.imshow(If, extent=extent)
        plt.plot(center_point[0], center_point[1], '*r')
        if plot_width is not None:
            plt.xlim(image_xlim)
            plt.ylim(image_ylim)
        plt.title("Fit")

        plt.subplot(2, 2, 3)
        if cx >= 0 and cx < data.shape[1]:
            plot_gaussian_1d_profile(Y_crop, data[:, int(cx)],
                                     xlim=profile_ylim)
            plt.title("X Profile")
        else:
            print("WARNING: Center point outside of image")

        plt.subplot(2, 2, 4)
        if cy >= 0 and cy < data.shape[0]:
            plot_gaussian_1d_profile(X_crop, data[int(cy), :],
                                     xlim=profile_xlim)
            plt.title("Y Profile")
        else:
            print("WARNING: Center point outside of image")

        plt.gcf().set_size_inches(10, 10)

        plt.gcf().suptitle(suptitle_str)

        if pause_on_plot:
            plt.show()
        else:
            plt.draw()

        if dbg_plot:
            plt.show()

    if return_fwhm:
        if return_xy_order:
            return [A, cx_um, cy_um, wx, wy, y0, theta]
        else:
            return [A, cy_um, cx_um, wy, wx, y0, theta]
    else:
        if return_xy_order:
            return [A, cx_um, cy_um, sx, sy, y0, theta]
        else:
            return [A, cy_um, cx_um, sy, sx, y0, theta]

