/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

int ledPin = 13;
bool prevSend = false;

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
char receivedChar;


void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  receivedChar = '0';
}

void loop() {
  if (Serial.available() > 0) {
    receivedChar = Serial.read();

    if (receivedChar == '1') {
      for (pos = 90; pos <= 180; pos += 2) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        if (prevSend == false) {
          Serial.println(pos);
        }
        prevSend = !prevSend;
        delay(15);                       // waits 15ms for the servo to reach the position
      }
      myservo.write(90);
      for (pos = 90; pos >= 0; pos -= 2) { // goes from 180 degrees to 0 degrees
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        if (prevSend == false) {
          Serial.println(pos);
        }
        prevSend = !prevSend;
        delay(15);                       // waits 15ms for the servo to reach the position
      }
      myservo.write(90);
    }
  }
}

