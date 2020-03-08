import json

def send_data(file_name):
	print("data:")
	with open(file_name) as json_file:
		data = json.load(json_file)
		print(json.dumps(data, indent=1))


send_data("../Frontend/client/data/log.json")