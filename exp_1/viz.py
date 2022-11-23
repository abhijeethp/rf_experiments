from scipy.fft import rfft, rfftfreq, fftshift
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter as fmt
from math import e, pi, sin, cos, floor

import sys

def window(X, lower_prcnt, upper_prcnt):
    n = X.size
    lower_index = int(n * lower_prcnt)
    upper_index = int(n * upper_prcnt)
    return X[lower_index : upper_index]

def w(X):
    return window(X, 0.25, 0.253)

pb_freqs = {
    "1 GHz": 0,
    "1.8 GHz":3,
    "2 GHz":6,
    "3 GHz" :9,
}
pb_freq = sys.argv[1]
bb_freq = [1, 5, 10]
sampling_duration_ms = 1   # milliseconds
sample_rate = 60 * 10**3   # samples / milliseconds
num_samples = int(sampling_duration_ms * sample_rate)

files = [pb_freqs[pb_freq]] # BB_FREQ : 1K
files += [files[-1] + 1]    # BB_FREQ : 5K
files += [files[-1] + 1]    # BB_FREQ : 10K

fig, axs = plt.subplots(2, 3)
fig.suptitle(f'Passband Frequency : {pb_freq}')
fig.tight_layout()

for i, f in enumerate(files):
    csv = np.genfromtxt(f"{f}.csv", delimiter=',').T
    Y_i, Y_q = csv[0], csv[1]
    Y = Y_i + Y_q * 1j
    T = np.linspace(0, sampling_duration_ms, num_samples)


    axs[0, i].plot(w(T),w(Y_i))
    axs[0, i].plot(w(T),w(Y_q))
    axs[0, i].set_title(f"Baseband Frequency : {bb_freq[i]}K")
    axs[0, i].set_xlabel("Time (ms)")
    axs[0, i].set_ylabel("Amplitude (?)")
    axs[0, i].xaxis.set_major_formatter(fmt('%.4f'))


    Yf_i = rfft(Y_i)
    Xf = rfftfreq(num_samples, 1/ (sample_rate * 10**3)) / 10**6
    axs[1, i].plot(Xf, np.abs(Yf_i))
    axs[1, i].set_title('Signal in Frequency Domain')
    axs[1, i].set_xlabel("Frequency (KHz)")
    axs[1, i].set_ylabel("Amplitude (?)")

plt.show()
