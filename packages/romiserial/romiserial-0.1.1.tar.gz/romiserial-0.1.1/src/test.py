import math
from romiseriel import RomiDevice
from romiserial import RomiDevice
motors = RomiDevice('/dev/ttyACM0')

encoder_steps = 13250
left_direction = 1
right_direction = -1
wheel_diameter = 0.322000
wheel_circumference = math.pi * wheel_diameter
max_speed_linear = 1
max_speed_angular = max_speed_linear / wheel_circumference
max_speed = int(1000.0 * max_speed_angular)
max_acceleration_linear = 1
max_acceleration_angular = max_acceleration_linear / wheel_circumference
max_acceleration = int(1000.0 * max_acceleration_angular)
kp = 0.08
kp_denominator = 100
kp_numerator = int(kp * kp_denominator)
ki = 0.12
ki_denominator = 100
ki_numerator = int(kp * ki_denominator)
max_amplitude = 40

motors.execute('?')
motors.execute('E', 1)
motors.execute('C',
               encoder_steps, left_direction, right_direction,
               max_speed, max_acceleration,
               kp_numerator, kp_denominator,
               ki_numerator, ki_denominator,
               max_amplitude)
motors.execute('V', 0.1, 0.1)
