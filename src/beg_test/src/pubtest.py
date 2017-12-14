#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import numpy as np

pub1 = rospy.Publisher('cmd_vel',Twist,queue_size=10)
rospy.init_node('cmdtest',anonymous=True)
rate = rospy.Rate(1)
while not rospy.is_shutdown():


    msg1 = Twist()
    msg1.linear.x = 200
    msg1.linear.y = 0
    msg1.linear.z = 0

    msg1.angular.x = 0
    msg1.angular.y = 0
    msg1.angular.z = 0 #Same as above

    pub1.publish(msg1)
    rate.sleep()




