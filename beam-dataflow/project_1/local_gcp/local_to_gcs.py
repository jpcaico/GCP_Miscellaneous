
import apache_beam as beam
import os


serviceAccount = '/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = serviceAccount

p1 = beam.Pipeline()

time_delay = (

p1
| "Import data time delay" >> beam.io.ReadFromText("flights.csv", skip_header_lines = 1)
| "Separate Commas time delay" >> beam.Map(lambda record: record.split(','))
| "Delayed flights time delay" >> beam.Filter(lambda record: int(record[8]) > 0)
| "Create Pair delay" >> beam.Map(lambda record: (record[4], int(record[8])))
| "Sum per key" >> beam.CombinePerKey(sum)
# | "Show results" >> beam.Map(print)

)


delay_qty = (

p1
| "Import data delay qty" >> beam.io.ReadFromText("flights.csv", skip_header_lines = 1)
| "Separate Commas delay qty" >> beam.Map(lambda record: record.split(','))
| "Delayed flights qty" >> beam.Filter(lambda record: int(record[8]) > 0)
| "Create Pair qty" >> beam.Map(lambda record: (record[4], int(record[8])))
| "Count per key" >> beam.combiners.Count.PerKey()
# | "Show results" >> beam.Map(print)

)

delay_table = (

{'Delay Quantity': delay_qty, 'Time Delay': time_delay}
| "Group by" >> beam.CoGroupByKey()
| "Save to gcs" >> beam.io.WriteToText('gs://beam-dataflow-jpcaico/delayed_flights.csv')

)

p1.run()