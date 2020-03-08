## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

from ctypes import *
import pyrealsense2 as rs
import numpy as np
import cv2
import imageio
from subprocess import Popen, PIPE
import os, fcntl
import select
import time

#import darknet
#from darknetpy.detector import Dectector

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
#config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

#darknet_image = darknet.make_image(darknet.network_width(netMain), darknet.network_height(netMain),3)
yolo_proc = Popen(["/home/dev/darknet-nnpack/darknet",
    "detect",
    "./cfg/yolov3-tiny.cfg",
    "./yolov3-tiny.weights",
    "-thresh", "0.1"],stdin = PIPE, stdout=PIPE
    )
fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)


# Start streaming
pipeline.start(config)

while True:
    stdout = yolo_proc.stdout.read()
    if stdout is not None:
        print("-------------prints DOWN-----------:")
        print(bytes(stdout))
        if (b'%\napple' in stdout):
            print("APPLE FOUND")
            index1 = stdout.index(b'%\napple') - 2
            #wrong index2
            index2 = stdout[index1:index1+2]
            search = b'Box ' + index2 + b' at (x,y)='
            print(search)
            if (search in stdout):
                index3 = stdout.index(search) + len(search)
                location = stdout[index3:index3+19]
                print(location)
        stdout = None
        print("-------------prints UP-----------:")
        pipeline.stop()
        time.sleep(4)
        pipeline.start(config)

    

    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    color_image_write = cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB)
    imageio.imwrite("/dev/shm/frame.jpg", color_image_write)
    
    yolo_proc.stdin.write(b'/dev/shm/frame.jpg\n')
    

import sys
sys.exit(0)





pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

yolo_proc = Popen(["/home/dev/darknet-nnpack/darknet",
    "detect",
    "./cfg/yolov3-tiny.cfg",
    "./yolov3-tiny.weights",
    "-thresh", "0.2"],stdin = PIPE, stdout=PIPE
    )
fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

def capture():         
    pipeline.start(config)
    
    frames = pipeline.wait_for_frames()
    time.sleep(1)
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    color_image_write = cv2.cvtColor(color_image,cv2.COLOR_BGR2RGB)
    imageio.imwrite("/dev/shm/frame.jpg", color_image_write)
    pipeline.stop()
    time.sleep(1)
    yolo_proc.stdin.write(b'/dev/shm/frame.jpg\n')
    
    while True:
        stdout = yolo_proc.stdout.read()
        if len(stdout.strip())>0:
                print('get %s' % stdout)

    
capture()
print("Doneeee")


