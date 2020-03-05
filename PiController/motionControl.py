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
        self.moveJointRelative(1, dp, verbose=True)

    def moveFB(self, dp):
        self.moveJointRelative(2, -dp / 2, verbose=True)
        self.moveJointRelative(3, dp / 2, verbose=True)

    def moveUD(self, dp):
        self.moveJointRelative(3, dp, verbose=True)
        self.moveJointRelative(5, dp, verbose=True)

    def moveGrab(self, dp):
        self.moveJointRelative(7, dp, verbose=True)

    def goReady(self):
        ready = [0,30,40,0,0,0,45]
        self.setPose(ready)

    def setPose(self,pose):
        self.moveJoint(self.base_shoulder_joint, pose[0], verbose=True)
        self.moveJoint(self.shoulder_arm_joint, pose[1], verbose=True)
        self.moveJoint(self.arm_elbow_joint, pose[2], verbose=True)
        self.moveJoint(self.elbow_forearm_joint, pose[3], verbose=True)
        self.moveJoint(self.forearm_wrist_joint, pose[4], verbose=True)
        self.moveJoint(self.wrist_hand_joint, pose[5], verbose=True)
        self.moveJoint(self.hand_tool_joint, pose[6], verbose=True)

    def moveJoint(self, joint, position, verbose=True):
        if joint in self.servoIDs:
            if verbose: print("moving joint ", joint, " to position ", position)
            self.servo_bus.moveDegrees(joint, position + self.low_limits[joint])
            self.current_pose[joint] = position
    
    def writeJSON(self):
        f = open('../Frontend/status.json','w')
        f.write(json.dumps({i : j for i, j in zip(self.joint_names, self.current_pose)}))
        f.close()
