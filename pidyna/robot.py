
from ax12 import Ax12_2
import ikpy
import numpy as np

class Robot:
    world_base_joint = 0
    base_shoulder_joint = 1
    shoulder_arm_joint = 2
    arm_elbow_join = 3
    elbow_forearm_joint = 4
    forearm_wrist_joint = 5
    wrist_hand_joint = 6
    hand_tool_joint = 7

    def __init__(self):
        self.servo_bus = Ax12_2()
        self.urdf = "./niryo_one.urdf"
        self.chain = ikpy.chain.Chain.from_urdf_file(self.urdf)
        self.servoIDs = self.servo_bus.learnServos(verbose=True)
        print('servoIDs = ',self.servoIDs)
        for i in self.servoIDs:
            self.servo_bus.setTorqueStatus(i, True)


    def moveJoint(self, joint, position, verbose=False):
        if joint in self.servoIDs:
            if verbose: print("moving joint ",joint," to position ", position)
            if verbose: print("current position ", self.servo_bus.readPositionDegrees(joint))
            self.servo_bus.moveDegrees( joint, position)

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


