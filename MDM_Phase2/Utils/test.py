import json

with open('certify_payload.json','r')as f:
    payload = json.load(f)
print(type(payload))

keys = payload.keys()
print(keys)

value_ata = payload['ata']
print(value_ata)

if 'xyz' in value_ata:
    print('xyz present')

from load_dotenv import load_dotenv
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH") #this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH") #this is Requests directory path

with open(config_file_path) as f:
    config = json.load(f)

for m in config['models_v2']:

    data_model = payload[m]
    print(data_model)

    device_name = data_model['vendorName']
    print(device_name)