"""lkcom - a Python library of useful routines.

This module contains misc utilities. Many of these routines can probably be
replaced with better alternatives or even internal Python functions.

Copyright 2015-2025 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import os
import sys
import time
import datetime

import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pyplot import get_cmap


class MultiPrinter(object):
    def __init__(self, *targets):
        self.targets = targets

    def write(self, obj):
        for f in self.targets:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.targets:
            f.flush()


class LogPrinter(object):
    def __enter__(self):
        self.log_file = open("output.log", "w")
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        print("Copying stdout and stderr stream to 'output.log'...")
        sys.stdout = MultiPrinter(sys.stdout, self.log_file)
        sys.stderr = MultiPrinter(sys.stderr, self.log_file)

    def __exit__(self, exc_type, exc_value, traceback):
        self.log_file.close()
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        print("Restoring stdout and stderr streams to defaults...")


def get_spec_line(line):
    if line == 'd':
        return 0.58756
    elif line == 'C':
        return 0.65627
    elif line == 'F':
        return 0.48613
    else:
        return None


def isnone(var):
    """Test if a variable is None.

    Works for numpy arrays, returns a single boolean result even if the
    variable is an array of None.

    """
    if isarray(var):
        if type(var) == np.ndarray:
            return var.size == 0
        if isinstance(var, type([])):
            # Iterate over the list
            for v in var:
                # Call isnone recursively for each list element. This should
                # handle lists of lists
                if v is not None:
                    # If at least one element is not None, the list is not None
                    return False
            # If the loop finishes, all elements are none
            return True
        warning_with_info("Asked for isnone() for an unknown array type")

    if isinstance(var, type(None)):
        return True

    return False


def issmth(var):
    """
    Test if variable is something other than None. A logical negation version
    of isnone()
    """
    return (isnone(var) is False)


def isarray(var):
    """
    Test if varialbe is array. List is treated as an array, but a string
    is not.
    """
    if isinstance(var, type(list())) \
            or isinstance(var, np.ndarray):
        return True
    else:
        return False


def isstring(var):
    """
    Test if a variable is a string.
    """
    return isinstance(var, str)


def hex2byte(hex_val):
    """
    Convert a hex value to a byte array.
    """

    hex_len = len(hex_val)

    byte_val = np.ndarray(int(hex_len/2), dtype=int)

    for ind in range(0, len(hex_val), 2):
        byte_val[int(ind/2)] = int(hex_val[ind:ind + 2], 16)

    return byte_val


def select_roi(data, center, size):
    """Select a ROI in 2D data."""
    cx = center[1]
    cy = center[0]
    szx = size[1]/2
    szy = size[0]/2

    from_y = np.max([int(np.round(cy - szx)), 0])
    to_y = np.min([int(np.round(cy + szy)), data.shape[0]])
    from_x = np.max([int(np.round(cx - szx)), 0])
    to_x = np.min([int(np.round(cx + szy)), data.shape[0]])

    return data[from_y:to_y, from_x:to_x]


def byte2hex(byte_val):
    """
    Convert byte values to hex.
    """

    byte_len = len(byte_val)

    hex_val = ""

    for ind in range(0, byte_len):
        hex_val = hex_val + hex(int(round(byte_val[ind])))[2:]

    return hex_val


def remove_nan(data):
    """Remove NaN values from an array.

    For 1D arrays, return non-NaN values. For 2D arrays remove entire rows if
    there is a single NaN value.
    """
    num_dims = len(data.shape)
    if num_dims == 1:
        inds = np.logical_not(np.isnan(data))
        return data[inds]
    elif num_dims == 2:
        inds = np.logical_not(np.isnan(data)).any(1)
        return data[inds, :]
    else:
        print("Only 1D and 2D arrays are supported")


def msdo(val):
    """Get the order of the most significant digit.

    The integer part of a base-10 logarithm is the order of the most
    significant digit.

    """
    if val == 0:
        return 1
    else:
        return np.floor(np.log10(np.abs(val)))


def arg2grep(arr, substr):
    g_inds = []
    g_el = []
    for (ind, el) in enumerate(arr):
        if substr in el:
            g_inds.append(ind)
            g_el.append(el)

    return g_inds, g_el


def arggrep(arr, substr):
    g_inds = arg2grep(arr, substr)[0]
    return g_inds


def grep(arr, substr, return_inds=False):
    g_inds, g_el = arg2grep(arr, substr)
    if return_inds:
        return (g_el, g_inds)
    else:
        return g_el


def get_rsd(A):
    """Get the relative standard deviation of an array."""
    return np.nanstd(A)/np.nanmean(A)


def find_first(
        arr, val, equal_only=False, fail_with_nan=False, start_ind=None):
    """
    Find the index of the first element in arr that is larger than or equal
    to val. If equal_only is True only equal elements are considered. If no
    elements are found None is returned, unless fail_with_nan is True, in which
    case NaN is returned insread.
    """
    if start_ind is not None:
        index = find_first(
            arr[start_ind:], val, equal_only=equal_only,
            fail_with_nan=fail_with_nan)
        if index:
            return start_ind + index
        else:
            return None

    if val is None:
        if fail_with_nan:
            return np.nan
        else:
            return None

    for index, item in enumerate(arr):
        if equal_only:
            if item == val:
                return index
        else:
            if item >= val:
                return index

    if fail_with_nan:
        return np.nan
    else:
        return None


def find_last(arr, val, finish_ind=None, start_ind=None):
    """
    Find the index of the last element in arr that is larger than or equal
    to val.
    """
    if start_ind is not None:
        index = find_last(
            arr[start_ind:], val)
        if index:
            return start_ind + index
        else:
            return None

    if finish_ind is not None:
        index = find_last(
            arr[:finish_ind], val)
        if index:
            return index
        else:
            return None

    ind = find_first(np.flip(arr), val)
    if ind is not None:
        return arr.size - ind - 1
    else:
        return None


def round_to(par, thr=1E-3):
    """Round to given precision."""
    if thr is not None:
        par = np.round(par/thr)*thr
        par[np.abs(par) < thr] = 0

    return par


def find_closest(arr, val):
    """
    Find the index of the closest value in an array.
    """

    if type(arr) == list:
        arr = np.array(arr)

    if isarray(val):
        return [find_closest(arr, val1) for val1 in val]
    else:
        if val is None:
            return None
        else:
            if isinstance(val, datetime.datetime):
                return np.nanargmin(np.array([delta.total_seconds() for delta in arr-val])**2)
            else:
                return np.nanargmin((arr-val)**2)


def interp(xval, xarr, yarr):
    """1D interpolation for increasing or decreasing xarr."""
    if (np.diff(xarr) > 0).all():
        return np.interp(xval, xarr, yarr)
    elif (np.diff(xarr) < 0).all():
        return np.interp(xval, xarr[::-1], yarr[::-1])
    else:
        print("WARNING: xarr is nonmonotonous, interpolation impossible")
        return None


def interp_closest(xarr, yarr, yval, yrng=0.1):
    """Interpolate closest intersection point."""
    center_ind = find_closest(yarr, yval)
    from_ind = find_closest(yarr, yval - yrng/2)
    to_ind = find_closest(yarr, yval + yrng/2)
    if to_ind - from_ind < 3:
        from_ind = center_ind - 1
        to_ind = center_ind + 2

    # NB: the numpy interp variant fails silently for nonincreasing data, i.e.
    # the falling edge of the peak, and gives subtly wrong results
    return interp(yval, yarr[from_ind:to_ind], xarr[from_ind:to_ind])


def cap_in_range(val, rng):
    """Cap a value inside the given range."""
    if val < rng[0]:
        return rng[0]
    if val > rng[1]:
        return rng[1]
    return val


def extend_range(rng, frac):
    """
    Extend the given range by a given fraction.
    """
    span = rng[1] - rng[0]
    return [rng[0] - span*frac, rng[1] + span*frac]


def get_common_range(*args, mode='overlap', expand_frac=0, symmetric=False):
    """
    Get a single value range for a set of ranges. In 'overlap' mode the range
    where values from all ranges overlap is returned. In 'bound' the range that
    spans all ranges is returned.
    """
    rng_min_arr = []
    rng_max_arr = []
    for rng in args:
        rng_min_arr.append(np.nanmin(rng))
        rng_max_arr.append(np.nanmax(rng))
    if mode == 'overlap':
        com_rng = [np.nanmax(rng_min_arr), np.nanmin(rng_max_arr)]
    elif mode == 'bound':
        com_rng = [np.nanmin(rng_min_arr), np.nanmax(rng_max_arr)]
    else:
        raise RuntimeError("Undefined mode")

    if expand_frac > 0:
        span = com_rng[1] - com_rng[0]
        com_rng[0] = com_rng[0] - span*expand_frac
        com_rng[1] = com_rng[1] + span*expand_frac

    if symmetric:
        com_rng = [-np.max(np.abs(com_rng)), np.max(np.abs(com_rng))]

    return com_rng


def get_granularity(A):
    """Get the granularity of a digitally-sampled signal."""
    if not isinstance(A[0], (float, int, np.integer, np.floating)):
        return np.nanmin([get_granularity(sub_arr) for sub_arr in A])

    d = np.abs(np.diff(A))
    d = d[d != 0]
    return np.nanmin(d)

def snap_to_closest_val(val):
    """Snap to the closest grid value, e.g. 1, 2, 5.

    Fint the closest value in a an array and return it. This is useful for
    snapping values to a 1, 2 or 5 grid, for example. The search scales to the
    most significant figure and works for 0.1, 0.2, 0.5 and other orders.
    Useful for figure tick markers.
    """
    # Step array to snap to
    step_arr = [1, 2, 5]
    # The order of the least signifficant digit of the value
    val_order = 10**np.floor(np.log10(val))
    # Index of the closest value in the step array
    closest_ind = np.argmin([(val//val_order - step)**2 for step in step_arr])
    # Return closest value with the correct order
    return val_order*step_arr[closest_ind]

def decimate(A, bins=2, stride=1):
    """
    decimate array A into bins where each bin contains alternating elements.
    """

    lenA = len(A)
    lenC = int(np.floor(lenA/bins))
    C = np.zeros([lenC, bins])
    ind_bin = 0
    indC = 0

    for ind in range(0, lenC*bins):
        from_ind = stride*ind
        to_ind = from_ind + stride

        C[indC:indC + stride, ind_bin] = A[from_ind:to_ind]

        ind_bin = ind_bin + 1
        if ind_bin == bins:
            ind_bin = 0
            indC = indC + stride

    return C


def cut_by_x_range(X, Y, rng=None, rng_fr=None, rng_to=None,
                   round_far_range_up=False, action='cut'):
    """Cut X, Y arrays to a range in X.

    The X array is assumed to contain monotonously increasing values. The X and
    Y arrays are sorted before cutting.

    The range can be specified either as tuple via 'rng', or as from and to
    X values via 'rng_fr' and 'rng_to'. If only either from or to bound is
    given, the other bound is taken as min/max of the range.
    """
    # Validate input
    if not isarray(X):
        print("X has to be an array")
        return [X, Y]
    if not isarray(Y):
        print("Y has to be an array")
        return [X, Y]
    if len(X) != len(Y):
        print("X and Y need to have equal lengths")
        return [X, Y]
    if len(Y) == 0:
        return [X, Y]

    # Make sure arrays are numpy
    if not isinstance(X, np.ndarray):
        X = np.array(X)

    if not isinstance(Y, np.ndarray):
        Y = np.array(Y)

    if rng is not None:
        rng_fr = rng[0]
        rng_to = rng[1]

    if rng_fr is None and rng_to is None:
        return [X, Y]

    # Don't do anything if the X array already fits the requested range
    if np.nanmin(X) > rng_fr and np.nanmax(X) < rng_to:
        return [X, Y]

    # Sort arrays
    sort_order = np.argsort(X)
    X = X[sort_order]
    Y = Y[sort_order]

    if rng_fr is None:
        rng_fr_ind = 0
    else:
        rng_fr_ind = find_closest(X, rng_fr)

    if rng_to is None:
        rng_to_ind = -1
    else:
        rng_to_ind = find_closest(X, rng_to)

    if round_far_range_up:
        rng_to_ind += 1

    if action == 'cut':
        return [X[rng_fr_ind:rng_to_ind], Y[rng_fr_ind:rng_to_ind]]
    elif action == 'nan':
        X[:rng_fr_ind] = np.nan
        X[rng_to_ind:] = np.nan
        Y[:rng_fr_ind] = np.nan
        Y[rng_to_ind:] = np.nan
        return [X, Y]


def remove_duplicate_points(X, Y):
    """
    Remove points that have duplicate consecutive X values.
    """

    X2 = np.empty_like(X)
    Y2 = np.empty_like(Y)

    last_val = None
    ind2 = 0
    for ind in range(0, len(X2)):
        if last_val is None:
            duplicate = False
        else:
            if Y[ind] == last_val:
                duplicate = True
            else:
                duplicate = False

        if not duplicate:
            X2[ind2] = X[ind]
            Y2[ind2] = Y[ind]
            last_val = Y[ind]
            ind2 = ind2 + 1

    X2 = X2[:ind2]
    Y2 = Y2[:ind2]

    return [X2, Y2]


def handle_special_points(
        arr, type='outlier', action='remove', thr_sigma_fac=3,
        verbose=True,
        var_name='Array', return_mask=False, test_column=None):
    """Handle special points in array.

    The special points can be either 'outliers' or 'nan'. The action can be
    eihter 'remove' or 'warn'.
    """
    if arr is None:
        return None

    if not isnone(test_column):
        test_arr = arr[:, test_column]
    else:
        test_arr = arr

    if isinstance(test_arr, list):
        multiple_inputs = True
        arr_len = len(test_arr[0])
    else:
        multiple_inputs = False
        arr_len = len(test_arr)

    if type == 'outlier':
        dev = np.abs(test_arr - np.nanmean(test_arr))
        thr = thr_sigma_fac*np.nanstd(test_arr)
        mask = np.logical_not(dev > thr)
    elif type == 'nan':
        if multiple_inputs:
            mask = test_arr[0] == test_arr[0]
            for test_arr1 in test_arr:
                mask = np.logical_and(
                    mask, np.logical_not(np.isnan(test_arr1)))
        else:
            mask = np.logical_not(np.isnan(test_arr))
    else:
        print("Unsupported speecial point type")
        return None

    if mask.all():
        num_pts = 0
    else:
        num_pts = arr_len - sum(mask)

    if num_pts > 0:
        warn_str = var_name + " contains {:d}".format(num_pts)
        pt_frac = num_pts/len(test_arr)
        if pt_frac > 0.01:
            warn_str += " ({:.1f}%)".format(pt_frac*100)
        if type == 'outlier':
            warn_str += " outliers"
        elif type == 'nan':
            warn_str += " NaNs"

        if action == 'remove':
            warn_str += '. Removing...'
            if verbose:
                print(warn_str)
            if not isnone(test_column):
                arr = arr[mask, :]
            else:
                if multiple_inputs:
                    arr_out = []
                    for arr1 in arr:
                        arr_out.append(arr1[mask])
                    arr = arr_out
                else:
                    arr = arr[mask]
        else:
            if verbose:
                print(warn_str)

    if return_mask:
        return arr, mask
    else:
        return arr


def warn_has_nan_vals(arr, var_name='Array'):
    handle_special_points(arr, type='nan', action='warn', var_name=var_name)


def remove_nan_points(arr, **kwargs):
    return handle_special_points(arr, type='nan', action='remove', **kwargs)


def remove_outlier_points(arr, **kwargs):
    return handle_special_points(
        arr, type='outlier', action='remove', **kwargs)


def unwrap_angle(angle, period=np.pi, plus_minus_range=True):
    """Unwrap angle value to one period range.

    If plus_minus_range is True the angle range is [-period/2, period/2] range,
    otherwise it is [0, period].
    """
    if plus_minus_range:
        return angle - np.round(angle/period)*period
    else:
        return angle - np.floor(angle/period)*period


def get_d4sigma(xarr, yarr, ignore_spacing_check=False, **kwargs):
    """Get 1D 4-sigma width."""
    if not ignore_spacing_check and np.std(np.diff(xarr)) != 0:
        raise RuntimeError("Does not work for data with unequal time spacing")

    xstep = np.mean(np.diff(xarr))
    xcenter = np.sum(yarr * xarr * xstep) / np.sum(yarr * xstep)
    mom2 = np.sum(yarr * (xarr - xcenter)**2 * xstep) / np.sum(yarr * xstep)

    # D4sigma in 2D is 2*np.sqrt(2)*np.sqrt(mom2x + mom2y)
    return 4*np.sqrt(mom2)


def estimate_fwhm(xarr, yarr):
    """Estimate FWHM from a single-peak trace."""
    return [interp_closest(
        xarr[:np.argmax(yarr)], yarr[:np.argmax(yarr)], np.max(yarr)/2),
            interp_closest(
        xarr[np.argmax(yarr):], yarr[np.argmax(yarr):], np.max(yarr)/2)]


def get_pulse_duration(tau_arr, ac_arr, autocorrelation=True, **kwargs):
    """Estimate pulse duration from a trace.

    Pulse duration is estimated in two ways:
      - By finding the FWHM points to the left and right from the curve maxium
      using interpolation. This will not work for nonmonotonous curves and may
      fail if the curve is noisy and the max position cannot be determined by
      np.max(ac_arr).
      - By calculating the D4sigma parameter. This should work for all traces
      when background is properly substracted or can be neglected.

    The function returns a dict with:
        - 'fwhm_pos': the x positions of the FWHM points, useful for plotting
        - 'fwhm': interpolated FWHM value
        - d4s: calculated D4sigma value
        - d4s_fwhmeq: an equivalent FWHM value calculated from the D4sigma
        value. This value is the same as true FWHM for Gaussian curves.
    """
    pulse_dur = dict()

    pulse_dur['fwhm_pos'] = estimate_fwhm(tau_arr, ac_arr)
    if np.array([val is not None for val in pulse_dur['fwhm_pos']]).all():
        pulse_dur['fwhm'] = np.abs(np.diff(pulse_dur['fwhm_pos'])[0])
    else:
        print("WARNING: failed to estimate pulse FWHM duration from curve")
        pulse_dur['fwhm'] = None

        if autocorrelation:
            pulse_dur['fwhm'] /= np.sqrt(2)

    pulse_dur['d4s'] = get_d4sigma(tau_arr, ac_arr, **kwargs)

    # Estimate equivalent FWHM duration from the D4sigma duration of the
    # autocorrelation trace. The conversion factor for the time envelope
    # would be 0.589, this includes the np.sqrt(2) second-order
    # autocorrelation factor.
    if autocorrelation:
        pulse_dur['d4s_fwhmeq'] = pulse_dur['d4s']*0.416
    else:
        pulse_dur['d4s_fwhmeq'] = pulse_dur['d4s']*0.589

    return pulse_dur


def reduce_trace(X, Y, szr=None, Yred_method='mean'):
    """Reduce trace to a given number of samples."""
    if szr is None:
        szr = 300

    sz = len(X)

    if sz <= szr:
        Xr = X
        Yr = Y
        Yr_sd = np.zeros_like(Xr)
        return [Xr, Yr, Yr_sd]

    stepr = round(sz/szr)

    Xr = np.ndarray(szr)
    Yr = np.ndarray(szr)
    Yr_sd = np.ndarray(szr)

    for ind in range(0, szr):

        ind_fr = ind*stepr
        ind_to = (ind+1)*stepr

        if ind_to > sz:
            ind_to = sz

        Xr[ind] = np.mean(X[ind_fr:ind_to])
        if Yred_method == 'mean':
            Yr[ind] = np.mean(Y[ind_fr:ind_to])
        elif Yred_method == 'bin':
            Yr[ind] = np.sum(Y[ind_fr:ind_to])

        Yr_sd[ind] = np.std(Y[ind_fr:ind_to])

    return [Xr, Yr, Yr_sd]


def hist_bin_edges_to_centers(binE):
    """Calculate bin center positions from edge values."""
    binC = np.ndarray(binE.size-1)
    for ind in range(binE.size-1):
        binC[ind] = (binE[ind] + binE[ind+1])/2

    return binC


def hist_bin_centers_to_edges(binC):
    """Calculate bin edge positions from center values."""
    binE = np.ndarray(len(binC)+1)
    bin_step = np.mean(np.diff(binC))
    binE[0] = binC[0] - (binC[1] - binC[0])/2
    binE[-1] = binC[-1] + (binC[-1] - binC[-2])/2
    for ind in range(1, len(binC)):
        binE[ind] = binC[ind] + (binC[ind-1] - binC[ind])/2

    return binE


def bin_data(D, binsz):
    """Bin data into bins of a given size."""

    Dlen = len(D)
    Blen = int(np.floor(Dlen/binsz))

    B = np.ndarray(Blen)

    for indB in range(0, Blen):
        ind_fr = indB*binsz
        ind_to = (indB+1)*binsz

        if ind_to > Dlen:
            ind_to = Dlen

        B[indB] = D[ind_fr:ind_to].sum()

    return B


def bin_data_by_x(X, Y, binsz_X):
    """
    Bin data into bins of a given X size. The difference between reduce_trace
    is that it just reduces the data into a size having a fixed number of
    samples, whereas this function reduces the data into bins having a fixed
    size in X.

    TODO: This is very slow. reduce_trace with average bin size works so much
        faster
    TODO: support nonequal X spacing
    """

    xlen = len(X)

    bins = [0]
    t = time.time()
    while True:
        ind = find_closest(X, X[bins[-1]] + binsz_X)

        if time.time() - t > 0.2:
            print("Binning data: {:.3f}".format(ind/xlen))
            t = time.time()

        if ind >= xlen and ind == bins[-1]:
            break

        bins.append(ind)

    numb = len(bins) - 1

    Xb = np.ndarray(numb)
    Yb = np.ndarray(numb)
    Yb_sd = np.ndarray(numb)

    for bind in range(0, numb):
        ind_fr = bins[bind]
        ind_to = bins[bind+1]

        Xb[bind] = X[ind_fr:ind_to].mean()
        Yb[bind] = Yb[ind_fr:ind_to].mean()
        Yb_sd[bind] = Yb_sd[ind_fr:ind_to].std()

    return [Xb, Yb, Yb_sd]


def bin_data_on_grid(xarr, yarr, xgrid, func='avg', verbose=False):
    """Bin data on a grid.

    Useful for averaging data while resampling on a nonmonotonous grid, e.g.
    when preparing data sampled on a linear x scale for display on a log scale.
    """
    ygrid = np.empty_like(xgrid)
    if verbose:
        print("Binning data on grid...")
        print("Function: {:}".format(func))
    for ind, xval in enumerate(xgrid):
        if verbose and np.mod(ind, 10) == 0:
            print("{:d}/{:d}".format(ind, len(xgrid)))
        if ind > 0:
            ind_from = find_closest(xarr, xgrid[ind-1])
        else:
            ind_from = 0
        if ind < len(xgrid)-1:
            ind_to = find_closest(xarr, xgrid[ind+1])
        else:
            ind_to = len(xarr)

        if func == 'max':
            ygrid[ind] = np.nanmax(yarr[ind_from:ind_to])
        elif func == 'avg':
            ygrid[ind] = np.nanmean(yarr[ind_from:ind_to])

    return ygrid


def running_average(xarr, yarr, num_bins=None, window_sz=None):
    """Perform a running average.

    TODO: This uses the very slow bin_and_slice_data() algorithm.
    """
    if num_bins and window_sz:
        raise ValueError("Specify either number of bins or window size")

    if window_sz:
        num_bins = int(len(xarr)/window_sz)

    return bin_and_slice_data(xarr, yarr, num_bins=num_bins)[0:2]


def columnize_array(arrs):
    """Arrange 1D lists and arrays into columns in a 2D ndarray."""
    num_rows = len(arrs[0])
    arr2d = np.ndarray([num_rows, len(arrs)])
    for ind, arr in enumerate(arrs):
        arr2d[:, ind] = arr

    return arr2d


def bin_and_slice_data(X=None, Y=None, num_slcs=None, num_bins=None):
    """Put data into bins with mean and percentiles.

    Combine the data into bins, slice each bin at equidistant percentile levels
    and calculate the value ranges of each level. The number of final bins is
    given by num_bins. The number of slices parameter (num_slcs) specifies the
    number of slices between 0 and median, so that if e.g. num_slcs = 2 the
    data is sliced at 1.0, 0.75, 0.5, 0.25 and 0 fractional levels and there
    are 2 slices above (1 to 0.75, 0.75 to 0.5) and below (0.5 to 0.25, 0.25
    to 0) the median level.
    """
    if num_slcs is None:
        num_slcs = 10

    fracs = np.linspace(100, 0, 2*num_slcs+1)

    if num_bins is None:
        num_bins = 500

    sz = len(X)

    if sz <= num_bins:
        Xb = X
        Yb = Y
        Yb_lvls = None
        return [Xb, Yb, Yb_lvls]

    bin_step = round(sz/num_bins)

    Xb = np.ndarray(num_bins)
    Yb = np.ndarray(num_bins)
    Yb_lvls = np.ndarray([num_bins, len(fracs)])

    for ind in range(0, num_bins):

        ind_fr = ind*bin_step
        ind_to = (ind+1)*bin_step

        if ind_to > sz:
            ind_to = sz

        Xb[ind] = np.mean(X[ind_fr:ind_to])
        Yb[ind] = np.mean(Y[ind_fr:ind_to])

        if ind_fr < ind_to:
            Yb_lvls[ind, :] = np.percentile(Y[ind_fr:ind_to], fracs)
        else:
            Yb_lvls[ind, :] = np.nan

    return [Xb, Yb, Yb_lvls]


def warning_with_info(message):
    print(message)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    if exc_obj is not None:
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_obj, exc_type, " in ", fname, exc_tb.tb_lineno)


def get_exception_info_str():
    """Get exception info string.

    Get a string conatining the exception message and type, and the file and
    line it w as raised at.
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return exc_obj.args[0] + ', ' + exc_type.__name__ + " in " + \
        fname + ': ' + str(exc_tb.tb_lineno)


