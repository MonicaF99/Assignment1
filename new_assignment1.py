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

	"""
	This function search a wall in front of the robot (amplitude 120 degrees).
	If there is a wall, the robot check the best way to rotate and rotate until the wall isn't on its road
	"""
	dist, rot_y = find_golden_token(0, 60)
	
	if dist == -1:
		return
	if dist < w_th:
		print("I see a wall too close to me!")
		right = right_is_better()
		
		if right:
			print("I choose to go right")
			while(dist < w2_th):
				turn(10, 0.1)
				dist, rot_y = find_golden_token(0, 20)
		else:
			print("I choose to go left")
			while(dist < w2_th):
				turn(-10, 0.1)
				dist, rot_y = find_golden_token(0, 20)
	return
	
def right_is_better():
	"""
	This function checks if the farthest wall is on the left or on the right.
	The direction of the furthest wall is the best to go.
	Return: True if the best way is right, False if the best way is left
	"""

	dist_l, rot_y_l = find_golden_token(-90, 10)
	dist_r, rot_y_r = find_golden_token(90, 10)	
	print("Distance right = " + str(dist_r))
	print("Distance left = " + str(dist_l))
	if dist_l < dist_r:
		return True
	else:
		return False
	
def go_and_catch_silver_token():

	"""
	This function check if there is a silver token in front of the robot without a wall between them.
	If it finds a catchable silver token it go to cacht it.
	It also choose which is the best way to move the token behind itself.
	"""
	dist, rot_y = find_silver_token(0, 80)
	if dist == -1:
		print("Not found")
		return
	dist_g, rot_y_g = find_golden_token(rot_y, 25)
	if dist_g < dist:
		return
	
	print("Let's go to catch the token!")
	while True:
		dist, rot_y = find_silver_token(0, 90)
		if dist <d_th: 
			R.grab() # if we are close to the token, we grab it.
			right = right_is_better()
			if right:
				print("Rotate right")
				turn(20, 3)
				print("Gotcha!") 
				R.release()
				turn(-20, 3)
			else:
				print("Rotate left")
				turn(-20, 3)
				print("Gotcha!") 
				R.release()
				turn(20, 3)
			return
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			drive(50, 0.1)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			turn(-2, 0.5)
		elif rot_y > a_th:
			turn(+2, 0.5)
	
def main():
	while True:
		drive(50, 0.1)
		go_and_catch_silver_token()
		print("No token seen")
		avoid_wall()
		
main()
