"""lkcom - a Python library of useful routines.

This module contains string utilities. Many of these routines can probably be
replaced with better alternatives or even internal Python functions.

Copyright 2015-2023 Lukas Kontenis
Contact: dse.ssd@gmail.com
"""
import string
import pathlib
import numpy as np

import datetime

from lkcom.util import isnone, isarray, grep, msdo, warning_with_info, \
    handle_general_exception, find_closest


def strip_nonnum(s):
    return strip_alpha(strip_punctuation(strip_whitespace(s)))


def str_is_decimal_num(str):
    try:
        val = int(str)
        return True
    except Exception as excpt:
        return False


def strip_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))


def strip_alpha(s):
    return s.translate(str.maketrans('', '', string.ascii_letters))


def strip_whitespace(s):
    return s.translate(str.maketrans('', '', string.whitespace))


def whitespace_to_underscore(s):
    return s.replace(' ', '_')


def find_str_in_list(test_str, ref_str_arr, case_sensitive=False,
                     exact_match=True, return_match_index=False):
    """Find the index of a string that matches a list."""
    for ind, ref_str in enumerate(ref_str_arr):
        if not case_sensitive:
            test_str = test_str.lower()
            ref_str = ref_str.lower()

        if exact_match:
            if test_str == ref_str:
                if return_match_index:
                    return ind
                else:
                    return True
        else:
            if ref_str.find(test_str) != -1 or test_str.find(ref_str) != -1:
                if return_match_index:
                    return ind
                else:
                    return True

    if return_match_index:
        return None
    else:
        return False


def search_list_in_string(test_str, ref_str_arr, case_sensitive=False):
    for ind, ref_str in enumerate(ref_str_arr):
        if case_sensitive:
            if test_str.find(ref_str) != -1:
                return ind
        elif test_str.lower().find(test_str.lower()) != -1:
            return ind

    return None


def compare_str_to_list(test_str, ref_str_arr, case_sensitive=False):
    """Compare a string to a list of strings."""
    out = []
    for ref_str in ref_str_arr:
        if case_sensitive:
            if test_str == ref_str:
                out.append(True)
            else:
                out.append(False)
        else:
            if test_str.lower() == ref_str.lower():
                out.append(True)
            else:
                out.append(False)

    return out


def check_str_in_str(src_str, search_str, case_sensitive=False):
    """Check if a string contains a string with optional case sensitivity."""
    if(case_sensitive):
        if src_str.find(search_str) != -1:
            return True
    else:
        if src_str.lower().find(search_str.lower()) != -1:
            return True

    return False


def check_lstr_in_str(src_str, search_lst, **kwargs):
    """Check if a string contains a list of strings."""
    match_list = []
    for search_str in search_lst:
        match_list.append(check_str_in_str(src_str, search_str, **kwargs))

    return match_list


def get_extension(file_name):
    """Get file extension."""
    return pathlib.Path(file_name).suffix[1:]


def rem_extension(file_name):
    """Remove file extension."""
    return str(pathlib.Path(file_name).with_suffix(''))


def get_bare_file_name(file_path):
    """Get bare file name without slashes."""
    return str(pathlib.Path(file_path).stem)


def get_absolute_file_path(file_name):
    """Get the absolute path of a file."""
    return pathlib.Path(file_name).absolute()

def join_paths(path1, path2):
    """Join to strings treating them as paths."""

    # The naive string version of this in lklib was the following. It might
    # have been more clever than it sounds.
    # join_str = ''
    # if(path1[-1] != '/'):
    #     join_str = '/'
    # return path1 + join_str + rem_local_path_prefix(path2)

    return pathlib.Path(path1) / pathlib.Path(path2)


def change_extension(file_name, new_ext):
    """Change file extension."""
    return rem_extension(file_name) + new_ext


def split_nonalpha(s):
    from_pos = 0
    to_pos = 1
    chunks = []
    while to_pos < len(s):
        if(not s[to_pos].isalnum()):
            chunks.append(strip_punctuation(s[from_pos:to_pos]))
            from_pos = to_pos
        to_pos += 1

    return chunks


