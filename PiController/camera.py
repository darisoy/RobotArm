import pyrealsense2 as rs
import numpy as np
from time import sleep
import cv2 as cv
import altusi.visualizer as vis
import strawberryDetector

class Cam:

    def __init__(self, width, height):
        self.depth_frame = None
        self.frames = None
        self.detectedObjects = None
        self.gp = strawberryDetector.DetectStrawberries()
        
        print("loading camera")
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, 30)
        self.pipeline.start(config)
        sleep(0.1)
        print("camera loaded")

    def stopCamera(self):
        self.pipeline.stop()

    def getFrame(self):
        self.frames = self.pipeline.wait_for_frames()
        color_frame = self.frames.get_color_frame()
        self.depth_frame = self.frames.get_depth_frame()
        self.frame = np.asanyarray(color_frame.get_data())
    
    def detectStrawberriesOnFrame(self):
        self.gp.process(self.frame)
        self.detectedObjects = self.gp.filter_contours_output
        return self.detectedObjects

    def getDepth(self, x, y):
        return self.depth_frame.get_distance(x, y)
    
    def displayImage(self):
        self.__drawBoxes()
        cv.imshow("Frame", self.frame)
        cv.imwrite("../Frontend/frame.jpg", self.frame)
        key = cv.waitKey(1)
        return key
    
    def __drawBoxes(self):
        if len(self.detectedObjects):
            self.frame = vis.plotBBoxes(self.frame, [(x, y, x + w, y + h) for x, y, w, h in self.detectedObjects], len(self.detectedObjects) * ['strawberry'], len(self.detectedObjects) * [0])
        self.frame = vis.plotInfo(self.frame, 'Flint View')
        self.frame = cv.cvtColor(np.asarray(self.frame), cv.COLOR_BGR2RGB)
