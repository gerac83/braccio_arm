#include <Bridge.h>
#include <Servo.h>
#include <Braccio.h>
#include <stdio.h>
#include <string.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

// Here we will hold the values coming from Python via Bridge.
char incomingMovementDetails[7];
char stringMovementDetails [50];

// Variables used to extract each Servo Motor's position
char * pch;
int servos_movements[6];
int i = 0;

// constants won't change. Used here to set a pin number :
const int ledPin =  LED_BUILTIN;// the number of the LED pin

// Variables will change :
int ledState = LOW;             // ledState used to set the LED

// Generally, you should use "unsigned long" for variables that hold time
// The value will quickly become too large for an int to store
unsigned long previousMillis = 0;        // will store last time LED was updated

// constants won't change :
const long interval = 1000;           // interval at which to blink (milliseconds)

 
void setup() {
  // Zero out the memory we're using for the Bridge.
  memset(incomingMovementDetails, 0, 1);
   
  // Initialize digital pins 12 and 13 as output.
  pinMode(ledPin, OUTPUT); 
 
  // Start using the Bridge.
  Bridge.begin();

  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position
  Braccio.begin();
}
 
void loop() {
//    size = sizeof(incomingMovementDetails);
  //  Serial.print("%d", size);
  // Read Braccio movement coming from Python
  Bridge.get("Braccio_movement", incomingMovementDetails, 50);
  strcpy(stringMovementDetails, incomingMovementDetails);
  
  // Remove spaces, commas and square brackets from the Python input
  // and save the result in an array
  pch = strtok(stringMovementDetails, " [,]");
  while (pch != NULL){
    //Serial.print("%s\n",pch);   // CHECK WHY THIS DOESN'T WORK -- printf works, but Serial.print doesn't
    servos_movements[i] = atoi(pch);
    i++;
    pch = strtok(NULL, " [,]");
  }
  
  Serial.print(stringMovementDetails);
  Serial.print("\n...\n");
  //int movementDetails = atoi(incomingMovementDetails);

  if(sizeof(stringMovementDetails) > 1){
    //Serial.print("Movement: %s \n\n", stringMovementDetails);    // this returns an error for some reason (?)
    //char test[20] = "Hello";
    //Serial.println("Movement: %s \n\n", test);
    digitalWrite(ledPin, HIGH);
    Serial.print("I'm inside");
    Serial.print(incomingMovementDetails[1]);

    
  }
  else{
    digitalWrite(ledPin, LOW);
  }
  
  // Wait one second
  delay(500);

  //Serial.print("Watch out, I'm about to move! \n");
                        //(step delay,   M1, M2,  M3,  M4, M5, M6);
  //int movementDetails[] = {20,           0,  15, 180, 170, 0,  73};
  braccioMovement(servos_movements);
}

void braccioMovement(int movementDetails[]) { 

  //(step delay, M1, M2, M3, M4, M5, M6);
  Braccio.ServoMovement(10,servos_movements[0], servos_movements[1], servos_movements[2], servos_movements[3],
                        servos_movements[4], servos_movements[5]);

  //Wait 1/2 second
  delay(500);

  Braccio.ServoMovement(20,           180,  165, 0, 0, 180,  10); 

  //Wait 1/2 second
  delay(500);
  Serial.print("Hello World \n");
  return;
  
}

