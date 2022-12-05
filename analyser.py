from math import pow, sqrt, cos, acos, pi

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

arm_rotations = [round(deg * 3 / 4, 4) for deg in servo_rotations_error_fixed]

def distance_at_degree(degree):
    a = degree * 2 * pi / 360
    return round(sqrt(pow(L_s, 2) + pow(L_m, 2) - 2 * L_s * L_m * cos(a)), 4)

d = [distance_at_degree(deg) for deg in arm_rotations]


wavelength = 15

def angle_of_arrival(d):
    phase_diff = 0
    return acos( phase_diff * wavelength / 2 * pi * d)

relative_aoa = [angle_of_arrival(distance) for d in ]


print("servo rotations\t: " + str(servo_rotations))    
print("servo rotations error fixed\t: " + str(servo_rotations_error_fixed))
print("arm rotations\t: " + str(arm_rotations))
print("d\t:" + str(d))

# calculate d given theta_m, L_m and L_s

# TODO : Generate phase differences at these points of time, from the bin file.
# TODO : calculate angle of arrival



