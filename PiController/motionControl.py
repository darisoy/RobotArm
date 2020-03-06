import comms
from time import sleep
import numpy as np
import json

class MotionControl:

    def __init__(self):
        self.servo_bus = comms.Messages()
        self.servoIDs = [1,2,3,4,5,6,7]
        self.current_pose = [0,0,0,0,0,0,0,0]
        self.world_base_joint = 0
        self.base_shoulder_joint = 1
        self.shoulder_arm_joint = 2
        self.arm_elbow_joint = 3
        self.elbow_forearm_joint = 4
        self.forearm_wrist_joint = 5
        self.wrist_hand_joint = 6
        self.hand_tool_joint = 7
        self.low_limits = [0,175,36,0,175,90,147,0]
        self.joint_names = ['base','shoulder','arm','elbow','forearm','wrist','hand']
        print('servoIDs = ',self.servoIDs)

        for i in self.servoIDs:
            if i > 3:
                self.moveJoint(i,0)
                self.servo_bus.enableTorque(i)
        print('done initializing')

    def moveJointRelative(self, joint, dp, verbose):
        self.moveJoint(joint, self.current_pose[joint] + dp, verbose=verbose)

    def moveLR(self, dp):
        self.moveJointRelative(1, dp, verbose=False)

    def moveFB(self, dp):
        self.moveJointRelative(2, -dp / 2, verbose=False)
        self.moveJointRelative(3, dp / 2, verbose=False)

    def moveUD(self, dp):
        self.moveJointRelative(3, dp, verbose=False)
        self.moveJointRelative(5, dp, verbose=False)

    def moveGrab(self, dp):
        self.moveJointRelative(7, dp, verbose=False)

    def goReady(self):
        ready = [0,30,40,0,0,0,45]
        self.setPose(ready)

    def setPose(self,pose):
        self.moveJoint(self.base_shoulder_joint, pose[0], verbose=False)
        self.moveJoint(self.shoulder_arm_joint,  pose[1], verbose=False)
        self.moveJoint(self.arm_elbow_joint,     pose[2], verbose=False)
        self.moveJoint(self.elbow_forearm_joint, pose[3], verbose=False)
        self.moveJoint(self.forearm_wrist_joint, pose[4], verbose=False)
        self.moveJoint(self.wrist_hand_joint,    pose[5], verbose=False)
        self.moveJoint(self.hand_tool_joint,     pose[6], verbose=False)

    def moveJoint(self, joint, position, verbose=True):
        if joint in self.servoIDs:
            if verbose: print("moving joint ", joint, " to position ", position)
            self.servo_bus.moveDegrees(joint, position + self.low_limits[joint])
            self.current_pose[joint] = position
    
    def writeJSON(self):
        f = open("../Frontend/client/data/log.json", 'r')
        obj = json.loads(f.read())
        obj["arm_config"] = {i : j for i, j in zip(self.joint_names, self.current_pose)}
        f.close()
        f = open("../Frontend/client/data/log.json", 'w')
        f.write(json.dumps(obj,indent=3))
        f.close()