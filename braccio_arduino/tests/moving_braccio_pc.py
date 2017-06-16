import sys
import requests
import json

def main(values):
    url = "http://192.168.1.129:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "moving_braccio",
        "params": {"val": values},
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
        
    print response
    
if __name__ == "__main__":
    # If the value for the movement is given, use it. Otherwise keep Braccio steady.
    if len(sys.argv) == 7:
    
        sys.argv.pop(0)
        
        # Convert string to int
        intValues = []
        try:
            for arg in sys.argv:
                intValues.append(int(arg))
            
            main(intValues)
        
        except ValueError:
            print "Expecting an int..."
        
    else:
        print "Expecting 6 values for the servos, " + str(len(sys.argv)-1) + " received. Command ignored."
        main(0)
