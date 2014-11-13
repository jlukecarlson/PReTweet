import csv, sys
from itertools import islice

filename = "input.csv"
reader = csv.reader(open('../data/' + filename, 'r'))

# skip header
next(reader,None)


# key -> tweet
# value -> is a dict of humor, approate, grammer. each of [total score, number of scorings]
tweets = {}

try:
    for row in reader:
        tweet = row[4];
        if tweet in tweets:
            values = tweets[tweet]
            tweets[tweet]["humor"] = [values["humor"][0] + int(row[1]),
                                      values["humor"][1] + 1]
            tweets[tweet]["appropriate"] = [values["appropriate"][0] + int(row[2]), 
                                            values["appropriate"][1] + 1]
            tweets[tweet]["grammar"] = [values["grammar"][0] + int(row[3]), 
                                        values["grammar"][1] + 1]            
        else:
            # initialize the value as a dict of each label with [total score, # scores]
            inner_dict = {"humor": [int(row[1]), 1], 
                          "appropriate": [int(row[2]), 1], 
                          "grammar": [int(row[3]), 1]}
            tweets[tweet] = inner_dict

except csv.Error as e:
      sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


tweet_key_file = open ('../data/tweet_keys.txt','w')
tweet_key_file.write("This file matches tweets to their IDs.\nEach tweet is assigned a specific ID because putting the entire tweet in output files could mess up the format.\n")
tweet_key_file.write("ID \t tweet\n")
# counter for ID values
ID = 1000
for tweet, v in tweets.iteritems():
    tweet_key_file.write('#' + str(ID) + '\t' + tweet + '\n')
    ID += 1

labels_file = open('../data/labels.csv','w')
labels_file.write("tweet ID , humor , appropriateness , grammar\n")
ID = 1000
for tweet, values in tweets.iteritems():
    # convert each [total score, # scores] into average score
    humor = values["humor"][0] / values["humor"][1]
    appropriate = values["appropriate"][0] / values["appropriate"][1]
    grammar = values["grammar"][0] / values["grammar"][1]
    line = '#' + str(ID) + ',' + str(humor) + ',' + str(appropriate) + ',' + str(grammar) + '\n' 
    labels_file.write(line)
    # we keep track of tweet IDS
    ID +=1
    print line
