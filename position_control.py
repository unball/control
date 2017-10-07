import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
number_of_robots = 3

def calculateErrorAngle(y, x):
	if x==0 and y==0:
		return 0
	th = atan2(-x, y)
	return (th)

def control(error_magnitude, error_angle, vector_y):
	k_linear=0.3
	k_angular=1
	return k_linear*error_magnitude, k_angular*error_angle

def position_control(vector):
		#this two lines make the transformation of cartesian to polar coordinates of the error vector
		error_magnitude = sqrt(vector[1]**2+vector[0]**2)
		error_angle = calculateErrorAngle(vector[1], vector[0])

		return control(error_magnitude, error_angle, vector[1])