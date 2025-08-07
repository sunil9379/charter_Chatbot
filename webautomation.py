# Importing the required libraries
import requests
import json
import logging
from datetime import datetime
# Code snippet for creating a log file
logging.basicConfig(
filename='CreateModels.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define the API endpoint and other details
url = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkZXZpY2VvcGVkaWEtdG9rZW4gc2NyaXB0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiREVWSUNFT1BFRElBX2NsaWVudCIsInJvbGVzIjpbIlNEX0NBVEFMT0dfQURNSU4iLCJTRF9GQVNfQURNSU4iLCJTRF9SRFVfQURNSU4iLCJTRF9NT05HT19BRE1JTiIsIlNEX1NVUEVSQURNSU4iXSwibmFtZSI6Im1lIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWUiLCJnaXZlbl9uYW1lIjoibWUiLCJmYW1pbHlfbmFtZSI6Im1lIn0.9zVJY_R1HY-4OfL25loOAd_OS_E5su7nAgXCtmXONqA"
payload = {
  "modelName": "ABE-040G-B1234AB1234",
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
    "referenceId": str(datetime.now()),
    "externalId": "Test" + str(datetime.now()),
    "userId": "P3205066"
  }
}


# Optional: Define headers if needed (e.g., for authentication)
headers = {
"Content-Type": "application/json",
'Authorization': f'Bearer {token}'
}

# Executing the POST API and logging messages upon success in th elog file
response = requests.post(url, json=payload, headers=headers, verify=False)
logging.info("Successfully executed the POST API")
logging.info(payload)

# Check and validating if the required response is rendered and logging the same in log file
if response.status_code == 201:
    response_msg = str((json.loads(response.text))["detail"])
    if "created document with id" in response_msg:
        print("Test Case is passed")
        logging.info("Successfully created the model")
        logging.info("Test case is passed")
    print("Success!")
    print(response.json())  # or response.text for raw output
    logging.info(response.status_code)

else:
    print(f"Failed with status code: {response.status_code}")
    print(response.json())
    logging.info(response.json())
    logging.info(response.status_code)


