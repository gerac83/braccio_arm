#include <Bridge.h>
#include <Console.h>
#include <Servo.h>
#include <Braccio.h>
#include <stdio.h>
#include <string.h>
#include <SPI.h>
#include <SD.h>

File myFile;
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

//short trajectory[50][6];
String nextPosition;

void setup() {
  
  // Start using the Bridge.
  Bridge.begin();
  SD.begin();
//  FileSystem.begin();

  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position
  Braccio.begin();

  // To output on the Serial Monitor
  Console.begin();

  /*for(int c1=0;c1<50;c1++){
      for(int c2=0;c2<6;c2++){
          trajectory[c1][c2] = -1;
      }
  }*/

  // Open serial communications and wait for port to open:
  Serial.begin(9600);

  if (!SD.begin(4)) {
    Console.println("initialization failed!");
    //return;
  }
  Console.println("initialization done.");

  myFile = SD.open("test.txt", FILE_WRITE);
  //myFile = SD.open("/root/first_test/trajectory.csv", FILE_READ);

if (myFile){
      Console.print("Writing to test.txt...\n");
      myFile.println("testing 1, 2, 3.");
      // close the file:
      myFile.close();
      Console.print("done.\n");
  }
  else{
      // if the file didn't open, print an error:
      Console.print("error opening test.txt");
  }

  // re-open the file for reading:
  myFile = SD.open("test.txt");
  if (myFile){
      Console.print("test.txt: ");
  
      // read from the file until there's nothing else in it:
      while (myFile.available()) {
        Console.print(myFile.read());
      }
      // close the file:
      myFile.close();
  } 
  else{
      // if the file didn't open, print an error:
      Console.print("error opening test.txt\n");
  }
}
 
void loop() {
    Console.print("Start\n");
    nextPosition = myFile.read();
    Console.println(String(myFile.read()));
    myFile.close();
    Console.print("End\n");
    delay(1000);
}
