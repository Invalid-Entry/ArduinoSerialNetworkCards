#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX


void setup() {
  Serial.begin(38400);
  while (!Serial) {
     ; // wait for serial port to connect. Needed for Native USB only
  }

  // set the data rate for the SoftwareSerial port
  mySerial.begin(38400);
}

void loop() // run over and over
{
  if (mySerial.available())
    Serial.write(mySerial.read());
  if (Serial.available())
    mySerial.write(Serial.read());
}
