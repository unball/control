import rospy
from PID import *
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import isnan
from math import atan2
from math import pi
from math import fabs
from math import sqrt

#Control constants
Kp_lin = [1, 1, 1]
Ki_lin = [0, 0, 0]

Kp_ang = [1, 1, 1]
Ki_ang  = [0, 0, 0]

wheel_reduction = 3/ 1 #motor -> wheel
r = 0.035 #wheel radius in m
L = 0.075 #distance between wheels in m

max_tics_per_s = 70000. #equivalent to 700 tics/10ms
encoder_resolution = 512.*19
max_motor_speed = (max_tics_per_s) / encoder_resolution
max_wheels_speed=max_motor_speed*2*pi/wheel_reduction

number_of_robots = 3

def calculateErrorAngle(y, x):
	if x==0 and y==0:
		return 0
	th = atan2(-x, y)
	return (th)


def saturate(u,w):
	w1=(2*u + L*w)/(2*r)
	w2=(2*u - L*w)/(2*r)

	if (w1 > max_wheels_speed) or (w2 > max_wheels_speed):
		if fabs(w1) >= fabs(w2):
			w2 = max_wheels_speed * w2/fabs(w1)
			w1 = max_wheels_speed * w1/fabs(w1)
		elif fabs(w2) >= fabs(w1):
			w1 = max_wheels_speed * w1/fabs(w2)
			w2 = max_wheels_speed * w2/fabs(w2)

	u = r*(w1+w2)/2
	w = r*(w1-w2)/L
	return u,w

def control(error_magnitude, error_angle):
	k_linear=1
	k_angular=10
	return k_linear*error_magnitude, k_angular*error_angle

def calculate_robot_speeds(vector):
	for robot in range(number_of_robots):
		#this two lines make the transformation of cartesian to polar coordinates of the error vector
		error_magnitude = sqrt(vector.y[robot]**2+vector.x[robot]**2)
		error_angle = calculateErrorAngle(vector.y[robot], vector.x[robot])

		speeds.linear_vel[robot],speeds.angular_vel[robot] = control(error_magnitude, error_angle)
		speeds.linear_vel[robot],speeds.angular_vel[robot] = saturate(speeds.linear_vel[robot],speeds.angular_vel[robot])

		print speeds
		

def robot_speed_control_node():
	print '[PositionControl]robot_speed_control_node: begin'

	global speeds
	speeds = robots_speeds_msg()

	rospy.init_node('position_control_node', anonymous=True)
	rate = rospy.Rate(10)

	pub = rospy.Publisher('robots_speeds', robots_speeds_msg, queue_size=10)
	rospy.Subscriber('relative_positions_topic', target_positions_msg, calculate_robot_speeds)

	while not rospy.is_shutdown():
		notAnumber = False
		for i in range(3):
			if isnan(speeds.linear_vel[i]) or isnan(speeds.angular_vel[i]):
				notAnumber = True
		if not notAnumber:
			pub.publish(speeds)
			rate.sleep()

if __name__ == '__main__':
	try:
		robot_speed_control_node()
	except rospy.ROSInterruptException:
		pass
