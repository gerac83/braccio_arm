import sys
import requests
import json

def main(positions):

    trajectory = range(0,len(positions))        # Create a list with the same length as the number of positions in the trajectory
    c = 0
    for position in positions:
        position.pop(0)
        trajectory[c] = [int(value) for value in position]          # Insert each joint coordinate casted to int into the trajectory list
        c+=1


    print trajectory
    '''
    if (intValues[0] < 0 or intValues[0] > 180 or intValues[1] < 15 or intValues[1] > 165 or
        intValues[2] < 0 or intValues[2] > 180 or intValues[3] < 0 or intValues[3] > 180 or
        intValues[4] < 0 or intValues[4] > 180):

        print ("\nNot every value is in the accepted range. \n\nM1=base degrees. Allowed "
              "values from 0 to 180 degrees\nM2=shoulder degrees. Allowed values from 15 to "
              "165 degrees \nM3=elbow degrees. Allowed values from 0 to 180 degrees \nM4=wrist "
              "vertical degrees. Allowed values from 0 to 180 degrees \nM5=wrist rotation "
              "degrees. Allowed values from 0 to 180 degrees\nM6=gripper degrees. Allowed "
              "values from 10 to 73 degrees. 10: the tongue is open, 73: the gripper is "
              "closed.")


    # Used for testing
    with open("positions.txt", "a") as f:
        to_be_written = str(intValues)
        to_be_written = to_be_written.replace("[","{")
        to_be_written = to_be_written.replace("]","}")
        data = f.write(to_be_written+",\n")
    # End of testing code
    '''

    url = "http://192.168.1.129:2883/jsonrpc"
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "moving_braccio",
        "params": {"trajectory":trajectory, "length":len(trajectory)},
        "jsonrpc": "2.0",
        "id": 0}

    try:
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()
        print response
        #return response["result"]
    except requests.ConnectionError:
        print "Connection error. Is moving_braccio_arduino.py running?"



if __name__ == "__main__":
    main(sys.argv)
