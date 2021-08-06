import numpy as np
from numpy import fft as fft
import scipy.integrate as intgr


# Computing Library for signals: 1D or 2D 
# 2D would comprise of an x- and y-axis (time / value)

"""
if the array is "discontinuous" (i.e. NaN values occur)
the function will fill in the NaN values with linear 
interpolation between surroudning points
"""
def fill_nan(signal):
    
    try:
        signal_copy = np.copy(signal)
        nan_idx = np.isnull(signal_copy)
        good_idx = np.logical_not(nan_idx)
        good_data = signal_copy[good_idx]

        interpolated = np.interp(nan_idx.nonzero()[0], 
                                good_idx.nonzero()[0], 
                                np.array(good_data, dtype='float64'))
        second_copy = signal_copy
        second_copy[nan_idx] = interpolated
        return second_copy
    except ValueError:
        print("Error in filling the NaNs")


"""
replaces signal values greater than hcut with NaN values
& fills them with linear interpolation
"""
def highcut(signal, hcut):
    a = np.copy(signal)
    a = np.where(a > hcut, a, np.nan)
    return fill_nan(a)



"""
shorthand for np.concatenate((left , right))
"""
def connect(left , right): # shorthand for np.concatenate
    # only works with 2 arrays
    return np.concatenate((left , right))


"""
computes baseline of signal, possibly pre-trigger / stimulus
from t=0 to endpoint, which is decided by the user
"""
def compute_baseline(signal, endpoint):
    if (endpoint >= len(signal)):
        print("Endpoint for baseline out of bounds")
    else:
        return np.mean(signal[:endpoint])


"""
all values of returned array are now in [1.0, -1.0], 
where 1.0 === baseline
"""
def normalize(signal, baseline):
    return signal / baseline


"""
Smoothens array through Fourier Filtering

"""
def fourier_filter(signal, fcut, samples_to_add=2000):

    # padding on both sides for better result
    left_pad = np.ones(samples_to_add)*signal[0]
    right_pad = np.ones(samples_to_add)*signal[-1]

    # new padded signal
    left_padded = connect(left_pad, signal)
    padded = connect(left_padded, right_pad)

    total_samples = padded.shape[0]

    # ensure that the number of samples is even, for shifting issues
    if total_samples %2 != 0:
        total_samples -=1
        padded = padded[:-1]

    # zero pad for the filter
    zero_pad = np.zeros(int(total_samples/2 - fcut))

    # linear filter. does __/\__ around zero
    filter = np.concatenate((zero_pad,
                                np.linspace(0, 1, fcut),
                                np.linspace(1, 0, fcut),
                                zero_pad))

    ft = np.fft.fft(padded)
    ftshifted = np.fft.fftshift(ft)

    assert(ftshifted.shape[0] == ft.shape[0]) # ensure same length for filter multiplication

    # applying filter by broadcasting
    filtered = (ftshifted * filter)
    filtered_shiftback = fft.ifft(fft.fftshift(filtered))

    # truncating to the original signal
    return filtered_shiftback[samples_to_add:-samples_to_add]
