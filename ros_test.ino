
#include <Servo.h>

Servo myservo;

String readString; //main captured String
int angle; //data String
int speed1;
int ind; // , locations
unsigned long prevTime = millis();

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(0);
}

void loop() {
  //expect a string like 90,10*
  if (Serial.available())  {
    prevTime = millis();
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == '*') {
      ind = readString.indexOf(',');  //finds location of first
      String s_angle = readString.substring(0, ind);   //captures first data String
      String s_speed1 = readString.substring(ind+1);   //captures second data String
      angle = s_angle.toInt();
      speed1 = s_speed1.toInt();
            
      Serial.println(s_angle+","+s_speed1);
      myservo.write(angle);
  
      readString=""; //clears variable for new input
      //angle="";
      //speed1="";
    } 
    else {     
      readString += c; //makes the string readString
    }
  }
  else if ( (millis()-prevTime) > 100) {
    myservo.write(0);
  }
  delay(1);
}
