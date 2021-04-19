#!/usr/bin/env python3
import time, os, rospy, rosnode, cv2
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage, LaserScan
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import pickle
from datetime import datetime
from xbox360controller import Xbox360Controller

'''ROS node for the recorder'''

TRAINING = True
fname = datetime.now().strftime('%m_%d_%H_%M_%S')

c_angle, c_speed, img, lscan = 0, 0, None, None
x, y, slam_rot = 0, 0, 0
angle, speed = 0, 0

def img_callback(data):
  global img, c_angle, c_speed, lscan, angle, speed, x, y, slam_rot, ff
  br = CvBridge()
  try:
    img = br.compressed_imgmsg_to_cv2(data, "bgr8")#cv2.rotate(br.compressed_imgmsg_to_cv2(data, "bgr8"), cv2.ROTATE_180)
  except CvBridgeError as e:
    print(e)

  pngname = datetime.now().strftime('%m_%d_%H_%M_%S.%f%')[:-3]
  data = {"time" : rospy.get_time(), "c_angle" : c_angle, "c_speed" : c_speed, \
          "slam_x" : x, "slam_y": y, "slam_rot" : slam_rot, \
          "lscan" : lscan, "img" : f"raspicam_{pngname}.png"}
  cv2.imwrite(f"train/raspicam_{pngname}.png",img)
  pickle.dump(String(data),ff)


def car_callback(data):
  global c_angle, c_speed
  try:
    c_angle, c_speed = map(float, data.data.split(','))
  except: #I don't know why this is happening - "c_angle == ''""
    #pass
    print(f"Can't convert to int: {data.data.split(',')}")

def slam_callback(data):
  global x, y, slam_rot
  x = data.pose.position.x
  y = data.pose.position.y
  slam_rot = data.pose.orientation.z
  

def lidar_callback(data):
  global lscan
  lscan = data.ranges

def NN_callback(data):
  global angle, speed
  angle, speed = tuple(map(float, data.data.split(',')))


def recordNode():
  global c_angle, c_speed, img, lscan, x, y, slam_rot, ff

  rospy.init_node('ros_node_recorder')
  ff = open(f"train/training_{fname}.p",'wb')

  NN_sub = rospy.Subscriber('/NN_angle_speed', String, NN_callback)
  img_sub = rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, img_callback)
  car_sub = rospy.Subscriber('/car_angle_speed', String, car_callback)
  lidar_sub = rospy.Subscriber('/rplidarNode/scan', LaserScan, lidar_callback)
  slam_sub = rospy.Subscriber('/slam_out_pose', PoseStamped, slam_callback)
  
  rate = rospy.Rate(60)

  while not rospy.is_shutdown():
    rate.sleep()
    
  ff.close()
  
if __name__ == '__main__':
  print("Starting Recording Laptop Node")
  try:
    recordNode()
  except rospy.ROSInterruptException:
    pass
