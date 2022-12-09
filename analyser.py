from math import pow, sqrt, sin, cos, acos, atan, pi, radians, degrees
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import irfft, rfft, rfftfreq, fftshift
from math import e, pi, sin, floor

from bin_csv_utils import bin2csv
from config import config
data_directory = "exp_5_data"

# SAR GEOMETRY
L_s = 26.8
L_m = 37.8

servo_drift_per_degree = 11.25 / 270
servo_rotations = [0, 10, 20, 30, 40] #, 50, 60, 70, 80, 90, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0, 10, 20, 30]
servo_rotations_error_fixed = [servo_rotations[0]]
for i in range(1, len(servo_rotations)):
    prev_deg = servo_rotations_error_fixed[i-1]
    deg_delta = servo_rotations[i] - servo_rotations[i-1]
    deg_delta = (deg_delta - deg_delta*servo_drift_per_degree) if deg_delta > 0 else (deg_delta + deg_delta * servo_drift_per_degree) if deg_delta < 0 else 0
    curr_deg = round(prev_deg + deg_delta, 4)
    servo_rotations_error_fixed.append(curr_deg)  

arm_rotations = [round(deg * 4/3, 4) for deg in servo_rotations_error_fixed]

def distance_at_degree(degree):
    a = radians(degree)
    return round(sqrt(pow(L_s, 2) + pow(L_m, 2) - 2 * L_s * L_m * cos(a)), 4)

d = [distance_at_degree(deg) for deg in arm_rotations]

wavelength = 299792458 / (1960 * 10**6) * 100


def phase_delta(sig_i1, sig_q1, sig_i2, sig_q2):
    yf_s = rfft(sig_i1)
    max_yf_s_pos =  np.argmax(np.abs(yf_s))
    phase_s = np.angle(yf_s[max_yf_s_pos])

    yf_m = rfft(sig_i2)
    max_yf_m_pos =  np.argmax(np.abs(yf_m))
    phase_m = np.angle(yf_m[max_yf_m_pos])

    phase_delta = phase_m - phase_s
    return phase_delta if phase_delta > 0 else 2 * pi + phase_delta

def aoa(signal, wavelength, d):
    sig_i1 = [i[0] for i in signal]
    sig_q1 = [i[1] for i in signal]
    sig_i2 = [i[2] for i in signal]
    sig_q2 = [i[3] for i in signal]
    phase_diff = phase_delta(sig_i1, sig_q1, sig_i2, sig_q2)
    return acos(wavelength * phase_diff / (2 * pi * d))


def angle_of_arrival(step_num, d):
    signal_file = f"{data_directory}/exp_rx_out_{servo_rotations[step_num]}_0.bin"
    signal = bin2csv(signal_file)
    return aoa( signal, wavelength, d)

relative_aoas = [angle_of_arrival(step_num, distance) for step_num, distance in enumerate(d)]

def angle_to_base(theta_m):
    theta_m_rad = radians(theta_m)
    return atan( L_m * sin(theta_m_rad) / (L_s - L_m * cos(theta_m_rad)) )

absolute_aoas = [relative_aoa + angle_to_base(arm_rotations[i]) for i, relative_aoa in enumerate(relative_aoas)]
absolute_aoa_deg = [degrees(x) for x in absolute_aoas]

print("servo rotations\t: " + str(servo_rotations))    
print("servo rotations error fixed\t: " + str(servo_rotations_error_fixed))
print("arm rotations\t: " + str(arm_rotations))
print("d\t:" + str(d))
print("relative AOA\t:" + str(relative_aoas))
print("absolute AOA\t:" + str(absolute_aoas))
print("absolute AOA in degrees\t:" + str(absolute_aoa_deg))




