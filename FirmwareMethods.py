#importing the required libraries
import logging
from datetime import datetime
from logsetup import *
from dummydummy import *
from Firmware_Methods_All import *

ref_id = "TestModel" + str(datetime.now().second)
ext_id = "TestModel" + str(datetime.now().second)
#formating the date to ddmm-yyyy format
date_str = str(datetime.now())
date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
formatted_date = date_obj.strftime("%d%m%Y")
ref_id = "TestModel" + str(datetime.now().second)
ext_id = "TestModel" + str(datetime.now().second)
getModel_url = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models/"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkZXZpY2VvcGVkaWEtdG9rZW4gc2NyaXB0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiREVWSUNFT1BFRElBX2NsaWVudCIsInJvbGVzIjpbIlNEX0NBVEFMT0dfQURNSU4iLCJTRF9GQVNfQURNSU4iLCJTRF9SRFVfQURNSU4iLCJTRF9NT05HT19BRE1JTiIsIlNEX1NVUEVSQURNSU4iXSwibmFtZSI6Im1lIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWUiLCJnaXZlbl9uYW1lIjoibWUiLCJmYW1pbHlfbmFtZSI6Im1lIn0.9zVJY_R1HY-4OfL25loOAd_OS_E5su7nAgXCtmXONqA"
# headers for the API
headers = {
"Content-Type": "application/json",
'Authorization': f'Bearer {token}'
}

#create firmware payload template:
payload = {
  "firmwareVersion": "string",
  "firmwareFilename": "string",
  "firmwareTransferProtocol": "TFTP",
  "firmwareTags": {
    "bhn": {},
    "twc": {},
    "global": {}
  },
  "upgrade": "true",
  "metadata": {
    "contextId": "QA01",
    "referenceId": ref_id,
    "externalId": ext_id,
    "userId": "P3205066"
  }
}

for models in data.values():
    FV = str(models["modelName"])
    cr_url = getModel_url + FV + "/firmwares"
    firmware_updated = {  "firmwareVersion": FV + "-P20-" + formatted_date + "-2025.2", "firmwareFilename": FV + "-P20-" + formatted_date + "-2025.2.charter",}
    for key,value in firmware_updated.items():
        if key in payload:
            payload[key] = value
    Get_fw_url = getModel_url + FV + "/firmwares/" + str(json.loads(firmware_updated["firmwareVersion"])) + "?referenceID=" + ref_id
    create_firmware(cr_url, payload, headers)
    get_firmware_v2(Get_fw_url)


