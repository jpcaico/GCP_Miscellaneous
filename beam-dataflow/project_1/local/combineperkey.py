# CombinePerKey is a transform operation in Apache Beam that aggregates the values associated with each key in a PCollection
#  of key-value pairs. The input PCollection is partitioned by key, and for each partition, the values associated with each key
#  are aggregated using a user-defined CombineFn. The CombineFn takes as input the values associated with a single key and returns 
# a single output value, which represents the aggregated result for that key.

# CombinePerKey is useful for reducing the size of data that is to be processed in a pipeline.
#  It allows you to perform some initial processing on each partition of data, before sending it on to the next stage of processing.
#  This can result in significant performance improvements, as the amount of data that needs to be processed in subsequent stages is
#  smaller.

# For example, you could use CombinePerKey to perform a sum operation on a PCollection of key-value pairs, where the keys represent
#  different categories, and the values represent amounts. The CombinePerKey transform would produce a new PCollection where each key
#  is associated with the sum of the values associated with that key in the input PCollection.

import apache_beam as beam

p1 = beam.Pipeline()

time_delay = (

p1
| "Import data" >> beam.io.ReadFromText("flights.csv", skip_header_lines = 1)
| "Separate Commas" >> beam.Map(lambda record: record.split(','))
| "LA departures" >> beam.Filter(lambda record: int(record[8]) > 0)
| "Create Pair" >> beam.Map(lambda record: (record[4], int(record[8])))
| "Sum per key" >> beam.CombinePerKey(sum)
| "Show results" >> beam.Map(print)

)

p1.run()