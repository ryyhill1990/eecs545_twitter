The interesting file here is raw_datapoints.txt. Each line has the following format:

term-index term-index ... #tag #tag #tag ...

There are 9697 different terms, so the resulting x-vector is a 9697-dimensional vector for which each dimension has been incremented some number of times. We need to use PCA (or possibly some other technique?) to reduce the dimensionality of that data, and then write that back to a file. I'm guessing that the resulting file, instead of listing all the dimensions that have been incremented like the original list, will just list the value of each dimension in the x-vector.
