"""lkcom - a Python library of useful routines.

This module contains plotting utilities. Many of these routines can probably be
replaced with better alternatives or even internal Python functions.

Copyright 2015-2024 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import copy
import numpy as np
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from matplotlib.legend_handler import HandlerTuple

from PIL import Image
import PIL.Image as image
from scipy.interpolate import interp2d
from matplotlib.cm import get_cmap

from subprocess import Popen

from lkcom.util import isnone, get_color, bin_and_slice_data, hex2byte, \
    get_granularity, handle_general_exception, hist_bin_centers_to_edges, \
    extend_range, printmsg, estimate_fwhm, snap_to_closest_val
from lkcom.string import get_human_val_str, rem_extension, strip_whitespace
from lkcom.standard_func import gaussian_1D


def get_pt2mm():
    """Get points per mm."""
    pt2mm = 0.352778
    return pt2mm


def get_plot_area_sz_in():
    """Get axes plot area size in inches."""
    bbox = plt.gca().get_window_extent().transformed(
        plt.gcf().dpi_scale_trans.inverted())
    ax_sz = np.array([bbox.width, bbox.height])
    return ax_sz


def get_plot_area_sz_mm():
    """Get axes plot area size in mm."""
    return get_plot_area_sz_in()*25.4


def get_symbol_sz_axis(symbol_sz):
    """Get scatter symbol size in axis units.

    Very useful to place text next to symbol with proper spacing.
    """
    if symbol_sz is None:
        return None

    # Axis size in mm
    ax_sz = get_plot_area_sz_mm()

    # Offset in mm. Symbol size is in terms of diameter in points squared.
    # There seems to be no pi involved.
    ofs_mm = np.sqrt(symbol_sz)*get_pt2mm()/2

    # Axis span in axis units
    xlim = plt.xlim()
    xspan = xlim[1] - xlim[0]

    # Offset in axis units
    ofs = ofs_mm*xspan/ax_sz[0]

    return ofs


def get_def_fig_size(numr, numc):
    """Get figure size based on the number of subplot panels."""
    panel_w = 110
    panel_h = 110
    panel_gap = 15

    fig_w = panel_w*numc + panel_gap*(numc-1)
    fig_h = panel_h*numr + panel_gap*(numr-1)

    return [fig_w/25.4, fig_h/25.4]


def get_figure_size(fig_width='1.5x', fig_height=None, **kwargs):
    """Get figure size that makes sense for printing.

    Figure wdith can be specified as '1x', '1.5x', or '2x' which corresponds to
    figures that are one column, one-and-half or double column wide in text
    that is formatted in two columns, which is typical for articles.

    Figure widths that are larger than '2x' no longer fit on a portrait A4 at
    100% scale.
    """
    fig_size = [4.724, 2.635]
    if fig_width == '1x':
        fig_size[0] = 3.504
    elif fig_width == '1.5x':
        fig_size[0] = 4.724
    elif fig_width == '2x':
        fig_size[0] = 7.205
    elif fig_width == '3x':
        fig_size[0] = 9.448

    if fig_height:
        fig_size[1] = 2.635*float(fig_height.replace('x', ''))

    if fig_size[0] > 8.3:
        print("Figure width is larger than A4 portrait 210 mm (8.3\").")

    return fig_size


def figure_with_subplots(numr=2, numc=2, title=None):
    """Create a figure with a subplot grid."""
    plt.figure(num=title, figsize=get_def_fig_size(numr, numc),)
    subplot_grid = gridspec.GridSpec(numr, numc, wspace=0.2, hspace=0.2)
    return subplot_grid


def new_figure(fig_id=None):
    """
    Create a new maximized figure in the left monitor.
    """
    if not plt.fignum_exists(fig_id):
        plt.figure(fig_id)
        mng = plt.get_current_fig_manager()
        mng.window.setGeometry(-500, 100, 100, 100)
        plt.pause(0.05)
        mng.window.showMaximized()

    return plt.figure(fig_id)


def export_figure(
        fig_name, size=None, output_format='.png', pdf_also=False,
        resize=False, suffix="", verbose=False,
        parent_file_path=None,
        fig_dpi=200, remove_fig_ext=True, **kwargs):
    """Export a figure to a PNG file.

    To save a PDF in addition to the selected output format set pdf_also
    to True. This is useful to generte a vector figure for post-processing in
    addition to the raster figure for quick viewing.
    """
    # Make sure figure drawing is completed
    plt.draw()

    if resize:
        if isnone(size):
            size = [19.2, 9.49]

        if type(size) == str:
            if size not in ['A4', 'A4-sq', 'big-sq']:
                print('Figure size string not recongnized, using A4')
                size = 'A4'
            if size == 'A4':
                fig_w = 11.69
                fig_h = 8.27
            if size == 'A4-sq':
                fig_w = 8.27
                fig_h = 8.27
            if size == 'big-sq':
                fig_w = 10
                fig_h = 10
        else:
            fig_w = size[0]
            fig_h = size[1]

        plt.gcf().set_size_inches(fig_w, fig_h)

    if isnone(suffix):
        suffix = ""

    if remove_fig_ext:
        fig_name = rem_extension(fig_name)

    if fig_name[-4:] == output_format:
        fig_file_name = rem_extension(fig_name) + suffix + output_format
    else:
        fig_file_name = fig_name + suffix + output_format

    if verbose:
        print("Exporting figure " + fig_file_name + "...")

    if parent_file_path:
        fig_file_name = Path(*[*Path(parent_file_path).parts[:-1],
                               fig_file_name])

    try:
        # Setting the bbox_inches option to 'tight' produces an exception in
        # Tkinter
        # plt.savefig(fig_file_name, dpi=600, bbox_inches='tight')
        plt.savefig(fig_file_name, dpi=fig_dpi)
    except Exception:
        handle_general_exception("Could not export figure")

    if pdf_also:
        try:
            pdf_fig_file_name = rem_extension(fig_file_name) + '.pdf'
            plt.savefig(pdf_fig_file_name, dpi=fig_dpi)
        except Exception:
            handle_general_exception("Could not export PDF figure")


def show_png_ext(FileName):
    Popen([r'C:\Program Files (x86)\XnView\xnview.exe', FileName])


def hist(
        yarr, bins=None, yrng=None, target_num_bins=256, hist_bin_sz_fac=1,
        ygran=None,
        with_histogram_dither=False, hist_dith_factor=4, hide_x_labels=False,
        hide_data_labels=False, hide_count_labels=False, stacked=False,
        orientation="vertical", xmarkers=None, ymarkers=None, ylim=None,
        log=False, legend_str=None,
        fit_envelope=False, ref_envelope_width=None,
        show_envelope_outliers=False,
        color=matplotlib.cm.get_cmap('Blues')(0.95)):
    """Plot a nice histogram with dithering and data granularity awareness."""
    if yrng is None:
        yrng = [np.min(yarr), np.max(yarr)]

    yspan = yrng[1] - yrng[0]

    if not isinstance(yarr[0], (float, int, np.integer, np.floating)):
        yarr_all = np.concatenate([arr for arr in yarr])
    else:
        yarr_all = yarr
        yarr = [yarr]

    if ygran is None:
        ygran = get_granularity(yarr_all)

    ymean = np.nanmean(yarr_all)

    print('Y granularity is {:.2e}, scale range is {:.2f} bits'.format(
        ygran, np.log2(yspan/ygran)))

    unique_vals = np.unique(yarr_all)

    if bins is None:
        if len(unique_vals) < target_num_bins:
            # If the number of unique data values is less than the number of
            # target histogram bins, the histogram will have bins with no
            # values in them, which indicates that the histogram resolution is
            # too high.
            bins = hist_bin_centers_to_edges(np.unique(yarr_all))
        else:
            num_bins = yspan/ygran
            ygrans_per_bin = np.max([np.round(num_bins/target_num_bins), 1])
            bins = np.arange(
                yrng[0], yrng[1], ygran*ygrans_per_bin*hist_bin_sz_fac)

    num_bins = len(bins)

    if abs(len(bins)/target_num_bins - 1) > 0.1:
        print("Number of histogram bins requested: {:d}, actual number is {:d}"
              " due to data granularity".format(target_num_bins, num_bins))

    if with_histogram_dither:
        # Calculate histogram dithering array. Elements of the array are
        # drawn from a Gaussian distribution centered at 1. The width of
        # the distribution is such that after dithering about 50% of the
        # data values in one histogram bin spill into the adjacent bin.
        # The strength of the dithering effect can be controlled by changing
        # the hist_dith_fac factor.
        bin_sz = bins[1] - bins[0]
        dith = np.random.normal(1, bin_sz/ymean*hist_dith_factor,
                                len(yarr_all))
        print("Applying histogram dithering with a factor of "
              "{:d}. ".format(hist_dith_factor) +
              "This is an experimental feature, so you might want to compare "
              " the histogram with and without dithering.")

    else:
        dith = 1

    yarr = [arr*dith for arr in yarr]

    if stacked and log:
        print("WARNING: Stacked histograms on a log Y scale may be difficult "
              "to read. For example, a second stacked identical histogram "
              "would appear compressed on a log scale. If that is not what "
              "you want consider using either stacked or log representation "
              "alone.")

    if stacked:
        bin_counts = plt.hist(
            yarr, bins=bins, orientation=orientation, stacked=True,
            color=color, zorder=10, log=log, alpha=0.5)[0]
    else:
        for arr in yarr:
            bin_counts = plt.hist(
                arr, bins=bins, orientation=orientation, color=color,
                zorder=10, log=log, alpha=0.5)[0]

    envelope_xarr = np.linspace(yrng[0], yrng[1], 500)
    if fit_envelope:
        fit_envelope_yarr = gaussian_1D(
            envelope_xarr, A=np.max(bin_counts), sigma=np.std(yarr),
            c=np.mean(yarr))
        if log:
            plt.semilogy(envelope_xarr, fit_envelope_yarr, c='r')
        else:
            plt.plot(envelope_xarr, fit_envelope_yarr, c='r')

        # Calculate counts outside the envelope
        if show_envelope_outliers:
            evenlope_test = np.interp(bins[1:], envelope_xarr,
                                      fit_envelope_yarr)
            # The difference between the fit envelope and and the data in the
            # center of the distribution isn't very useful. Values can be
            # strongly negative or positive depending on slight amplitude
            # changes and changes in center position. Differences in the wings
            # however are consistent.
            # Unmodified difference graph:
            # plt.plot(bins[:-1], bin_counts - evenlope_test)

            # Discrepancies from the distribution can be made more obvious by
            # ignoring data between the 1% and 99% percentiles, i.e. only
            # counting the outliers.
            outlier_rng = np.percentile(yarr, [1, 99])
            from lkcom.util import find_closest
            outlier_inds = find_closest(bins[:-1], outlier_rng)
            outlier_arr = bin_counts - evenlope_test

            outlier_fill_area = np.copy(bin_counts)
            outlier_fill_area[outlier_inds[0]:outlier_inds[1]] = np.nan
            outlier_fill_area[outlier_arr < 0] = np.nan

            outlier_arr[outlier_inds[0]:outlier_inds[1]] = np.nan
            outlier_arr[outlier_arr < 0] = np.nan

            outlier_frac = np.nansum(outlier_arr)/np.nansum(bin_counts)

            plt.fill_between(bins[:-1], outlier_fill_area, evenlope_test,
                             facecolor='red')
            add_infobox("Outliers: {:.2f}%".format(outlier_frac*100))

    if ref_envelope_width:
        ref_envelope_yarr = gaussian_1D(
            envelope_xarr, A=np.max(bin_counts), sigma=ref_envelope_width,
            c=np.mean(yarr))
        if log:
            plt.semilogy(envelope_xarr, ref_envelope_yarr, c='k', ls='--')
        else:
            plt.plot(envelope_xarr, ref_envelope_yarr, c='k', ls='--')

    if legend_str:
        plt.legend(legend_str)

    ax = plt.gca()

    if xmarkers:
        for xmarker in xmarkers:
            add_x_marker(xmarker, c=[0, 0, 0], ls='-')

    if ymarkers:
        # Add histogram y markers
        for ymarker in ymarkers:
            add_y_marker(ymarker, c=[0.75, 0.75, 0.75], ls='-', zorder=1)

    if orientation == 'vertical':
        plt.xlim(yrng)
        plt.gca().set_ylim(bottom=0.7)
        plt.ylim(ylim)
        plt.plot(plt.xlim(), [0, 0], color=[0, 0, 0, 0.25])
        ax = plt.gca()
        if hide_data_labels:
            ax.xaxis.set_ticklabels([])
        if hide_count_labels:
            ax.yaxis.set_ticklabels([])
    else:
        plt.ylim(yrng)
        plt.xlim(ylim)
        plt.plot(plt.ylim(), [0, 0], color=[0, 0, 0, 0.25])
        ax = plt.gca()
        if hide_data_labels:
            ax.yaxis.set_ticklabels([])
        if hide_count_labels:
            ax.xaxis.set_ticklabels([])

    set_ticks_inside()
    plt.grid('on')

    return ax


def make_histogram_panel(
        varr, ax_hist=None, ylim=None, rsd_val=None,
        ax_trace=None, hist_orientation='horizontal',
        log=True, **kwargs):
    """Make a histogram panel.

    Data in varr is plotted as histogram in a panel. The histogram can be
    displayed horizontally or vertically and fits nicely as a side panel.
    """
    if not ax_hist:
        ax_hist = plt.gca()

    if not ylim:
        ylim = [0, 1]

    plt.sca(ax_hist)
    hist_rng = ylim

    y_span = hist_rng[1] - hist_rng[0]
    y_gran = get_granularity(varr)
    num_hist_bins = y_span/y_gran
    target_hist_bins = 500
    y_grans_per_bin = np.ceil(num_hist_bins/target_hist_bins)
    bins = np.arange(hist_rng[0], hist_rng[1], y_gran*y_grans_per_bin)
    if abs(len(bins)/target_hist_bins - 1) > 0.1:
        print("Number of histogram bins requested: {:d}, actual number "
              "is {:d} due to Y data granularity".format(
                target_hist_bins, len(bins)))

    hist_y = plt.hist(
        varr, bins=bins, log=log, alpha=1.0, orientation=hist_orientation)[0]

    plt.grid('on')
    set_ticks_inside()

    if rsd_val:
        gauss_x = np.linspace(hist_rng[0], hist_rng[1], 500)
        gauss_y = gaussian_1D(gauss_x, A=np.max(hist_y), sigma=rsd_val, c=1)
        if hist_orientation == 'horizontal':
            if log:
                plt.semilogx(gauss_y, gauss_x, c='k', alpha=0.75)
            else:
                plt.plot(gauss_y, gauss_x, c='k', alpha=0.75)
        else:
            plt.plot(gauss_x, gauss_y, c='k', alpha=0.75)

        if kwargs.get('plot_fwhm_line', True):
            fwhm = 2.355*rsd_val
            hheight = np.max(hist_y)/2
            plt.plot([1 - fwhm/2, 1 + fwhm/2], [hheight, hheight],
                     'k', alpha=0.75)

    if hist_orientation == 'horizontal':
        plt.xlim([1, np.max(hist_y)*1.1])
        ax_hist.xaxis.set_ticks([])
        ax_hist.yaxis.set_ticklabels([])
        if ax_trace:
            ax_hist.set_yticks(ax_trace.get_yticks())
        plt.ylim(ylim)
        # add_infobox('log hist.') # does not work with log scale...
    else:
        ax_hist.yaxis.set_ticks([])
        plt.xlabel('Energy, a.u.')
        align_outer_tick_labels(ax_hist)


def CompareHistograms(
        img_arr, names=None, range=None, bins=64, histtype='step', xlabel=None,
        ylabel='Occurence', title=None):
    hist_pars = {'range': range, 'bins': bins, 'histtype': histtype}
    for img in img_arr:
        plt.hist(img, **hist_pars)

    plt.xlim(range)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(names)
    plt.title(title)


no_signal_color = [0.25, 0.25, 0.25]


def imshow_ex(
        img, ax=None,
        vmin=None, vmax=None, vrng_algorithm='minmax', min_vspan=None,
        vrng_symmetric=False,
        auto_vrng_percentile_min=0, auto_vrng_percentile_max=99.5,
        bad_color=no_signal_color, cmap='viridis',
        over_color=[1, 0, 0], mark_over=False,
        under_color=[0, 0, 1], mark_under=False,
        logscale=False,
        with_hist=True, hist_color=None, show_full_hist=False,
        title_str=None, is_angle=False,
        export_img=False,
        img_file_name='image.png',
        **kwargs):
    """Show an image with a histogram and colorbar.

    TODO: ShowImage says it does the same, integrate the two.
    """
    if kwargs.get('roi_sz'):
        roi_sz = kwargs.get('roi_sz')
        roi_ofs = kwargs.get('roi_sz', np.array(img.shape)/2)
        img = img[int(roi_ofs[0] - roi_sz[0]/2):int(roi_ofs[0] + roi_sz[0]/2),
                  int(roi_ofs[1] - roi_sz[1]/2):int(roi_ofs[1] + roi_sz[1]/2)]

    if ax is None:
        ax = plt.gca()

    if is_angle:
        img = img/np.pi*180

    if logscale:
        mask = img <= 0
        invmask = np.logical_not(mask)
        img2 = np.empty_like(img)
        img2[mask] = np.nan
        img2[invmask] = np.log10(img[invmask])
        img = img2

        # TODO: something about axis plotting breaks with logscale

        # This works with logscale:
        # img3 = copy.copy(img)
        # img3[img3<0.1] = 0.1
        # plt.imshow(np.log10(img3), vmin=np.log10(0.1), vmax=np.log10(1))

    if vrng_algorithm not in ['minmax', 'percentile']:
        print("Unknown vrng algorithm, resetting to 'minmax")
        vrng_algorithm = 'minmax'

    if vmin is None:
        if vrng_algorithm == 'minmax':
            vmin = np.nanmin(img)
        elif vrng_algorithm == 'percentile':
            vmin = np.nanpercentile(img.flatten(), auto_vrng_percentile_min)

    if vmax is None:
        if vrng_algorithm == 'minmax':
            vmax = np.nanmax(img)
        elif vrng_algorithm == 'percentile':
            vmax = np.nanpercentile(img.flatten(), auto_vrng_percentile_max)

    if min_vspan is not None and vmax - vmin < min_vspan:
        vmean = np.mean([vmin, vmax])
        vmin = vmean - min_vspan/2
        vmax = vmean + min_vspan/2

    if vrng_symmetric:
        vmax = np.max(np.abs([vmin, vmax]))
        vmin = -vmax

    cmap = copy.copy(matplotlib.cm.get_cmap(cmap))
    cmap.set_bad(color=bad_color)
    if mark_over:
        cmap.set_over(color=over_color)
    if mark_under:
        cmap.set_under(color=under_color)

    plt.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax)
    hide_axes()
    if export_img:
        plt.imsave(img_file_name, img, cmap=cmap, vmin=vmin, vmax=vmax)

    if title_str is None:
        title_str = ''

    if logscale:
        title_str += ' (log10)'

    plt.title(title_str)

    cbar = plt.colorbar(orientation='horizontal')
    cbar_ax = cbar.ax

    img_bb = ax.get_position().bounds
    img_x = img_bb[0]
    img_y = img_bb[1]
    img_w = img_bb[2]
    img_h = img_bb[3]


    if with_hist:
        hist_bb = (img_bb[0], img_bb[1] - img_h*0.11, img_bb[2], img_h*0.1)
        plt.axes(hist_bb)

        bins = np.linspace(vmin, vmax, 50)

        if show_full_hist:
            # Show the full histrogram using the same bin step. This makes it
            # easy to see how much of the data range is the image actually
            # showing. This doesn't work with current colormap display though.
            print("WARNING: show_full_hist is an experimental feature, the histogram x limits and the image colorbar are now out-of-sync")
            img_min = np.nanmin(img)
            img_max = np.nanmax(img)
            plt.hist(img.flatten(), bins=np.arange(img_min, img_max, np.mean(np.diff(bins))), log=True, orientation="vertical", color='gray')
        plt.hist(img.flatten(), bins=bins, log=True, orientation="vertical", color=hist_color)

        if show_full_hist:
            add_x_marker(vmin)
            add_x_marker(vmax)
            plt.xlim([img_min, img_max])
        else:
            plt.xlim([vmin, vmax])

        hide_axes()

    cbar_bb = np.array(cbar_ax.get_position().bounds)
    cbar_bb[0] = img_x
    cbar_bb[1] = img_y - cbar_bb[3] - img_h*0.02
    cbar_bb[2] = img_w

    if with_hist:
        cbar_bb[1] -= hist_bb[3]

    cbar_ax.set_position(cbar_bb)

    if is_angle:
        cbar.set_ticks([0, 45, 90, 135, 180])

    if logscale:
        ticks = cbar_ax.get_xticks()
        tick_labels = [get_human_val_str(10**x) for x in ticks]
        cbar_ax.set_xticklabels(tick_labels)


def img_with_profiles(
        img, disp_rng, cmap='viridis', img_title=None,
        xprof_index=None, yprof_index=None,
        show_section_avg_profile=False, show_avg_prof_value=False):
    """Show image with profile panels."""
    num_px = np.mean(img.shape[:2])
    if not xprof_index:
        xprof_index = int(num_px/2)
    if not yprof_index:
        yprof_index = int(num_px/2)

    profile_color = get_color('gray')

    plt.imshow(img, vmin=disp_rng[0], vmax=disp_rng[1], cmap=cmap)
    plt.title(img_title)
    plt.xticks([])
    plt.yticks([])

    # Get position coordinates of the image axes
    pos = plt.gca().get_position()._points

    # Axes creation using plt.axes uses relative figure coordinates, so to make
    # horizontal and vertical profile views of the same size the figure aspect
    # ratio needs to be taken into account
    profile_axes_sz = (pos[1, 0]-pos[0, 0])*0.4
    fig_ar = plt.gcf().bbox.height/plt.gcf().bbox.width

    # Create new axes, note that get_position() returns corner points, but
    # axes() expects x0, y0, width, height
    plt.axes([
        pos[0, 0],
        pos[0, 1] - profile_axes_sz,
        pos[1, 0] - pos[0, 0],
        profile_axes_sz])

    plt.xticks([])
    plt.yticks([])

    plt.xlim([0, num_px])
    plt.ylim(disp_rng)
    if show_avg_prof_value:
        add_y_marker(np.nanmean(img[yprof_index-5:yprof_index+5]), ls='-')
    if show_section_avg_profile:
        plt.plot(np.arange(0, num_px),
                 np.nanmean(img[yprof_index-5:yprof_index+5, :], 0))
    plt.plot(np.arange(0, num_px), img[yprof_index, :], c=profile_color)

    plt.axes([
        pos[1, 0],
        pos[0, 1],
        profile_axes_sz*fig_ar,
        pos[1, 1] - pos[0, 1]])
    plt.xticks([])
    plt.yticks([])

    plt.xlim(disp_rng)
    plt.ylim([0, num_px])
    if show_avg_prof_value:
        add_x_marker(np.nanmean(img[:, xprof_index-5:xprof_index+5]), ls='-')
    if show_section_avg_profile:
        plt.plot(np.nanmean(img[:, xprof_index-5:xprof_index+5], 1),
                 np.arange(0, num_px))
    plt.plot(img[:, xprof_index], np.arange(0, num_px), c=profile_color)


def add_infobox(
        infobox_str=None, show_infobox=True, infobox_hpos='left',
        text_va='top',
        infobox_vpos='top', ref_y=None, text_x=None, text_y=None, **kwargs):
    if show_infobox and infobox_str:
        xl = kwargs.get('xlim')
        if xl is None:
            xl = plt.gca().get_xlim()

        yl = kwargs.get('ylim')
        if yl is None:
            yl = plt.gca().get_ylim()

        ofs_x = (xl[1] - xl[0])*0.05
        ofs_y = (yl[1] - yl[0])*0.07

        text_ha = 'left'
        if not text_x:
            if infobox_hpos == 'left':
                text_x = xl[0] + ofs_x
                text_ha = 'left'
            elif infobox_hpos == 'right':
                text_x = xl[1] - ofs_x
                text_ha = 'right'

        if not text_y:
            if infobox_vpos == 'top':
                if ref_y is None:
                    ref_y = yl[1]
                if plt.gca().get_yaxis().get_scale() == 'log':
                    text_y = ref_y**(1-0.07)
                else:
                    text_y = ref_y - ofs_y

            elif infobox_vpos == 'middle':
                text_y = (yl[1] + yl[0])/2
            elif infobox_vpos == 'bottom':
                if ref_y is None:
                    ref_y = yl[0]
                text_y = ref_y + ofs_y

        plt.text(text_x, text_y, infobox_str, ha=text_ha, va=text_va,
                 bbox=dict(facecolor='white', alpha=0.75,
                           edgecolor='white'))


def add_marker(
        pos=None, label=None, axis='x', c='k', ls='--', zorder=None, xlim=None,
        verbose=False, ylim=None, label_pos='left', label_vpos='bottom', label_vpos_offs=None,
        scale_type=None, label_background=False,
        label_ha='center', label_va='center', **kwargs):
    """Add a vertical or horizontal marker line at the given position."""
    if pos is None:
        return

    if isinstance(pos, list) and len(pos) == 0:
        return

    if xlim is None:
        xlim = plt.xlim()
    if ylim is None:
        ylim = plt.ylim()

    if axis == 'x':
        plt.plot([pos, pos], ylim, c=c, ls=ls, zorder=zorder)
    elif axis == 'y':
        plt.plot(xlim, [pos, pos], c=c, ls=ls, zorder=zorder)

    if label is not None:
        text_opts = {}
        if label_background:
            text_opts['bbox'] = {'facecolor': 'white', 'edgecolor': 'none',
                                 'alpha': 0.75}
        if label_vpos not in ['top', 'bottom']:
            print("Invalid label_vpos, using 'top'")
            label_vpos = 'top'

        xspan = xlim[1] - xlim[0]
        yspan = ylim[1] - ylim[0]

        if axis == 'x':
            if label_pos == 'left':
                xpos = pos
            elif label_pos == 'right':
                xpos = pos + xspan*0.075
            text_opts['rotation'] = 90
            yscale_type = plt.gca().yaxis.get_scale()
            if yscale_type == 'linear':
                if label_vpos == 'bottom':
                    ypos = ylim[0] + yspan*0.03
                    label_va = 'bottom'
                elif label_vpos == 'top':
                    ypos = ylim[1] - yspan*0.03
                    label_va = 'top'
            else:
                print("Log axis for x label not yet supported")

            if label_vpos_offs is not None:
                ypos += label_vpos_offs

        elif axis == 'y':
            yscale_type = plt.gca().yaxis.get_scale()
            if yscale_type == 'linear':
                if label_vpos == 'bottom':
                    ypos = pos - yspan*0.03
                    label_va = 'top'
                elif label_vpos == 'top':
                    ypos = pos + yspan*0.03
                    label_va = 'bottom'
            elif yscale_type == 'log':
                if label_vpos == 'bottom':
                    ypos = 10**(np.log10(pos) - np.log10(yspan)*0.03)
                    label_va = 'top'
                elif label_vpos == 'top':
                    ypos = 10**(np.log10(pos) + np.log10(yspan)*0.03)
                    label_va = 'bottom'

            if not scale_type:
                scale_type = plt.gca().xaxis.get_scale()

            if scale_type == 'linear':
                if label_pos == 'left':
                    xpos = xlim[0]+xspan*0.075
                    label_ha = 'left'
                else:
                    xpos = xlim[1]-xspan*0.075
                    label_ha = 'right'
            elif scale_type == 'log':
                if label_pos == 'left':
                    xpos = 10**(np.log10(xlim[0])+np.log10(xspan)*0.03)
                    label_ha = 'left'
                else:
                    xpos = 10**(np.log10(xlim[0])-np.log10(xspan)*0.03)
                    label_ha = 'right'

        if verbose:
            print("Adding '{:}' label at ({:}, {:})".format(label, xpos, ypos))
        plt.text(
            xpos, ypos, label, ha=label_ha, va=label_va,
            **text_opts)

    plt.xlim(xlim)
    plt.ylim(ylim)


def add_x_marker(pos, label=None, label_ha='right', **kwargs):
    """Add a marker line at X position."""
    add_marker(pos, label, axis='x', label_ha=label_ha, **kwargs)


def add_y_marker(pos, label=None, **kwargs):
    """Add a marker line at Y position."""
    add_marker(pos, label, axis='y', **kwargs)


def fwhm_marker(xarr, yarr, color='k', ls='-', standoff=None):
    """Mark FWHM with a line."""
    color = np.append(np.copy(color), 0.75)
    fwhm_rng = estimate_fwhm(xarr, yarr)
    if standoff:
        xspan = np.diff(plt.xlim())
        fwhm_rng[0] += xspan*standoff
        fwhm_rng[1] -= xspan*standoff

    plt.plot(fwhm_rng, np.array([1, 1])*np.nanmax(yarr)/2, ls=ls, color=color)


def set_human_tick_marks(ax, data):
    """Set human-readable tick marks."""
    data_max = np.nanmax(data)
    data_min = np.nanmin(data)
    data_mean = 0.5*(data_max + data_min)
    data_rng = data_max - data_min
    scale_from = data_min - 0.1*data_rng
    scale_to = data_max + 0.1*data_rng

    # Find a nice scale step for humans to read
    scale_step = snap_to_closest_val((scale_to - scale_from)/4)

    # Adjust scale to snap to to a nice grid
    data_mean = np.round(data_mean/scale_step)*scale_step
    scale_from = np.floor((scale_from)/scale_step)*scale_step
    scale_to = np.ceil((scale_to)/scale_step)*scale_step

    # Set limits on a nice grid
    ax.set_ylim([scale_from, scale_to])

    # Set three ticks centered on the grid
    ticks = [data_mean + scale_step*ind for ind in [-1, 0, 1]]
    ax.set_yticks(ticks)
    # But skip the middle tick label to save space
    ax.yaxis.set_ticklabels(["{:.1f}".format(ticks[0]), '', "{:.1f}".format(ticks[2])])


def add_watermark(watermark_pos='center', fig=None):
    """Add a LC watermark to the figure."""
    if watermark_pos is None:
        return

    if watermark_pos not in ['center', 'upper-left', 'bottom-left']:
        print("Unsupported watermark position ''{:s}''".format(watermark_pos))
        return None

    if fig is None:
        fig = plt.gcf()

    # Figure size in px
    fig_sz = fig.get_size_inches()*fig.dpi

    # Axes size and position in px
    ax = plt.gca()
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    ax_sz = np.array([bbox.width, bbox.height])*fig.dpi
    ax_pos = np.array([bbox.x0, bbox.y0])*fig.dpi

    # Logo size in px
    file_name = str(Path(__file__).parent) + '\\lclogo.png'
    logo = Image.open(file_name)
    img_sz = logo.size

    if watermark_pos == 'center':
        scale_fac = np.min(fig_sz/img_sz)*0.7
        alpha_val = 0.075
    elif watermark_pos in ['lower-left', 'upper-left']:
        scale_fac = np.min(ax_sz/img_sz)*0.3
        alpha_val = 0.2

    logo = logo.resize(np.round(np.array(img_sz)*scale_fac).astype('int'))
    logo_sz = [logo.size[0], logo.size[1]]

    if watermark_pos == 'center':
        logo_pos = [(fig.bbox.xmax - logo_sz[0])/2,
                    (fig.bbox.ymax - logo_sz[1])/2]
    elif watermark_pos == 'lower-left':
        ofs = 0.3*np.min(logo_sz)
        logo_pos = [ax_pos[0]+ofs, ax_pos[1]+ofs]
    elif watermark_pos == 'upper-left':
        ofs = 0.3*np.min(logo_sz)
        logo_pos = [ax_pos[0]+ofs, ax_pos[1]+ax_sz[1]-logo_sz[1]-ofs]

    logo = np.array(logo).astype(np.float)/255
    fig.figimage(logo, logo_pos[0], logo_pos[1], alpha=alpha_val)


def hide_axes():
    """Hide X and Y axes in the current plot.

    Including tick marks and tick labels.
    """
    plt.tick_params(
        axis='both', which='both',
        bottom=False, top=False, left=False, right=False,
        labelleft=False, labelbottom=False)


def hide_xticklabels():
    """Hide X tick labels but keep the ticks."""
    plt.gca().axes.get_xaxis().set_ticklabels([])


def hide_yticklabels():
    """Hide Y tick labels but keep the ticks."""
    plt.gca().axes.get_yaxis().set_ticklabels([])


def set_ticks_inside():
    plt.gca().tick_params(axis='both', which='both', direction='in')


def align_outer_tick_labels(ax=None):
    """Align outer tick labels with axes edges.

    This prevents overlap between panels, especially for small figures."""
    xlabels = ax.get_xticklabels()
    if xlabels:
        xlabels[0].set_ha("left")
        xlabels[-1].set_ha("right")

    ylabels = ax.get_yticklabels()
    if ylabels:
        ylabels[0].set_va("bottom")
        ylabels[-1].set_va("top")


def add_symbol_text(xpos, ypos, val_str, symbol_sz=None, **kwargs):
    """Add text next to a symbol with spacing.

    Space between symbol and text is determined by converting the symbol size
    in pt**2 to mm, and then from mm to axis units. Text positioning next to
    the symbol is defined using va and ha arguments to plt.text. A space is
    added to the value string for a consistent gap between the symbol and the
    text at different symbol sizes.
    """
    # Add space to symbol text for propper alignment
    val_str = ' ' + val_str

    # Determine offset between symbol and text
    ofs = get_symbol_sz_axis(symbol_sz)

    if ofs is None:
        ofs = 0

    plt.text(
        xpos+ofs, ypos, val_str,
        bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': 0.75},
        zorder=0.9,
        **kwargs)


def plot_ellipse(center_point, width, theta0=None, c='w'):
    """Plot an ellipse on the current axes."""
    # Calculate ellipse
    th = np.linspace(0, 2*np.pi, 1000)
    cx = center_point[0]
    cy = center_point[1]
    wx = width[0]
    wy = width[1]
    a = np.max([wx, wy])
    b = np.min([wx, wy])
    ecc = np.sqrt(1 - (b/a)**2)
    r = b/np.sqrt(1-(ecc*np.cos(th))**2)/2

    if not theta0:
        theta0 = 0

    if theta0 < 0 and wx > wy:
        # TODO: A combination of positive or negative theta with either wx>wy
        # or wx<wy results in an ellipse which is rotated by 90 deg compared to
        # the fit. This is probably due to the fact that theta+pi/2 togetther
        # with a wx, wy swap produces the same fit.
        theta0 = -theta0
        temp = wx
        wx = wy
        wy = temp

    # Draw ellipse
    x = r * np.cos(th-theta0+np.pi/2) + cx
    y = r * np.sin(th-theta0+np.pi/2) + cy
    plt.plot(x, y, '-', c=c)

    # Draw ellipse axes
    r1 = np.array([wx/2.5, wy/2.5, wx/2.5, wy/2.5])
    r2 = np.array([wx/2, wy/2, wx/2, wy/2])
    th_ax = np.array([0, 0.5*np.pi, np.pi, 1.5*np.pi])

    x1_ax = r1 * np.cos(th_ax - theta0) + cx
    y1_ax = r1 * np.sin(th_ax - theta0) + cy
    x2_ax = r2 * np.cos(th_ax - theta0) + cx
    y2_ax = r2 * np.sin(th_ax - theta0) + cy

    for ind in range(len(x1_ax)):
        plt.plot([x1_ax[ind], x2_ax[ind]], [y1_ax[ind], y2_ax[ind]],
                 ls='-', c=c)


def plot_crosshair(center_point, sz=None, c=get_color('db')):
    """Plot a crosshair on the current axes."""
    if not sz:
        xl = plt.xlim()
        yl = plt.ylim()
        xspan = np.abs(xl[1] - xl[0])
        yspan = np.abs(yl[1] - yl[0])
        sz = np.mean([xspan, yspan])*0.10

    cx = center_point[0]
    cy = center_point[1]
    plt.plot([cx - sz/2, cx + sz/2], [cy, cy], c=c)
    plt.plot([cx, cx], [cy - sz/2, cy + sz/2], c=c)


def get_def_num_bins_bin_and_slice_data():
    """Return the default number of bins used in ``bin_and_slice_data()``."""
    return 500


def occurrence_plot(
        X, Y, sliced_data=None, num_slcs=None, extra_bin=None,
        show_avg_trace=True, yl=None, yl_frac=None, ymarker=None,  xlim=None,
        show_zero_line=True, show_unity_line=False, ymarker_label=None,
        round_auto_xlim=False, with_hist=True, target_hist_bins=256,
        show_title=True, title=None, xlabel=None, show_ylabel=True,
        ylabel=None, show_tltext=True, tltext=None, show_yticklabels=True,
        ignore_min_pts_limit=False, plot_sliced_data=True,
        with_histogram_dither=False, hist_dith_fac=4, hist_bin_size_fac=1,
        normalize_y_tick_labels_only=False, hist_ymarkers=None,
        show_legend=True, legend_loc='lower left',
        merge_slice_regions=False, force_plot_sample_trace=False,
        **kwargs):
    """
    Make a plot that maps the occurrence frequency of data samples to colour
    saturation so that more frequent data ranges appear darker.

    Some features, like histogram granularity and dithering only work if the Y
    data is not normalized. If normalize_y_tick_labels_only is true, the y axis
    tick labels are normalized instead to give the appearance of a normalized
    scale.
    TODO: integrate code from occurrence_plot2
    """

    vlvl = kwargs.get('verbosity')

    plot_sample_trace = False
    MIN_PTS_FOR_OCCURRENCE_PLOT = 5000
    if force_plot_sample_trace or \
            (isnone(sliced_data) and len(X) < MIN_PTS_FOR_OCCURRENCE_PLOT):
        if ignore_min_pts_limit:
            print("Number of points {:d} ".format(len(X)) +
                  "is likely too small to make an occurrence plot " +
                  "({:d} needed). ".format(MIN_PTS_FOR_OCCURRENCE_PLOT) +
                  "Ignore flag supplied so this limit is disregarded.")
        else:
            plot_sliced_data = False
            plot_sample_trace = True
            show_avg_trace = False
            if not force_plot_sample_trace:
                print("Number of points {:d} ".format(len(X)) +
                      "is too small to make an occurrence plot " +
                      "({:d} needed). ".format(MIN_PTS_FOR_OCCURRENCE_PLOT) +
                      "Will plot a sample trace instead.")

    if sliced_data is None:
        [Xb, Yb, Yb_lvls] = bin_and_slice_data(
            X=X, Y=Y, num_slcs=num_slcs, **kwargs)
        if Yb_lvls is not None and len(Yb_lvls.shape) > 1:
            num_lvls = int((Yb_lvls.shape[1]-1)/2)
    else:
        Xb = X
        Yb = Y
        Yb_lvls = sliced_data
        num_lvls = int((Yb_lvls.shape[1])/2)

        num_bins = kwargs.get('num_bins')
        if extra_bin is None and num_bins is not None \
                and len(Xb) > num_bins:
            print("{:d} graph points requested, but dataset has pre-sliced"
                  " data and {:d} rows. Sliced bins will be merged to "
                  "yield the requested graph points, but this is only "
                  "valid if the adjacent bins have similar "
                  "distributions".format(num_bins, len(Xb)))
            extra_bin = int(np.ceil(len(Xb)/num_bins))

        MAX_SLICED_LENGTH = 1000
        OPTIMAL_SLICED_LENGTH = 300
        if isnone(extra_bin) and len(Xb) > MAX_SLICED_LENGTH:
            print("Sliced dataset length is {:d} which larger than the maximum"
                  " {:d}".format(len(Xb), MAX_SLICED_LENGTH))
            extra_bin = int(len(Xb)/300)
            print("Optimal sliced length is {:d}, setting extra_bin "
                  "to {:d}".format(OPTIMAL_SLICED_LENGTH, extra_bin))

        if not isnone(extra_bin):
            Xb2 = []
            Yb2 = []
            Yb2_lvls = np.ndarray([
                int(np.ceil(Yb_lvls.shape[0]/extra_bin)), Yb_lvls.shape[1]])
            ind2 = 0
            for ind in range(0, len(Xb), extra_bin):
                Xb2.append(np.mean(Xb[ind:ind+extra_bin]))
                Yb2.append(np.mean(Yb[ind:ind+extra_bin]))
                Yb2_lvls[ind2, :] = np.mean(Yb_lvls[ind:ind+extra_bin, :], 0)
                ind2 += 1

            Xb = Xb2
            Yb = Yb2
            Yb_lvls = Yb2_lvls

    mean_y = np.nanmean(Y)

    if yl is None:
        # Determine Y display range
        if yl_frac:
            # If the display limits fraction is given, set the axis limits to
            # Â±fraction of the mean around the mean
            yl = [mean_y*(1-yl_frac), mean_y*(1+yl_frac)]
        else:
            # Otherwise set the axis limits to span the entire percentile range
            # with an extra 10%
            if Y is not None:
                yl = extend_range([
                    np.nanmin(Y), np.nanmax(Y)], 0.1)
            else:
                yl = extend_range([
                    np.nanmin(Yb_lvls), np.nanmax(Yb_lvls)], 0.1)

    plt.ylim(yl)

    if xlim is None:
        # Determine X axis limits automatically
        x_min = np.nanmin(X)
        x_max = np.nanmax(X)

        if round_auto_xlim:
            x_span = x_max - x_min

            # Round the limits to within 10% of the span. If the limits are
            # e.g. 0.0001 to 99.999, tick labels at 0 and 100 will not be shown
            # because they are outside of the axis limits. Rounding the limits
            # avoids that. The algorithm is a bit flaky and was tested only
            # for a few cases.
            if x_span > 10:
                sig_figs = int(np.round(np.log10(x_span))) - 1
            else:
                sig_figs = int(np.round(-np.log10(x_span/10))) + 1

            x_min = np.round(x_min, sig_figs)
            x_max = np.round(x_max, sig_figs)

        plt.xlim([x_min, x_max])
    else:
        plt.xlim(xlim)

    if show_zero_line and yl[0] < 0 and yl[1] > 0:
        add_y_marker(0, ls='-', zorder=0)

    if show_unity_line and yl[0] < 1.0 and yl[1] > 1.0:
        add_y_marker(1.0, ls='-', zorder=0)

    # Histogram bar color
    hist_color = matplotlib.cm.get_cmap('Blues')(0.95)

    # The medium red color (medium as in 'red' vs 'dr') works well with
    # nested slice regions since the innermost slice is dark blue. If
    # the slices are not shown, the medium red is still visible, but
    # dark blue works better together with the histogram.
    # So the average trace is medium red with sliced data, and dark blue when
    # on its own or when merge_slice_regions is enabled.
    avg_trace_color = hist_color

    if plot_sliced_data:
        min_cval = 0.1

        if merge_slice_regions:
            # The easiest way to merge all percentile regions is to for them
            # to have the same color
            max_cval = 0.1
        else:
            max_cval = 0.95
            avg_trace_color = get_color('red')

        lvls = np.linspace(min_cval, max_cval, num_lvls)
        cmap = matplotlib.cm.get_cmap('Blues')
        colors = cmap(lvls)

    if with_hist:
        grid = plt.GridSpec(1, 5, wspace=0.1, hspace=0.1)
        ax_trace = plt.subplot(grid[0, 0:4])
    else:
        ax_trace = plt.gca()

    legend_h = []
    legend_str = []

    plt.gca().set_axisbelow(True)

    if plot_sliced_data:
        for ind in range(0, num_lvls):
            ax_trace.fill_between(Xb, Yb_lvls[:, ind], Yb_lvls[:, -(ind+1)],
                                  color=colors[ind, :])

        # legend() does not support fill_between(), therefore two proxy artists
        # with first and last fill colors are used to represent it.
        legend_h.append((
            Rectangle((0, 0), 1, 1, fc=colors[0, :]),
            Rectangle((0, 0), 1, 1, fc=colors[-1, :])))
        legend_str.append('Percentile range')

    if show_avg_trace:
        h = plt.plot(Xb, Yb, color=avg_trace_color)
        legend_h.append(h[0])
        legend_str.append('Average')
        marker_color = get_color('darkred')

    if plot_sample_trace:
        h = plt.plot(X, Y, color=get_color('dr'))
        legend_h.append(h[0])
        legend_str.append('Sample')
        marker_color = get_color('black')



    xl = plt.xlim()

    if ymarker is not None:
        for ind, ym in enumerate(ymarker):
            h = plt.plot(xl, [ym, ym], ls='--', c=marker_color)
            if ind == 0:
                legend_h.append(h[0])
                if ymarker_label is not None:
                    legend_str.append(ymarker_label)
                else:
                    print("Y marker given, but no label specified, assuming it"
                          " is RSD range")
                    legend_str.append('Overall RSD range')

    if xlabel is not None:
        plt.xlabel(xlabel)

    if show_ylabel and ylabel is not None:
        plt.ylabel(ylabel)

    if show_title and title is not None:
        plt.title(title)

    if show_tltext and tltext is not None:
        ofs_x = (xl[1]-xl[0])*0.05
        ofs_y = (yl[1]-yl[0])*0.05

        plt.text(xl[0]+ofs_x, yl[1]-ofs_y, tltext, ha='left', va='top',
                 bbox=dict(facecolor='white', alpha=0.75,
                 edgecolor='white'))

    if not show_yticklabels:
        plt.gca().set_yticklabels([])

    if normalize_y_tick_labels_only:
        yticks = plt.yticks()[0]
        plt.yticks(yticks, np.round(yticks/mean_y, 2))
        plt.ylim(yl)

    plt.grid('on', which='both')

    if show_legend:
        plt.legend(legend_h, legend_str, numpoints=1, loc=legend_loc,
                   handler_map={tuple: HandlerTuple(ndivide=None)})

    plt.gca().tick_params(axis='both', which='both', direction='in')

    ax_hist = None
    if with_hist:
        ax_hist = plt.subplot(grid[0, 4])
        y_span = yl[1] - yl[0]
        y_gran = get_granularity(Y)

        y_units = 's'
        try:
            if ylabel:
                y_units = strip_whitespace(ylabel.split(',')[1])
        except Exception:
            y_units = ''
        printmsg('Y granularity is {:.2e} {:s}, '.format(y_gran, y_units) +
                 'scale range is {:.2f} bits'.format(np.log2(y_span/y_gran)),
                 'info', vlvl)

        unique_vals = np.unique(Y)

        if len(unique_vals) < target_hist_bins:
            # If the number of unique data values is less than the number of
            # target histogram bins the histogram can only shows the unique
            # data levels. This will usually result in a low-resolution
            # histogram.
            bins = hist_bin_centers_to_edges(unique_vals)
        else:
            num_hist_bins = y_span/y_gran
            y_grans_per_bin = np.max([
                np.round(num_hist_bins/target_hist_bins), 1])
            bins = np.arange(yl[0], yl[1],
                             y_gran*y_grans_per_bin*hist_bin_size_fac)

        num_bins = len(bins)

        if abs(len(bins)/target_hist_bins - 1) > 0.1:
            print("Number of histogram bins requested: {:d}, actual number is "
                  "{:d} due to Y data granularity".format(
                    target_hist_bins, num_bins))

        if with_histogram_dither:
            # Calculate histogram dithering array. Elements of the array are
            # drawn from a Gaussian distribution centered at 1. The width of
            # the distribution is such that after dithering about 50% of the
            # data values in one histogram bin spill into the adjacent bin.
            # The strength of the dithering effect can be controlled by chaning
            # the hist_dith_fac factor.
            bin_sz = bins[1] - bins[0]
            dith = np.random.normal(1, bin_sz/mean_y*hist_dith_fac, len(Y))
            print("Applying histogram dithering with a factor of "
                  "{:d}. ".format(hist_dith_fac) +
                  "This is an experimental feature, so you might want to "
                  "compare the histogram with and without dithering.")
        else:
            dith = 1

        plt.hist(Y*dith, bins=bins, orientation="horizontal",
                 color=hist_color, zorder=10)[0]

        if hist_ymarkers is not None:
            # Add histogram y markers
            for hist_ymarker in hist_ymarkers:
                add_y_marker(hist_ymarker, c=[0.75, 0.75, 0.75], ls='-',
                             zorder=1)

        if ymarker is not None:
            # Add y markers that are common for the histogram and the main
            # plot area
            for ym in ymarker:
                add_y_marker(ym, c=marker_color, zorder=20)

        plt.ylim(yl)
        plt.xticks([])
        plt.plot(plt.xlim(), [0, 0], color=[0, 0, 0, 0.25])
        ax_hist.axes.yaxis.set_ticklabels([])
        plt.gca().tick_params(axis='both', direction='in')
        plt.grid('on')

    return ax_trace, ax_hist


def occurrence_plot2(X, Y, num_slcs=None, show_avg_trace=False,
                     title=None, xlabel=None, ylabel=None):
    """
    Make a plot that maps the occurence frequency of data samples to colour
    saturation so that more frequent data ranges appear darker.
    TODO: needs to be integrated with occurrence_plot
    """

    [Xb, Yb, Yb_lvls] = bin_and_slice_data(X=X, Y=Y, num_slcs=num_slcs)
    num_lvls = int((Yb_lvls.shape[1]-1)/2)

    min_cval = 0.1
    max_cval = 0.95
    lvls = np.linspace(min_cval, max_cval, num_lvls)

    cmap = matplotlib.cm.get_cmap('Blues')

    colors = cmap(lvls)

    grid = plt.GridSpec(1, 5, wspace=0.1, hspace=0.1)

    ax_trace = plt.subplot(grid[0, 0:4])
    for ind in range(0, num_lvls):
        ax_trace.fill_between(Xb, Yb_lvls[:, ind], Yb_lvls[:, -(ind+1)],
                              color=colors[ind, :])

    if show_avg_trace:
        plt.plot(Xb, Yb, color=[255, 179, 179, 255]/255)

    plt.xlim([min(X), max(X)])
    plt.plot([min(X), max(X)], [0, 0], color=[0, 0, 0, 0.25])
    plt.ylim([-1, 1])
    if not isnone(xlabel):
        plt.xlabel(xlabel)

    if not isnone(ylabel):
        plt.ylabel(ylabel)

    if not isnone(title):
        plt.title(title)

    ax_hist = plt.subplot(grid[0, 4])
    bins = np.linspace(-1, 1, 256)
    plt.hist(Y, bins=bins, orientation="horizontal", color=colors[-1, :])

    plt.ylim([-1, 1])
    plt.xticks([])
    plt.plot(plt.xlim(), [0, 0], color=[0, 0, 0, 0.25])
    ax_hist.axes.yaxis.set_ticklabels([])


def block_map(
        int_img=None, map_img=None,
        int_file_name=None, map_file_name=None, int_rng=None, map_rng=None,
        cmap='hsv', log10int=False, map_type='block', show_hist=False):
    """Create a high-res image using a low-res value map.

    Create a full-resolution color-coded image shown a parameter distribution
    map when only a low-resolution map is available. If map_type is 'block' the
    color channels in the final images siply contain the parameter map pixelsas
    superpixels. If map_type is 'interp' the final image color values are
    interpolated from the map.

    The image is built using either simple HSV mapping or by applying a true
    RGB colormap. In either case, the final image in the HSV space has the
    full-res intensity image in the value channel, while the hue channel is
    built from the low-res parameter map, i.e. the image has different
    effective resolution in different channels. The saturation channel is
    constructed using nan values in the parameter map so that these areas
    appear grayscale in the final HSV image.

    RBG colormapping is experimental and will not work for all colormaps
    because the saturation and value channels are replaced rather than blended.
    For example, the 'cividis' colormap is rendered incorrectly.

    Copyright 2021 Lukas Kontenis
    Contact: dse.ssd@gmail.com
    """
    # Load intensity and value map images
    if int_img is None:
        int_img = image.open(int_file_name)

    if map_img is None:
        map_img = image.open(map_file_name)

    # Convert to numpy ndarrays
    int_img = np.array(int_img)
    map_img = np.array(map_img)

    if show_hist:
        # Show image and map histograms
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.hist(int_img.flatten(), 256, log=True)

        plt.subplot(1, 2, 2)
        plt.hist(map_img.flatten(), 256, log=True)

    if log10int:
        # Convert intensity to log10
        int_img = np.log10(int_img)
        int_img /= np.max(int_img)
    else:
        if int_rng is not None:
            # Cap intensity display values
            int_img = int_img/int_rng[1]
            int_img[int_img > 1] = 1

    if map_rng is not None:
        # Cap min/max map display values
        map_img = map_img - map_rng[0]
        map_img[map_img < 0] = 0
        map_img = map_img/(map_rng[1] - map_rng[0])
        map_img[map_img > 1] = 1

    # Create a map mask to indicate map blocks that are nan
    map_mask = np.empty_like(map_img)
    map_mask.fill(1)
    map_mask[np.isnan(map_img)] = 0

    # Set nan blocks in the map to 0
    map_img[np.isnan(map_img)] = 0

    num_row = int_img.shape[0]
    num_col = int_img.shape[1]

    # Create output hsv image
    img_hsv = np.ndarray([np.shape(int_img)[0], np.shape(int_img)[1], 3])
    img_rgb = np.empty_like(img_hsv)

    # Determine map bin size
    binsz = int(num_row/np.shape(map_img)[0])

    if map_type == 'block':
        for ind_row in range(num_row):
            map_row = int(np.floor(ind_row/binsz))
            map_cols = np.floor(np.arange(0, num_col)/binsz).astype('int')
            img_hsv[ind_row, :, 0] = map_img[map_row, map_cols]
            img_hsv[ind_row, :, 1] = map_mask[map_row, map_cols]

    elif map_type == 'interp':
        # Build X and Y index arrays for interplation functions
        xarr = np.arange(0, np.shape(map_img)[0])
        yarr = np.arange(0, np.shape(map_img)[1])

        # Define value map and mask interpolation functions
        map_func = interp2d(yarr, xarr, map_img)
        mask_func = interp2d(yarr, xarr, map_mask)

        # Calculate floating point index arrays for interpolation
        map_row_inds = np.arange(0, num_row)/binsz
        map_col_inds = np.arange(0, num_col)/binsz

        # Set the colour channel by interpolating low-res parameter map at the
        # full image resolution
        if cmap == 'hsv':
            # For HSV map just set the hue channel to the map values
            img_hsv[:, :, 0] = map_func(map_col_inds, map_row_inds)
        else:
            # For other colormaps use the map values as colormap indices and
            # generate an RGB image
            val = map_func(map_col_inds, map_row_inds)
            cmap_func = get_cmap(cmap)
            img_rgb[:, :, :] = cmap_func(val)[:, :, 0:3]

            # Then convert the image to HSV and replace saturation and
            # value channels by the mask and intensity
            img_rgb = image.fromarray(
                (img_rgb*255).astype('uint8'), mode='RGB')
            img_hsv = np.array(img_rgb.convert(mode='HSV'))/255

        # Interpolate map values and apply saturation mask
        img_hsv[:, :, 1] = mask_func(map_col_inds, map_row_inds)

    # Assign intensity channel
    img_hsv[:, :, 2] = int_img

    # Convert to 8-bit HSV image
    img_hsv = image.fromarray((img_hsv*255).astype('uint8'), mode='HSV')

    # Save
    file_name = 'image_out_' + map_type + '_' + cmap
    if log10int:
        file_name += '_log'
    else:
        file_name += '_lin'

    file_name += '.png'

    img_hsv.convert(mode='RGB').save(file_name)

    # Show
    plt.figure()
    plt.imshow(img_hsv)


def plot_linlog(xarr, yarr, xscale='lin', **kwargs):
    """Plot a trace on a lin or log scale."""
    if xscale == 'lin':
        return plt.plot(xarr, yarr, **kwargs)[0]
    elif xscale == 'log':
        return plt.semilogx(xarr, yarr, **kwargs)[0]
    else:
        print("Unknwon scale '{:s}'".format(xscale))


def long_term_stability_plot(X, Y, title=None, xlabel=None, ylabel=None,
                             ymarker=None, tltext=None, yl_min=0):
    marker_color = get_color('darkred')

    yl = [yl_min, np.max(Y)]

    min_cval = 0.1
    max_cval = 0.95
    lvls = np.linspace(min_cval, max_cval, 200)

    cmap = matplotlib.cm.get_cmap('Blues')

    colors = cmap(lvls)

    grid = plt.GridSpec(1, 5, wspace=0.1, hspace=0.1)

    ax_trace = plt.subplot(grid[0, 0:4])
    plt.plot(X, Y, color=colors[-1, :])

    plt.xlim([min(X), max(X)])
    plt.plot([min(X), max(X)], [0, 0], color=[0, 0, 0, 0.25])
    xl = plt.xlim()
#    for ym in ymarker:
#        plt.plot(xl,[ym,ym],'--', c=marker_color)
    plt.xlim(xl)
    plt.ylim(yl)

    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=13)

    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=13)

    if title is not None:
        plt.title(title, fontsize=13)

    if tltext is not None:
        ofs_x = (xl[1]-xl[0])*0.05
        ofs_y = (yl[1]-yl[0])*0.05
        plt.text(xl[0]+ofs_x, yl[1]-ofs_y, tltext, ha='left', fontsize=15)

    ax_hist = plt.subplot(grid[0, 4])
    y_span = yl[1] - yl[0]
    y_gran = get_granularity(Y)
    if y_span/y_gran < 256:
        bins = np.arange(yl[0], yl[1], y_gran)
    else:
        bins = np.linspace(yl[0], yl[1], 256)
    plt.hist(Y, bins=bins, orientation="horizontal", color=colors[-1, :])[0]
    xl = plt.xlim()

    plt.xlim(xl)

    plt.ylim(yl)
    plt.xticks([])
    plt.plot(plt.xlim(), [0, 0], color=[0, 0, 0, 0.25])
    ax_hist.axes.yaxis.set_ticklabels([])


def get_colormap(cmap=None):
    """Build a custom colormap.

    Default colormap names are passed though unaffected.
    """
    if cmap == 'lc':
        # Colormap used for beam profiles in LC.
        # Note that this colormap has been reconstructed for similar visual
        # appearance without the available colormap data.
        N = 5
        vals = np.ones((N, 3))
        vals[0, :] = hex2byte('29367d')/255
        vals[1, :] = hex2byte('85c1dc')/255
        vals[2, :] = hex2byte('98c06c')/255
        vals[3, :] = hex2byte('f0e936')/255
        vals[4, :] = hex2byte('c72c2f')/255

        cdict = {'red':   [[0.00, vals[0, 0], vals[0, 0]],
                           [0.25, vals[1, 0], vals[1, 0]],
                           [0.40, vals[2, 0], vals[2, 0]],
                           [0.60, vals[3, 0], vals[3, 0]],
                           [0.90, vals[4, 0], vals[4, 0]],
                           [1.00, vals[4, 0], vals[4, 0]]],
                 'green': [[0.00, vals[0, 1], vals[0, 1]],
                           [0.25, vals[1, 1], vals[1, 1]],
                           [0.40, vals[2, 1], vals[2, 1]],
                           [0.60, vals[3, 1], vals[3, 1]],
                           [0.90, vals[4, 1], vals[4, 1]],
                           [1.00, vals[4, 1], vals[4, 1]]],
                 'blue':  [[0.00, vals[0, 2], vals[0, 2]],
                           [0.25, vals[1, 2], vals[1, 2]],
                           [0.40, vals[2, 2], vals[2, 2]],
                           [0.60, vals[3, 2], vals[3, 2]],
                           [0.90, vals[4, 2], vals[4, 2]],
                           [1.00, vals[4, 2], vals[4, 2]]]}
        return LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)
    else:
        return cmap
