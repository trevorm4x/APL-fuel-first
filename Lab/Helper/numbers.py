from uncertainties import ufloat
from scipy.signal import find_peaks, peak_widths
import numpy as np

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

def print_unc(val, unc = []):
    if isinstance(unc, list):
        val, unc = val.n, val.s
    dig = get_leading_figure(unc)

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

def peak(a, n_peaks, prominence=1000, height=1):
    peaks, peak_dict = find_peaks(a, prominence=prominence, height=height)
    heights = peak_dict['peak_heights'].tolist()
    peaks = peaks.tolist()
    inds = []
    bigheights = []
    for i in range(n_peaks):
        if len(heights):
            peak_num = heights.index(max(heights))
            inds.append(peaks.pop(peak_num))
            bigheights.append(heights.pop(peak_num))
    return inds, bigheights

def halfmax(a, peak_inds):
    return peak_widths(a, peak_inds, .5)

