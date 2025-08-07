import datetime
import time
from operator import indexOf

from kafka import KafkaConsumer
import json
#from Phase_1.delete_device import delete_devices

def read_kafka(topic,model_name):
    start_time = time.time()
    print("Reading Kafka Topic")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="kafk-ctec-a04t.enwd.co.sa.charterlab.com:9092",
        auto_offset_reset='earliest',
        consumer_timeout_ms=10000,
    )
    absent = False
    present = False


    for message in consumer:

        #if time.time() - start_time > 120:
        #    print("Breaking, 2 mins elapsed")
        #    break

        if message.value==None:
            continue

        try:


            my_json = message.value.decode('utf-8',errors='ignore')
            index_my_json = my_json.index('{')
            my_json = my_json[index_my_json:]
            my_json = json.loads(my_json)

            #print("Type: ",type(message.key))
            print("Key: ",message.key)
            my_key = message.key.decode('utf-8',errors='ignore')

            #my_json = message.key
            #print("key: ", my_json)
            #print(my_json)
            print(type(my_key))
            #'''
            #models = []
            #models.append(my_json['modelName'])

            keys = []
            keys.append(my_key)

            if model_name in keys:
                #print(f"kafka message published for {model_name}")
                present = True
                break
            else:
                absent = True
            #'''
        except Exception as e:
            continue

    return present
