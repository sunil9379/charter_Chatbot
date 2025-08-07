'''
1] get model v2 - code 200
2] delete firmware - code 204
3] delete firmware - code 404
4] delete device - code 204
5] full and incremental kafka message
6] delete model - code 404
7] get device - code 404
'''


import datetime
import json
import os
import random
import requests

from Phase_1.log_setup import setup_log
from Phase_1.getv2_devices import get_call
from Phase_1.delete_device import delete_devices
from Phase_1.frimware_delete import delete_firmware
from dotenv import load_dotenv

load_dotenv()
req_dir_path = os.environ.get("P1_DEPLOY_LOG_PATH")
config_file_path = os.environ.get("P1_CONFIG_PATH")

def deploy_delete_flow():

    #get call call1
    print(f"GET CALL 1")
    get_call(req_dir_path,"deploy_delete_get_v2_devices_call1")

    #delete firmware call1
    print("DELETE FIRMWARE 1")
    delete_firmware(req_dir_path=req_dir_path,log_name="deploy_delete_firmware_call1",stage="deploy")

    #delete firmware call2
    print("DELETE FIRMWARE 2")
    delete_firmware(req_dir_path=req_dir_path,log_name="deploy_delete_firmware_call2",stage="deploy",call="call2")

    #deleting the model call1
    print("DELETE MODEL 1")
    delete_devices(req_dir_path=req_dir_path,log_name="deploy_delete_model_call1")

    #kafka messages
    #def deploy_kafka():

    #delete model call2
    print("DELETE MODEL 2")
    delete_devices(req_dir_path=req_dir_path,log_name="deploy_delete_model_call2",flow="call2")

    #get call call2
    print("GET CALL 2")
    get_call(req_dir_path,"deploy_delete_get_v2_devices_call2","call2")

#deploy_delete_flow()