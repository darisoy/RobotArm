import pyrealsense2 as rs
import numpy as np
from time import sleep

class Cam:

    def __init__(self, width, height):
        self.depth_frame = None
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

    def getFrames(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        self.depth_frame = frames.get_depth_frame()
        return np.asanyarray(color_frame.get_data())

    def getDepth(self, x, y):
        return self.depth_frame(x, y)
