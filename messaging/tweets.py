
import json
from celery import Celery
from config import celery 

def counter(word,dic):
	keys = dic.keys()
	for key in keys:
		if word==key:
			dic[key] +=1

@celery.task()
def tweets(tweet_file):
	dic = {'han':0,'hon':0,'det':0,'den':0, 'denna':0,'denne':0,'hen':0}	
	
	#swiftUrl ="http://smog.uppmax.uu.se:8080/swift/v1/tweets/"+tweet_file			
	#for tweet in urllib2.urlopen(swiftUrl):
	with open(tweet_file, 'r') as f:
		tweet = f.readlines()
		for line in tweet:
			if not line=='\n':

				j = json.loads(line)
				if "retweeted_status" not in j:
					tweet_messages = j['text'].split()
					for word in tweet_messages:
						counter(word.lower(),dic)

  	return dic

        

