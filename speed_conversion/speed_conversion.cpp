#include "robot.h"
#include "ball.h"
#include <math.h>
#include "ros/ros.h"
#include "speed_conversion.h"
#include <fstream>
#include <iostream>

void SpeedConversion::get_constants(Robot robot)
{
	std::string param_wr, param_r, param_L, param_mtps, param_encoder;
	param_wr = "robot"+std::to_string(robot.id)+"/wheel_reduction";
	param_r = "robot"+std::to_string(robot.id)+"/r";
	param_L = "robot"+std::to_string(robot.id)+"/L";
	param_mtps = "robot"+std::to_string(robot.id)+"/max_tics_per_s";
	param_encoder = "robot"+std::to_string(robot.id)+"/encoder_resolution";

	ros::param::get(param_wr,parameters[robot.id].wheel_reduction);
	ros::param::get(param_r,parameters[robot.id].r);
	ros::param::get(param_L,parameters[robot.id].L);
	ros::param::get(param_mtps,parameters[robot.id].max_tics_per_s);
	ros::param::get(param_encoder,parameters[robot.id].encoder_resolution);
}

Speeds SpeedConversion::wheels_speeds(Robot robot, Parameters p)
{
	Speeds wheels;
	wheels.right = (-robot.u + (p.L/2)*robot.w) / p.r;
	wheels.left = (-robot.u - (p.L/2)*robot.w) / p.r;
	wheels.right = wheels.right/(2*pi);
	wheels.left = wheels.left/(2*pi);
	return wheels;
}

Speeds SpeedConversion::normalize(Speeds s, float a)
{
		if (fabs(s.right) >= fabs(s.left))
		{
			s.left = a * s.left/fabs(s.right);
			s.right = a * s.right/fabs(s.right);
		}
		else if (fabs(s.left) > fabs(s.right))
		{
			s.right = a * s.right/fabs(s.left);
			s.left = a * s.left/fabs(s.left);
		}

	return s;
}

Speeds SpeedConversion::motor_speeds(Speeds wheels, Parameters p)
{
	Speeds motor;
	motor.right = p.wheel_reduction * wheels.right * p.encoder_resolution/100;
	motor.left = p.wheel_reduction * wheels.left * p.encoder_resolution/100;
	float max_motor_speed = p.max_tics_per_s/100;

	if (fabs(motor.right) > max_motor_speed || fabs(motor.left) > max_motor_speed)
	{
		motor = normalize(motor,max_motor_speed);
	}
	return motor;
}

Speeds SpeedConversion::start(Robot robot)
{
	Speeds motors;
	get_constants(robot);
	Speeds wheels = wheels_speeds(robot,parameters[robot.id]);
	motors = motor_speeds(wheels,parameters[robot.id]);

	return motors;

}