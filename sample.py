import json



file_path = "C:\\Users\P3205066\PycharmProjects\pythonProject\Config.json"
with open(file_path, 'r') as file:
    data = json.load(file)

model_name = data["modelName_onu"]
api_url = data["Get_model_info_v2_url"]
bearer_token = data["BearerToken"]
onu_model = data["onuModel"]
PUT_URL = data["Update_Device_PUT_URL"]

print(PUT_URL)












