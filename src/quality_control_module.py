


# Start off by filling tweets dictionary with output from other module
filename = "labels.csv"
reader = csv.reader(open('../data/' + filename, 'r'))

# skip header
next(reader,None)