def handle_general_exception(message):
    print(message)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_obj, exc_type, " in ", fname, exc_tb.tb_lineno)


def vlvl_str_to_id(vlvl):
    """Convert verbosity level to id.

    TODO: This should be an enum.
    """
    if vlvl == 'silent':
        return 0
    elif vlvl == 'debug':
        return 1
    elif vlvl == 'info':
        return 2
    elif vlvl == 'warning':
        return 3
    elif vlvl == 'error':
        return 4
    else:
        print('Invalid verbosity level')
        return None


def printmsg(msg, msg_vlvl, vlvl):
    """Print a message based on verbosity level.

    Verbosity levels: 'silent', 'debug', 'info', 'warning', 'error'.
    """
    if vlvl is None:
        vlvl = 'info'

    if vlvl_str_to_id(msg_vlvl) >= vlvl_str_to_id(vlvl):
        print(msg)


def ask_yesno(prompt, default=None):
    """Ask user a yes/no question."""

    valid_input = {'yes': True, 'ye': True, 'y': True,
                   'no': False, 'n': False}

    if default is None:
        def_str = ' [y/n]: '
    else:
        default = default.lower()
        if default == 'yes':
            def_str = ' [Y/n]: '
        elif default == 'no':
            def_str = ' [y/N]: '
        else:
            raise ValueError("default must be 'yes', 'no' or None")

    while 1:
        ans = input(prompt + def_str).lower()

        if ans == '' and default is not None:
            return valid_input[default]

        if ans in valid_input.keys():
            return valid_input[ans]


