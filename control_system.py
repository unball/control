#!/usr/bin/env python

import rospy
from strategy.msg import strategy_output_msg
from communication.msg import robots_speeds_msg
from measurement_system.msg import measurement_msg
import math
from control_options import *
from position_control import *
from pose_control import *
from pose_line_control import *
from angular_pose import *
from special_movements import *
from curve_control import *

number_of_robots = 3

def control_system_type(data):

	for robot in range(number_of_robots):

		relative_target = convertTargetPositions(data.x[robot],data.y[robot], allies_x[robot], allies_y[robot], allies_th[robot]);
		if data.control_options[robot] ==  control_options.position:
			speeds.linear_vel[robot], speeds.angular_vel[robot] = position_control(relative_target, robot)
		if data.control_options[robot] == control_options.pose:
			speeds.linear_vel[robot], speeds.angular_vel[robot] = pose_control(relative_target, data.th[robot], allies_th[robot])
		if data.control_options[robot] == control_options.pose_line:
			speeds.linear_vel[robot], speeds.angular_vel[robot] = pose_line_control(relative_target, data.th[robot], allies_th[robot], robot)
		if data.control_options[robot] == control_options.direct_speeds:
			speeds.linear_vel[robot], speeds.angular_vel[robot] = data.u[robot], data.w[robot]
		if data.control_options[robot] == control_options.angular_pose:
			speeds.linear_vel[robot], speeds.angular_vel[robot] = angular_pose(data.th[robot], allies_th[robot])
		if data.control_options[robot] == control_options.curve_control:
			robot_vector = [allies_x[robot], allies_y[robot]]
			desired_vector = [data.x[robot],data.y[robot]]
			robot_angle = allies_th[robot]
			desired_angle = data.th[robot]
			speeds.linear_vel[robot], speeds.angular_vel[robot] = curve_controller(robot_vector,desired_vector, robot_angle, desired_angle)
			print data.control_options
			
		speeds.linear_vel[robot], speeds.angular_vel[robot] = saturate(speeds.linear_vel[robot],speeds.angular_vel[robot])
		
		if 1<=int(data.u[robot])<=4:
			speeds.linear_vel[robot], speeds.angular_vel[robot] = special_movements(data.u[robot])
		#if data.control_options[robot] == control_options.special_movements:
		#	speeds.linear_vel[robot], speeds.angular_vel[robot] = special_movements(data.u[robot])
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
		if fabs(w1) >= fabs(w2):
			w2 = max_wheels_speed * w2/fabs(w1)
			w1 = max_wheels_speed * w1/fabs(w1)
		elif fabs(w2) >= fabs(w1):
			w1 = max_wheels_speed * w1/fabs(w2)
			w2 = max_wheels_speed * w2/fabs(w2)

	u = r*(w1+w2)/2
	w = r*(w1-w2)/L
	return u,w

def convertTargetPositions(target_x, target_y, robot_x, robot_y, robot_th):
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
    speeds = robots_speeds_msg()

    rospy.init_node('control_system_node')
    pub = rospy.Publisher('robots_speeds', robots_speeds_msg, queue_size=1)
    rospy.Subscriber('strategy_output_topic', strategy_output_msg, control_system_type)
    rospy.Subscriber('measurement_system_topic', measurement_msg, receiveGlobalPositions)
    rate = rospy.Rate(30)	
    try:
        while not rospy.is_shutdown():
            pub.publish(speeds)
            rate.sleep()
    except rospy.ROSInterruptException:
        exit(1)


if __name__ == '__main__':
	main()
