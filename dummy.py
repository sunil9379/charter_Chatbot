import requests
import json
import sample
import logging
from datetime import datetime
import example
import time
start_time = time.time()

model = sample.model_name
referenceId = str(datetime.now())
Log_File_Name = "UpdateModelLogs_" + str(datetime.now().second)


logging.basicConfig(
        filename=Log_File_Name,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


API_URL = sample.PUT_URL
# Define the API endpoint
url = API_URL + model + "?" + "status=Certified"
token = sample.bearer_token
payload = example.data
# Optional: Define headers if needed (e.g., for authentication)
headers = {
'Authorization': f'Bearer {token}'
}


# Send the GET request
response = requests.put(url, json=payload, headers=headers, verify=False)
logging.info("Successfully executed the PUT API")

# Check the status code and print the response
if response.status_code == 201:
    response_msg = str((json.loads(response.text)))
    if "updated device" in response_msg:
        print("test case is passed for onu model")
        logging.info("Success response received")
        logging.info(response.json())
        logging.info(response.status_code)
    else:
        print("Test Case is failed")
        logging.error("One or more attributes are not matching")
        logging.error("Test case is failed")

    logging.info(f'response code:{response.status_code}')
    print(response.json())  # or response.text for raw output
    logging.info(response.json())


else:
    print(f"Failed with status code: {response.status_code}")
    print(response.text)
    logging.error(f'Failed with Status code: {response.status_code}')
    logging.error(response.json())
    logging.info(response.url)

for i in range(1000000):
    _ = i * i

# End the timer
end_time = time.time()

total_time = end_time - start_time
print(f"Total execution time: {total_time:.6f} seconds")



