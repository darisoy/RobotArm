import robot
import time

my_robot = robot.Robot()
my_robot.goReady()
delay = 1
angle = 30

while True:
    time.sleep(delay)
    #angle *= -1
    my_robot.moveJoint(1, 5, verbose=True)
    time.sleep(delay)
    my_robot.moveJoint(1, 0, verbose=True)
    #my_robot.moveLR(angle)
    #my_robot.moveFB(angle)
    #my_robot.moveUD(angle)
