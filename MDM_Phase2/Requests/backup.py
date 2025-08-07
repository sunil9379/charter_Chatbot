import copy
import random
import re
import time

import deepdiff
from bs4 import BeautifulSoup
from deepdiff import DeepDiff
import requests
import json
import urllib3
from dotenv import load_dotenv
import os
import datetime
from Requests.Log.logger_setup import setup_log
from requests.structures import CaseInsensitiveDict as cid
from urllib.parse import unquote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
config_file_path = os.environ.get("CONFIG_PATH")  # this is config.json file path
req_dir_path = os.environ.get("REQ_DIR_PATH")  # this is Requests directory path
payload_deploy = os.environ.get("PAYLOAD_DEPLOY")
payload_import = os.environ.get("PAYLOAD_IMPORT")


# set up log file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}Log")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{timestamp}_backup_flow.txt")
logger = setup_log(log_file, logger_name="file16")

def backup_list():

    '''Test for listing backups'''

    print("Test initiated for get api which lists the backup files")
    logger.info("Test initiated for get api which lists the backup files")

    try:
        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]
    except Exception as e:
        logger.error("Could not load config.json")


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        list_url = url + "v2/mongo/backups/list"

        response = requests.get(list_url, headers=headers, verify=False)
        print("Response code: ",response.status_code)
        print("Response text: ",response.text)

        if response.status_code == 200:
            logger.info("Backup list request successful")
            logger.info(f"Response code: {response.status_code}\nResponse Body: {response.text}")
        else:
            logger.error("Backup list request failed")
            logger.error(f"Response code: {response.status_code}\nResponse Body: {response.text}")

    except Exception as e:
        logger.error("Request failed")

    finally:
        logger.info("Test for list backup completed")
        logger.info("----------------------------------------")

    return

def backup_creation():
    '''Test for creating backup'''

    print("Test initiated to create the backup file")
    logger.info("Test initiated to create the backup file")

    try:
        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]
        backup = config.get("backup_devices")
    except Exception as e:
        logger.error("Could not load config.json")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    print(f"Backup: {backup}")
    try:

        file_url = url + "v2/mongo/backups/asyncCreate"
        list_url = url + "v2/mongo/backups/list"

        value = "Test_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        payload = {"backupFilename": f"{value}"}

        response = requests.post(file_url, headers=headers, data=json.dumps(payload),verify=False)
        print("Response code: ", response.status_code)
        print("Response text: ", response.text)
        resp_json = response.json()
        resp_value = resp_json.get("backup_filename")
        print(f"Backup filename: {resp_value}")
        if response.status_code == 202:
            logger.info("Backup file created successfully")
            logger.info(f"Response code: {response.status_code}\nResponse Body: {response.text}")

            get_res = requests.get(list_url, headers=headers, verify=False)
            if get_res.status_code == 200:
                if resp_value in get_res.text:
                    print("Backupfile created present in db, validation successful")
                    logger.info("Backupfile created present in db, validation successful")

                    config['backup_devices'] = resp_value
                    with open(config_file_path,"w") as f:
                        json.dump(config,f,indent=4)
                    print("Backup info stored in config file")
                else:
                    print("Backupfile created not present in db, validation failed")
                    logger.error("Backupfile created not present in db, validation failed")
            else:
                print("Could not get backup file created")
                logger.error("Error while getting backup file created")
        else:
            logger.error("Failed to create backup file")
            logger.errror(f"Response code: {response.status_code}\nResponse Body: {response.text}")

    except Exception as e:
        logger.error("Request failed")

    finally:
        logger.info("Test for list backup completed")
        logger.info("----------------------------------------")

    return



def download_backup():

    '''Test for downloading backup'''

    print("Test initiated to download the backup file")
    logger.info("Test initiated to download the backup file" )

    try:
        with open(config_file_path,"r") as f:
            config = json.load(f)
        url = config["url"]
        token = config["token"]
        backup = config.get("backup_devices")
    except Exception as e:
        logger.error("Could not load config.json")


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:

        print("backup file: ",backup)
        bck_url = url + "v2/mongo/backups/download/" + backup
        #bck_url = url + "v2/mongo/backups/download/Test_062525_1221-2025_06_25-06:51:46_AM.tgz"
        response = requests.get(bck_url, headers=headers, verify=False)
        print("Response code: ", response.status_code)
        #print("Response text: ",response.content.decode('utf-8', errors='ignore'))
        print("headers from response ",response.headers)

        if response.status_code == 200:
            logger.info("Fetched the downloadable .tgz file successfully")
            logger.info(f"Response code: {response.status_code}")
            logger.info(f"Response body: {response.headers}")

            #as the headers here is CaseInsensitiveDict, need to convert that to dict and unquote the value
            reh = cid(response.headers) #here cid is CaseInsensitiveDict a special dict from requests library
            norm = dict(reh)
            cont = norm['content-disposition']

            pat = re.search(r"filename\*\=utf-8''(.+)", cont)
            if pat:
                enc = pat.group(1)
                dec = unquote(enc)
                resp_value = dec
                if resp_value == backup:
                    print("Backup file validation successful")
                    logger.info(f"{backup} is present and same as in content")
                else:
                    logger.error("Backup file validation failed")
                    print("Backup file validation failed")
            else:
                print(f"{backup} not found in headers")

        else:
            logger.error("Failed to fetch downloadable .tgz file")
            logger.error(f"Response code: {response.status_code}\nResponse Body: {response.text}")

    except Exception as e:
        logger.error("Request failed")

    finally:
        logger.info("Test completed for backup download")
        logger.info("----------------------------------------")

    return


#backup_creation()
#time.sleep(2)
#download_backup()