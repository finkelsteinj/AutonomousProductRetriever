#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port, Stop
from pybricks.robotics import DriveBase

wheel_diameter = 56
axle_track = 260.5

left_motor = Motor(Port.C)
right_motor = Motor(Port.B)

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

robot.settings(straight_speed=125, turn_rate=35)

robot.straight(304.8)     # drive 12 in.
robot.turn(90)            # turn clockwise 90 deg
robot.straight(304.8 * 8) # drive 96 in.