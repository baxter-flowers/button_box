#!/usr/bin/env python
from serial import Serial
from time import sleep, time
from sensor_msgs.msg import Joy
from button_box_ros.msg import ButtonEvent
import rospy

"""
This is a ROS button box publisher.
It publishes both events and a continuous stream on separated topics.
"""

class BBoxPublisher():
    def __init__(self, num_buttons, devices, speed_bps, timeout, topic_continuous_publisher, topic_event_publisher):
        self.devices = devices
        self.num_buttons = num_buttons
        self.current_device = 0
        self.serial = None
        self.timeout = timeout
        self.speed = speed_bps
        self.continuous_publisher = rospy.Publisher(topic_continuous_publisher, Joy, queue_size=100)
        self.event_publisher = rospy.Publisher(topic_event_publisher, ButtonEvent, queue_size=100)
        self.last_button_state = [False]*self.num_buttons

    def connect(self):
        success = False
        device = self.devices[self.current_device]
        try:
            self.serial = Serial(device, self.speed)
        except Exception, e:
            rospy.logwarn("[Button box publisher] Connection to {} at speed {} failed: {}".format(device, self.speed, e.message))
            self.serial = None
            self.current_device = (self.current_device+1) % len(self.devices)
        else:
            success = True
            rospy.loginfo("[Button box publisher] Connected to {} at speed {}!".format(device, self.speed))

        return success

    def connect_until(self, timeout):
        success = False
        while not rospy.is_shutdown():
            success = self.connect()
            if success: break
            sleep(0.05)
        return success

    def close(self):
        if self.serial:
            self.serial.close()
            self.serial = None

    def process_msg(self, message):
        message = message.strip()
        stamp = rospy.Time.now()
        if len(message)==self.num_buttons:

            # Continuous stream publishing
            joy = Joy(buttons=[int(message[button]) for button in range(len(message))])
            joy.header.stamp = stamp
            self.continuous_publisher.publish(joy)

            for button in range(len(message)):
                is_pressed = message[button]=='1'

                # Event publishing
                if self.last_button_state[button]!=is_pressed:
                    event = ButtonEvent(action= ButtonEvent.PRESSED if is_pressed else ButtonEvent.RELEASED, button_id=button)
                    event.header.stamp = stamp
                    self.event_publisher.publish(event)
                self.last_button_state[button] = is_pressed

    def run(self):
        while not rospy.is_shutdown():
            reconnect = True
            if self.serial and self.serial.isOpen():
                try:
                    msg = self.serial.readline()
                except:
                    pass
                else:
                    reconnect = False
                    self.process_msg(msg)
            if reconnect:
                self.connect_until(self.timeout)
        self.close()

if __name__=='__main__':
    rospy.init_node('button_box_ros')
    BBoxPublisher(10, ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3'], 115200, 120, # 10 buttons, 115200 bauds, 120 seconds of retries before failure
                  '/button_box/stream', '/button_box/events').run()