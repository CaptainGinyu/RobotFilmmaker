#include <Servo.h>
#include <RBD_Timer.h>

const int motorPin1 = 10;
const int motorPin2 = 5;

const int wheelMotorPin1 = 7;
const int wheelMotorPin2 = 8;
const int wheelMotorPin3 = 2;
const int wheelMotorPin4 = 12;
const int enable12 = 3;
const int enable34 = 4;
const long interval = 300;
RBD::Timer timer;

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

  pinMode(wheelMotorPin1, OUTPUT);
  pinMode(wheelMotorPin2, OUTPUT);
  pinMode(wheelMotorPin3, OUTPUT);
  pinMode(wheelMotorPin4, OUTPUT);
  pinMode(enable12, OUTPUT);
  pinMode(enable34, OUTPUT);
  digitalWrite(enable12, HIGH);
  digitalWrite(enable34, HIGH);

  digitalWrite(wheelMotorPin1, LOW);
  digitalWrite(wheelMotorPin2, LOW);
  digitalWrite(wheelMotorPin3, LOW);
  digitalWrite(wheelMotorPin4, LOW);

  Serial.begin(9600);
}

void loop()
{
  if (timer.onRestart())
  {
    digitalWrite(wheelMotorPin1, LOW);
    digitalWrite(wheelMotorPin2, LOW);
    digitalWrite(wheelMotorPin3, LOW);
    digitalWrite(wheelMotorPin4, LOW);
  }
  if (Serial.available())
  {
    motorInstructions = Serial.readString();
    for (int i = 0; i < motorInstructions.length(); i++)
    {
      char currChar = motorInstructions.charAt(i);
      if (currChar == 'r')
      {
        motor1Angle++;
        motor1.write(motor1Angle);
        delay(50);
      }
      if (currChar == 'l')
      {
        motor1Angle--;
        motor1.write(motor1Angle);
        delay(50);
      }
      if (currChar == 'u')
      {
        motor2Angle++;
        motor2.write(motor2Angle);
        delay(50);
      }
      if (currChar == 'd')
      {
        motor2Angle--;
        motor2.write(motor2Angle);
        delay(50);
      }
      if (currChar == 'f')
      {
        digitalWrite(wheelMotorPin1, HIGH);
        digitalWrite(wheelMotorPin2, LOW);
        digitalWrite(wheelMotorPin3, HIGH);
        digitalWrite(wheelMotorPin4, LOW);
        timer.setTimeout(interval);
        timer.restart();
        
      }
      if (currChar == 'b')
      {
        digitalWrite(wheelMotorPin1, LOW);
        digitalWrite(wheelMotorPin2, HIGH);
        digitalWrite(wheelMotorPin3, LOW);
        digitalWrite(wheelMotorPin4, HIGH);
        timer.setTimeout(interval);
        timer.restart();
      }
      if (currChar == 'z')
      {
        if (motor1Angle < 90)
        {
          while (motor1Angle < 90)
          {
            motor1Angle++;
            motor1.write(motor1Angle);
            delay(50);
          }
        }
        else if (motor1Angle > 90)
        {
          while (motor1Angle > 90)
          {
            motor1Angle--;
            motor1.write(motor1Angle);
            delay(50);
          }
        }
        if (motor2Angle < 90)
        {
          while (motor2Angle < 90)
          {
            motor2Angle++;
            motor2.write(motor2Angle);
            delay(50);
          }
        }
        else if (motor2Angle > 90)
        {
          while (motor2Angle > 90)
          {
            motor2Angle--;
            motor2.write(motor2Angle);
            delay(50);
          }
        }
      }
    }
  }
}
