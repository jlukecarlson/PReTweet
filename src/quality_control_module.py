import sys, csv


# first we get tweet ID to tweet value mappings
filename = "tweet_keys.txt"
reader = csv.reader(open('../data/' + filename, 'r'))

# skip header and info
next(reader,None)
next(reader,None)
next(reader,None)

ID_to_tweet = {'#1000': "Benedict Cumberbatch got engaged! I hope I get invited to his Cumberbatchelor party.", '#1001': "Family Believes Missing Engineers Body Was Found In San Francisco Bay http://tcrn.ch/1tIweL7 by @sarahbuhr"}

# Right now we are deciding how to label by ID so we will comment this out
#try:
#    for row in reader:
#        ID_to_tweet[row[0]] = row[1]
#except csv.Error as e:
#      sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))



# Now fill tweets dictionary with output from other module
filename = "labels.csv"
reader = csv.reader(open('../data/' + filename, 'r'))

# skip header and info
next(reader,None)


labels = {}
try:
    for row in reader:
        tweet_text = ID_to_tweet[row[0]]
        inner_dict = {"humor": int(row[1]), 
                      "appropriate": int(row[2]), 
                      "grammar": int(row[3])}

        labels[tweet_text] = inner_dict
except csv.Error as e:
      sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))



filename = "input.csv"
reader = csv.reader(open('../data/' + filename, 'r'))

# skip header and info
next(reader,None)

# key -> worker name
# value ->  is a two d array of [[url, opinion]..[]] 
workers = {}
try:
    for row in reader:
        name = row[0]
        inner_dict = {"humor": int(row[1]), 
                      "appropriate": int(row[2]), 
                      "grammar": int(row[3])}
        if name in workers:
            workers[name].append([row[4],inner_dict])
        else:
            # [tweet_text, labels]
            workers[name] = [[row[4], inner_dict]]

except csv.Error as e:
      sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

# we now have information on every label submitted by a worker

# qualities[wi] = (1 / |tweets[wi]|) * sigma tweets[wi] -> (|lui - labels[u]|)
qualities = {}

for worker, opinions in workers.iteritems():
    # example opinion : [['Benedict Cumberbatch got engaged! I hope I get invited to his Cumberbatchelor party.', {'grammar': 1, 'appropriate': 4, 'humor': 1}], ['Family Believes Missing Engineers Body Was Found In San Francisco Bay http://tcrn.ch/1tIweL7 by @sarahbuhr', {'grammar': 4, 'appropriate': 1, 'humor': 1}]]

    sigma = 0.0
    for opinion in opinions:
        tweet = opinion[0]
        values = opinion[1]
        difference = 0
        difference += abs(labels[tweet]["humor"] - values["humor"])
        difference += abs(labels[tweet]["appropriate"] - values["appropriate"])
        difference += abs(labels[tweet]["grammar"] - values["grammar"])
        # 15 is the total # of points. Worst score is a difference of 15, best is difference of 0
        # we divide by total to get a decimal between 0 and 1
        difference = float(difference) / 15.0
        # since we are basing this on the difference, we want to switch it such that 1 is best and 0 is worst
        sigma += 1.0 - difference
    qualities[worker] = sigma / float(len(opinions))


# qualities is now full so we can output it as a file
# if we did not need to manipulate qualities we could
# just write to the file in the above loop to reduce run time

f = open('../data/worker_quality.csv','w')
f.write("name, quality\n")
for k, v in qualities.iteritems():
    f.write(k + ',' + str(v) + '\n')
f.close()
