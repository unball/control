#include "robot.h"
#include "ball.h"
#include "control.h"
#include <math.h>
#include "ros/ros.h"
#include <fstream>
#include <iostream>

void Control::get_constants()
{
	ros::param::get("/position/u",k_u);
	ros::param::get("/position/w",k_w);
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

Robot Control::position_control(Robot robot)
{	
	Vector target = relative_target(robot);
	float orientation = copysignf(1,target.y);
	float distance_error = error_distance(target);
	float angle_error = error_angle(target,orientation);

	get_constants();

	robot.u = distance_error*orientation*k_u;
	robot.w = angle_error*k_w;

	return robot;
}

void Control::control(Robot robot[3])
{
	for (int i=0;i<3;i++)
	{
		if (robot[i].control == POSITION)
		{
			robot[i] = position_control(robot[i]);
		}
	}
}