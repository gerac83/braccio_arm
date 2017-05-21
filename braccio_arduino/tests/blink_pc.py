import requests
import json

def main():
    url = "http://arduino.local:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "led_status",
        "params": {"val": 0},
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
        
    print response
    
if __name__ == "__main__":
    main()
