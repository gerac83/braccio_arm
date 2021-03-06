import sys
import requests
import json


payload = {}
headers = {'content-type': 'application/json'}


def main(values, IP):

	global payload

	# If the value for the movement is given, use it. Otherwise keep Braccio steady.
	if len(values) == 7:

		values.pop(0)
		# Convert list of strings to int
		intValues = []
		try:
			for value in values:
				intValues.append(int(float(value)))


		except ValueError:
			print "Expecting an int..."

	else:
		print "Expecting 6 values for the servos, " + str(len(values)-1) + " received. Command ignored."
		intValues = [0]

	#print "choreography_controller prints intValues: ", intValues

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


	if (len(intValues) > 1):
		# Example echo method
		payload = {
			"method": "moving_braccio",
			"params": {"M1": intValues[0], "M2": intValues[1], "M3": intValues[2], "M4": intValues[3], "M5": intValues[4], "M6": intValues[5]},
			"jsonrpc": "2.0",
			"id": 0,
		}
	else:
		# Example echo method
		payload = {
			"method": "moving_braccio",
			"params": {"M6": 0},
			"jsonrpc": "2.0",
			"id": 0,
		}

	try:
		response = requests.post(
			IP, data=json.dumps(payload), headers=headers).json()
		print "Arduino ", IP, response


	except requests.ConnectionError:
		print "Connection error. Is moving_braccio_arduino.py running?"



if __name__ == "__main__":
	main(sys.argv)
