#ifndef ROBOT_H
#define ROBOT_H

typedef enum {position, pose, turn} ControlOption;

struct Robot
{
	float x, y, th;
	float target_x, target_y, target_th = 0;
	float u, w;
	float k_u, k_w;
	int id;
	ControlOption control;
};
#endif
