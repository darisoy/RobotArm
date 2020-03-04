
from ax12 import Ax12_2
from time import sleep
import ikpy
import numpy as np
import json

class Robot:
    world_base_joint = 0
    base_shoulder_joint = 1
    shoulder_arm_joint = 2
    arm_elbow_joint = 3
    elbow_forearm_joint = 4
    forearm_wrist_joint = 5
    wrist_hand_joint = 6
    hand_tool_joint = 7
    low_limits = [0,175,36,0,175,90,147,0]
    joint_names = ['base','shoulder','arm','elbow','forearm','wrist','hand']


    def __init__(self):
        self.servo_bus = Ax12_2()
        self.urdf = "./niryo_one.urdf"
        self.chain = ikpy.chain.Chain.from_urdf_file(self.urdf)
        #self.servoIDs = self.servo_bus.learnServos(minValue = 4, maxValue=6,verbose=True)
        #print(self.servo_bus.learnServos(minValue = 4, maxValue=6,verbose=True)) 
        self.servoIDs = [1,2,3,4,5,6,7]
        self.current_pose = [0,0,0,0,0,0,0,0]
        #self.servoIDs = [4,5,6]
        print('servoIDs = ',self.servoIDs)
        #print('enabling Torque on all servos')

        for i in self.servoIDs:
            if i > 3:
                self.moveJoint(i,0)
                self.servo_bus.setTorqueStatus(i, True,verbose=True)
        print('done initializing') 
        '''
        for i in range(3):
            self.moveJoint(1,0)
            self.moveJoint(2,-10)
            self.moveJoint(3,90)
        '''
    def writeJSON(self):
        f = open('../Frontend/status.json','w')
        f.write(json.dumps({i:j for i,j in zip(Robot.joint_names,self.current_pose)}))
        f.close()

    def moveJoint(self, joint, position, verbose=True):
        if joint in self.servoIDs:# and joint != 5:
            if verbose: print("moving joint ",joint," to position ", position)
            #if verbose: print("current position ", self.servo_bus.readPositionDegrees(joint))
            #print(position, Robot.low_limits[joint])
            self.servo_bus.moveDegrees( joint, position+Robot.low_limits[joint])
            self.current_pose[joint] = position

    def moveJointRelative(self, joint, dp, verbose):
        self.moveJoint(joint,self.current_pose[joint]+dp, verbose=verbose)

    def resetEffector(self): #deprecated
        self.moveJoint(5, -1*(90 - self.current_pose[2] + self.current_pose[3] + 10))

    def moveLR(self, dp):
        self.moveJointRelative(1, dp, verbose=True)

    def moveFB(self, dp):
        self.moveJointRelative(2, -dp/2, verbose=True)
        self.moveJointRelative(3, dp/2, verbose=True)

    def moveUD(self, dp):
        self.moveJointRelative(3, dp, verbose=True)
        self.moveJointRelative(5, dp, verbose=True)
        
    def moveGrab(self, dp):
        self.moveJointRelative(7, dp, verbose=True)

    def move3d(self,position):
        #position is 3d np vector, or 3 element list
        target_frame = np.eye(4)
        target_frame[:3, 3] = position
        degrees = self.chain.inverse_kinematics(target_frame) * (180 / np.pi) 
        degrees[4] = 0
        degrees[5] = -1*(90 - degrees[2] + degrees[3] + 10) #level out effector
        degrees[6] = 0
        print(degrees)
        for joint in range(1,7):
            self.moveJoint(joint, degrees[joint],verbose=True)

    def setPose(self,pose):
        self.moveJoint(Robot.base_shoulder_joint,pose[0],verbose=True) 
        self.moveJoint(Robot.shoulder_arm_joint,pose[1],verbose=True)
        self.moveJoint(Robot.arm_elbow_joint,pose[2],verbose=True)
        self.moveJoint(Robot.elbow_forearm_joint,pose[3],verbose=True)
        self.moveJoint(Robot.forearm_wrist_joint,pose[4],verbose=True)
        self.moveJoint(Robot.wrist_hand_joint,pose[5],verbose=True)
        self.moveJoint(Robot.hand_tool_joint,pose[6],verbose=True)


    def goReady(self):
        ready = [0,30,40,0,0,0,45]
        self.setPose(ready)
        #sleep(10)
    
    def resetHome(self):
        self.servo_bus.resetHome(1)
        self.servo_bus.resetHome(2)
        self.servo_bus.resetHome(3)
