#!/usr/bin/env python3
class Warehouse:
  def __init__(self):
    # (x, y) distance from Home A to bottom-left of shelf
    self.shelves = {
      'A1': [0, 12],
      'A2': [0, 36],
      'B1': [54, 12],
      'B2': [54, 36],
      'C1': [0, 60],
      'C2': [0, 84],
      'D1': [54, 60],
      'D2': [54, 84],
    }

    # (x, y) distance from bottom-left of shelf
    self.boxes = {
      '1': [9, 0],
      '2': [15, 0],
      '3': [21, 0],
      '4': [27, 0],
      '5': [33, 0],
      '6': [39, 0],
      '7': [9, 24],
      '8': [15, 24],
      '9': [21, 24],
      '10': [27, 24],
      '11': [33, 24],
      '12': [39, 24],
    }

    # (x, y) distance from Home A to 6 inches into the aisle from Home center
    self.fulfillment_areas = {
      'A': [0, 12],
      # 'B': [96, 12],
      'B': [48, 12],
      'C': [0, 102],
      'D': [96, 102],
    }
      

  '''Return the x-distance to the middle of the closest aisle to the box.'''
  def getDistanceBoxX(self, location):
    # slice 'location' input to get shelf and box location
    shelf = location[:2]
    box = location[3:]

    shelf_x_dist = self.shelves.get(shelf)[0]
    box_x_dist = self.boxes.get(box)[0]
    return shelf_x_dist + box_x_dist


  '''Return the y-distance to the middle of the closest aisle to the box.'''
  def getDistanceBoxY(self, location):
    # slice 'location' input to get shelf and box location
    shelf = location[:2]
    box = location[3:]

    shelf_y_dist = self.shelves.get(shelf)[1]
    box_y_dist = self.boxes.get(box)[1]
    return shelf_y_dist + box_y_dist
  

  '''
  Return the x-distance to either the westmost or eastmost aisle,
  wherever the 'fulfillment_area' is located.
  '''
  def getDistanceFulfillmentX(self, fulfillment_area, curr_location):
    box_x_dist = self.getDistanceBoxX(curr_location)
    fulfillment_x_dist = self.fulfillment_areas.get(fulfillment_area)[0]
    return fulfillment_x_dist - box_x_dist


  '''
  Return the y-distance to either the north or south fulfillment
  area, wherever the 'fulfillment_area' is located.
  '''
  def getDistanceFulfillmentY(self, fulfillment_area, curr_location):
    box_y_dist = self.getDistanceBoxY(curr_location)
    fulfillment_y_dist = self.fulfillment_areas.get(fulfillment_area)[1]
    return fulfillment_y_dist - box_y_dist


  '''Return the x-distance to travel to reach Home A.'''
  def getDistanceHomeX(self, fulfillment_area):
    home_x_dist = self.fulfillment_areas.get(fulfillment_area)[0]
    return home_x_dist


  '''Return the y-distance to travel to reach Home A.'''
  def getDistanceHomeY(self, fulfillment_area):
    home_y_dist = self.fulfillment_areas.get(fulfillment_area)[1]
    return home_y_dist
    


  '''Return 'left' or 'right' based on direction of of box location.'''
  def getBoxDirection(self, location):
    # slice 'location' input to get shelf and box location
    shelf = location[:2]
    box = location[3:]

    box_y_dist = self.boxes.get(box)[1]

    if(box_y_dist == 24):
      return 'right'
    else:
      return 'left'