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

define CHAR_LENGTH 4

// Here we will hold the values coming from Python via Bridge.
char M1[CHAR_LENGTH]; // Max value would be "999\n", hence buffer size is 4
char M2[CHAR_LENGTH];
char M3[CHAR_LENGTH];
char M4[CHAR_LENGTH];
char M5[CHAR_LENGTH];
char M6[CHAR_LENGTH];

char mem_done[2]; // This var can only take "0\n" or "1\n"

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
  memset(mem_done, 0, 2);
  
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
  Bridge.get("mem_done", mem_done, 2);
  if(mem_done == 1){
     // Read Braccio movement coming from Python
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

     Console.print("\nHELLO WORLD\n");
     if(M6int != 0){
       Console.print("\nM1: ");
       Console.print(M1int);
       Console.print("\nM2: ");
       Console.print(M2int);
       Console.print("\nM3: ");
       Console.print(M3int);
       Console.print("\nM4: ");
       Console.print(M4int);
       Console.print("\nM5: ");
       Console.print(M5int);
       Console.print("\nM6: ");
       Console.print(M6int);
       Braccio.ServoMovement(20, M1int, M2int, M3int, M4int, M5int, M6int);
     }
     else{
       Console.print("\n ...Waiting for a command...\n"); 
     }
     //braccioMovement(M1int, M2int, M3int, M4int, M5int, M6int);
     Console.print("\nBYE WORLD\n");
  }
  else{
   Console.print("\n ...Waiting for mem_done...\n");
  }
  //Wait
  delay(5000);
}

void braccioMovement(int m1, int m2, int m3, int m4, int m5, int m6) { 

  //(step delay, M1, M2, M3, M4, M5, M6);
  if(M6int != 0){
    Console.print("\nM1: ");
    Console.print(m1);
    Console.print("\nM2: ");
    Console.print(m2);
    Console.print("\nM3: ");
    Console.print(m3);
    Console.print("\nM4: ");
    Console.print(m4);
    Console.print("\nM5: ");
    Console.print(m5);
    Console.print("\nM6: ");
    Console.print(m6);
    Braccio.ServoMovement(20, m1, m2, m3, m4, m5, m6);
    digitalWrite(ledPin, HIGH);
    M6int = 0;
  }
  else{
    Console.print("\n ...Waiting for a command...\n");
    digitalWrite(ledPin, LOW);
  }


  return;
  
}

