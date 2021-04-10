#!/usr/bin/env python
import time, os, rospy, rosnode, cv2
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage, LaserScan
from cv_bridge import CvBridge, CvBridgeError
# from math import floor
# import numpy as np
# import matplotlib.pyplot as plt
import pickle
from datetime import datetime
from xbox360controller import Xbox360Controller
'''ROS node for the laptop'''

TRAINING = True
fname = datetime.now().strftime('%m_%d_%H_%M')

c_angle, c_speed, img, lscan = 0, 0, None, None

def img_callback(data):
  global img
  br = CvBridge()
  try:
    img = br.compressed_imgmsg_to_cv2(data, "bgr8")
  except CvBridgeError as e:
    print(e)
  cv2.imshow('raspicam', img)
  cv2.waitKey(1)

def car_callback(data):
  global c_angle, c_speed
  try:
    c_angle, c_speed = map(float, data.data.split(','))
  except: #I don't know why this is happening - "c_angle == ''""
    #pass
    print(f"Can't convert to int: {data.data.split(',')}")

# def lidar_callback(data):
#   global lscan
#   lscan = data.ranges

#   fig = plt.figure(1)
#   ax = plt.subplot(111, projection='polar')
#   line = ax.scatter(np.linspace(0, 360, len(lscan)), lscan, s=5, c=[0, 50],
#                           cmap=plt.cm.Greys_r, lw=0)
#   ax.set_rmax(4000)
#   ax.grid(True)

#   plt.show()

def laptopNode():
  global c_angle, c_speed, img, lscan
  print("h1")
  rospy.init_node('ros_node_laptop')
  print("h2")
  pub = rospy.Publisher('/NN_angle_speed', String, queue_size=1)
  print("h2.1")
  img_sub = rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, img_callback)
  print("h2.2")
  car_sub = rospy.Subscriber('/car_angle_speed', String, car_callback)
  # lidar_sub = rospy.Subscriber('/rplidarNode/scan', LaserScan, lidar_callback)
  print("h3")
  rate = rospy.Rate(30) # 30 hz
  if TRAINING:
    controller = Xbox360Controller()
  print("h4")
  while not rospy.is_shutdown():
    if not TRAINING:
      angle, speed = 0, 0#read_NN(img)

    else:
      angle = controller.axis_l.x if abs(controller.axis_l.x) > 0.15 else 0
      speed = controller.trigger_r.value-controller.trigger_l.value if abs(controller.trigger_r.value-controller.trigger_l.value) > 0.075 else 0

      # with open(f"training_{fname}.p",'a') as ff:
      #   pngname = {datetime.now().strftime('%m_%d_%H_%M_%S')}
      #   data = {"time" : rospy.get_time(), "c_angle" : c_angle, "c_speed" : c_speed, \
      #           "lscan" : lscan, "img" : f"raspicam_{pngname}.png"}
      #   cv2.imwrite(f"raspicam_{pngname}.png",img)
      #   pickle.dump(data,ff)

    pub.publish(f"{angle},{speed}")
    print(f"NN Ang: {round(angle,2)}\tNN Vel: {round(speed,2)}\tCar Ang: {round(c_angle,2)}\tCar Vel: {round(c_speed,2)}\tAng Err: {round(c_angle-angle,2)}\tVel Err: {round(c_speed-speed,2)}")
    rate.sleep()
  if TRAINING:
    controller.close()
  
if __name__ == '__main__':
  print("Starting MERL Bot Laptop Node")
  try:
    laptopNode()
  except rospy.ROSInterruptException:
    pass
