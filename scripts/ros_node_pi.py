import time, serial, os, rospy, rosnode
from std_msgs.msg import String
'''ROS node for the Raspberry Pi'''

ARDUINO_PORT = '/dev/ttyUSB0'
ARDUINO_BAUD_RATE = 9600
SERIAL_TIMEOUT = 0.01

angle, speed = 0, 0

def tv_callback(data):
  global angle, speed
  angle, speed = tuple(map(float, data.data.split(',')))


def piNode():
  global angle, speed
  #Open Arduino
  ser = serial.Serial(ARDUINO_PORT, ARDUINO_BAUD_RATE, timeout=SERIAL_TIMEOUT)

  rospy.init_node('ros_node_pi') 
  pub = rospy.Publisher('/car_angle_speed', String, queue_size=1)
  sub = rospy.Subscriber("/NN_angle_speed", String, tv_callback)
  
  rate = rospy.Rate(30) # 10hz

  while not rospy.is_shutdown(): 
    ser.flushOutput()
    #Read data from the Arduino
    data = tuple(ser.readline()[:-2].decode('utf-8').split(','))
    if len(data) > 1 :

      (c_angle, c_speed) = data
      #if c_angle == '':
      #  print("************************ERROR************************")
      pub.publish(f"{c_angle},{c_speed}")
      print(f"{c_angle},{c_speed}")

    #Read the angle and speed from the neural network using the ros_node_laptop topic
    if "/ros_node_laptop" in rosnode.get_node_names():
      #print(f"Callback: {angle},\t{speed}")
      ser.write(bytes(f'{angle},{speed}*', 'utf-8'))
    else:
      print("Laptop node does not exist! Stopping Robot!")
      ser.write(bytes('0,0*', 'utf-8'))

    #Write the angle and speed to the Arduino
     
    ser.flushInput()
    rate.sleep()

  ser.close()

if __name__ == '__main__':
  print("Starting MERL Bot Raspberry Pi Node")
  try:
    piNode()
  except rospy.ROSInterruptException:
    pass
