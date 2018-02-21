#ifndef ROBOT_H
#define ROBOT_H

typedef enum {POSITION, POSE} ControlOption;

struct Robot
{
	float x, y, th;
	float target_x, target_y, target_th;
	float u, w;
	ControlOption control;
};
#endif