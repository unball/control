#!/usr/bin/env python

import rospy
from strategy.msg import strategy_output_msg
from communication.msg import robots_speeds_msg
from measurement_system.msg import measurement_msg
import math
from control_options import *
from position_control import *

number_of_robots = 3


def control_system_type(data):
	if data.control_options[0] == control_options.position:
		relative_target = convertTargetPositions(data.x[0],data.y[0], data.th[0],
												 allies_x[0], allies_y[0], allies_th[0])
		speeds.linear_vel[0], speeds.angular_vel[0] = position_control(relative_target)
		pub.publish(speeds)

def saturate(u,w):
	wheel_reduction = 3/ 1 #motor -> wheel
	r = 0.035 #wheel radius in m
	L = 0.075 #distance between wheels in m

	max_tics_per_s = 70000. #equivalent to 700 tics/10ms
	encoder_resolution = 512.*19
	max_motor_speed = (max_tics_per_s) / encoder_resolution
	max_wheels_speed=max_motor_speed*2*pi/wheel_reduction

	w1=(2*u + L*w)/(2*r)
	w2=(2*u - L*w)/(2*r)

	if (fabs(w1) > max_wheels_speed) or (fabs(w2) > max_wheels_speed):
		print ('aa')
		if fabs(w1) >= fabs(w2):
			w2 = max_wheels_speed * w2/fabs(w1)
			w1 = max_wheels_speed * w1/fabs(w1)
		elif fabs(w2) >= fabs(w1):
			w1 = max_wheels_speed * w1/fabs(w2)
			w2 = max_wheels_speed * w2/fabs(w2)

	u = r*(w1+w2)/2
	w = r*(w1-w2)/L
	return u,w

def convertTargetPositions(target_x, target_y, target_th, robot_x, robot_y, robot_th):
    relative_target = [target_x - robot_x, target_y - robot_y]
    relative_target = convert_axis_to_robot(relative_target, robot_th)
    return relative_target

def convert_axis_to_robot(vector, th):
	#Receive angle in radians
    ax = vector[0]
    ay = vector[1]

    y = ax*math.cos(th) + ay*math.sin(th)
    x = ax*math.sin(th) - ay*math.cos(th)

    return [x,y]

allies_x = [0, 0, 0]
allies_y = [0, 0, 0]
allies_th = [0, 0, 0]

def receiveGlobalPositions(data):
    for robot in range(number_of_robots):
        allies_x[robot] = data.x[robot]
        allies_y[robot] = data.y[robot]
        allies_th[robot] = data.th[robot]
def main():
	print 'control_system node started'

	global speeds
	global pub
	speeds = robots_speeds_msg()

	rospy.init_node('control_system_node')
	pub = rospy.Publisher('robots_speeds', robots_speeds_msg, queue_size=10)
	rospy.Subscriber('strategy_output_topic', strategy_output_msg, control_system_type)
	rospy.Subscriber('measurement_system_topic', measurement_msg, receiveGlobalPositions)
	rospy.spin()


if __name__ == '__main__':
	main()
