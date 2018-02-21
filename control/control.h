#ifndef CONTROL_H
#define CONTROL_H

#include "robot.h"
#include "ball.h"

class Control
{
	private:
		Robot robot;
		float alpha, beta;

		float angdiff(float alpha, float beta);
		float error_angle(Robot robot);
		float error_distance(Robot robot);
		Robot position_control(Robot robot);

	public:
		Robot control(Robot robot);

};
#endif