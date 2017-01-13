#Importing libraries
import urllib
import os
import json
import tweepy

#Configuring Twitter account
def get_api(cfg):
	auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
	auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
	return tweepy.API(auth)

#Sending tweet
def tweeter(message):
  #Obviously, you must change the credentials
	cfg = { 
	    "consumer_key"        : "",
	    "consumer_secret"     : "",
	    "access_token"        : "",
	    "access_token_secret" : "" 
	    }

	api = get_api(cfg)
	tweet = message
	status = api.update_status(status=tweet) 




#Renaming the old file and importing data
print "Renaming old files"
os.rename('new.json','old.json')
#Fetching the new file and importing data
print "Fetching new data"
testfile = urllib.URLopener()
testfile.retrieve("https://3718fa66e6.optimicdn.com/alert_list.txt", "new.json")
print "Trying to compare the two"

with open('old.json') as old_file:    
    old_data = json.load(old_file)
with open('new.json') as new_file:    
    new_data = json.load(new_file)

old_id=str(old_data["alerts"][0]["id"])
new_id=str(new_data["alerts"][0]["id"])
	
if (new_id!=old_id):
	title=new_data["alerts"][0]["title"]
	url=new_data["alerts"][0]["share_urls"]["fr"]
	comm=str(title)[0:114]+" "+str(url)
	print comm
	tweeter(comm)
else:
	print "Nothing new, all seems fine"