def get_color(name):
    """Get RGBA values for standard colors."""
    if name == "darkred" or name == "dr":
        return hex2byte("e94040ff")/255

    if name == "red" or name == "r":
        return hex2byte("ffb9b9ff")/255

    if name == "lightred" or name == "lr":
        return hex2byte("fad1d1ff")/255

    if name == "darkgreen" or name == "dg":
        return hex2byte("52b656ff")/255

    if name == "green" or name == "g":
        return hex2byte("a0e4a1ff")/255

    if name == "lightgreen" or name == "lg":
        return hex2byte("d9f2d9ff")/255

    if name == "darkblue" or name == "db":
        return hex2byte("458ddeff")/255

    if name == "blue" or name == "b":
        return hex2byte("97b9f7ff")/255

    if name == "darkorange" or name == "do":
        return hex2byte("ee8e4aff")/255

    if name == "yellow" or name == "y":
        return hex2byte("ffea97ff")/255

    if name == "lightgray" or name == "lgr":
        return [230/255, 230/255, 230/255]

    if name == "gray" or name == "gr":
        return [0.5, 0.5, 0.5]

    if name == "black" or name == "k":
        return [0, 0, 0]

    # Vega/D3 Category20
    if name == "C20_0":
        return [0.1216, 0.4667, 0.7059]  # 1f77b4

    if name == "C20_1":
        return [0.6824, 0.7804, 0.9098]  # aec7e8

    if name == "C20_2":
        return [1.0000, 0.4980, 0.0549]  # ff7f0e

    if name == "C20_3":
        return [1.0000, 0.7333, 0.4706]  # ffbb78

    if name == "C20_4":
        return [0.1725, 0.6275, 0.1725]  # 2ca02c

    if name == "C20_5":
        return [0.5961, 0.8745, 0.5412]  # 98df8a

    if name == "C20_6":
        return [0.8392, 0.1529, 0.1569]  # d62728

    if name == "C20_7":
        return [1.0000, 0.5961, 0.5882]  # ff9896

    if name == "C20_8":
        return [0.5804, 0.4039, 0.7412]  # 9467bd

    if name == "C20_9":
        return [0.7725, 0.6902, 0.8353]  # c5b0d5

    if name == "C20_10":
        return [0.5490, 0.3373, 0.2941]  # 8c564b

    if name == "C20_11":
        return [0.7686, 0.6118, 0.5804]  # c49c94

    if name == "C20_12":
        return [0.8902, 0.4667, 0.7608]  # e377c2

    if name == "C20_13":
        return [0.9686, 0.7137, 0.8235]  # f7b6d2

    if name == "C20_14":
        return [0.4980, 0.4980, 0.4980]  # 7f7f7f

    if name == "C20_15":
        return [0.7804, 0.7804, 0.7804]  # c7c7c7

    if name == "C20_16":
        return [0.7373, 0.7412, 0.1333]  # bcbd22

    if name == "C20_17":
        return [0.8588, 0.8588, 0.5529]  # dbdb8d

    if name == "C20_18":
        return [0.0902, 0.7451, 0.8118]  # 17becf

    if name == "C20_19":
        return [0.6196, 0.8549, 0.8980]  # 9edae5

    # Vega/D3 Category20b
    if name == "C20b_0":
        return [0.2235, 0.2314, 0.4745]  # 393b79

    if name == "C20b_1":
        return [0.3216, 0.3294, 0.6392]  # 5254a3

    if name == "C20b_2":
        return [0.4196, 0.4314, 0.8118]  # 6b6ecf

    if name == "C20b_3":
        return [0.6118, 0.6196, 0.8706]  # 9c9ede

    if name == "C20b_4":
        return [0.3882, 0.4745, 0.2235]  # 637939

    if name == "C20b_5":
        return [0.5490, 0.6353, 0.3216]  # 8ca252

    if name == "C20b_6":
        return [0.7098, 0.8118, 0.4196]  # b5cf6b

    if name == "C20b_7":
        return [0.8078, 0.8588, 0.6118]  # cedb9c

    if name == "C20b_8":
        return [0.5490, 0.4275, 0.1922]  # 8c6d31

    if name == "C20b_9":
        return [0.7412, 0.6196, 0.2235]  # bd9e39

    if name == "C20b_10":
        return [0.9059, 0.7294, 0.3216]  # e7ba52

    if name == "C20b_11":
        return [0.9059, 0.7961, 0.5804]  # e7cb94

    if name == "C20b_12":
        return [0.5176, 0.2353, 0.2235]  # 843c39

    if name == "C20b_13":
        return [0.6784, 0.2863, 0.2902]  # ad494a

    if name == "C20b_14":
        return [0.8392, 0.3804, 0.4196]  # d6616b

    if name == "C20b_15":
        return [0.9059, 0.5882, 0.6118]  # e7969c

    if name == "C20b_16":
        return [0.4824, 0.2549, 0.4510]  # 7b4173

    if name == "C20b_17":
        return [0.6471, 0.3176, 0.5804]  # a55194

    if name == "C20b_18":
        return [0.8078, 0.4275, 0.7412]  # ce6dbd

    if name == "C20b_19":
        return [0.8706, 0.6196, 0.8392]  # de9ed6

    print("Undefined colour '" + name + "'")
    return get_colour("gray")