def string_with_units_to_float(s, units, unit_str=None):
    if(isnone(unit_str)):
        unit_str = s

    SI_preffix = unit_str[unit_str.find(units)-1]
    if(SI_preffix == 'k'):
        SI_fac = 1E3
    elif(SI_preffix == 'M'):
        SI_fac = 1E6
    else:
        SI_fac = 1

    # Replace comma as decimal separator
    s = s.replace(',', '.')

    try:
        return float(strip_alpha(s))*SI_fac
    except Exception:
        return None


def parse_num_by_preffix(s, preffix):
    """Parse a number in string by preffix."""

    chunks = split_nonalpha(s)

    sel_chunks, sel_chunk_inds = grep(chunks, preffix, return_inds=True)

    if(len(sel_chunks) == 0):
        return None
    sel_chunk = sel_chunks[0]
    sel_chunk_ind = sel_chunk_inds[0]

    if(len(strip_nonnum(sel_chunk)) == 0):
        return strip_nonnum(chunks[sel_chunk_ind+1])
    else:
        return strip_nonnum(sel_chunk)


def parse_num_by_units_name(s, units, split_token=None):
    """
    Parse a number of a complex string based on its units name. This should
    work for a unique number and unit pair with or without whitespace
    anywhere in any string.
    """
    if split_token is None:
        chunks = split_nonalpha(s)
    else:
        chunks = s.split(split_token)

    sel_chunks, sel_chunk_inds = grep(chunks, units, return_inds=True)

    if len(sel_chunks) == 0:
        return None
    sel_chunk = sel_chunks[0]
    sel_chunk_ind = sel_chunk_inds[0]

    if(len(strip_nonnum(sel_chunk)) == 0):
        units_chunk = sel_chunk
        num_chunk = chunks[sel_chunk_ind-1]
    else:
        units_chunk = sel_chunk
        num_chunk = sel_chunk

    if(len(strip_nonnum(num_chunk)) == 0):
        return None
    else:
        return string_with_units_to_float(num_chunk, units, units_chunk)


def multi_src_parse(val=None, src_arr=None, suffix=None, preffix=None,
                    split_token=None):
    """Parse a suffixed value from multiple strings."""
    try:
        if(not isnone(suffix) and not isarray(suffix)):
            suffix = [suffix]

        if(not isnone(preffix) and not isarray(preffix)):
            preffix = [preffix]

        val_arr = [val]
        for src in src_arr:
            if src is not None:
                if suffix is not None:
                    for sfx in suffix:
                        val_arr.append(parse_num_by_units_name(
                            src, sfx, split_token=split_token))
                if preffix is not None:
                    for pfx in preffix:
                        val_arr.append(parse_num_by_preffix(src, pfx))

        val_arr2 = []
        for val2 in val_arr:
            if(not(isnone(val2))):
                val_arr2.append(val2)
        val_arr = val_arr2

        if(len(val_arr) == 0):
            return None

        if(isnone(val)):
            val = val_arr[0]

        if(not all([val == v for v in val_arr])):
            warning_with_info("Not all parsed values are consistent")

        return val
    except Exception as excpt:
        print("Failed to parse string", excpt)
        return val


def multi_src_match(output_str=None, src_arr=None, match_arr=None):
    """Match multiple strings to an array of possible values."""
    output_str_arr = [output_str]
    for src in src_arr:
        if(not isnone(src)):
            ind = search_list_in_string(src, match_arr)
            if(not isnone(ind)):
                output_str_arr.append(match_arr[ind])

    ar = []
    for s in output_str_arr:
        if(not(isnone(s))):
            ar.append(s)
    output_str_arr = ar

    if(len(output_str_arr) == 0):
        return None

    if(isnone(output_str)):
        output_str = output_str_arr[0]

    if(not np.all(output_str_arr == output_str)):
        warning_with_info("Not all parsed values are consistent")

    return output_str


def parse_timestamp_str(t_str):
    """Parse timestamp string.

    Format a filename-safe timestamp string 'HH_MM_SS_.mmm_' to a nicer form
    'HH:MM:SS.mmm'.

    NOT: this function was called format_timestamp_string, but was renamed to
    not be confused with format_timestamp_into_string.
    """

    pieces = t_str.split('_')
    [HH, MM, SS, mmm] = pieces[0:3]
    mmm.strip('.')

    return (HH + ':' + MM + ':' + SS + '.' + mmm)


