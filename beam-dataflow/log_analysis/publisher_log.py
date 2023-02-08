
import time
from google.cloud import pubsub_v1
from generate_logs import random_log_entry
import json
import os

serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

topic = 'projects/beam-dataflow-376917/topics/log-topic'

publisher = pubsub_v1.PublisherClient()


while True:
        print('Generating Log: ')
        log = random_log_entry()
        message = json.dumps(log)
        print(message)
        publisher.publish(topic, message.encode("utf-8"))
        print('Message published.')
        time.sleep(2)