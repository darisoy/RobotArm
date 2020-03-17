import robot
import time

my_robot = robot.Robot()

#my_robot.move3d([0.1, 0.2, 0.1])
#time.sleep(10)
my_robot.goReady()

while True:
    print("enter a command (Ex: l30): ")
    command = input()
    if (len(command) <= 4 and len(command) >= 2):
        direction = command[0]
        angle = int(command[1:])
            
        if (direction == 'l'):
            my_robot.moveLR(angle)
        elif (direction == 'r'):
            my_robot.moveLR(-1 * angle)
        elif (direction == 'u'):
            my_robot.moveUD(angle)
        elif (direction == 'd'):
            my_robot.moveUD(-1 * angle)
        elif (direction == 'f'):
            my_robot.moveFB(angle)
        elif (direction == 'b'):
            my_robot.moveFB(-1 * angle)
        elif (direction == 'g'):
            my_robot.moveGrab(angle)
        elif (direction == 'x'):
            my_robot.moveGrab(-1 * angle)
    else:
        my_robot.goReady()

