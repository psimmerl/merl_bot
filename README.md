# 
UConn EE Senior Design Team 2107 ROS
=====================================================================

ROS Nodes for the UCOnn Senior Design Path Planning with Deep Neural Networks project, sponsored by Mitsubishi Electric Research Laboratories (MERL)


How to build merl_bot ros package
=====================================================================

On the Raspberry Pu use the Ubiquity Robotics ROS Distro *2020-11-07-ubiquity-xenial-lxde*
https://downloads.ubiquityrobotics.com/pi.html

Use the same code for the laptop and the Pi

```bash
sudo systemctl disable magni-base
cd ~/catkin_make/src
git clone https://github.com/psimmerl/merl_bot.git
chmod +x merl_bot_*
cp merl_bot_pi /bin/.
cp merl_bot_NN /bin/.
cd ..
catkin_make
```

On the Pi also run
```bash
sudo systemctl disable magni-base
```

Packages that may also need to be installed
====
- https://github.com/Slamtec/rplidar_ros
- Hector SLAM and make modifacations to the files
- https://github.com/UbiquityRobotics/raspicam_node
- https://pypi.org/project/pyserial/
- https://pypi.org/project/opencv-python/

---
How to run merl_bot ros package
=====================================================================

To run:


Laptop -> Terminal 1
```bash
roscore
```

Laptop -> Terminal 2
```bash
cd ~/catkin_ws/src/merl_bot
./merl_bot_laptop
```

Pi -> Terminal 1 (replace .... with current date/time)
```bash
sudo date --set="...."
roslaunch rplidar_ros rplidar.launch
```

Pi -> Terminal 2
```bash
roslaunch raspicam_node camerav2_410x308_15fps.launch
```

Pi -> Terminal 3
```bash
rosrun merl_bot pi.py
```

Laptop -> Terminal 3
```bash
roslaunch hector_slam_mapping tutorial.launch
```
In rviz add a camera image topic to view the camera output



If you are recording training data, change the **`TRAINING`** variable in *ros_node_laptop.py* to be `True`. This will record the car's current angle, speed, LIDAR scan, and camera image into a pickle (**training_*MONTH*_*DAY* _*HOUR* _*MINUTE*.p**). 