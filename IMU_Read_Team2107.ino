#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <PID_v1.h>

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)
Adafruit_BNO055 bno = Adafruit_BNO055(55);
 
double roll = 0, pitch = 0, yaw = 0;
double v = 0;
double traj = 0, vel = 0;
double servoGoal, motorGoal;

Servo servo;
Servo motor;

const int servoPin = 3, motorPin = 5;
const int kp_servo = 1, ki_servo = 0, kd_servo = 0;
const int kp_motor = 1, ki_motor = 0, kd_motor = 0;

PID servoPID(&yaw, &servoGoal, &traj, kp_servo, ki_servo, kd_servo, DIRECT);
PID motorPID(&v, &motorGoal, &vel, kp_motor, ki_motor, kd_motor, DIRECT);


void setup(void) {
  Serial.begin(9600);

  /* Initialise the sensor */
  if(!bno.begin()) {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
 
  delay(1000);
  bno.setExtCrystalUse(true);
  
  /* Turn the PIDs on */
  servo.attach(servoPin);
  motor.attach(motorPin);

  servoPID.SetMode(AUTOMATIC);
  motorPID.SetMode(AUTOMATIC);
  
}

void loop(void) {
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Display the floating point data */
  yaw = (double) event.orientation.x-180; // 0 is straight ahead
  pitch = (double) event.orientation.y;
  roll = (double) event.orientation.z; 
  v = 10; //TODO

  Serial.println(str(yaw)+','+str(pitch)+','+str(roll))+','+str(v);

  /* Read the NN predicted trajectory and velocity from Serial */
  std::string s; size_t pos = 0; traj = null;
  if (Serial.available() > 0) { 
    s = Serial.readString();
    while ((pos = s.find(',')) != std::string::npos) {
      int temp = stod(s.substr(0, pos),&std::string::size_type);
      if ( traj != null) { traj = temp; }
      else { vel = temp; }
      s.erase(0, pos + delimiter.length());
    }
  }
  //TODO: Include something that stop robots if no new input within 2(?) seconds

  servoPID.Compute()
  motorPID.Compute()

  servo.write(servoGoal);
  motor.write(motorGoal);
  /* Wait the specified delay before requesting nex data */
  delay(BNO055_SAMPLERATE_DELAY_MS);
}
