#include "robot.h"
#include "ball.h"
#include "control.h"
#include <math.h>
#include <iostream>

Control::Vector Control::relative_target(Robot robot)
{	
	Control::Vector vector;

	float x = robot.target_x - robot.x;
	float y = robot.target_y - robot.y;

    vector.y = x*cos(robot.th) + y*sin(robot.th);
	vector.x = x*sin(robot.th) - y*cos(robot.th);

	return vector;
}


float Control::error_angle(Vector vector)
{
	float angle_error = atan2(-vector.x,vector.y);

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
	float distance_error = error_distance(target);
	float angle_error = error_angle(target);

	robot.u = 0;//distance_error;
	robot.w = 0;//angle_error;

	std::cout<<angle_error<<std::endl;

	return robot;
}

Robot Control::control(Robot robot)
{
	if (robot.control == POSITION)
	{
		robot = position_control(robot);
	}

	return robot;
}