import copy
import datetime
import json
import logging
import random
import re
from http.client import responses
from wsgiref import headers

import requests

from Log.logger_setup import setup_log
import os
'''
def setup_log(log_file,level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
'''

'''
def example():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), "Log")
    logger = setup_log(os.path.join(log_dir, f"{timestamp}_example_1.text"))

    logger.info("Example 1")

def example_2():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    log_dir = os.path.join(os.path.dirname(__file__), "Log")
    logger = setup_log(os.path.join(log_dir, f"{timestamp}_example_2.text"))

    logger.info("Example 2")


example()
example_2()
'''

#TEST AND CERTIFY
'''with open('access_token.txt') as f:
    token = f.read()
with open("device_certify.json") as f:
    cert = json.load(f)
with open("device_test.json") as f:
    test = json.load(f)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
url_test = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models"
url_cert = f"https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models/Test_onu001?status=Certified"

tp = test['onu']
cp = cert['onu']
print("payload: ",tp)

response_test = requests.post(url=url_test, headers=headers, data=json.dumps(tp), verify=False)
print("Response code: ",response_test.status_code)
print("response body: ",response_test.text)

response_cert = requests.put(url=url_cert, headers=headers, data=json.dumps(cp), verify=False)
print("Response code: ",response_cert.status_code)
print("response body: ",response_cert.text)
'''

#DELETE DEVICES
'''
with open("config.json","r") as f:
    config = json.load(f)
url = config["url"]
token = config["token"]
headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
for m in config["models_v2"]:

    device = config['test_devices'][m]
    ref_id = "sd" + str(random.randint(1000, 9999))

    url_model = url + "v2/catalog/models/" + device + "?referenceId=" + ref_id + "&userId=P3289462"

    response = requests.delete(url=url_model, headers=headers, verify=False)
    print("Response code: ",response.status_code)
    print("Response body: ",response.text)
'''


#aggreagte view
'''
with open("device_deploy.json","r") as f:
    data = json.load(f)
payload = copy.deepcopy(data)
with open("config.json","r") as f:
    config = json.load(f)
url = config["url"]
token = config["token"]
headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
for m in config["models_v2"]:
    device_payload = payload[m]
    device_name = device_payload.get('modelName')
    vendor_name = device_payload.get('vendorName')
    firmware_edva = device_payload["firmwareDesc"]["eDvaFirmware"]["firmwareVersion"]
    firmware_tags = device_payload.get('firmwareDesc', {}).get('firmwareVersions', {}).get('firmwareTags')
    print("device details fetched")

    v1_url = f"{url}v1/legacy/aggregateView?vendor{vendor_name}&model={device_name}&firmware=+{firmware_edva}"
    ref_id = "sd" + str(random.randint(1000, 9999))

    response = requests.get(url=v1_url, headers=headers, data=json.dumps(device_payload),verify=False)
    print("Response code: ",response.status_code)
    print("Response body: ",response.text)
'''


'''
list_url = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/mongo/backups/list"
value = 'Test_062525_1221-2025_06_25-06:51:46_AM.tgz'
with open("config.json","r") as f:
    config = json.load(f)
    token = config["token"]
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
get_res = requests.get(list_url, headers=headers, verify=False)
files = json.loads(get_res.text)
#files =list(files)
#print("type ",type(files))
print(files)
if get_res.status_code == 200:
    if value in files:
       print("Backupfile created present in db, validation successfull")
    else:
        print("Backupfile created not present in db, validation failed")
else:
    print("got other code except 200")

a=["av","asd","vbn"]
if 'av' in a:
    print("av in a")
else:
    print("av not in a")
'''

'''
with open('dummy.json','r') as f:
    data = json.load(f)

firmware_desc = data.get('firmwareDesc')
firm_ver = firmware_desc.get('firmwareVersions')
third = firm_ver[2]
req = third.get('firmwareVersion')
print(req)

reqq = data.get('firmwareDesc').get('firmwareVersions')[2].get('firmwareVersion')
print(reqq)
'''

