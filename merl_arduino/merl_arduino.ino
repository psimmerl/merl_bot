#include <Servo.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* Set the delay between fresh samples */
const int BNO055_SAMPLERATE_DELAY_MS = 100;
Adafruit_BNO055 bno = Adafruit_BNO055(55);


Servo steer;
Servo motor;

String readString; //main captured String
float angleIn; //data String
float speedIn;
int ind; // , locations
double yaw = 0;//, pitch = 0, roll = 0;
sensors_event_t event;

unsigned long prevTime = millis();
unsigned long prevBNOTime = millis();

double mymap(double x, double in_min, double in_max,  double out_min, double out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}


void setup() {
  Serial.begin(9600);

  /* Initialise the sensor */
  if(!bno.begin()) {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
 
  delay(200);
  bno.setExtCrystalUse(true);
  
  steer.attach(9);
  motor.attach(10);
  steer.writeMicroseconds(1500);
  motor.writeMicroseconds(1500);
}

void loop() {
  if ((millis() - prevBNOTime) >= BNO055_SAMPLERATE_DELAY_MS ) {
    prevBNOTime = millis();
    /* Get a new sensor event */
    bno.getEvent(&event);
  
    /* Display the floating point data */
    yaw =(double) event.orientation.x; // 0 is straight ahead
    if ( yaw > 180 ) {
      yaw = mymap(yaw, 180, 360, -2, 0);//car turned 90 left is -1
    }
    else {
      yaw = mymap(yaw, 0, 180, 0, 2);//car turned 90 right is -1
    }
    //pitch = (double) event.orientation.y; roll = (double) event.orientation.z; 
  }
  
  
  //expect a string like 90,10*
  if (Serial.available())  {
    prevTime = millis();
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == '*') {
      ind = readString.indexOf(',');  //finds location of first
      String s_angleIn = readString.substring(0, ind);   //captures first data String
      String s_speedIn = readString.substring(ind+1);   //captures second data String
      angleIn = s_angleIn.toFloat();
      speedIn = s_speedIn.toFloat();
            
      steer.writeMicroseconds(mymap(angleIn, -1, 1, 2000, 1000));
      motor.writeMicroseconds(mymap(speedIn, -1, 1, 2000, 1000));
      int lenc = 2;
      int renc = 3;
      double speed = (lenc + renc) / 2.0; 
      Serial.print(String(angleIn)+","+String(speedIn)+","+String(lenc)+","+String(renc)+","+String(yaw)+","+String(speed)+"*");
  
      readString=""; //clears variable for new input
    } 
    else {     
      readString += c; //makes the string readString
    }
  }
  else if ( (millis()-prevTime) >= 1000) {
    steer.writeMicroseconds(1500);
    motor.writeMicroseconds(1500);
  }
}