def timestamp_str_to_seconds(ts_str):
    """
    Convert a timestamp string to seconds. Everything up to the hours is
    ignored.
    """

    ts_str = ts_str.strip('"')

    S = ts_str.split(' ')

    hour_part = S[1]

    # Calculating the number of days between any two months in a given year is
    # tricky. There's probably a standard function to do that.

    [hour_part, ms_str] = hour_part.split('.')

    ms = int(ms_str[:-1])

    [h_str, m_str, s_str] = hour_part.split(':')

    s = int(s_str)
    m = int(m_str)
    h = int(h_str)

    ts = s + (m+h*60)*60 + ms/1000

    return ts


def make_human_time_str(t):
    """
    Make a human-readable time string from a floating-point time value
    in seconds.
    """
    if(t > 60):
        return '{:.3g} min'.format(float(t)/60)
    else:
        return '{:.3g} s'.format(t)


def safe_str_format(val, fmt='{:}', missing_str='---'):
    """Format a value to string with safe None handling."""

    return fmt.format(val) if val is not None else missing_str


def get_val_si_order(val, override_order=None, suppress_suffix=''):
    """ Find the best SI suffix for a number.

    Find the most appropriate SI suffix for a number that would leave it's
    numeric part between 1 and 1000. E.g. 1.5M for 1.5E6. Use
    ``override_order`` to suppress certain suffixes - the exponent in the
    first column will be replaced with the one from the second. E.g. to
    get 0.001 instead of 1m set ``override_order`` to [-3, 0], to get 0.002M
    instead of 2k set it to [3, 6].
    """
    abs_val = round_to_sig_fig(np.abs(val), 3)
    if(abs_val >= 1E6):
        val_order = 6
    elif(abs_val >= 1E3):
        val_order = 3
    elif(abs_val >= 1 or abs_val < np.finfo(float).eps):  # Include zero value
        val_order = 0
    elif(abs_val > 1E-3):
        val_order = -3
    elif(abs_val > 1E-6):
        val_order = -6
    elif(abs_val > 1E-9):
        val_order = -9
    elif(abs_val > 1E-12):
        val_order = -12
    elif(abs_val > 1E-15):
        val_order = -15
    elif(abs_val > 1E-18):
        val_order = -18
    else:
        warning_with_info("Could not determine the SI order of the number")
        val_order = 0

    if suppress_suffix == 'm':
        if override_order is None:
            override_order = [-3, 0]
        else:
            print('Need to implement override_order with suppress_suffix')

    if(not isnone(override_order)):
        if len(np.shape(override_order)) == 1:
            override_order = [override_order]
        override_order = np.array(override_order)
        ind = np.squeeze(np.where(override_order[:, 0] == val_order))
        # ind = override_order[:, 0].index(val_order)
        if(not isnone(ind)):
            val_order = override_order[ind, 1]

    return val_order


def get_si_suffix(num_order):
    """Get the SI suffix of an order."""
    if(num_order == 9):
        return 'G'
    elif(num_order == 6):
        return 'M'
    elif(num_order == 3):
        return 'k'
    elif(num_order == 0):
        return ''
    elif(num_order == -3):
        return 'm'
    elif(num_order == -6):
        return 'u'
    elif(num_order == -9):
        return 'n'
    elif(num_order == -12):
        return 'p'
    elif(num_order == -15):
        return 'f'
    else:
        warning_with_info("Preffix undefined for SI order {:d}".format(
            num_order))


def round_to_sig_fig(val, sig_fig):
    msdo_val = msdo(val)
    return np.round(
        val / 10**msdo_val * 10**(sig_fig-1)) / 10**(sig_fig-1) * 10**msdo_val


