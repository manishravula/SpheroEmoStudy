#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import ColorRGBA, Float32, Bool
import numpy as np


pub1 = rospy.Publisher('cmd_vel',Twist,queue_size=10)

pub_setAngularVelocity = rospy.Publisher('set_heading',Float32,queue_size=10)
rospy.init_node('cmdtest',anonymous=True)
global_rate = 100.0
rate = rospy.Rate(global_rate)
flag = False
iter = 0

dir = 1
while not rospy.is_shutdown():

    osc_freq = 1
    osc_amp = 100


    msg1 = Twist()
    # if flag:
    #     msg1.linear.x = 10
    #     flag = False
    # else:
    #     msg1.linear.x = -10
    #     flag = True

    if iter%20==0:
        dir *= -1

    msg1.linear.x = osc_amp*np.sin(iter*osc_freq*np.pi*2/global_rate)
    msg1.linear.y = osc_amp*np.cos(iter*osc_freq*np.pi*2/global_rate)

    iter+=1
    msg1.linear.z = 0

    msg1.angular.z = 0
    msg1.angular.y = 0
    msg1.angular.x = 0 #Same as above

    msg2 = Float32()


    pub1.publish(msg1)
    # pub_setAngularVelocity.publish(100)
    rate.sleep()

