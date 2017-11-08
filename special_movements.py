import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *


def special_movements(tag):
	if tag==1:
		#full power forward
		return 1,0
	elif tag==2:
		#full power backward
		return -1,0
	elif tag==3:
		#full power anti-clockwise
		return 0, 15
	elif tag==4:
		#full power clockwise
		return 0,-15
	else:
		return 0,0