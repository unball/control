#ifndef ROBOT_H
#define ROBOT_H

typedef enum {POSITION, POSE} Control;

struct Robot
{
	float x, y, th;
	float target_x, target_y, target_th;
	Control control;
};
#endif