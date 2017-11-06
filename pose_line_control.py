import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *

m_v_linear = 0.0
m_v_angular = 0.0

def pose_line_control(vector, robot_angle, desired_angle):
		#this two lines make the transformation of cartesian to polar coordinates of the error vector
		error_magnitude = sqrt(vector[1]**2+vector[0]**2)
		sign = copysign(1,vector[1])
		error_angle = calculateErrorAngle(vector[1], vector[0], sign)

		k_linear = purple_curve(error_magnitude*8)
		k_angular = purple_curve(error_angle*0.3)

		v_linear = sign*k_linear*0.5
		v_angular = k_angular*14

		alpha_ang=0.1
		alpha_lin=0.1
		global m_v_angular
		global m_v_linear
		m_v_angular = (1-alpha_ang)*v_angular + alpha_ang*m_v_angular
		m_v_linear = (1-alpha_lin)*v_linear + alpha_lin*m_v_linear


		radius_tolerance = 0.1
		if error_magnitude > radius_tolerance:
			return m_v_linear, m_v_angular
		else:
			k_angular=2
		return 0, k_angular*angdiff(robot_angle, desired_angle)

