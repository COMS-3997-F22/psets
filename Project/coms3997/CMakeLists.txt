cmake_minimum_required(VERSION 2.8.3)
project(coms3997)

find_package(catkin REQUIRED COMPONENTS
  duckietown_msgs
  roscpp
  rospy
  std_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

endif()