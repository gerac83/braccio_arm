#include <FileIO.h>
#include <Console.h>

void setup() {
  // Initialize the Bridge and the Serial
  Bridge.begin();
  Serial.begin(9600);
  FileSystem.begin();
  Console.begin();

  /*while (!SerialUSB){
    Console.print("loop\n"); // wait for Serial port to connect.
  }*/
  
  Console.println("Filesystem datalogger\n");
}


void loop() {
  // make a string that start with a timestamp for assembling the data to log:
  String dataString;
  dataString += getTimeStamp();
  dataString += " = ";

  // read three sensors and append to the string:
  for (int analogPin = 0; analogPin < 3; analogPin++) {
    int sensor = analogRead(analogPin);
    dataString += String(sensor);
    if (analogPin < 2) {
      dataString += ",";  // separate the values with a comma
    }
  }

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  // The FileSystem card is mounted at the following "/mnt/FileSystema1"
  File dataFile = FileSystem.open("/mnt/sda1/trajectory.csv", FILE_APPEND);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    Console.println(dataString);
  }
  // if the file isn't open, pop up an error:
  else {
    Console.println("error opening datalog.txt");
  }

  delay(15000);

}

// This function return a string with the time stamp
String getTimeStamp() {
  String result;
  Process time;
  // date is a command line utility to get the date and the time
  // in different formats depending on the additional parameter
  time.begin("date");
  time.addParameter("+%D-%T");  // parameters: D for the complete date mm/dd/yy
  //             T for the time hh:mm:ss
  time.run();  // run the command

  // read the output of the command
  while (time.available() > 0) {
    char c = time.read();
    if (c != '\n') {
      result += c;
    }
  }

  return result;
}
