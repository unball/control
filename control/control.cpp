#include "robot.h"
#include "ball.h"
#include "control.h"
#include <math.h>
#include <iostream>

float pi = 3.14159265358;

float Control::angdiff(float alpha, float beta)
{
	float diff = alpha - beta;
	diff = fmod((diff + pi/2),pi) - pi/2;

	return diff;
}


float Control::error_angle(Robot robot)
{
	float angle = atan2((robot.y),(robot.x));
	float target_angle = atan2((robot.target_y),(robot.target_y));

	float angle_error = angdiff(target_angle,angle);

	return angle_error;
}

float Control::error_distance(Robot robot)
{
	float distance = pow((pow((robot.target_x - robot.x),2) + pow((robot.target_y - robot.y),2)),(1/2));
	return distance; 
}

Robot Control::position_control(Robot robot)
{
	float distance_error = error_distance(robot);
	float angle_error = error_angle(robot);

	robot.u = distance_error;
	robot.w = angle_error;

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