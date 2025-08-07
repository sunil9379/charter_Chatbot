# Importing the required libraries
import logging
import time
from CreateModel_Updated import *
import requests
import json
from datetime import datetime
from logsetup import *
from Get_Model_Info_v2 import *
from DeleteModel_V2 import *
# starting the timer to record the execution time
start_time = time.time()

# variable declaration
ref_id = "TestModel" + str(datetime.now().second)
ext_id = "TestModel" + str(datetime.now().second)
url = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models"
getModel_url = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models/"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkZXZpY2VvcGVkaWEtdG9rZW4gc2NyaXB0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiREVWSUNFT1BFRElBX2NsaWVudCIsInJvbGVzIjpbIlNEX0NBVEFMT0dfQURNSU4iLCJTRF9GQVNfQURNSU4iLCJTRF9SRFVfQURNSU4iLCJTRF9NT05HT19BRE1JTiIsIlNEX1NVUEVSQURNSU4iXSwibmFtZSI6Im1lIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWUiLCJnaXZlbl9uYW1lIjoibWUiLCJmYW1pbHlfbmFtZSI6Im1lIn0.9zVJY_R1HY-4OfL25loOAd_OS_E5su7nAgXCtmXONqA"
# headers for the API
headers = {
"Content-Type": "application/json",
'Authorization': f'Bearer {token}'
}

#payload for create device models
payload = {
    "onuModel":{
  "modelName": "TESTONU00012",
  "vendorName": "ALCATEL",
  "modelDesc": {
    "deviceTypeName": "onu",
    "deviceType": {
      "docsisVersion": "3.1"
    }
  },
  "status": "Test",
  "metadata": {
    "contextId": "QA01",
    "referenceId": ref_id,
    "externalId": ext_id,
    "userId": "P3205066"
  }
},
    "mtaModel":{
  "modelName": "TESTMTA00012",
  "vendorName": "Technicolor",
  "modelDesc": {
    "deviceTypeName": "mta",
    "deviceType": {
      "docsisVersion": "3.1"
    }
  },
  "status": "Test",
  "metadata": {
    "contextId": "QA01",
    "referenceId": ref_id,
    "externalId": ext_id,
    "userId": "P3205066"
  }
}
}
#Calling the Create, GET models, GET model info APIS
for models in payload.values():
    #constructing the API urls
    getModel_info_URL = getModel_url + str(models["modelName"]) + "?" + "referenceId=" + ref_id
    delete_model_url = getModel_url + str(models["modelName"]) + "?referenceId=" + ref_id + "&userId=P3205066"
    #getAllMatchedModels_URL = url + "?vendor=" + str(models["vendorName"]) + "&status" + str(models["status"]) + "&device_type=" + str(models["deviceTypeName"]) + "&referenceId=" + ref_id
    #Create model function call
    logging.info("Starting the test case execution to create the model " + models["modelName"])
    create_model(url,models,headers)
    logging.info("Completed the test case execution to create the model " + models["modelName"])
    logging.info("-----------------------------------------------------------")
    time.sleep(1)
    # Get model info function call
    logging.info("Starting the test case execution for Get model "+ models["modelName"])
    get_model_info(getModel_info_URL,headers,models)
    logging.info("Completed the test case execution for get the model " + models["modelName"])
    logging.info("-----------------------------------------------------------")
    time.sleep(1)
    # Get All matched models function call
    #logging.info("Starting the test case execution of Get all matched models for " + models["modelName"])
    #get_model_info(getModel_info_URL, headers, models)
    #logging.info("Completed the test case execution of Get all matched models for " + models["modelName"])
    #logging.info("-----------------------------------------------------------")
    #time.sleep(1)
    # Delete model info function call
    logging.info("Starting the test case execution for Delete model "+ models["modelName"])
    delete_model(delete_model_url,headers)
    logging.info("Completed the test case execution for Delete  model " + models["modelName"])
    logging.info("-----------------------------------------------------------")
    time.sleep(1)
    logging.info("Starting the test case execution for Get model after delete "+ models["modelName"])
    get_model_info(getModel_info_URL,headers,models)
    logging.info("Test case passed")
    logging.info("Completed the test case execution for get the model after delete " + models["modelName"])
    logging.info("-----------------------------------------------------------")
    time.sleep(1)
    logging.info("Starting the test case execution for Delete model after delete "+ models["modelName"])
    delete_model(delete_model_url,headers)
    logging.info("Test case passed")
    logging.info("Completed the test case execution for Delete  model after delete " + models["modelName"])
    logging.info("-----------------------------------------------------------")
    time.sleep(1)
end_time = time.time()
total_time = end_time - start_time
print(f"Execution Time: {total_time: .4f} in seconds")






