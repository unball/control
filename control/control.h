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
		const float  pi=3.14159265358979;
		float trigger_down = 120*(2*pi/360);
		float trigger_up = 60*(2*pi/360);

		Robot get_constants(Robot robot);
		int orientation_trigger(Vector vector);
		Vector relative_target(Robot robot);
		float error_angle(Vector vector, float orientation);
		float error_distance(Vector vector);
		Robot motion_control(Robot robot);
		Robot make_turn(Robot robot, float radius);

	public:
		void start(Robot robot[3]);

};
#endif
