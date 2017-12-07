const int pin1 = 9;
const int pin2 = 11;
String motorInstructions;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
      pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
//  Serial.println("Yo");
  if (Serial.available())
  {
    Serial.println("HI");
    motorInstructions = Serial.readString();
    for (int i = 0; i < motorInstructions.length(); i++)
    {
      char currChar = motorInstructions.charAt(i);
      Serial.println(currChar);
      if (currChar == 'f')
      {
        digitalWrite(pin1, LOW) ;
           delay(3000);
        digitalWrite(pin2, 100) ;
     
      }
      if (currChar == 'b')
      {
        analogWrite(pin1, 100);
                delay(3000);
        analogWrite(pin2, LOW);

      }
    }
  }
}
