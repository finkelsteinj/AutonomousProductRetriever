#!/usr/bin/env python3
from AutonomousProductRetriever import AutonomousProductRetriever
from Warehouse import Warehouse
import time
from ev3dev.ev3 import *

MM_IN_INCH = 25.4
ON = True
OFF = False
wh = Warehouse()
lcd = Screen()

# Subtask 1-4 Code
def subtask1(robot):
    inventory_location = input("inventory location: ")
    
    box_direction = wh.getBoxDirection(inventory_location)

    robot.driveToBox(inventory_location)
    time.sleep(5)
    robot.turnLeft()
    robot.driveToFulfillment('B', inventory_location)
    robot.driveDistance(10.5)
    time.sleep(5)

def subtask2(robot):
    robot.turnRight()
    robot.turnRight()
    robot.returnHome(True, 'B')

def subtask3(robot):
    barcode = input("barcode: ")

    robot.driveDistance(13.5)
    result = robot.scanBarcode(barcode, 'right')
    
    output = 'barcode matches' if result == True else 'barcode does not match'
    lcd.draw.text((48,13), output, fill='white')
    lcd.update()

def subtask4(robot):
    robot.pickUpItem('right')
    robot.turnRight()
    robot.driveDistance(24)
    robot.hook.on_for_degrees(10, 230, brake=True, block=True)
    robot.driveDistance(-3)


# Final Demo Code
def finalDemo(robot):
    inventory_location = input("inventory location: ")
    barcode = input("barcode: ")
    fulfillment_area = input("fulfillment area: ")

    box_direction = wh.getBoxDirection(inventory_location)

    robot.driveToBox(inventory_location)
    item_present = robot.scanBarcode(barcode, box_direction)
    
    if(item_present):
        # case: barcode matches
        robot.pickUpItem(box_direction)
        robot.driveToFulfillment(fulfillment_area, inventory_location)
        robot.dropOffItem()
        robot.returnHome(item_present, fulfillment_area)   # from fulfillment area
    else:
        # case: barcode does not match
        robot.returnHome(item_present, inventory_location) # from inventory location


# Main Function
if __name__ == "__main__":
    left_speed = 25
    right_speed = 24.8
    turn_speed = 10
    # avoid_objects = True

    bertha = AutonomousProductRetriever(left_speed, right_speed, turn_speed)

    # subtask1(bertha)
    # subtask2(bertha)
    # subtask3(bertha)
    # subtask4(bertha)
    finalDemo(bertha)
    