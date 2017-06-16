import sys
import requests
import json

def main(val):
    url = "http://192.168.1.129:4000/jsonrpc"
    headers = {'content-type': 'application/json'}
    
    # Example echo method
    payload = {
        "method": "led_status",
        "params": {"val": val},
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
        
    print response
    
if __name__ == "__main__":
    # If the value for the led is given, use it. Otherwise keep the led off.
    if len(sys.argv) == 2:
        # Convert string to int
        try:
            intValue = int(sys.argv[1])
            main(intValue)
        except ValueError:
            print "Expecting an int..."
        
    else:
        main(0)