def get_colour(name):
    """British wrapper for get_color()."""
    return get_color(name)


def get_color_seq(names=None, seq_name='Vega20'):
    """Get a color sequence for indexing."""
    if not seq_name:
        seq_name = 'rgb'

    if seq_name == 'rgb':
        names = ['dr', 'dg', 'db', 'r', 'g', 'b']
    elif seq_name == 'Vega10':
        names = []
        for ind in np.arange(1, 10):
            names.append('C10_{:d}'.format(ind))
    elif seq_name == 'Vega20b':
        names = []
        for ind in np.arange(0, 20, 2):
            names.append('C20b_{:d}'.format(ind))
    elif seq_name == 'Vega20':
        names = []
        for ind in np.arange(0, 20, 2):
            names.append('C20_{:d}'.format(ind))

    c = []
    for name in names:
        c.append(get_color(name))

    return c


def get_colourmap(name):
    """Get a custom colourmap."""
    if name == "KBW_Nice":
        colors = [(0, 0, 0), (151/255, 185/255, 247/255), (1, 1, 1)]
        return LinearSegmentedColormap.from_list(
                name, colors, N=256)

    if name == "KPW_Nice":
        colors = [(0, 0, 0), (190/255, 70/255, 196/255), (1, 1, 1)]
        return LinearSegmentedColormap.from_list(
                name, colors, N=256)

    if name == "KGW_Nice":
        colors = [(0, 0, 0), (160/255, 255/255, 161/255), (1, 1, 1)]
        return LinearSegmentedColormap.from_list(
                name, colors, N=256)

    if name == "KOW_Nice":
        colors = [(0, 0, 0), (255/255, 180/255, 128/255), (1, 1, 1)]
        return LinearSegmentedColormap.from_list(
                name, colors, N=256)

    if name == "KRW_Nice":
        colors = [(0, 0, 0), (233/255, 64/255, 64/255), (1, 1, 1)]
        return LinearSegmentedColormap.from_list(
                name, colors, N=256)

    if name == "GYOR_Nice":
        colors = [(0.0, (130/255, 220/255, 132/255)),
                  (0.25, (130/255, 220/255, 132/255)),
                  (0.5, (255/255, 234/255, 151/255)),
                  (0.75, (255/255, 180/255, 128/255)),
                  (1.0, (255/255, 180/255, 185/255))]

        return LinearSegmentedColormap.from_list(
                name, colors, N=256)

    if name == 'gray_sat':
        cm = get_cmap('gray')
        cm.set_over('r')
        cm.set_under('b')

        return cm

    return get_cmap(name)
