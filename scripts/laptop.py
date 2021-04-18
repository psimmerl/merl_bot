#!/usr/bin/env python3
import time, os, rospy, rosnode, cv2
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage, LaserScan
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
fname = datetime.now().strftime('%m_%d_%H_%M')

c_angle, c_speed, img, lscan = 0, 0, None, None

def img_callback(data):
  global img
  br = CvBridge()
  try:
    img = cv2.rotate(br.compressed_imgmsg_to_cv2(data, "bgr8"), cv2.ROTATE_180)
  except CvBridgeError as e:
    print(e)
  # cv2.imshow('raspicam', img)
  # cv2.waitKey(1)

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
  # controller = PurePursuit() #PurePursuitPlusPID()
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
  rate = rospy.Rate(45) # 30 hz
  if TRAINING:
    xbox = Xbox360Controller()
  print("h4")
  while not rospy.is_shutdown():
    if not TRAINING:
      # img = process_img(img)
      # # get into correct shape for network
      # img = img.reshape(1,200,400,3).reshape(1,1,200,400,3) 
      # prediction = model.predict(img)[0]
      # # construct line from predicted points, each being one meter apart
      # trajectory_prediction = np.array([[float(x),prediction[x]] for x in range(len(prediction))]) 
      # speed, angle = controller.get_control(trajectory_prediction, speed, desired_speed = 25, dt=1./FPS)
      speed, angle = 0, 0
    else:
      angle = xbox.axis_l.x if abs(xbox.axis_l.x) > 0.15 else 0
      speed = xbox.trigger_r.value-xbox.trigger_l.value if abs(xbox.trigger_r.value-xbox.trigger_l.value) > 0.075 else 0
      
      speed = -1* speed / 4
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
    xbox.close()
  
if __name__ == '__main__':
  print("Starting MERL Bot Laptop Node")
  try:
    laptopNode()
  except rospy.ROSInterruptException:
    pass
