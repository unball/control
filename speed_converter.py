#!/usr/bin/env python

import rospy

from communication.msg import comm_msg
from communication.msg import wheels_speeds_msg

msg = comm_msg()

def publishSpeeds(wheels_speed):
    global msg
    msg.MotorA = (wheels_speed.right_vel[0])*0.256
    msg.MotorB = (wheels_speed.left_vel[0])*0.256

def publisher():
    global msg
    pub = rospy.Publisher('radio_topic', comm_msg, queue_size=10)
    rospy.init_node('speed_converter', anonymous=True)
    rate = rospy.Rate(10)
    rospy.Subscriber('wheels_speed', wheels_speeds_msg, publishSpeeds)

    while not rospy.is_shutdown():
        msg.menu = 8           
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
