import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *


m_v_linear = 0.0
m_v_angular = 0.0

def position_control(vector):
	global m_v_linear
	global m_v_angular

	m_v_linear, m_v_angular = purple_curve_control(vector, 1, m_v_angular, m_v_linear)
	
	error_magnitude = sqrt(vector[1]**2+vector[0]**2)
	radius_tolerance = 0.1
	if error_magnitude > radius_tolerance:
		return m_v_linear, m_v_angular
	else:
		return 0,0