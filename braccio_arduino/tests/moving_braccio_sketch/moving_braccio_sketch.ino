#include <Bridge.h>
#include <Console.h>
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

#define CHAR_LENGTH 4

// Here we will hold the values coming from Python via Bridge.
char M1[CHAR_LENGTH]; // Max value would be "999\n", hence buffer size is 4
char M2[CHAR_LENGTH];
char M3[CHAR_LENGTH];
char M4[CHAR_LENGTH];
char M5[CHAR_LENGTH];
char M6[CHAR_LENGTH];

//char mem_done[2]; // This var can only take "0\n" or "1\n"

int M1int;
int M2int;
int M3int;
int M4int;
int M5int;
int M6int;

// constants won't change. Used here to set a pin number :
const int ledPin =  LED_BUILTIN;// the number of the LED pin

// Variables will change :
int ledState = LOW;             // ledState used to set the LED
 
void setup() {
  // Zero out the memory we're using for the Bridge.
  memset(M1, 0, CHAR_LENGTH);
  memset(M2, 0, CHAR_LENGTH);
  memset(M3, 0, CHAR_LENGTH);
  memset(M4, 0, CHAR_LENGTH);
  memset(M5, 0, CHAR_LENGTH);
  memset(M6, 0, CHAR_LENGTH);
  //memset(mem_done, 0, 2);
  
  // Initialize digital pins 12 and 13 as output.
  pinMode(ledPin, OUTPUT);
 
  // Start using the Bridge.
  Bridge.begin();

  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position
  Braccio.begin();

  // To output on the Serial Monitor
  Console.begin();
}
 
void loop() {
 
  // *********** ADD HERE AN IF STATEMENT TO CONTROL WHEN TO READ VALUES FROM MEMORY FOR EXAMPLE:
  // THIS WILL ENSURE THAT ALL VALUE HAVE BEEN WRITTEN IN MEMORY, SEE PYTHON SCRIPT
  //Bridge.get("mem_done", mem_done, 2);
  //if(mem_done == 1){
     // Read Braccio movement coming from Python
     Console.print("\n");
     Bridge.get("M1", M1, CHAR_LENGTH);
     M1int = atoi(M1);
     Console.print ("\n");
     Console.print(M1int);

     Bridge.get("M2", M2, CHAR_LENGTH);
     M2int = atoi(M2);
     Console.print ("\n");
     Console.print(M2int);

     Bridge.get("M3", M3, CHAR_LENGTH);
     M3int = atoi(M3);
     Console.print ("\n");
     Console.print(M3int);

     Bridge.get("M4", M4, CHAR_LENGTH);
     M4int = atoi(M4);
     Console.print ("\n");
     Console.print(M4int);

     Bridge.get("M5", M5, CHAR_LENGTH);
     M5int = atoi(M5);
     Console.print ("\n");
     Console.print(M5int);

     Bridge.get("M6", M6, CHAR_LENGTH);
     M6int = atoi(M6);
     Console.print ("\n");
     Console.print(M6int);

     // Perform the movement if a command was received
     if(M6int != 0){
       // Check that the values for each joint are within the correct ranges
       if (M1int > -1 && M1int < 181 && M2int > 14 && M2int < 166 && M3int > -1 && M3int < 181 &&
           M4int > -1 && M4int < 181 && M5int > -1 && M5int < 181 && M6int > 9 && M6int < 74){
        
          digitalWrite(ledPin, HIGH);
          Braccio.ServoMovement(20, M1int, M2int, M3int, M4int, M5int, M6int);
       }
       else{
          Console.print("\nThe values you sent for the joints are not within the correct range");
       }
     }
     else{
       digitalWrite(ledPin, LOW);
       Console.print("\n ...Waiting for a command...\n");
     }
     
  M6int = 0;
  //Wait
  delay(3000);
}

