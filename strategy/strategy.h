#ifndef STRATEGY_H
#define STRATEGY_H

#include "robot.h"
#include "ball.h"

class Strategy
{
	private:
		Robot robot;
		Ball ball;

		Robot go_to_ball(Robot robot, Ball ball);
	public:
		void strategy(Robot robot[3], Ball ball);
};
#endif