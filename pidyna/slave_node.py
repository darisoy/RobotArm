import robot
import requests
import time
import json

my_robot = robot.Robot()
my_robot.goHome()
time.sleep(5)

url = 'http://localhost:8080/'
while True:
    body = json.dumps(my_robot.current_pose)
    requests.post(url+'current_pose',body=body)

    data = requests.post(url+'target_pose')
    print(data)
    
    pose = data #json.loads(data)
    #my_robot.setPose(pose)

    time.sleep(2)
