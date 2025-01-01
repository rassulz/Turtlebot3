#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
import math, sys, time, random
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

############################## ROS Part   #############################

def active_cb():
    rospy.loginfo("Goal pose being processed")

def feedback_cb(feedback):
	     
    x1=feedback.base_position.pose.orientation.x
    y1=feedback.base_position.pose.orientation.y
    z1=feedback.base_position.pose.orientation.z
    w1=feedback.base_position.pose.orientation.w
    rospy.loginfo("Current Location: "  +str(feedback))
    return x1,y1,z1,w1  
	
def done_cb(status,result):
    if status==3:
    	rospy.loginfo("Goal reached")
    if status==2 or status==8:
    	rospy.loginfo("Goal cancelled")
    if status==8:
    	rospy.loginfo("Goal aborted")

######################  Start from here #################
# x=-0.593, y=-7.196, yaw=90
file1 = open("/home/ilyas/first_ws/src/mypkg/scripts/goalPoints.txt", 'r')        ## load goa_point_list          
lines=file1.readlines()

#######################################################################
for line in lines:

    line=line.strip()
    x1=line.split(',')
    print("X=",float(x1[0]),"Y=",float(x1[1]),"Yaw=",float(x1[2]) )
    print("--------------")

######################
    xt=float(x1[0])  # x-position
    yt=float(x1[1])  # y-position
    yaw=float(x1[2]) # Yaw (w.r.t x-axis of ROS_map)
######################

    rospy.init_node('send_goal')
    
    navclient=actionlib.SimpleActionClient('move_base',MoveBaseAction)
    navclient.wait_for_server()

# example of nav goal
    goal=MoveBaseGoal()
    goal.target_pose.header.frame_id="map"
    goal.target_pose.header.stamp=rospy.Time.now()

# Goal Position
    goal.target_pose.pose.position.x= xt 
    goal.target_pose.pose.position.y= yt 
    goal.target_pose.pose.position.z=yaw

# Goal Orientation
    roll=0.0
    pitch=0.0
    quat = quaternion_from_euler(roll, pitch,yaw)
    goal.target_pose.pose.orientation.x=quat[0]
    goal.target_pose.pose.orientation.y=quat[1]
    goal.target_pose.pose.orientation.z=quat[2]
    goal.target_pose.pose.orientation.w=quat[3]
    print("--IN----LOOP--------")
    navclient.send_goal(goal,done_cb,active_cb,feedback_cb)
    finished=navclient.wait_for_result()
    if not finished:
    	rospy.logerr("Action server Not available")
    else:
    	rospy.loginfo(navclient.get_result())

