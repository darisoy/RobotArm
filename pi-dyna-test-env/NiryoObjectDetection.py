# import the necessary packages
import RPi.GPIO as GPIO
import time
import cv2 as cv
import pyrealsense2 as rs
import numpy as np
import altusi.config as cfg
import altusi.visualizer as vis
from altusi import imgproc, helper
from altusi.logger import Logger
from altusi.objectdetector import ObjectDetector
import robot

GPIO.setmode(GPIO.BCM)

object_detector = ObjectDetector()

home_pin = 13 #GPIO pin connected to set home switch
delay = 1.2 # seconds
angle = 8 #degrees

xlen = 640
ylen = 480

x_center = xlen / 2
y_center = ylen / 2

x_range_low  = x_center - 20
x_range_high = x_center + 20
y_range_low  = y_center - 20
y_range_high = y_center + 20

# initialize the camera and grab a reference to the raw camera capture
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, xlen, ylen, rs.format.z16, 30)
config.enable_stream(rs.stream.color, xlen, ylen, rs.format.bgr8, 30)
pipeline.start(config)

# allow the camera to warmup
time.sleep(0.1)

#instantiate robot
my_robot = robot.Robot()
my_robot.goReady()
#time.sleep(3)

#call back function for GPIO interrupt
def home_pressed(channel):
    print("HOME PRESSED")
    my_robot.resetHome()
    #insert comms sequence here
    
#initialize GPIO interrupt for home button
GPIO.setup(home_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(home_pin, GPIO.RISING, callback=home_pressed, bouncetime=300)  


    
#print("waiting to set home position")
#GPIO.wait_for_edge(home_pin, GPIO.RISING)
#print("home successfully initiated")

# capture frames from the camera
start_time = 0
while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    frm = np.asanyarray(color_frame.get_data())

    _start_t = time.time()
    scores, bboxes = object_detector.getObjects(frm, def_score=0.4)
    _prx_t = time.time() - _start_t

    print("scores: ", scores)
    print("bboxes: ", bboxes)

    if len(bboxes) > 0 and (time.time() - start_time) > delay:
        target = bboxes[0]
        x1, y1, x2, y2 = target
        
        w = x2 - x1
        h = y2 - y1
        
        xmid = int((x1 + x2) /2)
        ymid = int((y1 + y2) /2)
        
        z = depth_frame.get_distance(xmid, ymid)
        z_horizontal = depth_frame.get_distance(0, ymid)
        z_vertical = depth_frame.get_distance(xmid, 0)
        increment = int(z * angle)
        #x_angle = int(np.degrees(np.arccos([z_horizontal / z])[0]))
        #y_angle = int(np.degrees(np.arccos([z_vertical / z])[0]))
        
        #print("x_angle: ", x_angle)
        #print("y_angle: ", y_angle)
        
        if (xmid < x_range_low):
            print("move LEFT")
            my_robot.moveLR(increment)
        elif (xmid > x_range_high):
            print("move RIGHT")
            my_robot.moveLR(-1 * increment)
        else:
            print("DO NOT MOVE, in the middle X")
        
        if (ymid < y_range_low):
            print("move UP")
            my_robot.moveUD(increment)
        elif (ymid > y_range_high):
            print("move DOWN")
            my_robot.moveUD(-1 * increment)
        else:
            print("DO NOT MOVE, in the middle Y")
         
        print(z)
        
        if (z > 0.2):
            my_robot.moveFB(increment)
            print("move FORWARD")
        elif (z == 0.0):
            my_robot.moveFB(-1 * increment)
            print("go home,cant see anything")
        else:
            print("DO NOT MOVE, in the middle Z")
            
        start_time = time.time()
        
    elif (len(bboxes) == 0) and (time.time() - start_time) > delay:
        #go home call
        my_robot.goReady()
        print("go home,cant see anything")
        start_time = time.time()
    
    if len(bboxes):
        frm = vis.plotBBoxes(frm, bboxes, len(bboxes) * ['person'], scores)
    frm = vis.plotInfo(frm, 'Raspberry Pi - FPS: {:.3f}'.format(1/_prx_t))
    frm = cv.cvtColor(np.asarray(frm), cv.COLOR_BGR2RGB)

    # show the frame
    cv.imshow("Frame", frm)
    cv.imwrite("../Frontend/frame.jpg", frm)
    
    key = cv.waitKey(1)
    if key in [27, ord('q')]:
        break
    #time.sleep(2)
    
pipeline.stop()
