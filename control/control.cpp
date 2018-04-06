#include "robot.h"
#include "ball.h"
#include "control.h"
#include <math.h>
#include "ros/ros.h"
#include <fstream>
#include <iostream>

int orientation = 1;

Robot Control::get_constants(Robot robot)
{
	std::string parameter_u, parameter_w;
	parameter_u = "robot"+std::to_string(robot.id)+"/u";
	parameter_w = "robot"+std::to_string(robot.id)+"/w";
	ros::param::get(parameter_u,robot.k_u);
	ros::param::get(parameter_w,robot.k_w);

	return robot;

}

Control::Vector Control::relative_target(Robot robot)
{
	Control::Vector vector;

	float x = robot.target_x - robot.x;
	float y = robot.target_y - robot.y;
	
	vector.y = x*cos(robot.th) + y*sin(robot.th);
	vector.x = x*sin(robot.th) - y*cos(robot.th);

	return vector;
}


float Control::error_angle(Vector vector, float orientation)
{
	float angle_error = atan2(-orientation*vector.x,orientation*vector.y);

	return angle_error;
}

float Control::error_distance(Vector vector)
{
	float distance = pow((pow(vector.x,2) + pow(vector.y,2)),(1/2));
	return distance;
}

Robot Control::motion_control(Robot robot)
{
	Vector target = relative_target(robot);
	orientation = orientation_trigger(target);
	float distance_error = error_distance(target);
	float angle_error = error_angle(target,orientation);

	robot = get_constants(robot);

	robot.u = distance_error*orientation*robot.k_u*cos(angle_error);
	robot.w = angle_error*robot.k_w;

	return robot;
}

int Control::orientation_trigger(Vector vector)
{

	if (orientation == 1)
	{
		if (fabs(atan2(-vector.x,vector.y)) > trigger_down)
		{
			orientation = -1;
		} 
	}
	else
	{
		if (fabs(atan2(-vector.x,vector.y)) < trigger_up)
		{
			orientation = 1;
		}
	}
	return orientation;
}

void Control::start(Robot robot[3])
{
	for (int i=0;i<3;i++)
	{
		if (robot[i].control == position)
		{
			robot[i] = motion_control(robot[i]);
		}
	}
}
