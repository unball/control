import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *


m_v_linear = 0.0
m_v_angular = 0.0
orientation = [1,1,1]


def fast_position_control(vector, robot):
	global m_v_linear
	global m_v_angular
	global orientation

	margin = 50
	margin = 2*pi*margin/360

	error = calculateErrorAngle(vector[1], vector[0],1)
	
	#if (orientation[robot] == 1) and (fabs(error)>(pi-margin)):
	#	orientation[robot] = -1
	#elif (orientation[robot] == -1) and (fabs(error)<margin):
	#	orientation[robot] = 1

	m_v_linear, m_v_angular = fast_purple_curve(vector, orientation[robot], m_v_angular, m_v_linear)

	return m_v_linear,m_v_angular
	
