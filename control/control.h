#ifndef CONTROL_H
#define CONTROL_H

#include "robot.h"
#include "ball.h"

class Control
{
	private:
		Robot robot;
		float orientation;
		float k_u, k_w;
		struct Vector {float x,y;};
		Vector vector;

		void get_constants();
		Vector relative_target(Robot robot);
		float error_angle(Vector vector, float orientation);
		float error_distance(Vector vector);
		Robot position_control(Robot robot);

	public:
		void control(Robot robot[3]);

};
#endif