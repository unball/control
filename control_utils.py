from math import *
import numpy as np

def calculateErrorAngle(y, x, orientation):
 	if x==0 and y==0:
 		return 0
	th = atan2(-x, y)

	if orientation == 1:
		th = atan2(-x, y)
	else:
		th = atan2(x, -y)

 	return (th)

def angdiff_180(robot_angle,desired_angle):
	return ((robot_angle - desired_angle + pi/2) % (pi)) - pi/2

def angdiff(robot_angle,desired_angle):
	#Difference between two angles, the result wrapped on the interval [-pi,pi].
	return ((robot_angle - desired_angle + pi) % (2*pi)) - pi

def purple_curve(x):
	return x/(1+fabs(x))


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

def drawLine(position,angle):
#this function receives as parameters a point and an angle and returns the line oriented to that angle that crosses that point
	m = tan(angle)
	n = position[1] - position[0] * m
	return m,n

def findIntersection(line1, line2):
#solves a linear system to find intersection between two lines
	a = np.array([[-line1[0] , 1] , [-line2[0], 1]])
	b = np.array([line1[1] , line2[1]])
	intersection = np.linalg.solve(a , b)
	return intersection

def findMiddlePoint(p,q,alpha):
#finds middle point between two points
	x = (alpha*p[0] + (1-alpha)*q[0])
	y = (alpha*p[1] + (1-alpha)*q[1])
	return [x,y]

def curve_control(robot_vector,desired_vector,robot_angle, desired_angle, alpha):
	robot_line = drawLine(robot_vector,robot_angle)
	desired_line = drawLine(desired_vector,desired_angle)
	intersection = findIntersection(robot_line,desired_line)
	middle_point = findMiddlePoint(robot_vector,desired_vector,0.5)
	target = findMiddlePoint(middle_point,intersection,alpha)
	return target



def purple_curve_control(vector, orientation,m_v_angular,m_v_linear,robot_angle=0, desired_angle=0):
	#this two lines make the transformation of cartesian to polar coordinates of the error vector
	error_magnitude = sqrt(vector[1]**2+vector[0]**2)
	error_angle = calculateErrorAngle(vector[1], vector[0], orientation)

	scaling_linear = 0.5;
	scaling_angular = 14;

	k_linear = 5
	k_angular = 1

	v_linear = orientation*scaling_linear*purple_curve(error_magnitude*k_linear)
	v_angular = k_angular*scaling_angular*purple_curve(error_angle*k_angular)

	alpha_ang=0.1
	alpha_lin=0.1

	output_angular = (1-alpha_ang)*v_angular + alpha_ang*m_v_angular
	output_linear = (1-alpha_lin)*v_linear + alpha_lin*m_v_linear 

	return output_linear, output_angular