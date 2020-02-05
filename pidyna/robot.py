
from ax12 import Ax12_2
from time import sleep
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
    minValue = 4
    maxValue = 5
    timeout = 0.05

    def __init__(self):
        self.servo_bus = Ax12_2()
        self.urdf = "./niryo_one.urdf"
        self.chain = ikpy.chain.Chain.from_urdf_file(self.urdf)
        self.servoIDs = self.learnServos(minValue, maxValue,verbose=True)
        print('servoIDs = ',self.servoIDs)
        print('enabling Torque on all servos')
        for i in self.servoIDs:
            # self.servo_bus.setTorqueStatus(i, True,verbose=True)
            self.setTorque(i, True, verbose=True)
        print('done initializing')

    def move3d(self,position):
        #position is 3d np vector, or 3 element list
        target_frame = np.eye(4)
        target_frame[:3, 3] = position
        degrees = self.chain.inverse_kinematics(target_frame) * (180 / np.pi)
        print(degrees)
        self.moveJoint(Robot.elbow_forearm_joint, degrees[Robot.elbow_forearm_joint],verbose=True)

    def record(self):
        for i in self.servoIDs:
            # self.servo_bus.setTorqueStatus(i,False)
            self.setTorque(i, False)
        arr = []
        try:
            while True:
                val = self.servo_bus.readPositionDegrees(self.elbow_forearm_joint)
                arr.append(val)
                print(val)
        except Exception as e:
            print(e)
            return arr

    def moveJoint(self, joint, position, verbose=False):
        #TODO: if timout send again
        def timeout(signum, frame):
            raise IOError("Timeout")

        try :
            signal.signal(signal.SIGALRM, timeout)
            signal.alarm(1)
            if joint in self.servoIDs:
                if verbose: print("moving joint ",joint," to position ", position)
                self.servo_bus.moveDegrees( joint, position)

        except Exception as detail:
            if verbose : print("Error setting torque on servo #" + str(i) + ': ' + str(detail))
            sleep(0.5)
            moveJoint(joint, position, verbose)
            pass
        signal.alarm(0)

    def setTorque(self, id, status, verbose=False):
        #TODO: if timout send again
        def timeout(signum, frame):
            raise IOError("Timeout")

        try :
            signal.signal(signal.SIGALRM, timeout)
            signal.alarm(1)
            temp = self.servo_bus.setTorqueStatus(id, status ,verbose)
            if verbose: print('set torque: ', status, ' on servo #', id)

        except Exception as detail:
            if verbose : print("Error setting torque on servo #" + str(i) + ': ' + str(detail))
            sleep(0.5)
            setTorque(id, status, verbose)
            pass
        signal.alarm(0)

    def learnServos(self, minValue=1, maxValue=6, verbose=False):
        servoList = []
        def timeout(signum, frame):
            raise IOError("Timeout")

        for i in range(minValue, maxValue + 1):
            try :
                signal.signal(signal.SIGALRM, timeout)
                signal.alarm(1)
                temp = self.servo_bus.ping(i)
                servoList.append(i)
                if verbose: print("Found servo #" + str(i))

            except Exception as detail:
                if verbose : print("Error pinging servo #" + str(i) + ': ' + str(detail))
                pass
        signal.alarm(0)
        return servoList

    def goHome(self):
        val = -30
        while 1:
            sleep(1)
            self.moveJoint(Robot.elbow_forearm_joint, val,verbose=True)
            self.moveJoint(Robot.forearm_wrist_joint, val,verbose=True)
            self.moveJoint(Robot.wrist_hand_joint, val,verbose=True)
            val += 5
