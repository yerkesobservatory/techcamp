#include <SPI.h>
#include <SD.h>

const int chipSelect = 10;

void setup() {
  Serial.println("GPS datalogger test.");
  Serial.begin(9600);
  Serial1.begin(9600);      // default NMEA GPS baud
  
/*  if (!SD.begin(chipSelect)) {
    Serial.println("card failed, or not present.");
    while (1);
    }
  Serial.println("card initialized.");*/

  // There is something wrong with the above section of code.
  // It messes with the output of the serial connection and
  // inserts random characters and deletes others.
}
     
void loop() {

  File dataFile = SD.open("datalog.txt", FILE_WRITE); 
  
  if (Serial.available()) {
    char c = Serial.read();
    Serial1.write(c);
    dataFile.write(c);
    dataFile.close();
  }
  if (Serial1.available()) {
    char c = Serial1.read();
    Serial.write(c);
    dataFile.write(c);
    dataFile.close();
  }
}
