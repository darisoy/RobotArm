
from ax12 import Ax12_2
from time import sleep
import ikpy
import numpy as np

class Robot:
    world_base_joint = 0
    base_shoulder_joint = 1
    shoulder_arm_joint = 2
    arm_elbow_joint = 3
    elbow_forearm_joint = 4
    forearm_wrist_joint = 5
    wrist_hand_joint = 6
    hand_tool_joint = 7
    low_limits = [0,175,36,0,175,100,147]

    def __init__(self):
        self.servo_bus = Ax12_2()
        self.urdf = "./niryo_one.urdf"
        self.chain = ikpy.chain.Chain.from_urdf_file(self.urdf)
        #self.servoIDs = self.servo_bus.learnServos(minValue = 4, maxValue=6,verbose=True)
        print(self.servo_bus.learnServos(minValue = 4, maxValue=6,verbose=True)) 
        self.servoIDs = [1,2,3,4]
        print('servoIDs = ',self.servoIDs)
        print('enabling Torque on all servos')
        #for i in self.servoIDs:
        #    if i > 3:
        #        self.servo_bus.setTorqueStatus(i, True,verbose=True)
        print('done initializing') 

    def moveJoint(self, joint, position, verbose=False):
        if joint in self.servoIDs:
            if verbose: print("moving joint ",joint," to position ", position)
            #if verbose: print("current position ", self.servo_bus.readPositionDegrees(joint))
            #print(position, Robot.low_limits[joint])
            self.servo_bus.moveDegrees( joint, position+Robot.low_limits[joint])

    def move3d(self,position):
        #position is 3d np vector, or 3 element list
        target_frame = np.eye(4)
        target_frame[:3, 3] = position
        degrees = self.chain.inverse_kinematics(target_frame) * (180 / np.pi) 
        print(degrees)
        self.moveJoint(Robot.elbow_forearm_joint, degrees[Robot.elbow_forearm_joint],verbose=True)
    
    def record(self):
        for i in self.servoIDs:
            self.servo_bus.setTorqueStatus(i,False)
        arr = []
        try:
            while True:
                val = self.servo_bus.readPositionDegrees(self.elbow_forearm_joint)
                arr.append(val)
                print(val)
        except Exception as e:
            print(e)
            return arr

    def goHome(self):
        poses = [
        [-90,10,10,45],
        [90,40,80,-45]
        ]
        state = 0 
        while 1:
            state = (state+1) % 2 
            val = poses[state]
            self.moveJoint(Robot.base_shoulder_joint,val[0])
            sleep(1)
            self.moveJoint(Robot.shoulder_arm_joint,val[1])
            sleep(1)
            self.moveJoint(Robot.arm_elbow_joint,val[2])
            sleep(1)
            self.moveJoint(Robot.elbow_forearm_joint,val[3])
            sleep(1)
            sleep(10)
            #self.moveJoint(Robot.elbow_forearm_joint, val,verbose=True)
            #sleep(1)
            #self.moveJoint(Robot.forearm_wrist_joint, val,verbose=True)
            #sleep(1)
            #self.moveJoint(Robot.wrist_hand_joint, val,verbose=True)
