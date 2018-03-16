#include "joystick.h"
#include <sensor_msgs/Joy.h>
#include <iostream>
#include "ros/ros.h"

void Joystick::receiveJoystickMessage(const sensor_msgs::Joy::ConstPtr &msg_j)
{
	joy = *msg_j;

	leftAxis.h = joy.axes[0];
	leftAxis.v = joy.axes[1];
	l2 = joy.axes[2];
	rightAxis.h = joy.axes[3];
	rightAxis.v = joy.axes[4];
	r2 = joy.axes[5];
	square = joy.buttons[3];

	std::cout << square << std::endl;

}

void Joystick::joystick(Robot robot[3])
{
	for (int i=0;i<3;i++)
	{
		robot[i].u = - (l2 - 1)/3.8 + (r2 - 1)/3.8;
		robot[i].w = leftAxis.h * 5;
	}
}