def get_human_val_and_err_str(
        val=None, err=None, num_err_sig_fig=1, fixed_width_sign=False,
        suppress_err=False, max_abs_value=None,
        min_abs_val=None, typ_val=None, min_err=None,
        round_val_to_err_sig_fig=True, round_val_to_err_sig_fig_thr=0.5,
        print_approximation_details=False, **kwargs):
    """Convert a numer and its error to a human-readable string.

    Make a human readable string for a value with error, e.g.
    15±2 M instead of val = 15.2145E6, err = 1.9586E6.

    If ``max_abs_val`` is given and ``val`` is larger than that,
    a '>max_abs_val' string is returned. If ``min_abs_val`` is given and
    ``val`` is less than that, a '~0' string is returned. If ``typ_val`` is
    given and ``val`` is equal to it within error, a '~typ_val'  string
    is returned.
    """
    # Handle array input
    if(isarray(val)):
        output = []
        for ind, v in enumerate(val):
            # TODO: Implement argument passing
            warning_with_info("Feature not fully implemented")
            output.append(get_human_val_and_err_str(v, err[ind]))
        return output

    try:
        if(np.isnan(val)):
            return 'NaN'

        # Get the most significant digit orders for value and error
        msdo_val = msdo(val)
        msdo_err = msdo(err)

        if(msdo_val > msdo_err):
            num_sig_fig = msdo_val - msdo_err + num_err_sig_fig
            order = get_val_si_order(val, **kwargs)
        else:
            num_sig_fig = num_err_sig_fig
            order = get_val_si_order(err, **kwargs)
            if(abs(val*10**num_err_sig_fig) < abs(err)):
                v = 0

        if round_val_to_err_sig_fig and msdo_val < msdo_err \
                and np.abs(val/err) <= round_val_to_err_sig_fig_thr:
            val = round_to_sig_fig(val, np.abs(msdo_err))

        sfx = get_si_suffix(order)

        fmt_val = {
            "num_sig_fig": num_sig_fig, 'str_order': order,
            "show_suffix": False, "fixed_width_sign": fixed_width_sign,
            "suppress_suffix": kwargs.get('suppress_suffix')}

        fmt_err = {
            "num_sig_fig": num_err_sig_fig, 'str_order': order,
            "show_suffix": False, "fixed_width_sign": False,
            "suppress_suffix": kwargs.get('suppress_suffix')}

        if not isnone(typ_val) and np.abs(val) < np.abs(err):
            # If value is close to typical, print it as '~typ'
            str = "~" + get_human_val_str(typ_val, num_sig_fig=2)
            approx = True
        elif not isnone(max_abs_value) and np.abs(val) > max_abs_value:
            # If value is greater than the maximum expected, print it as `>max'
            str = ">" + get_human_val_str(max_abs_value, num_sig_fig=2)
            approx = True
        elif not isnone(min_abs_val) and np.abs(val) < min_abs_val:
            # If value is less than the minimum expected, print it as '~0'
            str = '~0'
            approx = True
        else:
            # Otherwise format value and error normally
            str = get_human_val_str(val, **fmt_val)

            if not suppress_err:
                str += " ±" + get_human_val_str(err, **fmt_err)

            if not isnone(sfx):
                str += sfx
            approx = False

        if approx and print_approximation_details:
            # TODO:
            warning_with_info("Feature not fully implemented")
            str += " (", get_human_val_and_err_str(val, err) + ")"

    except Exception:
        warning_with_info("Parsing failed")
        str = "{:g} ±{:g}".format(val, err)

    return str

def get_human_readable_time_mult_suffix(val):
    """Get human readable multiplier and suffix for time."""
    if val > 3600:
        mult = 3600
        suffix = 'h'
    elif val > 120:
        mult = 60
        suffix = 'min'
    elif val > 1:
        mult = 1
        suffix = ''
    return [mult, suffix]

