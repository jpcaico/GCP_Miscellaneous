import apache_beam as beam

p1 = beam.Pipeline()

flights = (
p1 
| "Import data" >> beam.io.ReadFromText("flights.csv", skip_header_lines = 1)
| "Separate Commas" >> beam.Map(lambda record: record.split(','))
# | "Show results" >> beam.Map(print)
| "Save results" >> beam.io.WriteToText("flights.txt")

)

# Run Pipeline
p1.run()

