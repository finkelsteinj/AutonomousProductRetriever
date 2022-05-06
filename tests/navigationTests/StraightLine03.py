#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port, Stop
from pybricks.robotics import DriveBase

wheel_diameter = 56
axle_track = 260

left_motor = Motor(Port.C)
right_motor = Motor(Port.B)

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

robot.settings(straight_speed=125, turn_rate=35)

# drive 350 mm/sec for 7620 ms
robot.straight(304.8 * 5)