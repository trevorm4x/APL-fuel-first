from uncertainties import ufloat
from scipy.signal import find_peaks, peak_widths
import numpy as np
import pandas as pd

def get_leading_figure(unc):
    sci = str(unc).split('e')
    if len(sci) > 1:
        dig = -int(sci[-1])
    else:
        sp = str(unc).split('.')
        if len(sp) > 1:
            if int(sp[0]) > 0:
                decimal = False
            else:
                decimal = True            
        else:
            decimal = True

        if decimal:
            te = unc
            dig = 0
            while te < 1:
                te *= 10
                dig += 1

        else:
            te = unc
            dig = 0
            while te > 10:
                te /= 10
                dig -= 1
    return dig

def print_unc(val, unc = [], bprint = True):
    if isinstance(unc, list):
        val, unc = val.n, val.s
    dig = get_leading_figure(unc)
    if bprint:
        print("{:.{}f} +- {:.{}f}".format(val, dig, unc, dig))
    return np.round(val, dig), np.round(unc, dig), dig

def fft_filter(a, freq=.007):
    ruby_fft = np.fft.fft(a)
    freqs = np.fft.fftfreq(len(a))
    ruby_fft[np.where(abs(freqs) > freq)] = 0
    newby = np.fft.ifft(ruby_fft)
    return [n.real for n in newby]

def moving_avg_filter(a, bucket = 30):
    newby = [a.loc[0 if i-bucket//2 < 0 else i-bucket//2: i+bucket//2].mean()
             for i in range(len(a))]
    return newby

def peak(a,
        n_peaks,
        prominence=1000,
        height=1,
        threshold=100,
        distance=None,
        indeces=[]):

    peaks, peak_dict = find_peaks(
            a,
            prominence=prominence,
            height=height,
            distance=distance,
            threshold=threshold)

    heights = peak_dict['peak_heights'].tolist()
    peaks = peaks.tolist()
    inds = []
    bigheights = []

    for i in range(n_peaks):
        if len(heights):
            peak_num = heights.index(max(heights))
            inds.append(peaks.pop(peak_num))
            bigheights.append(heights.pop(peak_num))

    if len(indeces) == len(a):
        sample_width = indeces[1] - indeces[0]
        # inds = [i * sample_width + indeces[0] for i in inds]
        lengths = indeces[inds]
    else:
        lengths = inds
    return lengths, bigheights, inds

def halfmax(a, peak_inds):
    return peak_widths(a, peak_inds, .5)

def rising_edge(sig, times, first = False):

    if not first:
        max_ind, max_val = sig.idxmax(), sig.max()
    if first:
        inds, heights, _ = peak(sig, 177, 0, 0, 0)
        firstloc = inds.index(min(inds))
        max_ind, max_val = inds[firstloc], heights[firstloc]
    this_ind, this_val = max_ind, max_val
    next_ind = max_ind - 2
    next_val = sig[next_ind]

    while this_val - next_val > 0:
        this_ind = next_ind
        this_val = next_val
        next_ind -= 1
        if next_ind == -1:
            break
        next_val = sig[next_ind]

    start_ind = this_ind
    end_ind = max_ind

    rising_slice = sig[start_ind:end_ind]
    ran = rising_slice.tolist()[-1] - rising_slice.tolist()[0]
    ten = rising_slice.tolist()[0] + .1*ran
    ninety = rising_slice.tolist()[-1] - .1*ran
    ten_ind = rising_slice[rising_slice < ten].index[-1]
    ninety_ind = rising_slice[rising_slice < ninety].index[-1]
    rising_time = times[ninety_ind] - times[ten_ind]
    print("10-90 time", rising_time)

    return [[start_ind, end_ind], [ten_ind, ninety_ind]]

def fft(signal, t, order=None, magnitude=True, shift=True, window="hamming"):
    """
    Performs an fft and returns coefs and freqs
    """
    n = signal.shape[0]
    if order is not None:
        if signal.shape[0] < 2**order:
            n = 2**order

    sample_rate = t[1] - t[0]

    if window=='hamming':
        signal = signal.copy() * np.hamming(signal.shape[0])

    coefs = np.fft.fft(signal, n)
    freqs = np.fft.fftfreq(n, sample_rate)

    if magnitude:
        coefs = np.abs(coefs)

    if shift:
        coefs = np.fft.fftshift(coefs)
        freqs = np.fft.fftshift(freqs)

    return coefs, freqs

def read_scope_csv(path, n_sigs = 1, skiprows=0):
    ret = []
    for n in range(n_sigs):
        config = pd.read_csv(
                path,
                header=None,
                usecols=[1+6*n, 2+6*n],
                skiprows=skiprows
                ).loc[:2]
        config = [record_length, sample_interval, trigger_point] = [
            [float(val), unit] for val, unit in zip(config[1+6*n], config[2+6*n])]
        config= {
            'record_length': record_length,
            'sample_interval': sample_interval,
            'trigger_point': trigger_point
        }
        display(config)
        data = pd.read_csv(
                path, header = None, usecols=[3+6*n, 4+6*n], skiprows=skiprows
                ).loc[:2047]
        data.columns = ['ts', 'mV']
        ret.append([data, config])
    
    return ret
