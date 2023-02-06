# The Flatten transform in Apache Beam takes a collection of collections as input and returns a single collection that contains all
# the elements from the input collections.

# For example, if you have a collection of collections, each containing elements of different types, the Flatten transform will
# take all these collections and return a single collection that contains elements of all the different types, in the order in which
# they were originally present in the input collections.

# The Flatten transform is often used in Apache Beam pipelines to merge collections of elements produced by different transforms
#  into a single collection. This can be useful when the output of one transform needs to be used as input to another transform,
#   or when the output of multiple transforms needs to be combined into a single collection for further processing.

import apache_beam as beam

p = beam.Pipeline()

black = ('Lamar', 'Martin', 'Chris')
white = ('Jay', 'Ariana', 'Paul')
native_american = ('Elu', 'Dakota', 'Mika')

black_pc = p | "Creating black Pcollection" >> beam.Create(black)
white_pc = p | "Creating white Pcollection" >> beam.Create(white)
native_pc = p | "Creating native Pcollection" >> beam.Create(native_american)

people = ((black_pc, white_pc, native_pc) | beam.Flatten()) | beam.Map(print)

p.run()