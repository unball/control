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


def angdiff(robot_angle,desired_angle):
	#Difference between two angles, the result wrapped on the interval [-pi,pi].
	return ((robot_angle - desired_angle + pi) % (2*pi)) - pi
	

def pose_control(vector, robot_angle, desired_angle):
		#this two lines make the transformation of cartesian to polar coordinates of the error vector
		error_magnitude = sqrt(vector[1]**2+vector[0]**2)
		error_angle = calculateErrorAngle(vector[1], vector[0])

		k_linear=1
		k_angular=2
		radius_tolerance = 0.1
		if error_magnitude > radius_tolerance:
			return k_linear*error_magnitude, k_angular*error_angle
		else:
			k_angular=5
		return 0, k_angular*angdiff(robot_angle, desired_angle)