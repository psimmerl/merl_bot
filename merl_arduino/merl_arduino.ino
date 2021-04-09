#include <Servo.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* Set the delay between fresh samples */
// #define BNO055_SAMPLERATE_DELAY_MS (100)
// Adafruit_BNO055 bno = Adafruit_BNO055(55);


Servo steer;
Servo motor;

String readString; //main captured String
float angle; //data String
float speed1;
int ind; // , locations
double roll = 0, pitch = 0, yaw = 0;

unsigned long prevTime = millis();
unsigned long prevBNOTime = millis();


void setup() {
  Serial.begin(9600);

  /* Initialise the sensor */
  // if(!bno.begin()) {
  //   /* There was a problem detecting the BNO055 ... check your connections */
  //   Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
  //   while(1);
  // }
 
  delay(200);
  // bno.setExtCrystalUse(true);
  
  steer.attach(9);  // attaches the servo on pin 9 to the servo object
  motor.attach(10);
  //steer.writeMicroseconds(1500);
  //motor.writeMicroseconds(1500);
  steer.write(90);
  motor.write(90);
}

void loop() {

  // if (prevBNOTime - millis() >= BNO055_SAMPLERATE_DELAY_MS ) {
  //   prevBNOTime = millis();
  //   /* Get a new sensor event */
  //   sensors_event_t event;
  //   bno.getEvent(&event);
  
  //   /* Display the floating point data */
  //   yaw = (double) event.orientation.x; // 0 is straight ahead
  //   pitch = (double) event.orientation.y;
  //   roll = (double) event.orientation.z; 
  //   //Serial.print(String(yaw)+","+String(pitch)+"*");
  // }
  
  
  //expect a string like 90,10*
  if (Serial.available())  {
    prevTime = millis();
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == '*') {
      ind = readString.indexOf(',');  //finds location of first
      String s_angle = readString.substring(0, ind);   //captures first data String
      String s_speed1 = readString.substring(ind+1);   //captures second data String
      angle = s_angle.toFloat();
      speed1 = s_speed1.toFloat();
            
      //steer.writeMicroseconds(map(angle, -1, 1, 2000, 1000));
      //motor.writeMicroseconds(map(speed1, -1, 1, 2000, 1000);
      steer.write(map(angle, -1.0, 1.0, 180.0, 0.0));
      motor.write(map(speed1, -1.0, 1.0, 180.0, 0.0));
      Serial.print(String(angle)+","+String(speed1)+","+String(yaw)+","+String(pitch)+"*");
      //Serial.print(s_angle+","+s_speed1+","+String(yaw)+","+String(pitch)+"*");

  
      readString=""; //clears variable for new input
      //angle="";
      //speed1="";
    } 
    else {     
      readString += c; //makes the string readString
    }
  }
  /*else if ( (millis()-prevTime) >= 1000) {
    //steer.writeMicroseconds(1500);
    //motor.writeMicroseconds(1500);
    steer.write(90);
    motor.write(90);
  }*/
}
