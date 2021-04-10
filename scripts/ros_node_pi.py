#!/usr/bin/env python
import future
from glob import glob
import time, serial, os, rospy, rosnode
from std_msgs.msg import String
''' ROS node for the Raspberry Pi
  Don't run at 60hz -- it causes jitter in the arduino serial reading
'''

ARDUINO_PORT = glob('/dev/ttyACM*')[0]
ARDUINO_BAUD_RATE = 9600
SERIAL_TIMEOUT = 0.01

angle, speed = 0, 0

def NN_callback(data):
  global angle, speed
  angle, speed = tuple(map(float, data.data.split(',')))

def piNode():
  global angle, speed
  rospy.init_node('ros_node_pi') 

  pub = rospy.Publisher('/car_angle_speed', String, queue_size=1)
  sub = rospy.Subscriber('/NN_angle_speed', String, NN_callback)
  ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD_RATE, timeout=SERIAL_TIMEOUT)
  
  rate = rospy.Rate(15) # 30hz
  ser.flushInput()


  while not rospy.is_shutdown(): 
    try:
      while ser.inWaiting() and "*" not in data: 
        data+=ser.read().decode('utf-8')
        if "*" in data:
          print(data)
          (_, __, l_enc, r_enc, c_angle, c_speed) = tuple(data.replace('*','').split(','))
          pub.publish( "{},{}".format(c_angle,c_speed))
          data = ""
          pass
    except: 
      ser.flushInput()
      data = ""
      print("Error Reading Arduino")

    if "/ros_node_laptop" in rosnode.get_node_names():
      ser.write("{},{}*".format(angle,speed).encode('utf-8'))
    else:
      print("Laptop node does not exist! Stopping Robot!")
      ser.write('0,0*'.encode('utf-8'))

    rate.sleep()

  ser.close()

if __name__ == '__main__':
  print("Starting MERL Bot Raspberry Pi Node")
  try:
    piNode()
  except rospy.ROSInterruptException:
    pass
