class control_options:
    position = 1		#moves to x,y position, only forward
    pose = 2			#moves to x,y position and then turn to th, only forward
    momentum = 3		#not implemented
    angular_pose= 4		#turn to th
    direct_speeds = 5	#override control actions
    pose_line = 6		#moves to x,y position and turn to th or (th-180), go forward or backwards
    special_movements = 7