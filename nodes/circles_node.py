#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv
import rospy
from uav_msgs.msg import RoombaLocation, RoombaList

def findCircles(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 205, 200, cv2.THRESH_TOZERO_INV)
    cimg = cv2.medianBlur(gray,5)
    # Want to change param 2
    #                                                           Canny,    how many circles
    circles = cv2.HoughCircles(cimg,cv.CV_HOUGH_GRADIENT,1,200, param1=60,param2=40, minRadius=10,maxRadius=75)
    # My Pythonic knowledge is stuck: circles is None if there aren't any circles
    # However, a non-empty Numpy array isn't truthy - is there a way to do this without exceptions?
    try:
        return circles[0,:]
    except:
        return np.empty(0)

def circlesMain():
    # 0 for webcam
    cap = cv2.VideoCapture('/home/marcus/Documents/MIT/ExtraCurricular/UAV Team/iarc/iarc/vision/data/PICT0036.AVI')
    # ROS init stuff
    pub = rospy.Publisher('roombas', RoombaList, queue_size = 10)
    rospy.init_node('circlesNode', anonymous=True)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        circles = findCircles(frame)
        # c[0],c[1] is center, c[2] is radius
        message = RoombaList(roombas = [RoombaLocation(x=c[0], y=c[1]) for c in circles], timestamp = rospy.Time.now())
        pub.publish(message)
        r.sleep()

# PyRos stuff
if __name__ == '__main__':
    try:
        circlesMain()
    except rospy.ROSInterruptException: pass
