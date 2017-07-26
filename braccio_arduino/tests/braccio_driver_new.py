#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from moveit_msgs.msg import DisplayTrajectory
import moving_braccio_pc_new
import time


def callback(data):

    print "\n\nNew Trajectory: "
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", DisplayTrajectory.trajectory)

    text = str(data.trajectory[0])

    text = text.split("\n")
    positions = []
    for line in text:
        if "positions" in line:
            positions.append(line)

    trajectory = []
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


        trajectory.append(command+['10'])      # Keep the gripper open

    # variable result should be 'Done!'
    #result = moving_braccio_pc_new.main(trajectory)
    moving_braccio_pc_new.main(trajectory)

def listener():

    rospy.init_node("Positions_parser", anonymous=True)
    rospy.Subscriber("/move_group/display_planned_path", DisplayTrajectory, callback)

    rospy.spin()

if __name__ == "__main__":
    listener()
