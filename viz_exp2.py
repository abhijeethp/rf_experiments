import sys
from   pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import irfft, rfft, rfftfreq, fftshift
from math import e, pi, sin, floor

from bin_csv_utils import bin2csv
from config import config

rx_config = config()

def num_samples():
    return int(rx_config["samplerate"] * rx_config["duration_s"])

def cart2pol(x,y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho,phi

fig, axs = plt.subplots(3, 3)
n = int(620000 / 100)
for i in range(3):
    deg = sys.argv[1]
    signal = bin2csv(f"./exp_5_data/exp_rx_out_{deg}_{i}.bin")
    signal1_i = [i[0] for i in signal][-6200:]
    signal1_q = [i[1] for i in signal][-6200:]
    signal2_i = [i[2] for i in signal][-6200:]
    signal2_q = [i[3] for i in signal][-6200:]

    print(len(signal))    
    axs[0][i].plot( signal1_i)
    axs[0][i].plot( signal2_i)
    axs[0][i].set_title(f"Recieved RX1,2 | Trial - {i+1}")


    xf = rfftfreq(6200, 1 / (int(rx_config["samplerate"])))

    yf_s = rfft(signal1_i)
    axs[1][i].stem(xf, np.abs(yf_s))
    axs[1][i].set_title('RX1 (static) Signal in Frequency Domain!')

    yf_m = rfft(signal2_i)
    axs[2][i].stem(xf, np.abs(yf_m))
    axs[2][i].set_title('RX2 (moving) Signal in Frequency Domain!')

    # div = np.divide(np.add(signal1_i,0.000001), np.add(signal1_q,0.000001))
    # # idiv = irfft(div)
    # axs[3][i].plot(div)
    # axs[3][i].set_title('RXM/RXS Signal in Time Domain!')

    # axs[4][i].plot()

plt.show()


# signal = bin2csv(f"./exp_4_data/exp_rx_out_{30}_{0}.bin")
# signal1_i = [i[0] for i in signal][-620:]
# signal1_q = [i[1] for i in signal][-620:]
# signal2_i = [i[2] for i in signal][-620:]
# signal2_q = [i[3] for i in signal][-620:]


# x = {0: []}

# plt.axes(projection='polar')

# for i in range(len(signal1_i)):
#     mrho, mphi = cart2pol(signal1_i[i], signal1_q[i])
#     plt.polar(mphi, mrho, 'g.')
#     if mphi not in x:
#         x[mphi] = []

#     x[mphi].append(mrho)

# for mphi, v in x.items():
#     plt.polar(mphi, np.average(x[mphi]), 'r.')

# plt.show()



