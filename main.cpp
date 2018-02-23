#include "iostream"
#include "ros/ros.h"
#include "control/robots_speeds_msg.h"
#include "measurement_system/measurement_msg.h"
#include "strategy/strategy.h"
#include "control/control.h"
#include "include/robot.h"
#include "include/ball.h"

using namespace std;

measurement_system::measurement_msg position;
control::robots_speeds_msg robots_speeds;

Strategy strategy;
Control controller;

Robot robot[3];
Ball ball;

void receiveMeasurementMessage(const measurement_system::measurement_msg::ConstPtr &msg_m)
{
	position = *msg_m;

	for (int i=0; i<3; i++)
	{
		robot[i].x = position.x[i];
		robot[i].y = position.y[i];
		robot[i].th = position.th[i];
	}

	ball.x = position.ball_x;
	ball.y = position.ball_y;
	ball.x_pred = position.ball_x_pred;
	ball.y_pred = position.ball_y_pred;
	ball.x_walls = position.ball_x_walls;
	ball.y_walls = position.ball_y_walls;

}

void isOk()
{
	cout << robot[0].w << endl;
}

int main(int argc, char **argv){

	ros::init(argc, argv, "control_system_node");

	ros::NodeHandle n;
	ros::Publisher publisher = n.advertise<control::robots_speeds_msg>("robots_speeds",1);
	ros::Rate loop_rate(10);
	ros::Subscriber measurementSystemSubscriber = n.subscribe("measurement_system_topic",1,receiveMeasurementMessage);


	int count = 0;
	while (ros::ok())
	{
	//	isOk();
	robot[0] = strategy.go_to_ball(robot[0],ball);
	robot[0] = controller.control(robot[0]);
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