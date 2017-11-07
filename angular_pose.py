import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *


def angular_pose(robot_angle, desired_angle):
	k_angular_th = 2
	return 0, angdiff(robot_angle, desired_angle)*k_angular_th