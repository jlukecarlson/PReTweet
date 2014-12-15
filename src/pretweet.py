import crowdflower
import json
from time import sleep
from crowdflower.exception import CrowdFlowerError
from twilio.rest import TwilioRestClient

account_sid = "ACa36da6a5d565bc3deba7a0a59569cf9d"
account_token = "d11f04ec25188d4b2f181229087b0fa4"
client = TwilioRestClient(account_sid, account_token)
sid_list = []

initial_messages = client.messages.list()
for initial_m in initial_messages :
	sid_list.append(initial_m.sid)

tweet = ""
user= ""
message_recieved = False
while not message_recieved:
	messages = client.messages.list()
	for m in messages:
		if m.sid not in sid_list and m.status == 'received' :
			print m.body
                        tweet = m.body
                        user = m.from_
			sid_list.append(m.sid)
                        message_recieved = True
                        break
                        

print "connecting to crowdflower"

conn = crowdflower.Connection(api_key='1tLCReEneiiKf2bTPyhz')

data = [
    {'id': '1', 'content': tweet,},
    {'id': '2', 'content': 'California cleans up after a powerful storm triggered mudslides, flooding and a small tornado: http://apne.ws/1yNr1dd'},
    {'id': '3', 'content': 'When you\'re a creationist, regular museums become Believe It Or Not museums.'},
]

job = conn.upload(data)

hit_in_cml = """
<h4>Read the text below paying close attention to detail:</h4>
<div class="well">
{{content}}</div>
<cml:radios label="How appropriate is this tweet?" name="appropriate" aggregation="agg" validates="required" gold="true" class="" instructions="Read the instructions for a more detailed description of each score.">
  <cml:radio label="5: Universally Appropriate" value="yes"/>
  <cml:radio label="4: Mostly Appropriate" value="no"/>
  <cml:radio label="3: Appropriate" value="non_english"/>
  <cml:radio label="2: Mildly Inappropriate" value="mildly inappropriate"/>
  <cml:radio label="1: Inappropriate" value="inappropriate"/>
</cml:radios>
<!-- Relevance question ends -->
<!-- Sentiment questions begin --> 
<cml:radios label="How funny is this tweet?" name="humor" instructions="Read the instructions for a more detailed description of each score." gold="true" class="" validates="required"> 
  <cml:radio label="5: Hilarious" value="hilarious"/> 
  <cml:radio label="4: Funny" value="funny"/> 
  <cml:radio label="3: Indifferent" value="indifferent"/>
  <cml:radio label="2: Not funny" value="not funny"/>
  <cml:radio label="1: Really really not funny at all" value="really really not funny at all" id=""/> 
</cml:radios><cml:radios label="How correct are the grammar and spelling?" name="grammar" instructions="Read the instructions for a more detailed description of each score." gold="true" class="" validates="required" id=""> 
  <cml:radio label="5: No mistakes" value="no mistakes"/> 
  <cml:radio label="4: Barely noticeable" value="barely noticeable"/> 
  <cml:radio label="3: Intentional" value="intentional"/>
<cml:radio label="2: Poor" value="poor"/>
<cml:radio label="1: Distracting" value="distracting"/> 
</cml:radios>
<!-- Sentiment question ends -->"""



update_result = job.update({
    'title': 'Analyze Sentiments in Tweets',
    'included_countries': ['US', 'GB'],  # Limit to the USA and United Kingdom
        # Please note, if you are located in another country and you would like
        # to experiment with the sandbox (internal workers) then you also need
        # to add your own country. Otherwise your submissions as internal worker
        # will be rejected with Error 301 (low quality).
    'payment_cents': 10, # This is how much a contributor gets paid for each task or collection of units on a page.
    'judgments_per_unit': 2,
    'units_per_assignment':3, # This is the number of units that a contributor must complete on a page before submitting their answers. 
    'instructions': 'Please read the following tweet and rate the humor level, grammar, and expected audience',
    'cml': hit_in_cml,
    'options': {
        'front_load': 0, # quiz mode = 1; turn off with 0
    }
})
if 'errors' in update_result:
    print(update_result['errors'])
    exit()

job.launch(200, channels=['cf_internal'])

sleep(45) # give the job a moment to be uploaded

while(True):
    print job.ping()
    if job.properties['completed']:    
        print "hit completed"
        break;
    sleep(30)

responses = [] # holds each judgement
while(True):
    try:
        print job.properties['title']
        for judgment in job.judgments:
            responses.append(judgment);
        break
                    
    except:
        print "Please wait, CrowdFlower is parsing data"
        sleep(30);

print responses
results = []
for row in responses:
        if row['id'] == '1':
                results.append(row);

tempA = 0
tempH = 0
tempG = 0

count = 0
sumA = 0
sumH = 0
sumG = 0

def getAppropriateness (item) :
	s = item['appropriate']
	tempA = 0
	if s == "yes" :
		tempA = 5.0
	elif s == 'no' :
		tempA = 4.0
	elif s == 'non_english' :
		tempA = 3.0
	elif s == 'mildly inappropriate' :
		tempA = 2.0
	elif s == 'inappropriate' :
		tempA = 1.0
	return tempA

def getHumor (item) :
	s = item['humor']
	tempH = 0
	if s == "hilarious" :
		tempH = 5.0
	elif s == 'funny' :
		tempH = 4.0
	elif s == 'indifferent' :
		tempH = 3.0
	elif s == 'not funny' :
		tempH = 2.0
	elif s == 'really really not funny at all' :
		tempH = 1.0
	return tempH

def getGrammar (item) :
	s = item['grammar']
	tempG = 0
	if s == 'no mistakes' :
		tempG = 5.0
	elif s == 'barely noticeable' :
		tempG = 4.0
	elif s == 'intentional' :
		tempG = 3.0
	elif s == 'poor' :
		tempG = 2.0
	elif s == 'distracting' :
		tempG = 1.0
	return tempG

for record in results :
	sumA += getAppropriateness(record)
	sumH += getHumor(record)
	sumG += getGrammar(record)
	count += 1

avgA = sumA / count
avgH = sumH / count
avgG = sumG / count

print avgA
print avgH
print avgG

message_body = "Appropriateness Avg: {0}/5\nHumor Average: {1}/5\nGrammar Average: {2}/5".format(avgA,avgH,avgG)
new_message = client.messages.create(body=message_body, to=user, from_="+14705398873")
