#ifndef JOYSTICK_H_
#define JOYSTICK_H_

#include "robot.h"
#include "ball.h"
#include <sensor_msgs/Joy.h>

class Joystick
{
	private:
		Robot robot;
		sensor_msgs::Joy joy;

		struct axis {float v, h;};
		axis leftAxis;
		axis rightAxis;
		float l2;
		float r2;
		int square;

	public:
		
		void receiveJoystickMessage(const sensor_msgs::Joy::ConstPtr &msg_j);
		void joystick(Robot robot[3]);

};

#endif