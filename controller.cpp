#include "iostream"
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "control/robots_speeds_msg.h"
#include "strategy/strategy_output_msg.h"
#include "measurement_system/measurement_msg.h"

using namespace std;

strategy::strategy_output_msg target;
measurement_system::measurement_msg position;
control::robots_speeds_msg msg;

void receiveTargets(const strategy::strategy_output_msg::ConstPtr &msg_s)
{
	target = *msg_s;
}

void receiveMeasurementMessage(const measurement_system::measurement_msg::ConstPtr &msg_m)
{
	position = *msg_m;
}

int main(int argc, char **argv){

	ros::init(argc, argv, "control_system_node");

	ros::NodeHandle n;
	ros::Publisher publisher = n.advertise<control::robots_speeds_msg>("robots_speeds",1);
	ros::Rate loop_rate(10);
	ros::Subscriber strategySubscriber = n.subscribe("strategy_output_topic", 1, receiveTargets);
	ros::Subscriber measurementSystemSubscriber = n.subscribe("measurement_system_topic",1,receiveMeasurementMessage);

	int count = 0;
	while (ros::ok())
	{
		publisher.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
		++count;
	}
	return 0;
}