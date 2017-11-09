import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *

m_v_linear = [0.0, 0.0, 0.0]
m_v_angular = [0.0, 0.0, 0.0]
orientation = [1,1,1]

def pose_line_control(vector, robot_angle, desired_angle, robot):
	global m_v_angular
	global m_v_linear
	global orientation

	margin = 50
	margin = 2*pi*margin/360

	error = calculateErrorAngle(vector[1], vector[0],1)
	if (orientation[robot] == 1) and (fabs(error)>(pi-margin)):
		orientation[robot] = -1
	elif (orientation[robot] == -1) and (fabs(error)<margin):
		orientation[robot] = 1

	m_v_linear[robot], m_v_angular[robot] = purple_curve_control(vector, orientation[robot], m_v_angular[robot], m_v_linear[robot], robot_angle, desired_angle)

	error_magnitude = sqrt(vector[1]**2+vector[0]**2)
	radius_tolerance = 0.1
	if error_magnitude > radius_tolerance:
		return m_v_linear[robot], m_v_angular[robot]
	else:
		k_angular=2
		return 0, k_angular*angdiff(robot_angle, desired_angle)
