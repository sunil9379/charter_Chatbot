import datetime
import random
import time

import requests
import json
from Requests.Log.logger_setup import setup_log
import os
from load_dotenv import load_dotenv
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH") #this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH") #this is Requests directory path

'''
#set up log file
timestamp=datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir=os.path.join(os.path.dirname(__file__),f"{req_dir_path}Log")
logger=setup_log(os.path.join(log_dir,f"{timestamp}_getfirmware_info.text"))
'''

def get_firmware_infov1(modelname,vendors,firmware):

    with open(config_file_path,"r") as f:
        config = json.load(f)
    token = config["token"]
    url = config["url"]

    #with open(payload_import,"r") as f:
    #    data=json.load(f)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }


    #for key,value in vendors.items():

    firmware_urlv1 = f"{url}v1/catalog/vendors/{vendors}/models/{modelname}/firmwares/{firmware}?include_model_attrs=true"
    response = requests.get(url=firmware_urlv1, headers=headers, verify=False)
    rcode = response.status_code
    rbody = response.text

    results = {"Status Code": rcode, "Response Body": rbody}

    return results


def get_firmware_infov2(modelname,firmware):

    with open(config_file_path,"r") as f:
        config = json.load(f)
    token = config["token"]
    url = config["url"]

    #with open(payload_import,"r") as f:
    #    data=json.load(f)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    results = {}


    ref_id = str(random.randint(1000,9999))

    firmware_urlv2 = f"{url}v2/catalog/models/{modelname}/firmwares/{firmware}?referenceId={ref_id}"
    response = requests.get(url=firmware_urlv2, headers=headers, verify=False)
    rcode = response.status_code
    rbody = response.text

    results = {"Status Code": rcode, "Response Body": rbody}

    return results

#res=get_firmware_infov1("Test_ata001","Ubee","Test_ata001-P20-040625-2025.5")
#print(res)
#res = get_firmware_infov2("Test_ata001","Test_ata001-P20-040625-2025.5")
#print(res)