import csv
import time
from google.cloud import pubsub_v1
import os

serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

subscription = 'projects/beam-dataflow-376917/subscriptions/flights_subscription'
subscriber = pubsub_v1.SubscriberClient()

def show_messages(message):
    print(f'Message {message}')
    message.ack()

subscriber.subscribe(subscription, callback=show_messages)

while True:
    time.sleep(3)