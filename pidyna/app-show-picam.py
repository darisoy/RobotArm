# import the necessary packages
import time
import cv2 as cv

import pyrealsense2 as rs

import numpy as np

import altusi.config as cfg
import altusi.visualizer as vis
from altusi import imgproc, helper
from altusi.logger import Logger
from altusi.objectdetector import ObjectDetector


object_detector = ObjectDetector()

delay = 3 # seconds
xlen = 640
ylen = 480
x_range_low = (xlen / 2) - 20
x_range_high = x_range_low + 40
y_range_low = (ylen / 2) - 20
y_range_high = y_range_low + 40

# initialize the camera and grab a reference to the raw camera capture
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, xlen, ylen, rs.format.z16, 30)
config.enable_stream(rs.stream.color, xlen, ylen, rs.format.bgr8, 30)
pipeline.start(config)
start_time = 0

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    frm = np.asanyarray(color_frame.get_data())

    _start_t = time.time()
    scores, bboxes = object_detector.getObjects(frm, def_score=0.1)
    _prx_t = time.time() - _start_t

    #print("scores: ", scores)
    #print("bboxes: ", bboxes)

    if len(bboxes) > 0 and (time.time() - start_time) > delay:
        target = bboxes[0]
        x1, y1, x2, y2 = target
        
        w = x2 - x1
        h = y2 - y1
        
        xmid = int((x1 + x2) /2)
        ymid = int((y1 + y2) /2)
        
        z = depth_frame.get_distance(xmid, ymid)
        
        if (xmid < x_range_low):
            #add move command
            print("move LEFT 5 Degrees")
        elif (xmid > x_range_high):
            #add move command
            print("move RIGHT 5 Degrees")
        else:
            #add move command
            print("DO NOT MOVE, in the middle X")
        
        if (ymid < y_range_low):
            #add move command
            print("move UP 5 Degrees")
        elif (ymid > y_range_high):
            #add move command
            print("move DOWN 5 Degrees")
        else:
            #add move command
            print("DO NOT MOVE, in the middle Y")
            
        if (z > 0.15):
            #add move command
            print("move FORWARD 5 Degrees")
        else:
            #add move command
            print("go home,cant see anything")
            
        start_time = time.time()
    elif (len(bboxes) > 0):
        #go home call
        print("go home,cant see anything")
    
    if len(bboxes):
        frm = vis.plotBBoxes(frm, bboxes, len(bboxes) * ['person'], scores)
    frm = vis.plotInfo(frm, 'Raspberry Pi - FPS: {:.3f}'.format(1/_prx_t))
    frm = cv.cvtColor(np.asarray(frm), cv.COLOR_BGR2RGB)

    # show the frame
    cv.imshow("Frame", frm)

    key = cv.waitKey(1)
    if key in [27, ord('q')]:
        break
    
    
pipeline.stop()
