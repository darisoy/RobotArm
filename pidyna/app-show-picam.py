# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv

import numpy as np

import altusi.config as cfg
import altusi.visualizer as vis
from altusi import imgproc, helper
from altusi.logger import Logger

from altusi.objectdetector import ObjectDetector

 # initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
object_detector = ObjectDetector()

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    frm = frame.array

    frm = imgproc.resizeByHeight(frm, 720)


    _start_t = time.time()
    scores, bboxes = object_detector.getObjects(frm, def_score=0.1)
    _prx_t = time.time() - _start_t

    print("scores: ", scores)
    print("bboxes: ", bboxes)

    if len(bboxes):
        frm = vis.plotBBoxes(frm, bboxes, len(bboxes) * ['person'], scores)
    frm = vis.plotInfo(frm, 'Raspberry Pi - FPS: {:.3f}'.format(1/_prx_t))
    frm = cv.cvtColor(np.asarray(frm), cv.COLOR_BGR2RGB)

    # show the frame
    cv.imshow("Frame", frm)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    key = cv.waitKey(1)
    if key in [27, ord('q')]:
        break
