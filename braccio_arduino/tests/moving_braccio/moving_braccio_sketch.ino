#include <Bridge.h>
#include <Servo.h>
#include <Braccio.h>
#include <stdio.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

// Here we will hold the values coming from Python via Bridge.
char D12value[2];
int incomingMovementDetails[7];

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
  memset(D12value, 0, 1);
   
  // Initialize digital pins 12 and 13 as output.
  pinMode(ledPin, OUTPUT); 
 
  // Start using the Bridge.
  Bridge.begin();

  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position
  Braccio.begin();
}
 
void loop() {
  Serial.print(D12value);
  Serial.print("Incoming Movement: ");
  //Serial.print(incomingMovementDetails);
  Serial.print("\n");
  // Write current value of D12 to the pin (basically turning it on or off).
  Bridge.get("L13_status", D12value, 2);
  int D12int = atoi(D12value);

  if(D12int == 1){
    digitalWrite(ledPin, HIGH);
  }else{
    digitalWrite(ledPin, LOW);
  }
   
  // An arbitrary amount of delay to make the whole thing more reliable. YMMV
  delay(10);

  Serial.print("Watch out, I'm about to move! \n");
                        //(step delay,   M1, M2,  M3,  M4, M5, M6);
  int movementDetails[] = {20,           0,  15, 180, 170, 0,  73};
  braccioMovement(movementDetails);
}

void braccioMovement(int movementDetails[]) { 

                     //(step delay,   M1, M2,  M3,  M4, M5, M6);
  Braccio.ServoMovement(movementDetails[0], movementDetails[1], movementDetails[2], movementDetails[3],
                        movementDetails[4], movementDetails[5], movementDetails[6]);

  //Wait 1/2 second
  delay(500);

  Braccio.ServoMovement(20,           180,  165, 0, 0, 180,  10); 

  //Wait 1/2 second
  delay(500);
  Serial.print("Hello World \n");
  return;
  
}

