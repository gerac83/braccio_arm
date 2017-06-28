#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState

positions = []
last_published = []

def callback(data):
    global positions

    print "\n\nNew Position: "
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", JointState.position)
    names = data.name
    positions.append(data.position)
    
    #print dir(data)
    for name, position in zip(names, positions[-1]):
        print name + ": ", (position)
    print "callback"
    
    return

def publish_positions():
    global last_published
    flag = True
    print "publish_positions"

    pub = rospy.Publisher('positions', String, publish_positions, queue_size=10)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        rospy.loginfo(''.join(map(str, positions)))
    
        print "\n\n\n\nHELLO"
        with open("test.txt", "r") as myfile:
            line = myfile.readlines()

        if len(line[0]) > 1:
            print "hi"
            line = line[0][:-1]

        
        if ''.join(map(str, positions)) != line:
            print "I'M IN!"
            with open("test.txt", "w") as myfile:
                myfile.write(''.join(map(str, positions)))
                myfile.write("\n")

            flag = False

        elif len(positions) > 1:
            pub.publish(''.join(map(str, positions)))
            flag = False

        rate.sleep()


def listener():

    while True:
        rospy.init_node("Positions_parser", anonymous=True)
        rospy.Subscriber("/move_group/fake_controller_joint_states", JointState, callback)
        
#        if len(positions)>1 and positions != last_published:
#            publish_positions()
        publish_positions()
        break
    rospy.spin()

if __name__ == "__main__":
    listener()
