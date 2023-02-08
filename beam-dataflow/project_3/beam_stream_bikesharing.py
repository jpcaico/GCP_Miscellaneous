import apache_beam as beam
# import os
import argparse
import logging
from apache_beam.transforms.combiners import Sample
from apache_beam.options.pipeline_options import PipelineOptions
import json

# A. Reading data from gcs
# Sampling 10 records
# Printing the records as logs

# read data from a gcs file and write the output back to gcs
# serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

INPUT_SUBSCRITION = "projects/beam-dataflow-376917/subscriptions/bike-sharing-trips-subs-1"
OUTPUT_TABLE = "beam-dataflow-376917:raw_bikesharing.bike_trips_streaming"

# use args if running in cloud shell environment with argument parser

parser = argparse.ArgumentParser()
args, beam_args = parser.parse_known_args()


beam_options_dict = {
'project': 'beam-dataflow-376917',
'runner': 'DirectRunner',
'region':'us-east1',
#'staging_location': 'gs://beam-dataflow-jpcaico/temp',
'temp_location':'gs://beam-dataflow-jpcaico/temp',
#'template_location':'gs://beam-dataflow-jpcaico/template/batch_job',
'job_name': 'log-job-streaming',
'streaming': True
}

beam_options = PipelineOptions.from_dictionary(beam_options_dict)

#beam_options = PipelineOptions(beam_args)

if __name__ == '__main__':
    #logging.getLogger().setLevel(logging.INFO)
    with beam.Pipeline(options=beam_options) as p: (

         p | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(subscription=INPUT_SUBSCRITION)
        | 'Decode' >> beam.Map(lambda x: x.decode('utf-8'))
        | "Parse JSON" >> beam.Map(json.loads)
        | 'Write to Table' >> beam.io.WriteToBigQuery(OUTPUT_TABLE,

            schema='trip_id:STRING,start_date:TIMESTAMP,start_station_id:STRING,bike_number:STRING,duration_sec:INTEGER',
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))
    
    # result = p.run()
    # result.wait_until_finish()
    p.run()