def get_human_val_str(
        val, num_sig_fig=2, num_decimal_places=None, str_order=None,
        space_before_suffix=False, is_time=False, fixed_width_sign=False,
        fixed_str_len=None,  show_suffix=True,
        min_abs_value=None, below_min_val_str='~0', trim_decimal_zeros=False,
        limit_decimal_places_to_num_sig_fig=False,
        limit_min_order_to_num_sig_fig=False, **kwargs):
    """Convert numbers to human-readable strings.

    Convert numbers to human-readable strnigs with SI suffixes, e.g. 15M, 100k,
    65u.

    Args:
        limit_decimal_places_to_num_sig_fig (bool): Treat a decimal 0 as a
            significant figure.
        limit_min_order_to_num_sig_fig (bool): Values of order smaller than
            ``num_sig_fig`` will be turned to '0'.
        fixed_width_sign (bool): Append a space to positive number strings.
        below_min_val_str (str): Use this string for values smaller than
            ``min_abs_val``
    """
    # If val is a classVE instance, GetHumanReadableValAndErr should be used

    # Gracefully handle None input
    if val is None:
        return ''

    min_order = None
    if limit_min_order_to_num_sig_fig:
        min_order = - num_sig_fig

    # varargin = RemArg(varargin, { 'NumSigFig',
    # 'LimitDecimalPlacesToNumSigFig', ...
    #    'LimitMinOrderToNumSigFig', 'Order', 'ShowSuffix',
    # 'MaxDecimalPlaces', ...
    #   'FixedWidthSign', 'MinAbsValue', 'TypicalValue',
    # 'PrintApproximationDetails' });

    suffix = ''
    mult = 1
    try:
        # Strings for trivial cases
        if np.isinf(val):
            # Value is infinity
            output_str = 'Inf'
        elif np.isnan(val):
            # Value is NaN
            output_str = 'NaN'
        elif val == 0:
            # Value is ecactly zero
            output_str = '0'
        elif not isnone(min_abs_value) and abs(val) < min_abs_value:
            # An expected minimum value is set and the given value is below it.
            output_str = below_min_val_str
        else:
            output_str = None

        if output_str is None and num_decimal_places is not None:
            fmt_str = "{:." + "{:d}".format(num_decimal_places) + "f}"
            output_str = fmt_str.format(val)

        if output_str is None:
            # Get the SI order of the number
            if(isnone(str_order)):

                str_order = get_val_si_order(val, **kwargs)
                suffix = get_si_suffix(str_order)
                mult = 10**str_order

                # Time is different, because it's minutes and hours rather than
                # kiloseconds. Override the multiplier and suffix if a number
                # representing time is large, but use SI suffixes below a
                # second.
                if(is_time):
                    [mult, suffix] = get_human_readable_time_mult_suffix(val)
            else:
                suffix = get_si_suffix(str_order)
                mult = 10**str_order

            val_order = msdo(val)

            # Get the digits part of the output number string
            output_val = val/mult

            if(not isnone(min_order) and val_order < min_order):
                return '0'

            # Determine the number of digits before the comma – nd1
            #
            # To find the number of digis, the output value is divided by
            # increasing orders of ten until the remainder equals the original
            # value.The absolute value is taken because the modulus returned
            # has the same sign as the divisor.
            nd1 = 0
            while(np.mod(abs(output_val), 10**nd1) != abs(output_val)):
                nd1 = nd1 + 1

            # If the number of sig figs before the comma exceeds the total
            # requested number o sig figs, the output string will have no comma
            # and no digits after it, and the number will be rounded to the
            # requested number of sig figs
            if nd1 >= num_sig_fig:
                nd2 = 0
                output_val = round(
                    output_val/10**(nd1 - num_sig_fig)*10**(nd1 - num_sig_fig))

                # Calculate back the unscaled original value
                val_check = output_val*mult

                # If the suffix order of the rounded value has changed, call
                # the function recursivelly to get the human-readable value
                # TODO: This seems to be more complicated than it needs to be
                # if(get_val_si_order(val, **kwargs) != str_order):
                #    return get_human_readable_str(val_check, **kwargs)
            else:
                # Digits after the comma to be included in the number of sig
                # figs calculation. This is the tricky bit.

                # If the number of sig figs before the coma is zero, there may
                # still be zeros after the comma which don't count as sig figs,
                # for example the number 0.0023 is given with two sig figs,
                # even though there are four digits after the comma

                if 0 and val_order < 0:
                    # Not sure what this was handling but it doesn't work for
                    # small numbers with val_order < -3
                    nd2 = -val_order - 1 + num_sig_fig
                else:
                    nd2 = num_sig_fig - nd1

                # nd2 = str_order - val_order + (num_sig_fig-1)
                if(limit_decimal_places_to_num_sig_fig and nd2 > num_sig_fig):
                    nd2 = num_sig_fig

            # Build a human-readable value
            output_str = ("{:." + "{:d}f".format(int(nd2)) + "}").format(
                output_val)

        if trim_decimal_zeros:
            output_str = str_trim_decimal_zeros(output_str)

        if show_suffix:
            if space_before_suffix:
                output_str += ' '
            output_str = output_str + suffix
    except Exception:
        warning_with_info("Parsing of number {:g} failed".format(val))
        output_str = "{:g}".format(val)

    if fixed_width_sign and val >= 0:
        output_str = ' ' + output_str

    if fixed_str_len:
        pad_str = ''
        for ind in range(fixed_str_len - len(output_str) + 1):
            pad_str += ' '
        output_str = pad_str + output_str

    if is_time and mult < 60:
        output_str = output_str + 's'

    return output_str


