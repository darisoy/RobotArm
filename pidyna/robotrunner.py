import robot
import time

my_robot = robot.Robot()

my_robot.move3d([0.1, 0.2, 0.1])
time.sleep(2)
my_robot.record()
