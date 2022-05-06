#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveDifferential, MoveTank, MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.wheel import EV3Tire
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import GyroSensor
from time import sleep
import sys

axle_track = 0 * 8   # distance b/w motor-attached wheels, in mm
speed = SpeedRPM(80) # travel speed, in rotations per min
distance = 20        # drive distance, in mm

Robot = MoveDifferential(OUTPUT_B, OUTPUT_C, EV3Tire, axle_track)

Robot.on_for_distance(speed, distance)
