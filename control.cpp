#include "iostream"
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "control/robots_speeds_msg.h"
#include "strategy/strategy_output_msg.h"

using namespace std;

void printMessage(const strategy::strategy_output_msg::ConstPtr &msg_v)
{
	strategy::strategy_output_msg message = *msg_v;
	cout << message.x[1] << endl;
}

int main(int argc, char **argv){

	ros::init(argc, argv, "control_system_node");

	ros::NodeHandle n;
	ros::Publisher publisher = n.advertise<control::robots_speeds_msg>("robots_speeds",1);
	ros::Rate loop_rate(10);
	ros::Subscriber subscriber = n.subscribe("strategy_output_topic", 1, printMessage);

	int count = 0;
	while (ros::ok())
	{
		control::robots_speeds_msg msg;
		msg.linear_vel[0] = 1;
		msg.linear_vel[1] = 0;
		msg.linear_vel[2] = 0;
		msg.angular_vel[0] = 15;
		msg.angular_vel[1] = 0;
		msg.angular_vel[2] = 0;
		publisher.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
		++count;
	}
	return 0;
}