from math import pow, sqrt, sin, cos, acos, atan, pi

data_directory = "/tmp"

# SAR GEOMETRY
L_s = 40
L_m = 30

servo_drift_per_degree = 11.25 / 270
servo_rotations = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0, 10, 20, 30]
servo_rotations_error_fixed = [servo_rotations[0]]
for i in range(1, len(servo_rotations)):
    prev_deg = servo_rotations_error_fixed[i-1]
    deg_delta = servo_rotations[i] - servo_rotations[i-1]
    deg_delta = (deg_delta - servo_drift_per_degree) if deg_delta > 0 else (deg_delta + servo_drift_per_degree) if deg_delta < 0 else 0
    curr_deg = round(prev_deg + deg_delta, 4)
    servo_rotations_error_fixed.append(curr_deg)  

arm_rotations = [round(deg * 4/3, 4) for deg in servo_rotations_error_fixed]

def distance_at_degree(degree):
    a = degree * 2 * pi / 360
    return round(sqrt(pow(L_s, 2) + pow(L_m, 2) - 2 * L_s * L_m * cos(a)), 4)

d = [distance_at_degree(deg) for deg in arm_rotations]

wavelength = 15
def angle_of_arrival(step_num, d):
    signal_file = f"{data_directory}/exp_rx_out_{step_num}.bin"
    phase_diff = 0 # TODO
    return acos( phase_diff * wavelength / 2 * pi * d)

relative_aoas = [angle_of_arrival(step_num, distance) for step_num, distance in enumerate(d)]

def angle_to_base(theta_m):
    theta_m_rad = theta_m * 2 * pi / 360
    return atan( L_m * sin(theta_m_rad) / (L_s - L_m * cos(theta_m_rad)) )

absolute_aoas = [relative_aoa + angle_to_base(arm_rotations[i]) for i, relative_aoa in enumerate(relative_aoas)]

print("servo rotations\t: " + str(servo_rotations))    
print("servo rotations error fixed\t: " + str(servo_rotations_error_fixed))
print("arm rotations\t: " + str(arm_rotations))
print("d\t:" + str(d))
print("relative AOA\t:" + str(relative_aoas))
print("absolute AOA\t:" + str(absolute_aoas))



