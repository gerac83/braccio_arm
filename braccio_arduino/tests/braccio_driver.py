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
    
    final_positions = []

    for elem in positions:
        start = elem.index("[")
        end = elem.index("]")
        final_positions.append(elem[start+1:end].split(","))    # Useless if using next line
        to_be_appended = elem[start+1:end].split(",")
        command = ['__ignored__']
        for elem in to_be_appended:
            #command = command + [abs(float(elem))*(57.2958)]      # Append degrees and not radians
            #command = command + [float(elem)*(57.2958)]
            if 'e' in elem:
                command = command + [0]
            else:
                command = command + [float(elem)*(57.2958)+90]
                #command = command + [float(elem)]
        
        print "\n\n"
        print command
        moving_braccio_pc.main(command+['73'])      # Keep the gripper closed
        #time.sleep(3)
        
    
    #moving_braccio_pc.main(['__ignored__', '180', '165', '0', '0', '180', '73'])

def listener():

    rospy.init_node("Positions_parser", anonymous=True)
    rospy.Subscriber("/move_group/display_planned_path", DisplayTrajectory, callback)
    
    rospy.spin()

if __name__ == "__main__":
    listener()
