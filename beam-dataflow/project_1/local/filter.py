import apache_beam as beam

p1 = beam.Pipeline()

flights = (
p1 
| "Import data" >> beam.io.ReadFromText("flights.csv", skip_header_lines = 1)
| "Separate Commas" >> beam.Map(lambda record: record.split(','))
| "LA flights" >> beam.Filter(lambda record: record[3] == "LAX")
| "Show results" >> beam.Map(print)

)

# Run Pipeline
p1.run()


#### Using function

words = ['quatro', 'um']

def findWords(i):
    if i in words:
        return True

p2 = beam.Pipeline()

poem = (

p2 | "Import data" >> beam.io.ReadFromText("poem.txt", skip_header_lines = 1)
| "Apply FlatMap" >> beam.FlatMap(lambda record: record.split(' '))
| "Filter Words" >> beam.Filter(findWords)
| "Save Results" >> beam.io.WriteToText("results_filtered.txt")

)

p2.run()