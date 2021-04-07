import time, os, rospy, cv2
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage, LaserScan
from cv_bridge import CvBridge, CvBridgeError
from math import floor
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import pickle
from datetime import datetime
'''ROS node for the laptop'''

TRAINING = True

c_angle, c_speed, img, lscan = 0, 0, None, None

def img_callback(data):
  global img
  br = CvBridge()
  try:
    img = br.compressed_imgmsg_to_cv2(data, "bgr8")
  except CvBridgeError as e:
    print(e)
  cv2.imshow('raspicam', img)
  #cv2.imwrite("raspicam.png",img)
  cv2.waitKey(1)

def car_callback(data):
  global c_angle, c_speed
  try:
    c_angle, c_speed = map(int, data.data.split(','))
  except: #I don't know why this is happening - "c_angle == ''""
    pass
    #print(f"Can't convert to int: {data.data.split(',')}")

def lidar_callback(data):
  global lscan
  lscan = data.ranges

  fig = plt.figure(1)
  ax = plt.subplot(111, projection='polar')
  line = ax.scatter(np.linspace(0, 360, len(lscan)), lscan, s=5, c=[0, 50],
                          cmap=plt.cm.Greys_r, lw=0)
  ax.set_rmax(4000)
  ax.grid(True)

  plt.show()


def laptopNode():
  global c_angle, c_speed, img, lscan
  pub = rospy.Publisher('/NN_angle_speed', String, queue_size=1)
  rospy.init_node('ros_node_laptop')
  img_sub = rospy.Subscriber('/cv_camera/image_raw/compressed', CompressedImage, img_callback, queue_size=1)
  #img_sub = rospy.Subscriber('/raspicam_node/image/CompressedImage', CompressedImage, img_callback)
  car_sub = rospy.Subscriber('/car_angle_speed', String, car_callback)
  lidar_sub = rospy.Subscriber('/rplidarNode/scan', LaserScan, lidar_callback)
  
  rate = rospy.Rate(30) # 30 hz
  angle, speed = 0, 0

  if TRAINING:
    ff = open(f"training_{datetime.now().strftime('%m_%d_%H_%M')}.p",'wb')

  while not rospy.is_shutdown():
    print(f"NN Ang: {angle}\tNN Vel: {speed}\tCar Ang: {c_angle}\tCar Vel: {c_speed}\tAng Err: {c_angle-angle}\tVel Err: {c_speed-speed}")
    
    if not TRAINING:
      angle, speed = (c_angle+10)%180, 10#read_NN(img)
    else:
      #print("Training")
      angle, speed = (c_angle+10)%180, 10#read_NN(img)
      data = {"time" : rospy.get_time(), "c_angle" : c_angle, "c_speed" : c_speed, "lscan" : lscan, "img" : img}
      pickle.dump(data,ff)
      #print(data)
    pub.publish(f"{angle},{speed}")
    rate.sleep()
  
  ff.close()

if __name__ == '__main__':
  print("Starting MERL Bot Laptop Node")
  try:
    laptopNode()
  except rospy.ROSInterruptException:
    pass
