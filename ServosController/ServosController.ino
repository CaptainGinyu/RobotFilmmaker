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
    for (int i = 0; i < motorInstructions.length(); i++)
    {
      char currChar = motorInstructions.charAt(i);
      if (currChar == 'r')
      {
        for (int j = 0; j < 10; j++)
        {
          motor1Angle++;
          motor1.write(motor1Angle);
          delay(50);
        }
      }
      if (currChar == 'l')
      {
        for (int j = 0; j < 10; j++)
        {
          motor1Angle--;
          motor1.write(motor1Angle);
          delay(50);
        }
      }
      if (currChar == 'u')
      {
        for (int j = 0; j < 10; j++)
        {
          motor2Angle++;
          motor2.write(motor2Angle);
          delay(50);
        }
      }
      if (currChar == 'd')
      {
        for (int j = 0; j < 10; j++)
        {
          motor2Angle--;
          motor2.write(motor2Angle);
          delay(50);
        }
      }
    }
  }
}
