#include <Bridge.h>
#include <Console.h>
#include <Servo.h>
#include <Braccio.h>
#include <stdio.h>
#include <string.h>
#include <SD.h>

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

int M1int,M2int,M3int,M4int,M5int,M6int = -1;
short trajectory[60][6];
int c=0;
bool flag = false;

// constants won't change. Used here to set a pin number :
const int ledPin =  LED_BUILTIN;// the number of the LED pin

// Variables will change :
int ledState = LOW;             // ledState used to set the LED



void setup() {
  //void execute_trajectory(int trajectory[], int *c);
  // Zero out the memory we're using for the Bridge.
  memset(M1, -1, CHAR_LENGTH);
  memset(M2, -1, CHAR_LENGTH);
  memset(M3, -1, CHAR_LENGTH);
  memset(M4, -1, CHAR_LENGTH);
  memset(M5, -1, CHAR_LENGTH);
  memset(M6, -1, CHAR_LENGTH);
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

  for(int c1=0;c1<60;c1++){
      for(int c2=0;c2<6;c2++){
          trajectory[c1][c2] = -1;
      }
  }

  Bridge.put("M6","-1");
}
 
void loop() {
     // Read Braccio movement coming from Python
     ////Console.print("\n");
     Bridge.get("M1", M1, CHAR_LENGTH);
     M1int = atoi(M1);
     //Console.print ("\n");
     //Console.print(M1int);

     Bridge.get("M2", M2, CHAR_LENGTH);
     M2int = atoi(M2);
     //Console.print ("\n");
     //Console.print(M2int);

     Bridge.get("M3", M3, CHAR_LENGTH);
     M3int = atoi(M3);
     //Console.print ("\n");
     //Console.print(M3int);

     Bridge.get("M4", M4, CHAR_LENGTH);
     M4int = atoi(M4);
     //Console.print ("\n");
     //Console.print(M4int);

     Bridge.get("M5", M5, CHAR_LENGTH);
     M5int = atoi(M5);
     //Console.print ("\n");
     //Console.print(M5int);

     Bridge.get("M6", M6, CHAR_LENGTH);
     M6int = atoi(M6);
     //Console.print ("\nM6int: ");
     //Console.print(M6int);
     
     if(M6int != -1){
         trajectory[c][0] = M1int;
         trajectory[c][1] = M2int;
         trajectory[c][2] = M3int;
         trajectory[c][3] = M4int;
         trajectory[c][4] = M5int;
         trajectory[c][5] = M6int;

         if(M6int == 73){
            flag = true;
         }
         // Reset the value of M6 to its safe value
         M6int = -1;
         Bridge.put("M6","-1");
         Bridge.put("END","command_received");
         //Console.print("\n Command put into trajectory");
         
         c++;
     }

     //Console.print("\nc: ");
     //Console.print(c);
     //Console.print("\n");
     for (int z=0; z<c; z++){
          //Console.print(trajectory[z][0]);
          //Console.print(" ");
          //Console.print(trajectory[z][1]);
          //Console.print(" ");
          //Console.print(trajectory[z][2]);
          //Console.print(" ");
          //Console.print(trajectory[z][3]);
          //Console.print(" ");
          //Console.print(trajectory[z][4]);
          //Console.print(" ");
          //Console.print(trajectory[z][5]);
          //Console.print(" \n");
     }

     if(flag){
         //Console.print("\n                     In Execution \n");
         //Bridge.put("END","in_execution");
         for(int d=0; d<c; d++){
              //Console.print("LORENZO\n");
              Braccio.ServoMovement(10, trajectory[d][0], trajectory[d][1], trajectory[d][2], trajectory[d][3], trajectory[d][4], trajectory[d][5]);
              //Console.print(trajectory[d][0]);
              //Console.print(" ");
              //Console.print(trajectory[d][1]);
              //Console.print(" ");
              //Console.print(trajectory[d][2]);
              //Console.print(" ");
              //Console.print(trajectory[d][3]);
              //Console.print(" ");
              //Console.print(trajectory[d][4]);
              //Console.print(" ");
              //Console.print(trajectory[d][5]);
              //Console.print(" \n");
              trajectory[d][0] = -1;
              trajectory[d][1] = -1;
              trajectory[d][2] = -1;
              trajectory[d][3] = -1;
              trajectory[d][4] = -1;
              trajectory[d][5] = -1;
         }
         //Console.print("\n Command Executed");
         flag = false;
         Bridge.put("M6","-1");
         M6int = -1;
         //Console.print("\n Command Executed2");
         Bridge.put("END","command_executed");
         c=0;
     }
     
     //Bridge.put("END","waiting_for_a_command");
     digitalWrite(ledPin, LOW);
     
}
