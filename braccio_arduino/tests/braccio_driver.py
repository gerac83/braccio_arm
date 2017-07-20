#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from moveit_msgs.msg import DisplayTrajectory
import moving_braccio_pc
import time


def callback(data):

    print "\n\nNew Position: "
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", DisplayTrajectory.trajectory)
    
    text = str(data.trajectory[0])

    text = text.split("\n")
    positions = []
    for line in text:
        if "positions" in line:
            positions.append(line)

    last_command = []           # Save the last command
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
        
        print "\n\n"
        print command
        moving_braccio_pc.main(command+['10'])      # Keep the gripper open
        last_command = command
        
    moving_braccio_pc.main(last_command+['73'])      # Close the gripper to grasp the object
        

def listener():

    rospy.init_node("Positions_parser", anonymous=True)
    rospy.Subscriber("/move_group/display_planned_path", DisplayTrajectory, callback)
    
    rospy.spin()

if __name__ == "__main__":
    listener()
