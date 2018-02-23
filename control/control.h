#ifndef CONTROL_H
#define CONTROL_H

#include "robot.h"
#include "ball.h"

class Control
{
	private:
		Robot robot;
		float alpha, beta;
		float x, y;
		struct Vector {float x,y;};
		Vector vector;

		Vector relative_target(Robot robot);
		float error_angle(Vector vector);
		float error_distance(Vector vector);
		Robot position_control(Robot robot);

	public:
		Robot control(Robot robot);

};
#endif