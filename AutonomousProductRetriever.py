#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, MoveDifferential, MoveTank, MoveSteering, OUTPUT_A, OUTPUT_C, OUTPUT_D
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor, GyroSensor
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3Tire
from time import sleep
from Warehouse import Warehouse

MM_IN_INCH = 25.4
DISTANCE_MULTIPLIER = 14
CIRCUMFERENCE = 3.14159 * (53.8 / MM_IN_INCH)
AVG_VELOCITY = 15

class AutonomousProductRetriever:

  wh = Warehouse()
  hook = MediumMotor(OUTPUT_C)
  left_color = ColorSensor(INPUT_1)
  right_color = ColorSensor(INPUT_4)
  ultrasonic = UltrasonicSensor(INPUT_3)
  motor = LargeMotor(OUTPUT_D)
  gyro = GyroSensor(INPUT_2)


  '''AutonomousProductRetriever constructor.'''
  def __init__(self, LEFT_SPEED, RIGHT_SPEED, TURN_SPEED, avoid_objects=False):
    self.LEFT_SPEED = -LEFT_SPEED
    self.RIGHT_SPEED = -RIGHT_SPEED
    self.TURN_SPEED = -TURN_SPEED
    self.avoid_objects = avoid_objects

    self.robot = MoveTank(OUTPUT_D, OUTPUT_A, "", LargeMotor)
    self.robot_diff = MoveDifferential(OUTPUT_D, OUTPUT_A, EV3Tire, 82)
    
    self.gyro.calibrate()

  '''Drive for 'distance' via MoveTank's 'on_for_rotations' function.'''
  def driveDistance(self, distance):
    total_rotations = distance / CIRCUMFERENCE
    self.robot.on_for_rotations(
      self.LEFT_SPEED, 
      self.RIGHT_SPEED, 
      total_rotations, 
      brake=True,
      block=False)

    d = self.ultrasonic.distance_inches
    if(d < 6 and self.avoid_objects):
      print('Object Detected\n')
      self.robot.off()
      return
    
    self.motor.wait_until_not_moving()


  '''Drive for 'distance' via MoveTank's 'on_for_rotations' function.'''
  def driveDistance_Old(self, distance):
    total_rotations = distance / CIRCUMFERENCE * DISTANCE_MULTIPLIER
    num_rotations = 0
    time_drove = 0
    self.gyro.reset()

    self.robot.on_for_rotations(
      SpeedRPM(self.LEFT_SPEED), 
      SpeedRPM(self.RIGHT_SPEED), 
      total_rotations, 
      brake=True, 
      block=False)
    
    while(True):
      left_correction = 0
      right_correction = 0

      # if distance reached, stop, otherwise drive for another 0.5 seconds
      print("  num rotations =", num_rotations)
      print("total rotations =", total_rotations, end="\n\n")
      if(num_rotations >= total_rotations):
        self.robot.off()
        return
      else:
        sleep(0.1)
        time_drove += 0.1
        num_rotations += time_drove * AVG_VELOCITY / 60
      
      # object detection
      d = self.ultrasonic.distance_inches
      if(d < 6 and self.avoid_objects):
        print('Object Detected\n')
        self.robot.off()
        break

      # correct any leftward drifting
      if(self.gyro.angle < 0):
        print('correct leftward drift\n')
        left_correction -= 1
        self.robot.on_for_rotations(
          SpeedRPM(self.LEFT_SPEED + left_correction), 
          SpeedRPM(self.RIGHT_SPEED + right_correction), 
          total_rotations - num_rotations, 
          brake=True, 
          block=False)

      # correct any rightward drifting
      if(self.gyro.angle > 0):
        print('correct rightward drift\n')
        right_correction -= 1
        self.robot.on_for_rotations(
          SpeedRPM(self.LEFT_SPEED + left_correction), 
          SpeedRPM(self.RIGHT_SPEED + right_correction), 
          total_rotations - num_rotations, 
          brake=True, 
          block=False)


  '''Turn 90 degrees counterclockwise.'''
  def turnLeft(self):
    # self.gyro.reset()
    self.robot_diff.turn_left(SpeedRPM(self.TURN_SPEED), 89.75)


  '''Turn 90 degrees clockwise.'''
  def turnRight(self):
    # self.gyro.reset()
    self.robot_diff.turn_right(SpeedRPM(self.TURN_SPEED), 89.75)


  '''Drive to given box location from starting point (Home A).'''
  def driveToBox(self, location):
    x_distance = self.wh.getDistanceBoxX(location)
    y_distance = self.wh.getDistanceBoxY(location)

    # navigate to box
    self.driveDistance(y_distance) # drive to aisle
    self.turnRight()               # turn right 90 degrees
    self.driveDistance(x_distance) # drive to box location


  '''From current box location, drive to given fulfillment area.'''
  def driveToFulfillment(self, fulfillment_area, curr_location):
    x_distance = self.wh.getDistanceFulfillmentX(fulfillment_area, curr_location)
    y_distance = self.wh.getDistanceFulfillmentY(fulfillment_area, curr_location)

    if(x_distance < 0):
      # drive to westmost aisle
      self.turnLeft()
      self.driveDistance(-x_distance)
      
      if(y_distance < 0):
        # drive to Home A
        self.turnLeft()
        self.driveDistance(-y_distance)
      else:
        # drive to Home C
        self.turnRight()
        self.driveDistance(y_distance)
    else:
      # drive to eastmost aisle
      self.turnRight()
      self.driveDistance(x_distance)

      if(y_distance < 0):
        # drive to Home D
        self.turnRight()
        self.driveDistance(-y_distance)
      else:
        # drive to Home B
        self.turnLeft()
        self.driveDistance(y_distance)


  '''
  From either a box or a fulfillment area, drive to Home A and 
  turn 180 degrees to face north.
  '''
  def returnHome(self, item_found, curr_location):
    x_distance = self.wh.getDistanceHomeX(curr_location)
    y_distance = self.wh.getDistanceHomeY(curr_location)

    # if(y_distance < 0):
    #   self.driveDistance(-y_distance)
    #   if(x_distance < 0):
    #     self.turnRight()
    #     self.driveDistnace(x_distance)
    #     self.turnLeft()
    # else:
    #   self.driveDistance(y_distance)
    #   if(x_distance < 0):
    #     self.turnLeft()
    #     self.driveDistnace(-x_distance)
    #     self.turnRight()

    self.driveDistance(y_distance)
    self.turnLeft()
    self.driveDistance(x_distance)
    self.turnLeft()
    self.driveDistance(12)
    self.turnLeft()
    self.turnLeft()


  '''
  Preform barcode scan and return True if it matches given barcode, 
  otherwise return False.
  '''
  def scanBarcode(self, barcode, direction):
    # determine color sensor to use
    color_sensor = self.left_color if direction == 'left' else self.right_color
    color_sensor.mode = 'COL-REFLECT'
    
    # step and read barcode
    barcode_at_box = ""
    for i in range(4):
      color_val = color_sensor.color
      
      if(color_val == 1):
        barcode_at_box += "1"
      else:
        barcode_at_box += "0"
    
      self.driveDistance(0.365)
      sleep(1)

    # compare barcode at box to barcode expected
    print(barcode_at_box)
    if barcode == barcode_at_box:
      return True
    else:
      return False


  '''Rotate towards box, drive forward, pick it up, and rotate to face north.'''
  def pickUpItem(self, direction):
    speed = SpeedRPM(-10)
    # turn towards box
    self.robot_diff.on_for_distance(speed, 2 * MM_IN_INCH)
    if(direction == 'left'):
      self.turnRight()
      self.robot_diff.on_for_distance(-10, 65)
      self.turnRight()
      self.turnRight()
    else:
      self.turnLeft()
      self.robot_diff.on_for_distance(-10, 65)
      self.turnLeft()
      self.turnLeft()
    
    # lower hook and drive towards box
    self.hook.on_for_degrees(10, 250, brake=True, block=True)
    self.robot_diff.on_for_distance(-10, 50)
    sleep(3)

    # pick up box and reverse
    self.hook.on_for_degrees(10, -230, brake=True, block=True)
    self.driveDistance(-2)
    
    # face north
    if(direction == 'left'):
      pass
    else:
      self.turnLeft()
      self.turnLeft()
    
    sleep(1)


  '''
  Drive forward 12 inches, drop off box, turn 180 degrees, and 
  drive forward 6 inches.
  '''
  def dropOffItem(self):
    self.driveDistance(12)
    self.hook.on_for_degrees(10, 250, brake=True, block=True)
    self.driveDistance(-3)
    self.turnRight()
    self.turnRight()
    self.driveDistance(3)
    