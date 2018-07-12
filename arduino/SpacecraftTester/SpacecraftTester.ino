/*
 * Program for the Spacecraft component Tester:
 * 
 * To test Servo:
 * - Conect servo data in to pin 9
 * - Connect pot output poin to A1
 * 
 * To test motor:
 * - Connect with button to GND and 5V
 * 
 * To test Distance sensor:
 * - Connect distance sensor analog output to A0
 * - Connect RGB LED R->3 G->4 B->5
 * 
 */

#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int potpin = A1;  // analog pin used to connect the potentiometer
int distpin = A0; // analog pint to connect distance sensor
int redpin = 3;   // RGB LED pins (High for on)
int greenpin = 4;
int bluepin = 5;
int val;    // variable to read the value from the analog pin
int distval; // variable to read distance sensor

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600); // Setup serial communication
  pinMode(redpin, OUTPUT); // Set pins for LED
  pinMode(greenpin, OUTPUT); // Set pins for LED
  pinMode(bluepin, OUTPUT); // Set pins for LED  
}

void loop() {
  // Servo
  val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
  val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
  myservo.write(val);                  // sets the servo position according to the scaled value
  Serial.print("Servo Value:");
  Serial.print(val);
  // Read Distance
  distval = analogRead(distpin);
  // Set RGB depending on distance
  if(distval < 30){
    setRGB(HIGH, LOW, LOW);
  } else if(distval > 100){
    setRGB(LOW, LOW, HIGH);
  } else {
    setRGB(LOW, HIGH, LOW);
  }
  Serial.print(" .   Distance Value:");
  Serial.println(distval);
  delay(30);                           // waits for the servo to get there
}

// Function to set RGB LED r, g, b can be LOW or HIGH
void setRGB(int r, int g, int b){ 
  digitalWrite(redpin, r);  
  digitalWrite(greenpin, g);  
  digitalWrite(bluepin, b);  
}


