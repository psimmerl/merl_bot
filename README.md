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

- https://github.com/Slamtec/rplidar_ros
- https://github.com/UbiquityRobotics/raspicam_node


How to run merl_bot ros package
=====================================================================

On the Raspberry Pi from any terminal

```bash
merl_bot_pi
```

On the Laptop running the NN
```bash
merl_bot_NN
```