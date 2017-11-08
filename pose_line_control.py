import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *

m_v_linear = 0.0
m_v_angular = 0.0
orientation = 1

def pose_line_control(vector, robot_angle, desired_angle):
	global m_v_angular
	global m_v_linear
	global orientation

	if orientation == 1:
		orientation = copysign(1,vector[1] + 0.1)
	else:
		 orientation = copysign(1,vector[1] - 0.1)

	m_v_linear, m_v_angular = purple_curve_control(vector, orientation, m_v_angular, m_v_linear, robot_angle, desired_angle)

	error_magnitude = sqrt(vector[1]**2+vector[0]**2)
	radius_tolerance = 0.1
	if error_magnitude > radius_tolerance:
		return m_v_linear, m_v_angular
	else:
		k_angular=2
	return 0, k_angular*angdiff(robot_angle, desired_angle)
