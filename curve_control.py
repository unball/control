import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *
from relative_position_converter import *
from new_arch import point
from planar import Vec2

m_v_linear = 0.0
m_v_angular = 0.0
orientation = 1

def curve_controller(robot_vector,desired_vector, robot_angle, desired_angle):
	global m_v_angular
	global m_v_linear
	global orientation



	target = curve_control(robot_vector,desired_vector, robot_angle, desired_angle, 0.8)
	relative_vector = convertTargetPosition(target,robot_vector,robot_angle)
	orientation = 1 #copysign(1,relative_vector[1])

	m_v_linear, m_v_angular = purple_curve_control(relative_vector,orientation, m_v_angular, m_v_linear, robot_angle,0)

	error_magnitude = sqrt(relative_vector[1]**2+relative_vector[0]**2)
	radius_tolerance = 0.01
	if error_magnitude > radius_tolerance:
		return m_v_linear, m_v_angular
	else:
		return 0,0