'''
#for get_aggregate view
url = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/legacy/aggregateView?vendor=Ubee&model=Test_ata001&firmware=Test_ata001-P20-041025-2025.1"
with open("config.json","r") as f:
    config = json.load(f)
token = config["token"]

with open("device_deploy.json","r") as f:
    data = json.load(f)
val_data = data['ata']
print(val_data)


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

response = requests.get(url=url,headers=headers,verify=False)
rep_data = response.json()
print(type(rep_data))
print(f"response data: {rep_data}\ntype: {type(rep_data)}")

#fetch only base from it
req = rep_data['base']['twc']['Ubee|Test_ata001|Test_ata001-P20-041025-2025.1']
print(type(req))
print(req)


actu={
    "bhn":
           {
             "autoprov": "",
             "device-class": "ata",
             "ipv6-cpe": "",
             "smh": "",
             "throughput-cap": "1G",
             "voice-class": "ata"
           },
            "twc":
            {
              "autoprov": "",
              "device-class": "ata",
              "ipv6-cpe": "",
              "smh": "",
              "throughput-cap": "1G",
              "voice-class": "ata"
            }
}

bhn_keys=actu['bhn'].keys()

print(bhn_keys)
print(type(bhn_keys))
bhn_values=actu['bhn'].values()
twc_keys=actu['twc'].keys()
twc_values=actu['twc'].values()

val_status=False
for i,j in zip(bhn_keys,bhn_values):
    if i in req and j in req:
        print(f"The key {i} has value {j} in response payload")
        val_status=True

    else:
        print(f"{i}/{j} not in payload response payload")
        val_status=False

if val_status==True:
    print("Validation succeeded")
else:
    print("Failed to validate")
'''

'''
from requests.structures import CaseInsensitiveDict as cid
with open("config.json","r") as f:
    config = json.load(f)
token = config["token"]
url = config["url"]
backup = config["backup_devices"]

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
murl = url + "v2/mongo/backups/download/" + backup
response = requests.get(url=murl,headers=headers,verify=False)
print(response.status_code)
print(response.headers)
hea = response.headers
if backup in hea:
    print("true")
else:
    print("false")

print("code: ",response.status_code)
print(response.headers)
print("type: ",type(response.headers))


reh = cid(response.headers)
norm = dict(reh)
print("new type: ",type(norm))
content = norm["content-disposition"]
from urllib.parse import unquote

if pat:
    enc = pat.group(1)
    dec = unquote(enc)
    print(dec)
else:
    print(f"{backup} not found in headers")

def doc_validation(value,url,headers):
    from requests.structures import CaseInsensitiveDict as cid
    from urllib.parse import unquote

    response = requests.get(url=url,headers=headers,verify=False)
    if response.status_code == 200:
        reh = cid(response.headers)
        content = reh["content-disposition"]
'''

'''
with open("config.json","r") as f:
    config = json.load(f)
token = config["token"]
url = config["url"]
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
payload={
  "firmwareVersion": "Test_ata001-P20-040625-25.5",
  "firmwareFilename": "Test_ata001-P20-040625-25.5.charter",
  "firmwareTransferProtocol": "HTTPS",
  "firmwareTags": {
    "bhn": {},
    "twc": {},
    "global": {}
  },
  "upgrade": 'true',
  "metadata": {
    "contextId": "QA01",
    "referenceId": "bn43",
    "externalId": "bn43",
    "userId": "P3289462"
  }
}
murl = f"{url}v2/catalog/models/Test_ata001/firmwares"
response = requests.post(url=murl, json=payload, headers=headers, verify=False)
print(response.status_code)
print(response.text)
'''

with open("config.json","r") as f:
  config = json.load(f)
token = config["token"]
data = config["patch_payload"]
url="https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models/Test_ata000/firmwares"
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {token}"
}
data['eDvaFirmware'] = None
response = requests.patch(url=url,json=data,headers=headers,verify=False)
print("code: ",response.status_code)
print("body: ",response.text)
if
