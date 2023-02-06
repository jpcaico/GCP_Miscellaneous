
import apache_beam as beam
import os
from apache_beam.options.pipeline_options import PipelineOptions

pipeline_options = {

'project': 'beam-dataflow-376917',
'runner': 'DataflowRunner',
'region':'us-east1',
'staging_location': 'gs://beam-dataflow-jpcaico/temp',
'temp_location':'gs://beam-dataflow-jpcaico/temp',
'template_location':'gs://beam-dataflow-jpcaico/template/batch_job_bigquery',
'save_main_session': True

}

pipeline_options = PipelineOptions.from_dictionary(pipeline_options)

p1 = beam.Pipeline(options=pipeline_options)

serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

class filterFn(beam.DoFn):
    def process(self, record):
        if int(record[8]) > 0:
            return [record]

def create_dict_level1(record):
    dict_ = {} 
    dict_['airport'] = record[0]
    dict_['list'] = record[1]
    return(dict_)

def unnest_dict(record):
    def expand(key, value):
        if isinstance(value, dict):
            return [ (key + '_' + k, v) for k, v in unnest_dict(value).items() ]
        else:
            return [ (key, value) ]
    items = [ item for k, v in record.items() for item in expand(k, v) ]
    return dict(items)

def create_dict_level0(record):
    dict_ = {} 
    dict_['airport'] = record['airport']
    dict_['list_qty_delay'] = record['list_qty_delay'][0]
    dict_['list_delay_time'] = record['list_delay_time'][0]
    return(dict_)

table_schema = 'airport:STRING, list_qty_delay:INTEGER, list_delay_time:INTEGER'
table = 'beam-dataflow-376917.flights.table_flights'

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

{'qty_delay': delay_qty, 'delay_time': time_delay}
| beam.CoGroupByKey()
| beam.Map(lambda record: create_dict_level1(record))
| beam.Map(lambda record: unnest_dict(record))
| beam.Map(lambda record: create_dict_level0(record))
| beam.io.WriteToBigQuery(
    table,
    schema= table_schema,
    write_disposition= beam.io.BigQueryDisposition.WRITE_APPEND,
    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
    custom_gcs_temp_location='gs://beam-dataflow-jpcaico/temp'
)

)

p1.run()