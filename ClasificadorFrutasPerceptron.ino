#include <ESP32Servo.h>


Servo servo;
int pinServo = 2;
char dato;

void setup() {

  servo.attach(pinServo, 500, 2500);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    dato = Serial.read();
    if (dato == '1') {  
      servo.write(90);
      Serial.println("Moviendo a 90 grados");
    } else if (dato == '2') { 
      servo.write(180);
      Serial.println("Moviendo a 180 grados");
    }
  }
}
