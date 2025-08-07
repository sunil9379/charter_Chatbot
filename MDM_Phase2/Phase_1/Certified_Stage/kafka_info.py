import datetime
from operator import indexOf

from kafka import KafkaConsumer
import json

def read_kafka(topic):
    start_time = datetime.datetime.now()
    print("Reading Kafka Topic")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="kafk-ctec-a04t.enwd.co.sa.charterlab.com:9092",
        auto_offset_reset='earliest'
    )
    absent = False
    present = False
    for message in consumer:

        if message.value is None:
            continue

        try:
            my_json = message.value.decode('utf-8',errors='ignore')
            index_my_json = my_json.index('{')
            my_json = my_json[index_my_json:]
            #my_json = message.value
            #print(my_json)
            my_json = json.loads(my_json)
            #print(type(my_json))

            '''
            models = []
            models.append(my_json['modelName'])

            if model_name in models:
                print(f"kafka message published for {model_name}")
                present = True
                break
            else:
                absent = True
                #print(f"{model_name} is not present in the imported devices")
            '''
        except Exception as e:
            continue
    #if absent:
    #    print("message not published")
    return my_json,present