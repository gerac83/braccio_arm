#include <FileIO.h>
#include <Console.h>
#include <Bridge.h>
#include <Servo.h>
#include <Braccio.h>
#include <string.h>

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

#define CHAR_LENGTH 4
// Here we will hold the value coming from Python via Bridge.
char bridge_flag[CHAR_LENGTH];

String line;
short trajectory[100][6];
int c=0;
char key[] = ",";         // Used to split a command to get each joint's position
int start_index;          // Used with comma_index for parsing the joint's position
int comma_index;          // Index of the first comma found in the String


void setup() {
  // Zero out the memory we're using for the Bridge.
  memset(bridge_flag, 0, CHAR_LENGTH);
  
  // Initialize the Bridge and the Serial
  Bridge.begin();
  Serial.begin(9600);
  FileSystem.begin();
  Console.begin();

  // Start using the Bridge.
  Bridge.begin();

  // Initialization functions and set up the initial position for Braccio
  // All the servo motors will be positioned in the "safety" position
  Braccio.begin();

  // new_trj will work as a flag to know when MoveIt has sent a new trajectory to be followed by Braccio
  Bridge.put("new_trj", "F");
}


void loop() {

  // Check if MoveIt has sent a new trajectory
  Bridge.get("new_trj", bridge_flag, CHAR_LENGTH);

  // If new trajectory available, read the file where it is written and execute it
  if(bridge_flag[0] == 'T'){
      // Open the file
      File dataFile = FileSystem.open("/mnt/sda1/trajectory.csv", FILE_READ);
    
      // if the file is available, read and print the first line
      if(dataFile){
          
          while(dataFile.available()){
              line = String(dataFile.readStringUntil(10));     // newLine in ASCII
              
              if(line != "" && c!=100){
                  start_index = 0;
                  
                  for (int z=0;z<5;z++){
                    comma_index = strcspn(line.c_str(),key);
                    trajectory[c][z] = (short)line.substring(start_index,comma_index).toInt();
                    line[comma_index] = '.';
                    start_index = comma_index+1;
                  }
                  
                  trajectory[c][5] = (short)line.substring(comma_index+1,(comma_index+3)).toInt();  // 10 < gripper < 73
                  c++;
              }
              else if(c == 100){
                  Console.println("\nERROR:The trajectory limit (100 positions) has been reached");
              }
              
          }
      }
      else{
          Console.println("\nERROR: File not found. Make sure that the SD card is inserted in the Arduino and that the file /mnt/sda1/trajectory.csv exists");
          delay(1000);
      }
    
      dataFile.close();
      
      for(int d=0; d<c; d++){
          Braccio.ServoMovement(10, trajectory[d][0], trajectory[d][1], trajectory[d][2], trajectory[d][3], trajectory[d][4], trajectory[d][5]);
          if(d==0){
              delay(50);       // After the initial position, wait a moment -- useful visually when Braccio isn't in the right initial position but this line can be removed
          }
      }

      Bridge.put("END","command_executed");       // Tell Python the command was executed
      c=0;                                        // Reset the number of positions in the trajectory
      Bridge.put("new_trj", "F");                 // Reset the new trajectory flag
  }
  else{
      Console.println("... Waiting for a command...");
  }
  
  delay(20);

}
