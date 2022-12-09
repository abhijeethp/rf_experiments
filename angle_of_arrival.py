from math import pi, acos, degrees, radians
from scipy.fft import rfft, rfftfreq, fftshift
import numpy as np

def phase_delta(sig_i1, sig_q1, sig_i2, sig_q2, wavelength):
    yf_s = rfft(sig_i1)
    max_yf_s_pos =  np.argmax(np.abs(yf_s))
    phase_s = np.angle(yf_s[max_yf_s_pos])

    yf_m = rfft(sig_i2)
    max_yf_m_pos =  np.argmax(np.abs(yf_m))
    phase_m = np.angle(yf_s[max_yf_m_pos])
   
    phase_delta = phase_m - phase_s
    return phase_delta if phase_delta > 0 else 2 * pi + phase_delta

def get(signal, wavelength, d):
    sig_i1 = [i[0] for i in signal]
    sig_q1 = [i[1] for i in signal]
    sig_i2 = [i[2] for i in signal]
    sig_q2 = [i[3] for i in signal]
    return get(sig_i1, sig_q1, sig_i2, sig_q2, wavelength, d)

def get(sig_i1, sig_q1, sig_i2, sig_q2, wavelength, d):
    phase_diff = phase_delta(sig_i1, sig_q1, sig_i2, sig_q2, wavelength)
    aoa = acos(wavelength * phase_diff / (2 * pi * d))
    return aoa

