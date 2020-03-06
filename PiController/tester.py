import json, os


joint_names = ['base','shoulder','arm','elbow','forearm','wrist','hand']
current_pose = [0,0,0,0,0,0,0,0]

# print(os.getcwd())

# sib_path = os.path.join(os.path.dirname(__file__), '..', 'Frontend')

# print(sib_path)

# for filename in os.listdir(sibB):
#     if filename.endswith('.txt'):
#         with open(os.path.join(sibB, filename)) as f:
#             print(f.read())
# print(os.path.join(sib_path, "client/data/log.json"))
# with open(os.path.join(sib_path, "client/data/log.json")) as f:

   # print(f.read())
   # print(f.read())
f = open("../Frontend/client/data/log.json", 'r')
obj = json.loads(f.read())
print(obj["arm_config"])
obj["arm_config"] = {i : j for i, j in zip(joint_names, current_pose)}
print(obj["arm_config"])
f.close()

f = open("../Frontend/client/data/log.json", 'w')
f.write(json.dumps(obj,indent=3))
f.close()