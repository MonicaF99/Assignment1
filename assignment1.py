from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance between the robot and a block to cacth"""

w_th = 0.8
""" float: Threshold for the control of the linear distance between the robot and a wall (avoid collision)"""

w2_th = 2.0
""" float: Threshold for the control of the linear distance between the robot and a wall (choose direction)"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def find_golden_token(direction, amplitude):
    """
    Function to find the closest golden token in a certain direction
    
    Input: 
    	direction = angle between the robot and the direction where I want to search a token
    	amplitude = width of the visual field

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=500
    for token in R.see():
        if token.dist < dist and token.info.marker_type == MARKER_TOKEN_GOLD and (direction - amplitude) <= token.rot_y <= (direction + amplitude):
            dist=token.dist
	    rot_y=token.rot_y
    if dist==500:
	return -1, -1
    else:
   	return dist, rot_y    
   	
def find_silver_token(direction, amplitude):
    """
    Function to find the closest silver token in a certain direction
    
    Input: 
    	direction = angle between the robot and the direction where I want to search a token
    	amplitude = width of the visual field	

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=500
    for token in R.see():
        if token.dist < dist and token.info.marker_type == MARKER_TOKEN_SILVER and (direction - amplitude) <= token.rot_y <= (direction + amplitude):
            dist=token.dist
	    rot_y=token.rot_y
    if dist==500:
	return -1, -1
    else:
   	return dist, rot_y
   	
def avoid_wall():
	dist, rot_y = find_golden_token(0, 40)
	if dist == -1:
		return
	if dist < w_th:
		if rot_y < 0:
			while(dist < w2_th):
				turn(10, 0.1)
				dist, rot_y = find_golden_token(0, 20)
		else:
			while(dist < w2_th):
				turn(-10, 0.1)
				dist, rot_y = find_golden_token(0, 20)
	return
	
def go_and_catch_silver_token():
	dist, rot_y = find_silver_token(0, 90)
	if dist == -1:
		print("Not found")
		return
	dist_g, rot_y_g = find_golden_token(rot_y, 10*a_th)
	print("Silver dist: " + str(dist))
	print("Golden dist: " + str(dist_g))
	if dist_g < dist:
		return
	while True:
		dist, rot_y = find_silver_token(0, 90)
		if dist <d_th: 
			R.grab() # if we are close to the token, we grab it.
			turn(20, 3)
			print("Gotcha!") 
			R.release()
			turn(-20, 3)
			return
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			drive(10, 0.5)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			turn(-2, 0.5)
		elif rot_y > a_th:
			turn(+2, 0.5)
	
def main():
	while True:
		drive(30, 0.2)
		go_and_catch_silver_token()
		print("No token seen")
		avoid_wall()
		
main()
