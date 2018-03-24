#ifndef ROBOT_H
#define ROBOT_H

typedef enum {position, pose} ControlOption;

struct Robot
{
	float x, y, th;
	float target_x, target_y, target_th;
	float u, w;
	float k_u, k_w;
	int id;
	ControlOption control;
};
#endif
