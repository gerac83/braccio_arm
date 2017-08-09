import choreography_controller
import time


IP1 = 'http://192.168.1.129:4000/jsonrpc'
IP2 = 'http://192.168.1.139:4000/jsonrpc'
IP3 = 'http://192.168.1.141:4000/jsonrpc'

def move_to_initial_positions(IP1,IP2,IP3):
    # Braccio3 is in the position in which it is like if it just gave the ball to Braccio1
    choreography_controller.main(['__ignored__']+[21,133,0,60,90,10], IP3)
    choreography_controller.main(['__ignored__']+[21,133,0,60,90,74], IP3)
    # Braccio1 moves up to receive the ball from the user
    choreography_controller.main(['__ignored__']+[21,133,90,0,0,10], IP1)
    choreography_controller.main(['__ignored__']+[21,133,90,0,0,74], IP1)
    time.sleep(1)
    # Braccio2 is in the waiting position
    choreography_controller.main(['__ignored__']+[79,133,0,60,90,10], IP2)
    choreography_controller.main(['__ignored__']+[79,133,0,60,90,74], IP2)
    time.sleep(1)
    choreography_controller.main(['__ignored__']+[79,90,90,90,90,10], IP1)
    choreography_controller.main(['__ignored__']+[79,90,90,90,90,74], IP1)
    print "Insert ball in the gripper of the Braccio that is pointing up, \
           then press Enter and wait for the gripper to close."
    user_input = 'a'
    while user_input != '':
        user_input = raw_input()
    time.sleep(1)
    # Close gripper
    choreography_controller.main(['__ignored__']+[79,90,90,90,90,73], IP1)
    choreography_controller.main(['__ignored__']+[79,90,90,90,90,74], IP1)
    # Avoid collision through an upward movement
    time.sleep(1)
    choreography_controller.main(['__ignored__']+[21,115,90,0,0,73], IP1)
    choreography_controller.main(['__ignored__']+[21,115,90,0,0,74], IP1)
    time.sleep(1)
    choreography_controller.main(['__ignored__']+[21,133,0,60,0,73], IP1)
    choreography_controller.main(['__ignored__']+[21,133,0,90,0,74], IP1)

    return ((['__ignored__']+[21,133,0,60,0]),(['__ignored__']+[79,133,0,60,90]),(['__ignored__']+[21,133,0,60,90]))



def close_gripper(command, IP):
    time.sleep(0.5)
    choreography_controller.main(command+['73'], IP)        # 73 = closed gripper
    choreography_controller.main(command+['74'], IP)
    time.sleep(0.5)

def open_gripper(command, IP):
    time.sleep(0.5)
    choreography_controller.main(command+['10'], IP)
    choreography_controller.main(command+['74'], IP)
    time.sleep(0.5)

def move_to_the_right(IP):
    '''positions = []
    with open("choreographies/move_to_the_right.csv", "r") as f:
        for line in f:
            line = line[:-1]
            positions.append(line.split(","))

    for position in positions:
        command = ['__ignored__']
        for joint in position:
            command.append(joint)

        # variable result should be 'Done!'
        result = choreography_controller.main(command+['10'], IP)       # gripper = open
        last_command = command

    result = choreography_controller.main(last_command+['74'], IP)      # Suggest end of trajectory
    time.sleep(1)
    #close_gripper(last_command, IP)
    time.sleep(1)'''
    command = [79,133,0,60,90]

    # Braccio1 seems to be slightly lower than the others so increasing its height
    # by 6 degrees on M2 while waiting for the ball should make it the same as B1 and B2
    if '129' in IP:
        command = [79,139,0,60,90]

    # Fix Braccio3 orientation by a couple of degrees
    if '141' in IP:
        command = [82,133,0,58,90]

    choreography_controller.main(['__ignored__']+command+[10], IP)
    choreography_controller.main(['__ignored__']+command+[74], IP)
    return (['__ignored__']+command)

def move_to_the_left(IP):
    command = [79,133,90,0,0]
    # Avoid collision - move up and left
    choreography_controller.main(['__ignored__']+command+[73], IP)
    choreography_controller.main(['__ignored__']+command+[74], IP)
    time.sleep(1)
    command = [21,133,0,60,0]
    # Fix Braccio3 orientation by a couple of degrees
    if '141' in IP:
        command = [18,133,0,60,0]
    choreography_controller.main(['__ignored__']+command+[73], IP)
    choreography_controller.main(['__ignored__']+command+[74], IP)
    time.sleep(1)
    return([['__ignored__'],21,133,0,60,0])
    '''
    # Part 1
    positions = []
    with open("choreographies/move_to_the_left1.csv", "r") as f:
        for line in f:
            line = line[:-1]
            positions.append(line.split(","))

    for position in positions:
        command = ['__ignored__']
        for joint in position:
            command.append(joint)

        # variable result should be 'Done!'
        result = choreography_controller.main(command+['73'], IP)       # gripper = closed
        last_command = command

    result = choreography_controller.main(last_command+['74'], IP)      # Suggest end of trajectory

    time.sleep(1)
    # Part 1
    positions = []
    with open("choreographies/move_to_the_left2.csv", "r") as f:
        for line in f:
            line = line[:-1]
            positions.append(line.split(","))

    for position in positions:
        command = ['__ignored__']
        for joint in position:
            command.append(joint)

        # variable result should be 'Done!'
        result = choreography_controller.main(command+['73'], IP)       # gripper = closed
        last_command = command

    result = choreography_controller.main(last_command+['74'], IP)      # Suggest end of trajectory
    #time.sleep(1)
    '''



'''
positions_b1 = []
with open("choreographies/choreography1_b1.csv", "r") as f:
    for line in f:
        line = line[:-1]
        positions_b1.append(line.split(","))

positions_b2 = []
with open("choreographies/choreography1_b2.csv", "r") as f:
    line = f.readline()[:-1]
    positions_b2.append(line.split(","))

positions_b3 = []
with open("choreographies/choreography1_b3.csv", "r") as f:
    line = f.readline()[:-1]
    positions_b3.append(line.split(","))

last_command = []           # Save the last command
result = ""
'''

b1_last_command, b2_last_command, b3_last_command = move_to_initial_positions(IP1,IP2,IP3)

while(True):

    # S1
    print "\nS1"
    time.sleep(0.5)
    b2_last_command = move_to_the_right(IP2)
    time.sleep(0.5)
    close_gripper(b2_last_command, IP2)
    time.sleep(0.5)
    b3_last_command = move_to_the_right(IP3)
    ###

    # S2
    print "\nS2"
    time.sleep(0.5)
    open_gripper(b1_last_command,IP1)
    time.sleep(0.5)
    b2_last_command = move_to_the_left(IP2)
    ###

    # S3
    print "\nS3"
    time.sleep(0.5)
    b1_last_command = move_to_the_right(IP1)
    time.sleep(0.5)
    close_gripper(b3_last_command, IP3)
    ###

    # S4
    print "\nS4"
    time.sleep(0.5)
    open_gripper(b2_last_command, IP2)
    time.sleep(0.5)
    b3_last_command = move_to_the_left(IP3)
    ###

    # S5
    print "\nS5"
    time.sleep(0.5)
    close_gripper(b1_last_command, IP1)
    time.sleep(0.5)
    b2_last_command = move_to_the_right(IP2)
    time.sleep(0.5)
    ###

    # S6
    print "\nS6"
    time.sleep(0.5)
    open_gripper(b3_last_command, IP3)
    time.sleep(0.5)
    b1_last_command = move_to_the_left(IP1)
