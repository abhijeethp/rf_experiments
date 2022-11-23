import scipy.fftpack
from scipy.fft import rfft, rfftfreq, fftshift
import numpy as np
import csv
import time
from math import e, pi, sin, cos, floor
import matplotlib.pyplot as plt

# theta = np.linspace(0,np.pi)
# r = [sin(x) for x in theta]
# c = ax.scatter(theta, r, c=r, s=10)

# fig = plt.figure()
# ax = fig.add_subplot(111, polar=True)
# ax.set_thetamin(0)
# ax.set_thetamax(180)

# plt.show()


# CONFIG FOR SIGNAL GENERATION
n = 256                   # sample size
N = range(n)              
t = 0.05                  # step size / sample interval
a, f, θ = 6, 0.6, 0       # amplitude, frequency, phase

def sinWave(n, a, f, θ):
  ω = 2 * pi * f
  T = [t*i for i in range(n)]
  Y = [ a*(cos(ω * T[i] + θ) + 1j*sin(ω * T[i] + θ)) for i in range(n)]
  return T, Y


T, Y1 = sinWave(n, a, f, θ)
T, Y2 = sinWave(n, a, f, θ+pi/8)

fig, axs = plt.subplots(3, 1)
axs[0].plot(T, [y.real for y in Y1])
# ax.plot(T, [y.imag for y in Y1])

axs[0].plot(T, [y.real for y in Y2])
# ax.plot(T, [y.imag for y in Y1])


Yf_i = rfft([y.real for y in Y1])
Yf_i2 = rfft([y.real for y in Y2])

Xf = rfftfreq(n, 1/ (20))
axs[1].stem(Xf, np.abs(Yf_i))
axs[1].stem(Xf, np.abs(Yf_i2))
axs[1].set_title('Signal in Frequency Domain')
axs[1].set_xlabel("Frequency (KHz)")
axs[1].set_ylabel("Amplitude (?)")

axs[2].stem(Xf, np.angle(Yf_i)*180/pi)
axs[2].stem(Xf, np.angle(Yf_i2)*180/pi)
axs[2].set_title('Signal in Frequency Domain')
axs[2].set_xlabel("Frequency (KHz)")
axs[2].set_ylabel("phase (degrees)")

plt.show()