def arr_summary_str(arr, **kwargs):
    """Print a one-line summary string for an array."""
    mean_val = np.nanmean(arr)
    std_val = np.nanstd(arr)
    min_val = np.nanmin(arr)
    max_val = np.nanmax(arr)
    if std_val < mean_val/1E6:
        return "mean: " + get_human_val_str(mean_val, **kwargs) + \
               ", all values the same"
    else:
        return "mean: " + get_human_val_str(mean_val, **kwargs) + \
               ", min: " + get_human_val_str(min_val, **kwargs) + \
               ", max: " + get_human_val_str(max_val, **kwargs)


def str_trim_decimal_zeros(s):
    """Trim decimal zeros from a number string.

    Remove zeros after the decimal point from a string representing a number
    so that a '2.000' string becomes '2' and a '2.010' becomes '2.01'

    """
    sa = s.split('.')

    # The string has no decimal part
    if(len(sa) == 1):
        return sa[0]

    s1 = sa[0]
    s2 = sa[1]

    # Reversed returns an object, joining to an empty string makes it a string
    # again
    for ind, c in enumerate(''.join(reversed(s2))):
        # Now iterating over the string in reverse
        if(c == '0'):
            # Skip over zeros
            continue
        else:
            # Return the final string with the zeros trimed
            return s1 + '.' + s2[:len(s2)-ind]

    # The decimal string portion was all zeros
    return s1


def str_to_wavelength_rng(s):

    if(isarray(s)):
        rng_out = []
        for s1 in s:
            rng_out.append(str_to_wavelength_rng(s1))

        return rng_out

    ind = s.find("BP")
    if(ind >= 0):
        ind2 = s.find("-")
        l_c = float(s[ind+2:ind2])
        l_bw = float(s[ind2+1:])
        return [l_c-l_bw/2, l_c+l_bw/2]

    ind = s.find("LP")
    l_min = None
    if(ind >= 0):
        ind2 = ind + 2 + 3
        l_min = float(s[ind + 2:ind2])

    ind = s.find("SP")
    l_max = None
    if(ind >= 0):
        ind2 = ind+2+3
        l_max = float(s[ind + 2:ind2])

    if(not isnone(l_min) and isnone(l_max)):
        return [l_min, np.Inf]

    if(isnone(l_min) and not isnone(l_max)):
        return [-np.Inf, l_max]

    if(not isnone(l_min) and not isnone(l_max)):
        return [l_min, l_max]

    return None


def str_to_wavelength_rng_str(s):

    if(isarray(s)):
        s_out = []
        for s1 in s:
            s_out.append(str_to_wavelength_rng_str(s1))

        return s_out

    rng = str_to_wavelength_rng(s)
    if(isnone(rng)):
        return s

    if np.isinf(rng[1]):
        return ">%0.f nm".format(rng[0])

    if(np.isinf(rng[0])):
        return ">%0.f nm".format(rng[1])

    return "%.0f - %.0f nm".format(rng[0], rng[1])


def wavelength_str_to_color(s):
    if(isarray(s)):
        c_arr = []
        for s1 in s:
            c_arr.append(wavelength_str_to_color(s1))

        return c_arr

    rng = str_to_wavelength_rng(s)

    if(isnone(rng)):
        return "k"

    avg_val = np.mean(rng)

    c_str = 'tab:purple', 'tab:blue', 'tab:cyan', 'tab:green', 'tab:orange',
    'tab:red', 'tab:pink', 'tab:brown'
    c_avg = 350, 430, 470, 530, 575, 650, 700, 850

    return c_str[find_closest(c_avg, avg_val)]
