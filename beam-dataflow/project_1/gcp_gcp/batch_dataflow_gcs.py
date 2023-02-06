
import apache_beam as beam
import os
from apache_beam.options.pipeline_options import PipelineOptions

pipeline_options = {

'project': 'beam-dataflow-376917',
'runner': 'DataflowRunner',
'region':'us-east1',
'staging_location': 'gs://beam-dataflow-jpcaico/temp',
'temp_location':'gs://beam-dataflow-jpcaico/temp',
'template_location':'gs://beam-dataflow-jpcaico/template/batch_job'

}

pipeline_options = PipelineOptions.from_dictionary(pipeline_options)

p1 = beam.Pipeline(options=pipeline_options)

serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

class filterFn(beam.DoFn):
    def process(self, record):
        if int(record[8]) > 0:
            return [record]

time_delay = (

p1
| "Import data time delay" >> beam.io.ReadFromText(r"gs://beam-dataflow-jpcaico/input/flights.csv", skip_header_lines = 1)
| "Separate Commas time delay" >> beam.Map(lambda record: record.split(','))
| "Delayed flights time delay" >> beam.ParDo(filterFn())
| "Create Pair delay" >> beam.Map(lambda record: (record[4], int(record[8])))
| "Sum per key" >> beam.CombinePerKey(sum)
# | "Show results" >> beam.Map(print)

)


delay_qty = (

p1
| "Import data delay qty" >> beam.io.ReadFromText(r"gs://beam-dataflow-jpcaico/input/flights.csv", skip_header_lines = 1)
| "Separate Commas delay qty" >> beam.Map(lambda record: record.split(','))
| "Delayed flights qty" >> beam.ParDo(filterFn())
| "Create Pair qty" >> beam.Map(lambda record: (record[4], int(record[8])))
| "Count per key" >> beam.combiners.Count.PerKey()
# | "Show results" >> beam.Map(print)

)

delay_table = (

{'Delay Quantity': delay_qty, 'Time Delay': time_delay}
| "Group by" >> beam.CoGroupByKey()
| "Save to gcs" >> beam.io.WriteToText(r"gs://beam-dataflow-jpcaico/output/delayed_flights.csv")

)

p1.run()