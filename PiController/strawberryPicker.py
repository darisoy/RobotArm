import time
import numpy as np
import ikpy
import motion
import camera


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

ik_chain = ikpy.chain.Chain.from_urdf_file("./ik/niryo_one.urdf")
cam = camera.Cam(xlen, ylen)
motion = motion.MotionControl()
#motion.goReady()
print("robot initialized")

start_time = 0
while True:
    cam.getFrame()
    time.sleep(0.01)
    strawberries = cam.detectStrawberriesOnFrame()

    if len(strawberries) > 0 and (time.time() - start_time) > delay:
        tracking = 1
        x1, y1, w, h = strawberries[0]
        x2 = x1 + w
        y2 = y1 + h
        xmid = int((x1 + x2) /2)
        ymid = int((y1 + y2) /2)
        increment = 5
        
        if stage == SEARCH_LR:
            if (xmid < x_range_low):
                print("move LEFT")
                #motion.moveLR(increment)
                motion.writeJSON()
            elif (xmid > x_range_high):
                print("move RIGHT")
                #motion.moveLR(-1 * increment)
                motion.writeJSON()
            else:
                print("DO NOT MOVE, in the middle X")
                stage = ALIGN_UD
                continue

        if stage == ALIGN_UD:
            if (ymid < y_range_low):
                print("move UP")
                #motion.moveUD(increment)
                motion.writeJSON()
            elif (ymid > y_range_high):
                print("move DOWN")
                #motion.moveUD(-1 * increment)
                motion.writeJSON()
            else:
                print("DO NOT MOVE, in the middle Y")
                stage = IK
                continue

        if stage == IK:
            pose = motion.current_pose[:8]
            pose[1] = 0
            pose[4] = 0
            pose[6] = 0
            pose[7] = 0
            current_position_frame = ik_chain.forward_kinematics(pose)
            z = cam.getDepth(xmid, ymid)
            cyl_x = current_position_frame[:3,3][0]
            cyl_z = current_position_frame[:3,3][2]
            target_vector = [cyl_x + z ,0, cyl_z]
            target_frame = np.eye(4)
            target_frame[:3, 3] = target_vector
            target_angles = ik_chain.inverse_kinematics(target_frame)
            target_pose = [motion.current_pose[1],target_angles[2],target_angles[3],0,target_angles[5],0,45]
            #motion.setPose(target_pose)
            time.sleep(4)
            stage = GRAB
            continue

        if stage == GRAB:
            motion.moveGrab(-30)
            time.sleep(2)
            stage = HOME
            continue

        if stage == HOME:
            motion.goReady()
            time.sleep(4)
            stage = SEARCH_LR
            tracking = 0
            continue

        start_time = time.time()

    elif (len(strawberries) == 0) and (time.time() - start_time) > delay:
        tracking = 0
        stage = SEARCH_LR
        #motion.goReady()
        print("go home, can't see anything")
        start_time = time.time()
    
    key = cam.displayImage()
    if key in [27, ord('q')]:
            break
        
cam.stopCamera()


