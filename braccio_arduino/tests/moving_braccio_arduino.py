#!/usr/bin/python 

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge')
from time import sleep 
from bridgeclient import BridgeClient as bridgeclient


value = bridgeclient()

@dispatcher.add_method
def moving_braccio(**kwargs):
    value.put('M1',str(kwargs["M1"]))
    value.put('M2',str(kwargs["M2"]))
    value.put('M3',str(kwargs["M3"]))
    value.put('M4',str(kwargs["M4"]))
    value.put('M5',str(kwargs["M5"]))
    value.put('M6',str(kwargs["M6"]))
    return "Done!"

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('192.168.1.129', 2883, application)

