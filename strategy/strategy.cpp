#include "strategy.h"
#include "robot.h"
#include "ball.h"
#include "math.h"
#include <iostream>

Robot Strategy::go_to_ball(Robot robot, Ball ball)
{
	robot.target_x = ball.x;
	robot.target_y = ball.y;

	robot.control = position;

	return robot;
}

Robot Strategy::olympic_lap(Robot robot)
{
	float next_target_x, next_target_y;
	if(robot.target_y == 0.5 && robot.target_x ==0.5)
	{
		next_target_x = -0.5;
		next_target_y = 0.5;

	}
	else if(robot.target_y == 0.5 && robot.target_x == -0.5)
	{
		next_target_x = -0.5;
		next_target_y = -0.5;

	}
	else if(robot.target_y == -0.5 && robot.target_x == -0.5)
	{
		next_target_y = -0.5;
		next_target_x = 0.5;

	}
	else if(robot.target_y == -0.5 && robot.target_x == 0.5)
	{
		next_target_y = 0.5;
		next_target_x = 0.5;
		
	}
	else
	{
		robot.target_y = 0.5;
		robot.target_x = 0.5;
	
	}
	if(fabs(robot.y - robot.target_y) <=0.1 && fabs(robot.x - robot.target_x) <=0.1)
	{
		robot.target_x = next_target_x;
		robot.target_y = next_target_y;
	}
	robot.control = position;
	std::cout << robot.target_y << std::endl;
	return robot;
}


void Strategy::strategy(Robot robot[3], Ball ball)
{
	robot[0] = olympic_lap(robot[0]);
	for (int i=1;i<3;i++)
	{
		robot[i] = go_to_ball(robot[i],ball);
	}


}
