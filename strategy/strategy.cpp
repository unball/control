#include "strategy.h"
#include "robot.h"
#include "ball.h"

Robot Strategy::go_to_ball(Robot robot, Ball ball)
{
	robot.target_x = ball.x;
	robot.target_y = ball.y;

	robot.control = position;

	return robot;
}


void Strategy::strategy(Robot robot[3], Ball ball)
{
	for (int i=0;i<3;i++)
	{
		robot[i] = go_to_ball(robot[i], ball);
	}


}
