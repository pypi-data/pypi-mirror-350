#import sys
#sys.path.insert(0, "../romiserial")

import math
import time
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
ki = 1.2
ki_denominator = 100
ki_numerator = int(kp * ki_denominator)
max_amplitude = 100

motors.execute('?')
motors.execute('C',
               encoder_steps, left_direction, right_direction,
               max_speed, max_acceleration,
               kp_numerator, kp_denominator,
               ki_numerator, ki_denominator,
               max_amplitude)
motors.execute('E', 1)


while True:
    print(-5000)
    motors.execute('V', -5000, -5000)
    time.sleep(5)
    print(0)
    motors.execute('V', 0, 0)
    time.sleep(5)
    print(5000)
    motors.execute('V', 5000, 5000)
    time.sleep(5)
    
