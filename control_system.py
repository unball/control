import rospy
from strategy.msg import strategy_output_msg
from communication.msg import robots_speeds_msg
from math import *




def control_system_type(data):
	print data.flag


def main():
	print 'control_system node started'

	global speeds
	speeds = robots_speeds_msg()

	rospy.init_node('control_system_node')
	pub = rospy.Publisher('robots_speeds', robots_speeds_msg, queue_size=10)
	rospy.Subscriber('strategy_output_topic', strategy_output_msg, control_system_type)
	rospy.spin()


if __name__ == '__main__':
	main()