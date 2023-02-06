import apache_beam as beam

p1 = beam.Pipeline()

flights = (
p1 
| "Import data" >> beam.io.ReadFromText("flights.csv", skip_header_lines = 1)
| "Separate Commas" >> beam.Map(lambda record: record.split(','))
| "Show results" >> beam.Map(print)

)

# Run Pipeline
p1.run()


p2 = beam.Pipeline()

p2 | "List" >> beam.Create( [1,2,3]) | "Print List" >> beam.Map(print)

p2.run()
