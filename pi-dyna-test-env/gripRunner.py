# import the necessary packages
print("beginning execution")
import grip
import time
import cv2 as cv
import pyrealsense2 as rs
import numpy as np
import altusi.visualizer as vis
import robot
import ikpy
print("libraries imported")

gp = grip.GripPipeline()
print("grip instantiated")

SEARCH_LR = 0
ALIGN_UD = 1
IK = 2
GRAB = 3
HOME = 4

stage = 0
tracking = 0

my_chain = ikpy.chain.Chain.from_urdf_file("./niryo_one.urdf")

#object_detector = ObjectDetector()

home_pin = 13 #GPIO pin connected to set home switch
delay = 1.2 # seconds
angle = 2 #degrees

xlen = 640
ylen = 480

x_center = xlen / 2
y_center = ylen / 2

x_range_low  = x_center - 20
x_range_high = x_center + 20
y_range_low  = y_center - 20
y_range_high = y_center + 20

# initialize the camera and grab a reference to the raw camera capture
print("loading camera")
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, xlen, ylen, rs.format.z16, 30)
config.enable_stream(rs.stream.color, xlen, ylen, rs.format.bgr8, 30)
pipeline.start(config)
print("camera loaded")

# allow the camera to warmup
time.sleep(0.1)

#instantiate robot
print("instantiating robot")
my_robot = robot.Robot()
my_robot.goReady()
print("robot went home")

#call back function for GPIO interrupt
def home_pressed(channel):
    print("HOME PRESSED")
    my_robot.resetHome()
    

# capture frames from the camera
_start_t = time.time()
start_time = 0
while True:
    _prx_t = time.time() - _start_t
    _start_t = time.time()
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    frm = np.asanyarray(color_frame.get_data())
    _start_t = time.time()
    time.sleep(0.01)
    gp.process(frm)
    bboxes = gp.filter_contours_output
    #scores, bboxes = object_detector.getObjects(frm, def_score=0.4)
    

    
    if len(bboxes) > 0 and (time.time() - start_time) > delay:
        tracking = 1
        target = bboxes[0]
        x1, y1, w, h = target
        
        x2 = x1 + w
        y2 = y1 + h
        
        w = x2 - x1
        h = y2 - y1
        
        xmid = int((x1 + x2) /2)
        ymid = int((y1 + y2) /2)
        
        z = depth_frame.get_distance(xmid, ymid)
        increment = 5 
        
        if stage == SEARCH_LR:
            if (xmid < x_range_low):
                print("move LEFT")
                my_robot.moveLR(increment)

                my_robot.writeJSON()
            elif (xmid > x_range_high):
                print("move RIGHT")
                my_robot.moveLR(-1 * increment)
                my_robot.writeJSON()
            else:
                print("DO NOT MOVE, in the middle X")
                stage = ALIGN_UD
                continue
        if stage == ALIGN_UD:
            if (ymid < y_range_low):
                print("move UP")
                my_robot.moveUD(increment)
                my_robot.writeJSON()
            elif (ymid > y_range_high):
                print("move DOWN")
                my_robot.moveUD(-1 * increment)
                my_robot.writeJSON()
            else:
                print("DO NOT MOVE, in the middle Y")
                stage = IK
                continue
        if stage == IK:
            pose = my_robot.current_pose[:8]
            pose[1] = 0
            pose[4] = 0
            pose[6] = 0
            pose[7] = 0
            current_position_frame = my_chain.forward_kinematics(pose)
            cyl_x = real_frame[:3,3][0]
            cyl_z = real_frame[:3,3][2]

             
            target_vector = [cyl_x + z ,0, cyl_z]
            target_frame = np.eye(4)
            target_frame[:3, 3] = target_vector
            target_angles = my_chain.inverse_kinematics(target_frame)
            target_pose = [my_robot.current_pose[1],target_angles[2],target_angles[3],0,target_angles[5],0,45]
            my_robot.setPose(target_pose)
            time.sleep(4)
            stage = GRAB
            continue
        if stage == GRAB:
            my_robot.moveGrab(-30)
            time.sleep(2)
            stage = HOME
            continue
        if stage == HOME:
            my_robot.goReady()
            time.sleep(4)
            stage = SEARCH_LR
            tracking = 0
            continue
        
        start_time = time.time()
        
    elif (len(bboxes) == 0) and (time.time() - start_time) > delay:
        tracking = 0
        stage = SEARCH_LR
        #go home call
        my_robot.goReady()
        print("go home,cant see anything")
        start_time = time.time()
    
    if len(bboxes):
        frm = vis.plotBBoxes(frm, [(x,y,x+w,y+h) for x,y,w,h in bboxes], len(bboxes) * ['strawberry'], len(bboxes)*[0])
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
