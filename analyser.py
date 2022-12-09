from math import pow, sqrt, sin, cos, acos, atan, pi, radians, degrees
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft,rfft, rfftfreq
from math import e, pi, sin, floor
from bin_csv_utils import bin2csv
from constants import config, L_s, L_m, wavelength

def cart2pol(x,y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho,phi

# Things to Plot
things_to_plot = {
    "should_plot_raw_signals" : 0,    # 0. Raw Signals
    # "should_plot_i_vs_q" : 1,       # 1. IvsQ of Signals
    "should_plot_ffts" : 1,           # 2. FFT of Signal1
    "should_plot_fftm" : 2,           # 3. FFT of Signal2
    "should_plot_aoa_estimate" : 3,   # 4. AoA Estimate
}

data_directory = "exp_2_data"
trial_num = 2

fig = plt.figure()
fig.suptitle(f'Trial - {trial_num}', fontsize=16)

servo_error = 35/90
servo_rotations = [0, 10, 20, 30, 40] #, 50, 60, 70, 80, 90, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0, 10, 20, 30]
servo_rotations_error_fixed = [x + x * servo_error for x in servo_rotations]

arm_rotations = [round(deg * 4/3, 4) for deg in servo_rotations_error_fixed]

def distance_at_degree(L_s, L_m, degree):
    a = radians(degree)
    return round(sqrt(pow(L_s, 2) + pow(L_m, 2) - 2 * L_s * L_m * cos(a)), 4)

d = [distance_at_degree(L_s, L_m, deg) for deg in arm_rotations]

def phase_delta(sig_1, sig_2, step_num):
    yf_s = rfft(sig_1)
    max_yf_s_pos =  np.argmax(np.abs(yf_s))
    phase_s = np.angle(yf_s[max_yf_s_pos])

    yf_m = rfft(sig_2)
    max_yf_m_pos =  np.argmax(np.abs(yf_m))
    phase_m = np.angle(yf_m[max_yf_m_pos])

    xf = rfftfreq(len(sig_1), d=1./config()["samplerate"])

    if("should_plot_ffts" in things_to_plot):
        chart_s = plt.subplot(len(things_to_plot), len(servo_rotations), len(servo_rotations) * things_to_plot["should_plot_ffts"]  + step_num + 1)
        chart_s.plot(xf, np.abs(yf_s), color="blue")
    
    if("should_plot_fftm" in things_to_plot):
        chart_m = plt.subplot(len(things_to_plot), len(servo_rotations), len(servo_rotations) * things_to_plot["should_plot_fftm"] + step_num + 1)
        chart_m.plot(xf, np.abs(yf_m), color="orange")

    phase_delta = phase_m - phase_s
    return phase_delta if phase_delta > 0 else 2 * pi + phase_delta


def angle_of_arrival(step_num, d):
    signal_file = f"{data_directory}/exp_rx_out_{servo_rotations[step_num]}_{trial_num}.bin"
    signal = bin2csv(signal_file)
    sig_i_1 = [x[0] for x in signal]
    sig_q_1 = [x[1] for x in signal] 
    sig_i_2 = [x[2] for x in signal]
    sig_q_2 = [x[3] for x in signal]


    if("should_plot_raw_signals" in things_to_plot):
        chart = plt.subplot(len(things_to_plot), len(servo_rotations),len(servo_rotations) * things_to_plot["should_plot_raw_signals"] + step_num + 1)
        chart.set_title(f"Deg={servo_rotations[step_num]}")
        chart.plot(sig_i_1[-1000:-900], color="blue")
        chart.plot(sig_i_2[-1000:-900], color="orange")

    if("should_plot_i_vs_q" in things_to_plot):
        chart = plt.subplot(len(things_to_plot), len(servo_rotations),len(servo_rotations) * things_to_plot["should_plot_i_vs_q"] + step_num + 1, polar=True)
        for i in range(len(sig_i_1)):
            rho, phi = cart2pol(sig_i_1[i], sig_q_1[i])
            chart.plot(phi, rho, 'g.')

    phase_diff = phase_delta(sig_i_1, sig_i_2, step_num)
    return acos(wavelength * phase_diff / (2 * pi * d))

relative_aoas = [angle_of_arrival(step_num, distance) for step_num, distance in enumerate(d)]

def angle_to_base(theta_m):
    theta_m_rad = radians(theta_m)
    return atan( L_m * sin(theta_m_rad) / (L_s - L_m * cos(theta_m_rad)) )

absolute_aoas = [relative_aoa + angle_to_base(arm_rotations[i]) for i, relative_aoa in enumerate(relative_aoas)]
absolute_aoa_deg = [degrees(x) for x in absolute_aoas]

for step_num, angle in enumerate(absolute_aoas):
    if("should_plot_aoa_estimate" in things_to_plot):
        chart = plt.subplot(len(things_to_plot), len(servo_rotations),len(servo_rotations)*3 + step_num + 1, polar=True)
        chart.plot(angle, 5, 'r.')

print("servo rotations\t: " + str(servo_rotations))    
print("servo rotations error fixed\t: " + str(servo_rotations_error_fixed))
print("arm rotations\t: " + str(arm_rotations))
print("d\t:" + str(d))
print("relative AOA\t:" + str(relative_aoas))
print("absolute AOA\t:" + str(absolute_aoas))
print("absolute AOA in degrees\t:" + str(absolute_aoa_deg))

plt.show()