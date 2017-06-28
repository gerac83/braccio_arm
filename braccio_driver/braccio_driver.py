#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from moveit_msgs.msg import DisplayTrajectory

def callback(data):

    print "\n\nNew Position: "
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", DisplayTrajectory.trajectory)
    
    #print dir(data)
    text = str(data.trajectory[0])
    #print text

    text = text.split("\n")
    positions = []
    for line in text:
        if "positions" in line:
            positions.append(line)
    
    final_positions = []
    for elem in positions:
        start = elem.index("[")
        end = elem.index("]")
        final_positions.append(elem[start+1:end].split(","))
    
    publish_positions(final_positions)

def publish_positions(final_positions):
    print "publish_positions"

    pub = rospy.Publisher('positions', String, queue_size=10)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        rospy.loginfo(final_positions)
        pub.publish(''.join(map(str, final_positions)))

        rate.sleep()

def listener():

    rospy.init_node("Positions_parser", anonymous=True)
    rospy.Subscriber("/move_group/display_planned_path", DisplayTrajectory, callback)
    
    rospy.spin()

if __name__ == "__main__":
    print "Working"
    listener()
