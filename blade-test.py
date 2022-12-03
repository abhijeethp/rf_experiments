import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import csv
from math import e, pi, sin, floor


a = 100
f = 50
T = np.linspace(0, 1, 40 * 10**3)
ω = 2 * pi * f
Y = a*np.cos(ω*T)+ 1j*a*np.sin(ω*T)

print("writing to file")
f = open('/tmp/sin_in.csv', 'w')
writer = csv.writer(f)
for y in Y:
    writer.writerow([round(y.real), round(y.imag)])
f.close()


plt.rcParams["figure.figsize"] = (27,10)

# RX PROPERTIES
rx_config = {
    "frequency": 1572.46 * 10**6,
    "samplerate": 40 * 10**6 - 1,
    "bandwidth": 10 * 10**6,
    "gain": 60,
    "duration_s": 0.1
}

tx_config = {
    "frequency": 1572.46 * 10**6,
    "samplerate": 40 * 10**6 - 1,
    "bandwidth": 10 * 10**6,
    "gain": 60,
    "duration_s": 1
}

def num_samples(config):
    return config["samplerate"] * config["duration_s"]

def exec(command):
    sp.run(["bladeRF-cli", "-e"] + [command])

cmds = []
# print("-------------INIT BLADE-RF DEVICE-------------")
cmds.append(f"set agc off")

# print("-------------INIT BLADE-RF CONFIG-------------")
cmds.append(f"set frequency rx {rx_config['frequency']}")
cmds.append(f"set samplerate rx {rx_config['samplerate']}")
cmds.append(f"set bandwidth rx {rx_config['bandwidth']}")
cmds.append(f"set gain rx {rx_config['gain']}")

cmds.append(f"set frequency tx {rx_config['frequency']}")
cmds.append(f"set samplerate tx {rx_config['samplerate']}")
cmds.append(f"set bandwidth tx {rx_config['bandwidth']}")
cmds.append(f"set gain tx {rx_config['gain']}")

cmds.append("info")
cmds.append("print")

# print("-------------START TX/RX-------------")
file_format = file_ext = "csv"
file_out_name = "/tmp/rx_out"
file_in_name = "/tmp/sin_in"

cmds.append(f"rx config file={file_out_name}.{file_ext} format={file_format} n={num_samples(rx_config)}")
# cmds.append(f"tx config file={file_in_name}.{file_ext} format={file_format} repeat=0 delay=4000")

# cmds.append("tx start")
# cmds.append("tx")
time.sleep(0.2)
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

print("---------------------XXX---------------------")

print("; ".join(cmds))

print("---------------------XXX---------------------")


#csv = np.genfromtxt('/tmp/test123.csv', delimiter=',').T
#signal_i = csv[0]
#signal_q = csv[1]
#signal = signal_i + signal_q * 1j
#T = np.linspace(0, int((rx_config["duration_s"] * 100) ), int(num_samples(rx_config))) / 100


#fig, ax = plt.subplots()
#ax.plot(T, signal_i)
#plt.show()
