#include <Servo.h>

const int motorPin1 = 10;
const int motorPin2 = 5;

Servo motor1;
Servo motor2;

String motorInstructions;
int motor1Angle;
int motor2Angle;
int commaLocation;

void setup()
{
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  motor1.attach(motorPin1);
  motor2.attach(motorPin2);

  motor1Angle = 90;
  motor2Angle = 90;

  motor1.write(motor1Angle);
  motor2.write(motor2Angle);

  Serial.begin(9600);
}

void loop()
{
  if (Serial.available())
  {
    motorInstructions = Serial.readString();
    commaLocation = motorInstructions.indexOf(",");
    motor1Angle = motorInstructions.substring(0, commaLocation).toInt() + motor1Angle;
    motor2Angle = motorInstructions.substring(commaLocation + 1).toInt() + motor2Angle;
    motor1.write(motor1Angle);
    motor2.write(motor2Angle);
  }
}
