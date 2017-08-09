#!/usr/bin/python

'''
Change the IP address on line 57 to the one
assigned to your Arduino, upload this script,
ssh into your Arduino and run this script.
NOTE: you'll need to have Python, requests
and Werkzeug installed.
'''
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge')
from time import sleep
from bridgeclient import BridgeClient as bridgeclient
import csv

value = bridgeclient()
trajectory = []

@dispatcher.add_method
def moving_braccio(**kwargs):
    global trajectory
    trajectory.append([str(kwargs["M1"]),str(kwargs["M2"]),str(kwargs["M3"]),str(kwargs["M4"]),str(kwargs["M5"]),str(kwargs["M6"])])

    if trajectory[-1][-1] == '74':
        executed = False

        # Write to SD card
        with open("/mnt/sda1/trajectory.csv", "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for position in trajectory[:-1]:                    # ignore the last position (trajectory[-1][-1]=74 is used as a flag)
                writer.writerow((position[0],position[1],position[2],position[3],position[4],position[5]))

        reset_trajectory()

        value.put('new_trj','T')
        while (not executed):
            result = value.get('END')
            if result == "command_executed":
                executed = True

    # ALSO RESET CSV FILE MAYBE, depending on what line 24 does (append or overwrite?)!!!!!!!!!!!!!!
    return "Done!"

def reset_trajectory():
    global trajectory
    trajectory = []
    return

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('192.168.1.140', 4000, application)
