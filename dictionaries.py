from datetime import datetime
import deepdiff
ref_id = "TestModel" + str(datetime.now().second)
ext_id = "TestModel" + str(datetime.now().second)
payload = {
    "onuModel":{
  "modelName": "ONUTEST04",
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
  "modelName": "TESTMTA04",
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

for models in payload.values():
    def extract_keys(original_dict, keys_to_extract):
        # Use dictionary comprehension to extract the desired keys
        expected_response = {key: original_dict[key] for key in keys_to_extract if key in original_dict}
        return expected_response


    # Example usage

    keys_to_extract = ['modelName', 'vendorName', 'modelDesc', 'status']
    payload_new = extract_keys(models, keys_to_extract)
    devictype_extracted = payload_new.get('modelDesc',{}).get('deviceTypeName')
    print(devictype_extracted)
