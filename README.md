# Button box ROS publisher

This is a ROS publisher for an [arduino-based button box](https://github.com/jgrizou/buttonbox).

It has automatic reconnection in case of loss of signal and publishes two ROS topics:
* /button_box/stream: An infinite stream publishing the button states via a standard sensor_msgs/Joy message. The casual implementation for ROS joysticks.
* /button_box/events: A topic publishing only changes, i.e. when buttons are pressed or released, via a custom ButtonEvent message.

# A picture of our lovely button box
![](/misc/our_lovely_button_box.jpg?raw=1)

# Inside...
![](/misc/inside_the_box.jpg?raw=1)
