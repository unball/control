import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *

def calculateErrorAngle(y, x, orientation):
 	if x==0 and y==0:
 		return 0
	th = atan2(-x, y)

	if orientation == 1:
		th = atan2(-x, y)

	else:
		th = atan2(x, -y)

 	return (th)

def purple_curve(x):
	return x/(1+fabs(x))


m_v_linear = 0.0
m_v_angular = 0.0

def position_control(vector):
			#this two lines make the transformation of cartesian to polar coordinates of the error vector
		error_magnitude = sqrt(vector[1]**2+vector[0]**2)
		#sign = vector[1]/fabs(vector[1])
		sign = copysign(1,vector[1])
		error_angle = calculateErrorAngle(vector[1], vector[0], sign)


		k_linear = purple_curve(error_magnitude*5)
		k_angular = purple_curve(error_angle*0.1)

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
			#return k_linear*error_magnitude, k_angular*error_angle
			return m_v_linear, m_v_angular
			#return scale_velocity(sign*k_linear*error_magnitude, k_angular*error_angle, 0.5)
		else:
			return 0,0


def scale_velocity(u,w,k):
	wheel_reduction = 3/ 1 #motor -> wheel
	r = 0.035 #wheel radius in m
	L = 0.075 #distance between wheels in m

	max_tics_per_s = 70000. #equivalent to 700 tics/10ms
	encoder_resolution = 512.*19
	max_motor_speed = (max_tics_per_s) / encoder_resolution
	max_wheels_speed=max_motor_speed*2*pi/wheel_reduction

	w1=(2*u + L*w)/(2*r)
	w2=(2*u - L*w)/(2*r)

	if fabs(w1) >= fabs(w2):
		w2 = k*max_wheels_speed * w2/fabs(w1)
		w1 = k*max_wheels_speed * w1/fabs(w1)
	elif fabs(w2) >= fabs(w1):
		w1 = k*max_wheels_speed * w1/fabs(w2)
		w2 = k*max_wheels_speed * w2/fabs(w2)

	u = r*(w1+w2)/2
	w = r*(w1-w2)/L
	return u,w
