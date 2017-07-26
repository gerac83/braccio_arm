#!/usr/bin/python

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge')
from time import sleep
from bridgeclient import BridgeClient as bridgeclient


value = bridgeclient()
trajectory = []

@dispatcher.add_method
def moving_braccio(**kwargs):
    global trajectory
    trajectory.append([str(kwargs["M1"]),str(kwargs["M2"]),str(kwargs["M3"]),str(kwargs["M4"]),str(kwargs["M5"]),str(kwargs["M6"])])

    if trajectory[-1][-1] == '73':
        executed = False
        for position in trajectory:
            
            value.put('M1',position[0])
            value.put('M2',position[1])
            value.put('M3',position[2])
            value.put('M4',position[3])
            value.put('M5',position[4])
            value.put('M6',position[5])

            if position[5] != '73':
                while(value.get('END') != 'command_received'):
                    pass

        reset_trajectory()
        while (not executed):
            result = value.get('END')
            if result == "command_executed":
                executed = True
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
    run_simple('192.168.1.129', 2883, application)
