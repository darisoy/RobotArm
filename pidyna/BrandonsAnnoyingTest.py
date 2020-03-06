import robot
import time
import ax12

my_robot = ax12.Ax12_2()
delay = 1
angle = 30
joint = 5

for i in range(7):
    if i > 3:
        my_robot.setTorqueStatus(i, True,verbose=True)

while True:
    time.sleep(delay)
    angle *= -1
    my_robot.moveDegrees( 4, 90)
    my_robot.moveDegrees( 5, 90)
    my_robot.moveDegrees( 6, 90)
    time.sleep(delay)
    my_robot.moveDegrees( 4, 95)
    my_robot.moveDegrees( 5, 95)
    my_robot.moveDegrees( 6, 95)
    

#ff ff fd 00 05 09 00 03 74 00 aa 02 00 00