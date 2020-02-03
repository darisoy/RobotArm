#!/usr/bin/env python
from ax12 import Ax12_2
import time
import ikpy
import numpy as np
from ikpy import plot_utils

def main():
    servo_bus = Ax12_2()

    my_chain = ikpy.chain.Chain.from_urdf_file("./niryo_one.urdf")

    world_base_joint = 0
    base_shoulder_joint = 1
    shoulder_arm_joint = 2
    arm_elbow_joint = 3
    elbow_forearm_joint = 4
    forearm_wrist_joint = 5
    wrist_hand_joint = 6
    hand_tool_join = 7

    target_vector = [ 0.1, -0.2, 0.1]
    target_frame = np.eye(4)
    target_frame[:3, 3] = target_vector
    #print(target_frame)

    radians = my_chain.inverse_kinematics(target_frame)
    raw = np.floor(((radians * (180 / (np.pi)) + 180) % 360) * (4096/360))

    print(raw)


    print("----ping start----")
    print(servo_bus.ping(elbow_forearm_joint).hex())
    #print(servo_bus.ping(forearm_wrist_joint).hex())
    print("----torque enable-")
    print(servo_bus.setTorqueStatus(elbow_forearm_joint, True))
    #print(servo_bus.setTorqueStatus(forearm_wrist_joint,True))
    print("----move start----")
    #print(servo_bus.move(4, 116).hex())
    #print(servo_bus.move(5, 116).hex())
    while True:
        servo_bus.move(elbow_forearm_joint, 0)
        #servo_bus.move(forearm_wrist_joint,1024)
        time.sleep(2)
        servo_bus.move(elbow_forearm_joint, int(raw[elbow_forearm_joint]))
        #servo_bus.move(forearm_wrist_joint,2048)
        time.sleep(2)

if __name__ == '__main__':
    main()
