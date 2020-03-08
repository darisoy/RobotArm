import motionControl
import time

my_robot = motionControl.MotionControl()
my_robot.goReady()
delay = 1
angle = 30

while True:
    time.sleep(delay)
    #angle *= -1
    my_robot.moveJoint(4, 175, verbose=True)
    time.sleep(0.01)
    my_robot.moveJoint(5, 90, verbose=True)
    time.sleep(0.01)
    my_robot.moveJoint(6, 147, verbose=True)
    time.sleep(delay)
    my_robot.moveJoint(4, 190, verbose=True)
    time.sleep(0.01)
    my_robot.moveJoint(5, 100, verbose=True)
    time.sleep(0.01)
    my_robot.moveJoint(6, 160, verbose=True)
    #my_robot.moveLR(angle)
    #my_robot.moveFB(angle)
    #my_robot.moveUD(angle)
