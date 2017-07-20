#! /usr/bin/env python

import rospy
from __future__ import print_function
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction
from trajectory_msgs.msg import JointTrajectory
from sensor_msgs.msg import JointState

class RobotTrajectoryFollower(object):
    RATE = 0.02

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, FollowJointTrajectoryAction,self.on_goal, self.on_cancel, auto_start=False)
        self.goal_handle = None
        self.traj = JointTrajectory()
        
        #get joint names from parameter server!
        
        # Hack to close the loop between controller and moveit, this is OK for a virtual controller
        rospy.Subscriber("/joint_states", JointState, self._get_states)
        
        self.update_timer = rospy.Timer(rospy.Duration(self.RATE), self._update)
    
    def start(self):
        self._as.start()
        print "The action server for braccio_controller has started!"
        
    def on_goal(self, goal_handle):
    
        if self.goal_handle:
            # If goal_handle doesn't exist, cancels the existing goal
            self.goal_handle.set_canceled()
            self.goal_handle = None
    
        # check that robot is connected
        
        # get joint_names
        joint_names = goal_handle.get_goal().trajectory.joint_names
        joint_positions = goal_handle.get_goal().trajectory.points
        self.traj = goal_handle.get_goal().trajectory
        
        # TODO: Checks that the trajectory has velocities
        
        self.goal_handle.set_accepted()
        
    def on_cancel(self, goal_handle)
    
        if goal_handle == self.goal_handle:
            self.goal_handle.set_canceled()
            self.goal_handle = None
        else:
            goal_handle.set_canceled()
            
    def _update(self, event):
        #update robot state
        
        if self.traj:
        



if __name__ == '__main__':
    rospy.init_node('braccio_controller')
