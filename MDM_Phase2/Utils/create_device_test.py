import datetime
import copy
import random
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

#set up log file
timestamp=datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir=os.path.join(os.path.dirname(__file__),f"{req_dir_path}Log")
logger=setup_log(os.path.join(log_dir,f"{timestamp}_create_test_device.text"))

def create_test_device():

    print("test initiated to create device in test stage")
    logger.info("Test initiated to create device in test stage")

    #import config file
    try:
        with open (config_file_path,"r") as f:
            config = json.load(f)
        print("Config file imported")

    except Exception as e:

        print("Exception occurred while importing the config.json file")
        logger.error("Exception occurred while importing the config.json file")

    #headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['token']}"
    }

    try:
        if 'models_v2' in config and 'test_device_payload' in config:
            models = config['models_v2']
            data = config['test_device_payload']
            payload = copy.deepcopy(data)
            random_m_id = str(random.randint(100,999))
            random_ref_id = str(random.randint(1000,9999))
            for m in models:
                print("in for loop")
                model_url = config['url'] + "v2/catalog/models"

                if m=='mta':
                    payload['modelName'] = 'Test_' + m + random_m_id
                    payload['vendorName'] = 'Technicolor'
                    payload['modelDesc']['deviceTypeName'] = m
                    payload['metadata']['referenceId'] = 'AtmnRef_' + random_ref_id
                    payload['metadata']['externalId'] = 'AtmnExt_' + random_m_id
                    payload['modelDesc']['deviceType'] = {}
                    payload['modelDesc']['deviceType']['docsisVersion'] = "1.1"

                elif m=='cwl':
                    payload['modelName'] = 'Test_' + m + random_m_id
                    payload['vendorName'] = 'Motorola'
                    payload['modelDesc']['deviceTypeName'] = m
                    payload['metadata']['referenceId'] = 'AtmnRef_' + random_ref_id
                    payload['metadata']['externalId'] = 'AtmnExt_' + random_m_id
                    payload['modelDesc']['deviceType'] = {}
                    payload['modelDesc']['deviceType']['docsisVersion'] = "1.1"

                elif m=='snu':
                    payload['modelName'] = 'Test_' + m + random_m_id
                    payload['vendorName'] = 'Humax'
                    payload['modelDesc']['deviceTypeName'] = m
                    payload['metadata']['referenceId'] = 'AtmnRef_' + random_ref_id
                    payload['metadata']['externalId'] = 'AtmnExt_' + random_m_id
                    payload['modelDesc']['deviceType']={}
                    payload['modelDesc']['deviceType']['docsisVersion'] = "1.1"

                elif m=='onu':
                    payload['modelName'] = 'Test_' + m + random_m_id
                    payload['vendorName'] = 'ALCATEL'
                    payload['modelDesc']['deviceTypeName'] = m
                    payload['metadata']['referenceId'] = 'AtmnRef_' + random_ref_id
                    payload['metadata']['externalId'] = 'AtmnExt_' + random_m_id
                    payload['modelDesc']['deviceType'] = {}
                    payload['modelDesc']['deviceType']['docsisVersion'] = "1.1"

                elif m=='ata':
                    payload['modelName'] = 'Test_' + m + random_m_id
                    payload['vendorName'] = 'Ubee'
                    payload['modelDesc']['deviceTypeName'] = m
                    payload['metadata']['referenceId'] = 'AtmnRef_' + random_ref_id
                    payload['metadata']['externalId'] = 'AtmnExt_' + random_m_id
                    del payload['modelDesc']['deviceType']

                #initiate to create models in test stage by Post api
                response_post = requests.post(url=model_url,headers=headers,data=json.dumps(payload),verify=False)
                print(f"Response_code for {m}: {response_post.status_code}")
                print(f"Response_text for {m}: {response_post.text}")

                if response_post.status_code == 201:
                    logger.info(f"Response code for {m}: {response_post.status_code}")
                    logger.info(f"Response text for {m}: {response_post.text}")

                    if m in config['test_devices']:
                        config['test_devices'][m] = payload['modelName']
                    with open(config_file_path,'w') as f:
                        json.dump(config,f,indent=4)
                else:
                    logger.error(f"Response code for {m}: {response_post.status_code}")
                    logger.error(f"Response text for {m}: {response_post.text}")
        else:
            print("models/payload not present in config file")
            logger.error("models/payload not present in config file")

    except Exception as e:
        print("Exception occurred while creating device: ",e)
        logger.error(f"Exception occurred while creating device: {e}")

    finally:
        print("Test completed for pushing device in test stage")
        logger.info(f"Test completed for pushing device in test stage")




#create_test_device()