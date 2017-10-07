def convertTargetPositions(global_target, position):
    relative_target = [global_target.x - position.x, global_target.y - position.y]
    relative_target = convert_axis_to_robot(relative_target, position.th)
    return relative_target
#Receive angle in radians
def convert_axis_to_robot(vector, th):
    ax = vector[0]
    ay = vector[1]

    y = ax*math.cos(th) + ay*math.sin(th)
    x = ax*math.sin(th) - ay*math.cos(th)

    return [x,y]