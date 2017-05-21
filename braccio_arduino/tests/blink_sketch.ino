#include <Bridge.h>
#include <stdio.h>
 
// Here we will hold the values coming from Python via Bridge.
char D12value[2];

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
}
 
void loop() {
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
}

