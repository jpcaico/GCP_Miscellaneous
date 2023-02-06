# Map and FlatMap are two transform operations in Apache Beam.

# Map operation applies a function to each element in the input data and returns an output collection for each input element.
#  The size of the output collection can be different from the size of the input collection, but it will have the same number of elements in total.

# FlatMap operation applies a function to each element in the input data and returns a single output element for each input element.
# The output elements are then concatenated into a single collection, which is the output of the FlatMap operation.
#  The size of the output collection will be less than or equal to the size of the input collection.

# In summary, Map can change the number of elements in the collection while preserving their count, while FlatMap can change both the number and the count of elements in the collection.

import apache_beam as beam

## Map
p1 = beam.Pipeline()

flights = (
p1 
| "Import data" >> beam.io.ReadFromText("flights.csv", skip_header_lines = 1)
| "Separate Commas" >> beam.Map(lambda record: record.split(','))
| "Show results" >> beam.Map(print)

)

# Run Pipeline
p1.run()


## flatmap

p2 = beam.Pipeline()

poem = (

p2 | "Import data" >> beam.io.ReadFromText("poem.txt", skip_header_lines = 1)
| "Apply FlatMap" >> beam.FlatMap(lambda record: record.split(' '))
| "Save Results" >> beam.io.WriteToText("results.txt")

)

p2.run()