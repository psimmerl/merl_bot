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

#from keras.models import load_model
# from neural_net.pure_pursuit import PIDController, PurePursuitPlusPID, PurePursuit
#from neural_net.pure_pursuit import PurePursuitPlusPID
#from neural_net.helper_functions import *
# model_file = "pilotnet_model.h5"
# model = load_model(model_file)

'''ROS node for the laptop'''

TRAINING = True
# fname = datetime.now().strftime('%m_%d_%H_%M_%S')

c_angle, c_speed, img, lscan = 0, 0, None, None
x, y, slam_rot = 0, 0, 0

def img_callback(data):
  global img
  br = CvBridge()
  try:
    img = br.compressed_imgmsg_to_cv2(data, "bgr8")#cv2.rotate(br.compressed_imgmsg_to_cv2(data, "bgr8"), cv2.ROTATE_180)
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

def slam_callback(data):
  global x, y, slam_rot
  x = data.pose.position.x
  y = data.pose.position.y
  slam_rot = data.pose.orientation.z
  

def lidar_callback(data):
  global lscan
  lscan = data.ranges

def laptopNode():
  global c_angle, c_speed, img, lscan, x, y, slam_rot
  # controller = PurePursuit() #PurePursuitPlusPID()

  rospy.init_node('ros_node_laptop')
  pub = rospy.Publisher('/NN_angle_speed', String, queue_size=1)
  img_sub = rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, img_callback)
  car_sub = rospy.Subscriber('/car_angle_speed', String, car_callback)
  lidar_sub = rospy.Subscriber('/rplidarNode/scan', LaserScan, lidar_callback)
  slam_sub = rospy.Subscriber('/slam_out_pose', PoseStamped, slam_callback)
  
  rate = rospy.Rate(60) # 30 hz
  if TRAINING:
    xbox = Xbox360Controller()
    # ff = open(f"train/training_{fname}.p",'wb')

  while not rospy.is_shutdown():
    if not TRAINING:
      # get into correct shape for network
      img = img.reshape(1,200,400,3).reshape(1,1,200,400,3) 
      prediction = model.predict(img)[0]
      # construct line from predicted points, each being one meter apart
      trajectory_prediction = np.array([[float(i),prediction[i]] for i in range(len(prediction))]) 
      speed, angle = controller.get_control(trajectory_prediction, speed, desired_speed = 25, dt=1./FPS)
    else:
      angle = xbox.axis_l.x if abs(xbox.axis_l.x) > 0.15 else 0
      speed = ( xbox.trigger_r.value-xbox.trigger_l.value ) / 4 if abs(xbox.trigger_r.value-xbox.trigger_l.value) > 0.075 else 0
      
      # if img is not None:
      #   pngname = datetime.now().strftime('%m_%d_%H_%M_%S.%f%')[:-3]
      #   data = {"time" : rospy.get_time(), "c_angle" : c_angle, "c_speed" : c_speed, \
      #           "slam_x" : x, "slam_y": y, "slam_rot" : slam_rot, \
      #           "lscan" : lscan, "img" : f"raspicam_{pngname}.png"}
      #   cv2.imwrite(f"train/raspicam_{pngname}.png",img)
      #   pickle.dump(String(data),ff)

    pub.publish(f"{angle},{speed}")
    print(f"Ang: {round(angle,2)}\tVel: {round(speed,2)}\tC_Ang: {round(c_angle,2)}\tC_Vel: {round(c_speed,2)}\tC_x: {round(x,2)}\tC_y: {round(y,2)}\tC_z: {round(slam_rot,2)}")
    #Ang Err: {round(c_angle-angle,2)}\tVel Err: {round(c_speed-speed,2)}")
    rate.sleep()
  if TRAINING:
    xbox.close()
    # ff.close()
  
if __name__ == '__main__':
  print("Starting MERL Bot Laptop Node")
  try:
    laptopNode()
  except rospy.ROSInterruptException:
    pass
