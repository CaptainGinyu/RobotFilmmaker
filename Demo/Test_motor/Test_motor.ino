#include <Servo.h> 
 
Servo t;  // create servo object to control a servo 
Servo p; 
int pos;
int pos2;
int motor1Angle = 90;
int motor2Angle  = 45;
String  motorInstructions;
int motor1Angle_update;
int motor2Angle_update;
int commaLocation;
 
void setup() 
{ 
   Serial.begin(9600);
  t.attach(5); 
  p.attach(10);
} 
 
void loop() 
{ 
  if (Serial.available())
  {
    Serial.println("------------------------------------------------------------------");
    motorInstructions = Serial.readString();
    commaLocation = motorInstructions.indexOf(",");
    Serial.println("commaLocation: ");
    Serial.print(commaLocation);
    motor1Angle_update = motorInstructions.substring(0, commaLocation).toInt();
    Serial.println("Input 1: ");
    Serial.print(motor1Angle_update);
    motor2Angle_update = motorInstructions.substring(commaLocation+1).toInt();
    Serial.println("Input 2: ");
    Serial.print(motor2Angle_update);
    if (motor1Angle < 140 and motor2Angle < 90 and motor1Angle > 0 and motor2Angle < 0)
    {
      if (motor1Angle_update > 0)
      {
        for(pos=motor1Angle; pos <=motor1Angle + motor1Angle_update; pos++)
           {
            Serial.println("Motor 1 +");
             t.write(pos);
             delay(60);
             Serial.println(pos);
           }
       }
       else 
       {
        for(pos=motor1Angle; pos >= motor1Angle + motor1Angle_update; pos--)
           {
            Serial.println("Motor 1 -");
             t.write(pos);
             delay(60);
             Serial.println(pos);
           }
       }

       
      if (motor2Angle_update > 0)
      {
        for(pos2=motor2Angle; pos2 <=motor2Angle + motor2Angle_update; pos2++)
           {
            Serial.println("Motor 2 +");
             p.write(pos2);
             delay(60);
             Serial.println(pos2);
           }
       }
       else 
       {
        for(pos2=motor2Angle; pos2 >= motor2Angle + motor2Angle_update; pos2--)
           {
            Serial.println("Motor 2 -");
             p.write(pos2);
             delay(60);
             Serial.println(pos2);
           }
       }
    }
    else 
    {
      motor1Angle= 90;
      motor2Angle = 45;
      }
    
    motor1Angle = motor1Angle + motor1Angle_update;
    motor2Angle = motor2Angle + motor2Angle_update;
    Serial.println("Motor 1 Updated Angle: ");
    Serial.println(motor1Angle);
    Serial.println("Motor 2 Updated Angle: ");
    Serial.println(motor2Angle);
    }

}

