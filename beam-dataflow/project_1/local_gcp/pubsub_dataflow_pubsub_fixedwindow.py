import apache_beam as beam
import os
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms import window

pipeline_options = {

'project': 'beam-dataflow-376917',
'runner': 'DataflowRunner',
'region':'us-east1',
'staging_location': 'gs://beam-dataflow-jpcaico/temp',
'temp_location':'gs://beam-dataflow-jpcaico/temp',
'template_location':'gs://beam-dataflow-jpcaico/template/streaming_fixed',
'save_main_session': True,
'streaming': True
}

pipeline_options = PipelineOptions.from_dictionary(pipeline_options)

p1 = beam.Pipeline(options=pipeline_options)

serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

subscription = 'projects/beam-dataflow-376917/subscriptions/flights_subscription'
#create a new topic
output = 'projects/beam-dataflow-376917/topics/flights_output'


class split_lines(beam.DoFn):
  def process(self,record):
    return [record.decode("utf-8").split(',')]

class filterFn(beam.DoFn):
    def process(self, record):
        if int(record[8]) > 0:
            return [record]

pcollection_input = (

p1 | 'Read from pubsub topic' >> beam.io.ReadFromPubSub(subscription=subscription)

)


time_delay = (

pcollection_input
| "Separate Commas time delay" >> beam.ParDo(split_lines())
| "Delayed flights time delay" >> beam.ParDo(filterFn())
| "Create Pair delay" >> beam.Map(lambda record: (record[4], int(record[8])))
| "Window" >> beam.WindowInto(window.FixedWindows(5))
| "Sum per key" >> beam.CombinePerKey(sum)
# | "Show results" >> beam.Map(print)

)


delay_qty = (

pcollection_input
| "Separate Commas delay qty" >> beam.ParDo(split_lines())
| "Delayed flights qty" >> beam.ParDo(filterFn())
| "Create Pair qty" >> beam.Map(lambda record: (record[4], int(record[8])))
| "Window qty" >> beam.WindowInto(window.FixedWindows(5))
| "Count per key" >> beam.combiners.Count.PerKey()
# | "Show results" >> beam.Map(print)

)

delay_table = (

{'qty_delay': delay_qty, 'delay_time': time_delay}
| beam.CoGroupByKey()
| 'Converting to byte string' >> beam.Map(lambda row: (''.join(str(row)).encode('utf-8')) )
| "Write to topic" >> beam.io.WriteToPubSub(output)
)

result = p1.run()
result.wait_until_finish()