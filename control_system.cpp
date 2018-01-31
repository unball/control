#include <ros/ros.h>

ros::Publisher publisher;


int main(){

    ros::init(argc, argv, "control_system_node");
    ros::NodeHandle n;
    ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
    ros::Rate loop_rate(10);

    while (ros::ok()){
         ros::spinOnce();
        loop_rate.sleep();
    }


  return 0;
}
    return 0;
}