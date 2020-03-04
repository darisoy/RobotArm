import robot
import time

my_robot = robot.Robot()
#my_robot.goReady()
delay = 1
angle = 30
joint = 1

while True:
    time.sleep(delay)
    angle *= -1
    my_robot.moveJoint(joint, angle, verbose=True)
    

