# ROS packages
Some public ROS packages for experiments with Baxter

## How to clone and update submodules?
```
git clone --recursive git@github.com:baxter-flowers/ros_packages.git
```
To update after a clone:
```
cd ros_packages
git submodule foreach git pull origin master
```
