#include "iostream"
#include "ros/ros.h"
#include "vector"
#include "control/robots_speeds_msg.h"
#include "measurement_system/measurement_msg.h"
#include "strategy/strategy.h"
#include "control/control.h"
#include "include/robot.h"
#include "include/ball.h"
#include "joystick/joystick.h"

using namespace std;

measurement_system::measurement_msg positions;
control::robots_speeds_msg robots_speeds;

Strategy strategy;
Control controller;
Joystick joystick;

Robot robot[3];
Ball ball;

bool using_joystick;

void receiveMeasurementMessage(const measurement_system::measurement_msg::ConstPtr &msg_m)
{
	positions = *msg_m;

	for (int i=0; i<3; i++)
	{
		robot[i].x = positions.x[i];
		robot[i].y = positions.y[i];
		robot[i].th = positions.th[i];
		robot[i].id = i;
	}

	ball.x = positions.ball_x;
	ball.y = positions.ball_y;
	ball.x_pred = positions.ball_x_pred;
	ball.y_pred = positions.ball_y_pred;
	ball.x_walls = positions.ball_x_walls;
	ball.y_walls = positions.ball_y_walls;
}

void isOk()
{
	cout << robot[0].w << endl;
}

int main(int argc, char **argv){

	ros::init(argc, argv, "planning_node");

	ros::NodeHandle n;
	ros::Publisher publisher = n.advertise<control::robots_speeds_msg>("robots_speeds",1);
	ros::Rate loop_rate(10);

	ros::param::get("system/using_joystick", using_joystick);

	ros::Subscriber subscriber = n.subscribe("measurement_system_topic",1,receiveMeasurementMessage);

	if (using_joystick)
	{
		subscriber = n.subscribe("joy", 1, &Joystick::receiveJoystickMessage, &joystick);
	}

	int count = 0;
	while (ros::ok())
	{
	//	isOk();
		if (using_joystick)
		{
			joystick.joystick(robot);
		}

		else
		{
			strategy.strategy(robot,ball);
			controller.start(robot);
		}

		for (int i=0;i<3;i++)
		{
			robots_speeds.linear_vel[i] = robot[i].u;
			robots_speeds.angular_vel[i] = robot[i].w;
		}
		publisher.publish(robots_speeds);
		ros::spinOnce();
		loop_rate.sleep();
		++count;
	}
	return 0;
}
