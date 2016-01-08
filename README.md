# ROS packages
Some public ROS packages for experiments with Baxter

## How to clone and update submodules?

```
git clone --recursive git@github.com:baxter-flowers/ros_packages.git
```

After that command, in each of your submodules you appear as being detached reulting as a non possible pull. Use this commands to change the branch to follow the master one:

```
git submodule foreach git pull origin master

```

To update after a clone:

```
cd ros_packages
git submodule foreach git pull origin master
```
