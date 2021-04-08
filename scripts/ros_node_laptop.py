#!/usr/bin/env python
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

TRAINING = False

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
    c_angle, c_speed = map(float, data.data.split(','))
  except: #I don't know why this is happening - "c_angle == ''""
    #pass
    print(f"Can't convert to int: {data.data.split(',')}")

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

angle, speed = 0, 0
def tv_callback(data):
  global angle, speed
  angle, speed = tuple(map(float, data.data.split(',')))

# import signal
# from xbox360controller import Xbox360Controller
# def on_axis_moved(axis):
#     global angle, speed
#     angle, speed = (axis.x+1)*90, axis.y
#     # print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))


def laptopNode():
  global angle, speed
  global c_angle, c_speed, img, lscan
  pub = rospy.Publisher('/NN_angle_speed', String, queue_size=1)
  rospy.init_node('ros_node_laptop')
  # img_sub = rospy.Subscriber('/cv_camera/image_raw/compressed', CompressedImage, img_callback, queue_size=1)
  # img_sub = rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, img_callback)
  car_sub = rospy.Subscriber('/car_angle_speed', String, car_callback)
  #lidar_sub = rospy.Subscriber('/rplidarNode/scan', LaserScan, lidar_callback)
  
  
  dumb_sub = rospy.Subscriber('/NN_angle_speed', String, tv_callback)
  
  rate = rospy.Rate(15) # 60 hz

  # if TRAINING:
  #   ff = open(f"training_{datetime.now().strftime('%m_%d_%H_%M')}.p",'wb')
    
  while not rospy.is_shutdown():
    print(f"NN Ang: {round(angle,2)}\tNN Vel: {round(speed,2)}\tCar Ang: {round(c_angle,2)}\tCar Vel: {round(c_speed,2)}\tAng Err: {round(c_angle-angle,2)}\tVel Err: {round(c_speed-speed,2)}")

    
    if not TRAINING:
      angle, speed = c_angle%180, (c_speed)%180#read_NN(img)
    else:
      print("Training")
      # with Xbox360Controller(0, axis_threshold=0.2) as controller:
      #   controller.axis_r.when_moved = on_axis_moved
    #   data = {"time" : rospy.get_time(), "c_angle" : c_angle, "c_speed" : c_speed, "lscan" : lscan, "img" : img}
    #   pickle.dump(data,ff)

    pub.publish(f"{angle},{speed}")
    rate.sleep()
  
  # ff.close()

if __name__ == '__main__':
  print("Starting MERL Bot Laptop Node")
  try:
    laptopNode()
  except rospy.ROSInterruptException:
    pass
