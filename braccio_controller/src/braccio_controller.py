#! /usr/bin/env python

import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction
from control_msgs.msg import FollowJointTrajectoryResult
from trajectory_msgs.msg import JointTrajectory
from sensor_msgs.msg import JointState
import sys
sys.path.append('/home/lorenzo/catkin_ws/src/braccio_arm/braccio_arduino/tests')
import moving_braccio_pc


joint_names = ['braccio_joint_1', 'braccio_joint_2', 'braccio_joint_3', 'braccio_joint_4', 'braccio_joint_5']

class RobotTrajectoryFollower(object):
    RATE = 0.02

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.ActionServer(self._action_name+"/follow_joint_trajectory", FollowJointTrajectoryAction, self.on_goal, self.on_cancel, auto_start=False)
        self.goal_handle = None
        self.traj = None
        self.lenpoints = None
        self.index = 0

        self.current_positions = [0.0] * len(joint_names)

        self.pub_joint_states = rospy.Publisher('joint_states', JointState, queue_size=1)

        self.update_timer = rospy.Timer(rospy.Duration(self.RATE), self._update)

    def start(self):
        self._as.start()
        rospy.logwarn("The action server for braccio_controller has started")

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

        rospy.loginfo("Accepting goal!")
        # Replaces the goal
        self.goal_handle = goal_handle
        self.traj = goal_handle.get_goal().trajectory
        self.lenpoints = len(self.traj.points)
        self.index = 0
        self.goal_handle.set_accepted("Trajectory accepted!")
        print self.traj
        print type(self.traj)
        text = str(self.traj)
        text = text.split("\n")
        positions = []
        for line in text:
            if "positions" in line:
                positions.append(line)

        last_command = []           # Save the last command
        result = ""
        for elem in positions:
            start = elem.index("[")
            end = elem.index("]")
            to_be_appended = elem[start+1:end].split(",")
            command = ['__ignored__']
            for elem in to_be_appended:
                if 'e' in elem:
                    command = command + [0]
                else:
                    command = command + [float(elem)*(57.2958)+90]

            # variable result should be 'Done!'
            result = moving_braccio_pc.main(command+['10'])       # Keep the gripper open
            last_command = command

        result = moving_braccio_pc.main(last_command+['73'])      # Close the gripper to grasp the object

    def on_cancel(self, goal_handle):

        if goal_handle == self.goal_handle:
            self.goal_handle.set_canceled()
            self.goal_handle = None
        else:
            goal_handle.set_canceled()

    def _update(self, event):
        #update robot state
        now = rospy.get_rostime()

        msg = JointState()
        msg.header.stamp = now
        msg.header.frame_id = "From arduino webserver for braccio"
        msg.name = joint_names

        if self.traj and self.goal_handle:
            #rospy.logwarn("UPDATE ************************")
            #rospy.logwarn(self.traj)

            if self.index == self.lenpoints:
                msg_success = 'Trajectory execution successfully completed'
                rospy.logwarn(msg_success)
                res = FollowJointTrajectoryResult()
                res.error_code=FollowJointTrajectoryResult.SUCCESSFUL
                self.goal_handle.set_succeeded(result=res, text=msg_success)
                self.goal_handle = None
                self.index = 0
                self.lenpoints = None
                self.traj = None
            else:
                position = self.traj.points[self.index].positions
                self.index += 1
                self.current_positions = position

        msg.position = self.current_positions
        #msg.effort = [0] * 5
        self.pub_joint_states.publish(msg)



if __name__ == '__main__':
    rospy.init_node('braccio_controller')
    as_ = RobotTrajectoryFollower("braccio_controller")
    as_.start()
    rospy.spin()
