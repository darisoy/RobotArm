#import os
#os.chdir("/home/dev/475wi20/PiController")

import time
import numpy as np
import ikpy
import motionControl
import camera
import json

SEARCH_LR = 0
ALIGN_UD = 1
IK = 2
GRAB = 3
HOME = 4

DELAY = 1.2 #seconds
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_X_CENTER = int(FRAME_WIDTH / 2)
FRAME_Y_CENTER = int(FRAME_HEIGHT / 2)
TARGET_OFFSET = 20
TARGET_X_MIN  = FRAME_X_CENTER - TARGET_OFFSET
TARGET_X_MAX = FRAME_X_CENTER + TARGET_OFFSET
TARGET_Y_MIN  = FRAME_Y_CENTER - TARGET_OFFSET
TARGET_Y_MAX = FRAME_Y_CENTER + TARGET_OFFSET

ik_chain = ikpy.chain.Chain.from_urdf_file("../PiController/ik/niryo_one.urdf")
cam = camera.Cam(FRAME_WIDTH, FRAME_HEIGHT)
motion = motionControl.MotionControl()
motion.goReady()
print("robot initialized")

def moveRobotWithIK():
    pose = motion.current_pose[:8]
    pose[1] = 0
    pose[4] = 0
    pose[6] = 0
    pose[7] = 0
    current_position_frame = ik_chain.forward_kinematics(pose)
    cyl_x = current_position_frame[:3,3][0]
    cyl_z = current_position_frame[:3,3][2]
    
    z = cam.getDepth(xmid, ymid)
    if (z == 0.0) : #try again
        z = cam.getDepth(xmid, ymid)

    target_vector = [cyl_x + z , 0, cyl_z]
    target_frame = np.eye(4)
    target_frame[:3, 3] = target_vector
    target_angles_radian = ik_chain.inverse_kinematics(target_frame)
    target_angles_degree = np.degrees(target_angles_radian).astype(int)
    target_pose = [motion.current_pose[1], 90 + target_angles_degree[2], target_angles_degree[3],
                    0, target_angles_degree[5], 0, 45]
    print(target_pose)
    motion.setPose(target_pose)

# main loop
stage = SEARCH_LR
start_time = 0
scan = -45
motion.moveLR(scan)
while True:
    strawberries = cam.detectStrawberriesOnFrame()

    if (time.time() - start_time) > DELAY:
        if len(strawberries) > 0:
            x1, y1, w, h = strawberries[0]
            xmid = int(x1 + (w / 2))
            ymid = int(y1 + (h / 2))
            increment = 3
            
            if stage == SEARCH_LR:
                if (xmid < TARGET_X_MIN):
                    print("move LEFT")
                    motion.moveLR(increment)
                elif (xmid > TARGET_X_MAX):
                    print("move RIGHT")
                    motion.moveLR(-1 * increment)
                else:
                    print("DO NOT MOVE, in the middle X")
                    stage = ALIGN_UD
                    continue
            
            if stage == ALIGN_UD:
                if (ymid < TARGET_Y_MIN):
                    print("move UP")
                    motion.moveUD(increment)
                elif (ymid > TARGET_Y_MAX):
                    print("move DOWN")
                    motion.moveUD(-1 * increment)
                else:
                    print("DO NOT MOVE, in the middle Y")
                    stage = IK
                    continue

            if stage == IK:
                moveRobotWithIK()
                time.sleep(2 * DELAY)
                stage = GRAB
                continue

            if stage == GRAB:
                motion.moveGrab(-30)
                time.sleep(2 * DELAY)
                stage = HOME
                continue

            if stage == HOME:
                motion.goReady()
                time.sleep(2 * DELAY)
                stage = SEARCH_LR
                scan += 15
                if (scan > 45):
                    scan = -45
                motion.moveLR(scan)
                continue

            motion.writeJSON()

        elif (len(strawberries) == 0):
            stage = SEARCH_LR
            motion.goReady()
            scan += 15
            if (scan > 45):
                scan = -45
            motion.moveLR(scan)
            print("go to ready position, can't see anything")
        
        start_time = time.time()
    print("before displayImage")
    key = cam.displayImage()
    print("after displayImage")
    if key in [27, ord('q')]:
            break
        
cam.stopCamera()


