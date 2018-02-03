cmake_minimum_required(VERSION 2.8.3)
project(control)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  rospy
  rosserial_arduino
  rosserial_client
  joy
)

add_definitions (-std=c++11)

find_package(Boost REQUIRED COMPONENTS system)

add_message_files(DIRECTORY msg FILES
  robots_speeds_msg.msg)
generate_messages(DEPENDENCIES std_msgs)

catkin_package()


include_directories(
  include/
  ${catkin_INCLUDE_DIRS}
  ${Boost_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
  ${SDFormat_INCLUDE_DIRS}
)

link_directories(
  ${Boost_LIBRARY_DIRS}
  ${GAZEBO_LIBRARY_DIRS}
  ${SDFormat_LIBRARY_DIRS}
)



catkin_install_python(PROGRAMS control_system.py
                      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

add_executable(control control.cpp)
target_link_libraries(control ${catkin_LIBRARIES})
