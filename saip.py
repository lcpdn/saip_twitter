#Importing libraries
import urllib
import os
import json
import tweepy
import requests
import logging
import logging.handlers

def twitter_api():
	access_token = ""
	access_token_secret = ""
	consumer_key = ""
	consumer_secret = ""
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	return api


def tweet_image(url, message):
    api = twitter_api()
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        api.update_with_media(filename, status=message)
        os.remove(filename)
    else:
        print("Unable to download image")

def syslog_alert(message):
	my_logger = logging.getLogger('SAIP')
	my_logger.setLevel(logging.DEBUG)
	handler = logging.handlers.SysLogHandler('/dev/log')
	my_logger.addHandler(handler)
	my_logger.debug(message)


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

try:
        old_id=str(old_data["alerts"][-1]["id"])
except:
        print "Fail: no alert in this old file"
        old_id=0
try:
        new_id=str(new_data["alerts"][-1]["id"])
except:
        print "Fail: no alert in new file"
        new_id=0

n=-1
test=0
if ((new_id!=old_id)and(new_data["alerts"][n]["status"]=="ongoing")):
	try:
		title=new_data["alerts"][n]["title"]
		lon=new_data["alerts"][n]["area"]["center"]["lon"]
		lat=new_data["alerts"][n]["area"]["center"]["lat"]
		urlmap="https://maps.googleapis.com/maps/api/staticmap?center="+str(lat)+","+str(lon)+"&zoom=11&size=600x300"
		print urlmap
		titleshort=title[0:114]
		url=new_data["alerts"][n]["share_urls"]["fr"]
		comm=agent_info = u' '.join((titleshort, url)).encode('utf-8').strip()
		message="application=\"SAIP\" new_alert=\"1\" title=\""+str(title.encode('utf-8').strip())+"\" "+"id=\""+str(new_data["alerts"][n]["id"])+"\" "+"category=\""+str(new_data["alerts"][n]["category"])+"\" "+"status=\""+str(new_data["alerts"][n]["status"])+"\" "+"severity=\""+str(new_data["alerts"][n]["severity"])+"\" "+"start_time=\""+str(new_data["alerts"][n]["start_time"])+"\" "+"broadcast_time=\""+str(new_data["alerts"][n]["broadcast_time"])+"\" "+"version=\""+str(new_data["alerts"][n]["version"])+"\" "+"details_fr=\""+str(new_data["alerts"][n]["details"]["fr"].encode('utf-8').strip())+"\" "+"details_en=\""+str(new_data["alerts"][n]["details"]["en"].encode('utf-8').strip())+"\" "+"url_fr=\""+str(new_data["alerts"][n]["share_urls"]["fr"])+"\" "+"url_en=\""+str(new_data["alerts"][n]["share_urls"]["en"])+"\" "+"lon=\""+str(new_data["alerts"][n]["area"]["center"]["lon"])+"\" "+"lat=\""+str(new_data["alerts"][n]["area"]["center"]["lat"])+"\" "
		syslog_alert(message)
		print comm
		tweet_image(urlmap, comm)
	except:
		print "End"
		test=1
else:
	print "Nothing new, all seems fine"
	message="application=\"SAIP\" new_alert=\"none\""
	syslog_alert(message)

