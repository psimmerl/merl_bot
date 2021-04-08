import time, serial, os, rospy, rosnode
from std_msgs.msg import String
'''ROS node for the Raspberry Pi'''

ARDUINO_PORT = '/dev/ttyUSB0'
ARDUINO_BAUD_RATE = 9600
SERIAL_TIMEOUT = 0.01

angle, speed = 0, 0

def tv_callback(data):
  global angle, speed
  print "********************************here**********************************"
  angle, speed = tuple(map(float, data.data.split(',')))

def piNode():
  global angle, speed
  #Open Arduino
  ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD_RATE, timeout=SERIAL_TIMEOUT)

  rospy.init_node('ros_node_pi') 
  pub = rospy.Publisher('/car_angle_speed', String, queue_size=1)
  sub = rospy.Subscriber("/NN_angle_speed", String, tv_callback)
  
  rate = rospy.Rate(30) # 30hz
  ser.flushInput()

  data = ""
  while not rospy.is_shutdown(): 
    #ser.flushOutput()
    #Read data from the Arduino
    #data = tuple(ser.readline()[:-2].decode('utf-8').split(','))
    while ser.inWaiting(): 
      data+=ser.read().decode('utf-8')
      if "*" in data:
        (c_angle, c_speed) = tuple(data.replace('*','').split(','))
        #if c_angle == '':
        #  print("************************ERROR************************")
        pub.publish( "{},{}".format(c_angle,c_speed))
        print "Serial:\t{},\t{}".format(c_angle,c_speed)
        data = ""

    #Read the angle and speed from the neural network using the ros_node_laptop topic
    if "/ros_node_laptop" in rosnode.get_node_names():
      print "Callback:\t{},\t{}".format(angle,speed)
      ser.write("{},{}*".format(angle,speed).encode('utf-8'))
    else:
      print "Laptop node does not exist! Stopping Robot!" 
      ser.write('0,0*'.encode('utf-8'))

    #Write the angle and speed to the Arduino
     
    # ser.flushInput()
    rate.sleep()

  ser.close()

if __name__ == '__main__':
  print "Starting MERL Bot Raspberry Pi Node"
  try:
    piNode()
  except rospy.ROSInterruptException:
    pass
