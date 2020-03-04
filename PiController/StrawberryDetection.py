# import the necessary packages
import grip
import time
import cv2 as cv
import numpy as np
import ikpy
import robot
import camera
import altusi.visualizer as vis

SEARCH_LR = 0
ALIGN_UD = 1
IK = 2
GRAB = 3
HOME = 4

stage = 0
tracking = 0

delay = 1.2 #seconds
angle = 2 #degrees
xlen = 640
ylen = 480
x_center = xlen / 2
y_center = ylen / 2
x_range_low  = x_center - 20
x_range_high = x_center + 20
y_range_low  = y_center - 20
y_range_high = y_center + 20

gp = grip.GripPipeline()
my_chain = ikpy.chain.Chain.from_urdf_file("./ik/niryo_one.urdf")
cam = camera.Cam(xlen, ylen)
my_robot = robot.Robot()
my_robot.goReady()
print("robot initialized")

start_time = 0
while True:
    frm = cam.getFrames()
    time.sleep(0.01)
    gp.process(frm)
    detectedObjects = gp.filter_contours_output

    if len(detectedObjects) > 0 and (time.time() - start_time) > delay:
        tracking = 1
        x1, y1, w, h = detectedObjects[0]
        x2 = x1 + w
        y2 = y1 + h
        xmid = int((x1 + x2) /2)
        ymid = int((y1 + y2) /2)

        z = cam.getDepth(xmid, ymid)
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
            cyl_x = current_position_frame[:3,3][0]
            cyl_z = current_position_frame[:3,3][2]
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

    elif (len(detectedObjects) == 0) and (time.time() - start_time) > delay:
        tracking = 0
        stage = SEARCH_LR
        my_robot.goReady()
        print("go home, can't see anything")
        start_time = time.time()

    if len(detectedObjects):
        frm = vis.plotBBoxes(frm, [(x, y, x + w, y + h) for x, y, w, h in detectedObjects], len(detectedObjects) * ['strawberry'], len(detectedObjects) * [0])
    frm = vis.plotInfo(frm, 'Flint View')
    frm = cv.cvtColor(np.asarray(frm), cv.COLOR_BGR2RGB)

    displayImage(frm)

cam.stopCamera()

def displayImage(frame):
    cv.imshow("Frame", frame)
    cv.imwrite("../Frontend/frame.jpg", frame)
