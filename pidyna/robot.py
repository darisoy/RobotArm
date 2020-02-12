
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
    low_limits = [0,175,36,0,175,00,147]

    def __init__(self):
        self.servo_bus = Ax12_2()
        self.urdf = "./niryo_one.urdf"
        self.chain = ikpy.chain.Chain.from_urdf_file(self.urdf)
        #self.servoIDs = self.servo_bus.learnServos(minValue = 4, maxValue=6,verbose=True)
        #print(self.servo_bus.learnServos(minValue = 4, maxValue=6,verbose=True)) 
        self.servoIDs = [1,2,3,4,5,6]
        print('servoIDs = ',self.servoIDs)
        print('enabling Torque on all servos')
        '''
        for i in self.servoIDs:
            if i > 5:
                self.servo_bus.setTorqueStatus(i, True,verbose=True)
        print('done initializing') 
        
        for i in range(3):
            self.moveJoint(1,0)
            self.moveJoint(2,-10)
            self.moveJoint(3,90)
        '''

    def moveJoint(self, joint, position, verbose=False):
        if joint in self.servoIDs and joint != 5:
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


    def setPose(self,pose):
        delay = 0.1
        self.moveJoint(Robot.base_shoulder_joint,pose[0]) 
        sleep(delay)
        self.moveJoint(Robot.shoulder_arm_joint,pose[1])
        sleep(delay)
        self.moveJoint(Robot.arm_elbow_joint,pose[2])
        sleep(delay)
        self.moveJoint(Robot.elbow_forearm_joint,pose[3])
        sleep(delay)
        self.moveJoint(Robot.forearm_wrist_joint,pose[4])
        sleep(delay)
        self.moveJoint(Robot.wrist_hand_joint,pose[5])
        

    def goHome(self):
        for i in range(10):
            self.setPose([0,0,0,0,0,0])

        poses = [0,30,50,45,30,-30]
        self.setPose(poses)

        for i in range(3):
            self.setPose([-30,30,50,0,0,0])
            sleep(2)
            self.setPose([30,30,50,0,0,0])
            sleep(2)
        self.setPose(poses)

        target_vector = [ 0.1, -0.2, 0.1]
        target_frame = np.eye(4)
        target_frame[:3, 3] = target_vector
        angles = self.chain.inverse_kinematics(target_frame)
        result = np.zeros(6)
        for i in range(6)
            result[i] = angles[i+1]

        self.setPose(result)
        
