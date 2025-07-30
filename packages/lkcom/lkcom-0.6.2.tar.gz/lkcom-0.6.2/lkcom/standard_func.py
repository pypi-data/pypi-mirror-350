"""lkcom - a Python library of useful routines.

This module contains various standard mathematical functions.

Copyright 2015-2023 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import numpy as np
import matplotlib.pyplot as plt

from lkcom.util import get_color

def gaussian_1D(X=None, A=1, w=None, c=None, y0=0, sigma=None):
    """Evaluate a 1D Gaussian."""
    if X is None:
        sz = 100
        X = np.arange(0, sz, 1, float)
    else:
        sz = len(X)

    if w is None:
        w = sz/5

    if c is None:
        c = sz/2

    if sigma is None:
        sigma = w/np.sqrt(8*np.log(2))

    return A*np.exp(-(X-c)**2/(2*sigma**2)) + y0


def gaussian_1D_arglist(args, X=None):
    """Evaluate a 1D Gaussian"""
    return gaussian_1D(X, A=args[0], w=args[1], c=args[2], y0=args[3])


def plot_gaussian_1D(
        X=None, A=1, width=None, center=None, y0=0,
        c=get_color('r'), ls='-', ls_markers='--'):
    """
    Plot a nice 1D Gaussian.
    """
    if X is None:
        X = np.arange(0, 100)

    sz = len(X)

    if width is None:
        width = sz/10

    if center is None:
        center = sz/2

    Y = gaussian_1D(X, A=A, w=width, c=center, y0=y0)
    plt.plot(X, Y, c=c, ls=ls)

    w_X = np.array([-1., 1.])*width/2 + center
    w_Y = np.array([1., 1.])*A/2 + y0
    plt.plot(w_X, w_Y, c=c, ls=ls_markers)

    c_X = np.array([1, 1])*center
    c_Y = np.array([y0, A+y0])

    plt.plot(c_X, c_Y, c=c, ls=ls_markers)

    plt.plot([np.min(X), np.max(X)], [y0, y0], c=c, ls=ls_markers)


def plot_gaussian_1D_arglist(args, X=None, **kwargs):
    """Plot a 1D Gaussian."""
    return plot_gaussian_1D(
        X, A=args[0], width=args[1], center=args[2], y0=args[3], **kwargs)


def gaussian_2D(sz, A=1, c=None, sigma=None, w=None, y0=0, theta=0):
    """Evaluate a 2D gaussian."""
    if np.isscalar(sz):
        szx = szy = sz
    elif len(sz) == 2:
        szy = sz[0]
        szx = sz[1]

    if w is None:
        wx = szx/5
        wy = szy/5
    elif np.isscalar(w):
        wx = wy = w
    elif(len(w) == 2):
        wy = w[0]
        wx = w[1]

    if c is None:
        cx = szx/2
        cy = szy/2
    elif np.isscalar(c):
        cx = cy = c
    elif len(c) == 2:
        cy = c[0]
        cx = c[1]

    X = np.arange(0, szx, 1, float)

    Y = np.ndarray([szy, 1])

    Y[:, 0] = np.arange(0, szy, 1, float)

    if sigma is not None:
        sigma_x = sigma[0]
        sigma_y = sigma[1]
    else:
        sigma_x = wx/np.sqrt(8*np.log(2))
        sigma_y = wy/np.sqrt(8*np.log(2))

    if theta != 0:
        cx_rot = cx * np.cos(theta) - cy * np.sin(theta)
        cy_rot = cx * np.sin(theta) + cy * np.cos(theta)
        cx = cx_rot
        cy = cy_rot

        X_rot = X * np.cos(theta) - Y * np.sin(theta)
        Y_rot = X * np.sin(theta) + Y * np.cos(theta)
        X = X_rot
        Y = Y_rot

    return A*np.exp(-((X-cx)**2/(2*sigma_x**2) + (Y-cy)**2/(2*sigma_y**2))) \
        + y0

def gaussian_2D_lambda(A, cx, cy, sx, sy, y0):
    """
    Evaluate a 2D gaussian as a lambda function.
    """
    sx = float(sx)
    sy = float(sy)
    return lambda x, y: A*np.exp(-(x-cx)**2/(2*sx**2) - (y-cy)**2/(2*sy**2)) \
        + y0


def gaussian_2D_rot_lambda(A, cx, cy, sx, sy, y0, theta):
    """
    Evaluate a 2D gaussian as a lambda function.
    """
    sx = float(sx)
    sy = float(sy)

    if(theta != 0):
        theta = -theta
        cx_rot = cx * np.cos(theta) - cy * np.sin(theta)
        cy_rot = cx * np.sin(theta) + cy * np.cos(theta)
        cx = cx_rot
        cy = cy_rot

    def eval_Gaussian2Drot(x, y):
        if(theta != 0):
            x_rot = x * np.cos(theta) - y * np.sin(theta)
            y_rot = x * np.sin(theta) + y * np.cos(theta)
            x = x_rot
            y = y_rot

        return A*np.exp(-(x-cx)**2/(2*sx**2) - (y-cy)**2/(2*sy**2)) + y0

    return lambda x, y: eval_Gaussian2Drot(x, y)


def pulse_response(x, a=1, x0=0, tau00=0.1, tau01=0, tau1=0.1, b=0):
    formula = 'v1'
    if formula == 'v1':
        return a / (1 + np.exp(-(x-x0)/tau00)) * 1 / (1 + np.exp(-(x-x0)/tau01)) * np.exp(-(x-x0)/tau1) + b
    elif formula == 'v2':
        return a / (1 + np.exp(-(x-x0)/tau00)) * 1 / (1 + np.exp(-(x-x0)/tau01)) * np.exp(-(x-x0)/tau1) + b



def poly_1(x, k1, k0):
    """
    Evaluate a 1st order polynomial.
    """
    return k1*x + k0


def poly_2(x, k2, k1, k0):
    """
    Evaluate a 2nd order polynomial.
    """
    return k2*x**2 + k1*x + k0


def poly_n(x, *p):
    """
    Evaluate an n-th order polynomial with coefficients p at values x.
    """
    return np.polyval(p, x)
