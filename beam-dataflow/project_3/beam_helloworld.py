import apache_beam as beam
# import os
import argparse
import logging
from apache_beam.transforms.combiners import Sample
from apache_beam.options.pipeline_options import PipelineOptions

# A. Reading data from gcs
# Sampling 10 records
# Printing the records as logs

# read data from a gcs file and write the output back to gcs
# serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

INPUT_FILE = "gs://beam-dataflow-jpcaico/dataset/logs_example.txt"
OUTPUT_PATH = "gs://beam-dataflow-jpcaico/output/"

# use args if running in cloud shell environment with argument parser

parser = argparse.ArgumentParser()
args, beam_args = parser.parse_known_args()


beam_options_dict = {
'project': 'beam-dataflow-376917',
'runner': 'DataflowRunner',
'region':'us-east1',
#'staging_location': 'gs://beam-dataflow-jpcaico/temp',
'temp_location':'gs://beam-dataflow-jpcaico/temp',
#'template_location':'gs://beam-dataflow-jpcaico/template/batch_job',
'job_name': 'log-job-script'}

beam_options = PipelineOptions.from_dictionary(beam_options_dict)


#beam_options = PipelineOptions(beam_args)


#The key difference between ParDo and the Map function in Beam is that Map
#  always returns one row at a time, while ParDo is more flexible—it can return one to many rows per process

def split_map(records):
    rows = records.split(" ")
    return {

        'ip': str(rows[0]),
        'date': str(rows[3]),
        'method': str(rows[5]),
        'url': str(rows[6])
    }

class Split(beam.DoFn):
    def process(self, element):
        rows = element.split(" ")
        return [
                {

        'ip': str(rows[0]),
        'date': str(rows[3]),
        'method': str(rows[5]),
        'url': str(rows[6])
    }]


if __name__ == '__main__':
    #logging.getLogger().setLevel(logging.INFO)
    with beam.Pipeline(options=beam_options) as p: (
        p
        | 'Read' >> beam.io.ReadFromText(INPUT_FILE)
        #| 'Split' >> beam.Map(split_map)
        | 'Split' >> beam.ParDo(Split()) 
        | 'Get URL' >> beam.Map(lambda s: (s['url'], 1))
        | 'Count per Key' >> beam.combiners.Count.PerKey() 
       # | 'Sample' >> Sample.FixedSizeGlobally(10)
       # | 'Print' >> beam.Map(print)
       | 'Write' >> beam.io.WriteToText(OUTPUT_PATH)
    )
    # result = p.run()
    # result.wait_until_finish()
    p.run()