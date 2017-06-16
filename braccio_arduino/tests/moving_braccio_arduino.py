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
    value.put('Braccio_movement',str(kwargs["val"]))
    return "done!"

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('192.168.1.129', 4000, application)

