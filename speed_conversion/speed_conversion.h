#ifndef SPEED_CONVERSION_H
#define SPEED_CONVERSION_H
#include "robot.h"

struct Speeds{float right, left;};

class SpeedConversion
{
	public:
		Speeds start(Robot robot);

	private:
		struct Parameters {float wheel_reduction, r, L, max_tics_per_s, encoder_resolution;};
		const float  pi=3.14159265358979;

		Parameters parameters[3];

		void get_constants(Robot robot);
		Speeds motor_speeds(Speeds wheels, Parameters p);
		Speeds normalize(Speeds s, float a);
		Speeds wheels_speeds(Robot robot, Parameters p);		
};

#endif