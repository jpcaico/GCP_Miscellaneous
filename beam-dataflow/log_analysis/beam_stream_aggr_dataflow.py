import apache_beam as beam
import os
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
import json
from apache_beam.transforms import window

serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

INPUT_SUBSCRITION = "projects/beam-dataflow-376917/subscriptions/log-topic-sub"
OUTPUT_TABLE = "beam-dataflow-376917:logs_datasets.logs_data_streaming_summary"

class BuildRecordFn(beam.DoFn):
    def process(self, element,  window=beam.DoFn.WindowParam):
        window_start = window.start.to_utc_datetime().isoformat()
        return [element + (window_start,)]


beam_options_dict = {
'project': 'beam-dataflow-376917',
'runner':'DataflowRunner',
'region':'us-east1',
'temp_location':'gs://beam-dataflow-jpcaico/temp',
'job_name': 'log-job-streaming-aggr',
'streaming': True
}

beam_options = PipelineOptions.from_dictionary(beam_options_dict)


if __name__ == '__main__':

    with beam.Pipeline(options=beam_options) as p: (

        p | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(subscription=INPUT_SUBSCRITION)
        | 'Decode' >> beam.Map(lambda x: x.decode('utf-8'))
        | 'Parse JSON' >> beam.Map(json.loads)
        | 'FixedWindow' >> beam.WindowInto(beam.window.FixedWindows(120))
        | 'Group By Log Level' >> beam.Map(lambda elem: (elem['log_level'], 1))
        | 'Sum' >> beam.CombinePerKey(sum)
        | 'Add time window' >> beam.ParDo(BuildRecordFn())
       | 'Parse to JSON' >> beam.Map(lambda x : {'log_level': x[0],'count_occurrences':x[1],'window_snapshot':x[2]})
       | 'Write to Table' >> beam.io.WriteToBigQuery(OUTPUT_TABLE,
                        schema='log_level:STRING,count_occurrences:INTEGER,window_snapshot:TIMESTAMP',
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)

    )
    
    p.run()