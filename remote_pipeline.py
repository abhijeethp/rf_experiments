import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from scipy.fft import rfft, rfftfreq, fftshift
import csv
from math import e, pi, sin, floor

exp_num = 0
rx_config = {
    "frequency": 2000 * 10**6,
    "samplerate": 60 * 10**6,
    "bandwidth": 10 * 10**6,
    "gain": 40,
    "duration_s": 0.001
}

# 1Khz
# 

tx_config = {
    "frequency": 1572.46 * 10**6,
    "samplerate": 40 * 10**6 - 1,
    "bandwidth": 10 * 10**6,
    "gain": 60,
    "duration_s": 1
}

def num_samples(config):
    return config["samplerate"] * config["duration_s"]


cmds = []
# -------------INIT BLADE-RF DEVICE-------------
cmds.append(f"set agc off")

# -------------INIT BLADE-RF CONFIG-------------
cmds.append(f"set frequency rx {rx_config['frequency']}")
cmds.append(f"set samplerate rx {rx_config['samplerate']}")
cmds.append(f"set bandwidth rx {rx_config['bandwidth']}")
cmds.append(f"set gain rx {rx_config['gain']}")

# cmds.append(f"set frequency tx {rx_config['frequency']}")
# cmds.append(f"set samplerate tx {rx_config['samplerate']}")
# cmds.append(f"set bandwidth tx {rx_config['bandwidth']}")
# cmds.append(f"set gain tx {rx_config['gain']}")

cmds.append("info")
cmds.append("print")

# print("-------------START TX/RX-------------")
file_format = file_ext = "csv"
file_out_name = "/tmp/rx_out"
file_in_name = "/tmp/sin_in"
rx_channels = ["1","2"]
rx_channels_str = ",".join(rx_channels)

cmds.append(f"rx config file={file_out_name}.{file_ext} format={file_format} n={num_samples(rx_config) * len(rx_channels)} channel={rx_channels_str}")
# cmds.append(f"tx config file={file_in_name}.{file_ext} format={file_format} repeat=0 delay=4000")

# cmds.append("tx start")
# cmds.append("tx")
# time.sleep(0.2)
cmds.append("rx start")
cmds.append("rx")

cmds.append("rx wait")
cmds.append("rx")
time.sleep(0.2)

# cmds.append("tx stop")
# cmds.append("tx wait")
# cmds.append("tx")

print("Executing commands in the following order")
for i,cmd in enumerate(cmds):
    print(f"\t {i}." + cmd)

print("---------------------RUNNING SSH---------------------")
sp.run(["ssh", "phyg@172.20.10.2"] + ["bladeRF-cli -e \"" + "; ".join(cmds) +"\""])

print("---------------------COPYING OUTPUT---------------------")
sp.run(["scp", "phyg@172.20.10.2:/tmp/rx_out.csv", f"./test_{exp_num}.csv"])

print("---------------------VIZ---------------------")
csv = np.genfromtxt(f"test_{exp_num}.csv", delimiter=',').T

signal1_i = csv[0]
signal1_q = csv[1]
signal2_i = csv[2]
signal2_q = csv[3]

signal1 = signal1_i + signal1_q * 1j
signal2 = signal2_i + signal2_q * 1j 

fig, axs = plt.subplots(3)
T = np.linspace(0, int((rx_config["duration_s"] * 1000) ), int(num_samples(rx_config))) / 1000

axs[0].plot(T, signal1_i)
# axs[0].plot(T, signal1_q)
axs[0].plot(T, signal2_i)
# axs[0].plot(T, signal2_q)
axs[0].set_title(f"Recieved RX1,2 Signals!")

n=int(num_samples(rx_config))
xf = rfftfreq(n, 1 / (rx_config["samplerate"]))

yf_1 = rfft(signal1_i)
axs[1].stem(xf, np.abs(yf_1))
axs[1].set_title('RX1 Signal in Frequency Domain!')

yf_2 = rfft(signal2_i)
axs[2].stem(xf, np.abs(yf_2))
axs[2].set_title('RX2 Signal in Frequency Domain!')

maxpos1 = np.argmax(np.abs(yf_1))
print(np.angle(yf_1[maxpos1], deg=True))

maxpos2 = np.argmax(np.abs(yf_2))
print(np.angle(yf_2[maxpos2], deg=True))
print(np.angle(yf_1[maxpos1], deg=True) - np.angle(yf_2[maxpos1], deg=True))
# plt.show()