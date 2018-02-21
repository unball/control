#include "strategy.h"
#include "robot.h"
#include "ball.h"


Robot Strategy::go_to_ball(Robot robot, Ball ball)
{
	robot.target_x = ball.x;
	robot.target_x = ball.x;

	robot.control = POSITION;

	return robot;
}