import csv
import time
from google.cloud import pubsub_v1
import os

serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

topic = 'projects/beam-dataflow-376917/topics/flights-topic'

publisher = pubsub_v1.PublisherClient()

input = '/Users/jalvi/Desktop/github-personal/GCP_Miscellaneous/beam-dataflow/local_gcp/flights.csv'

with open(input, 'rb') as file:
    for row in file:
        print('Publishing in a Topic')
        publisher.publish(topic, row)
        time.sleep(2)