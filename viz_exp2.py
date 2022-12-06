import sys
from   pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import irfft, rfft, rfftfreq, fftshift
from math import e, pi, sin, floor

from bin_csv_utils import bin2csv

fig, axs = plt.subplots(3, 3)
n=500

for i in range(3):
    deg = sys.argv[1]
    signal = bin2csv(f"./exp_2_data/exp_rx_out_{deg}_{i}.bin")
    signal1_i = [i[0] for i in signal][:n]
    signal1_q = [i[1] for i in signal][:n]
    signal2_i = [i[2] for i in signal][:n]
    signal2_q = [i[3] for i in signal][:n]

    axs[0][i].plot( signal1_i)
    axs[0][i].plot( signal2_i)
    axs[0][i].set_title(f"Recieved RX1,2 | Trial - {i+1}")


    xf = rfftfreq(n, 1 / (31* 10**6))

    yf_s = rfft(signal1_i)
    axs[1][i].stem(xf, np.abs(yf_s))
    axs[1][i].set_title('RX1 (static) Signal in Frequency Domain!')

    yf_m = rfft(signal2_i)
    axs[2][i].stem(xf, np.abs(yf_m))
    axs[2][i].set_title('RX2 (moving) Signal in Frequency Domain!')

    # //deg
    print(yf_s)

    # div = np.divide(yf_m, yf_s)
    # idiv = irfft(div)
    # axs[3][i].plot(idiv)
    # axs[3][i].set_title('RXM/RXS Signal in Time Domain!')

plt.show()