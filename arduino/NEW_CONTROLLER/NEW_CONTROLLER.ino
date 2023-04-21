#include <SoftwareSerial.h>

int motor1pin1 = 4;
int motor1pin2 = 5;
int motor2pin1 = 6;
int motor2pin2 = 7;

String msg;
int value;
char direction;

SoftwareSerial BT(10, 11);

void setup() {
  Serial.begin(9600);
  BT.begin(9600);
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);

  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  analogWrite(8, 0); // ENA pin
  analogWrite(9, 0); // ENB pin
}

void loop() {
  if (BT.available()) {
    msg = BT.readStringUntil('\n');
    int separator = msg.indexOf(',');
    value = msg.substring(0, separator).toInt();
    direction = msg.charAt(separator + 1);

    analogWrite(8, value); // ENA pin
    analogWrite(9, value); // ENB pin

    switch (direction) {
      case 'B': // Adelante
        digitalWrite(motor1pin1, HIGH);
        digitalWrite(motor1pin2, LOW);
        digitalWrite(motor2pin1, HIGH);
        digitalWrite(motor2pin2, LOW);
        break;
      case 'F': // Atrás
        digitalWrite(motor1pin1, LOW);
        digitalWrite(motor1pin2, HIGH);
        digitalWrite(motor2pin1, LOW);
        digitalWrite(motor2pin2, HIGH);
        break;
      case 'L': // Izquierda
        digitalWrite(motor1pin1, HIGH);
        digitalWrite(motor1pin2, LOW);
        digitalWrite(motor2pin1, LOW);
        digitalWrite(motor2pin2, HIGH);
        break;
      case 'R': // Derecha
        digitalWrite(motor1pin1, LOW);
        digitalWrite(motor1pin2, HIGH);
        digitalWrite(motor2pin1, HIGH);
        digitalWrite(motor2pin2, LOW);
        break;
      case 'S': // Detener
        digitalWrite(motor1pin1, LOW);
        digitalWrite(motor1pin2, LOW);
        digitalWrite(motor2pin1, LOW);
        digitalWrite(motor2pin2, LOW);
        break;
    }
  }
}
