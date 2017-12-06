#include <Servo.h>

const int motorPin1 = 10;
const int motorPin2 = 5;

const int left_side = 12;
const int right_side = 13;
const int left_side_2 = 9;
const int right_side_2 = 11;

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
    pinMode(left_side, OUTPUT);
  pinMode(right_side, OUTPUT);
      pinMode(left_side_2, OUTPUT);
  pinMode(right_side_2, OUTPUT);
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
      if (currChar == 'f')
      {
        analogWrite(left_side, 100);
        analogWrite(right_side, 100);
        digitalWrite(left_side_2,LOW) ;
        digitalWrite(right_side_2,LOW) ;
        delay(3000)
      }
      if (currChar == 'b')
      {
        analogWrite(left_side_2, 100);
        analogWrite(right_side_2, 100);
        digitalWrite(left_side,LOW) ;
        digitalWrite(right_side,LOW) ;
        delay(3000)
      }
    }
  }
}
