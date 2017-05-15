#!/usr/bin/python
from twython import Twython, TwythonError
import random
import sys
import os
import time
import urllib
import string
import random
import filecmp
import shutil
from pprint import pprint
import PIL
from PIL import Image, ImageDraw, ImageFont

from clarifai import rest
from clarifai.rest import ClarifaiApp

from keys import *

app = ClarifaiApp(CLIENT_ID, CLIENT_SECRET)
model = app.models.get("general-v1.3")

W = 440

def id_generator(size=5, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

cmd = '/opt/vc/bin/vcgencmd measure_temp'
line = os.popen(cmd).readline().strip()
temp = line.split('=')[1].split("'")[0]

dir = '/home/pi/TwitPiBot/'
os.chdir(dir)

def main():
	shutil.copyfile(dir+'img.jpg', dir+'imgold.jpg')
	while True:
		id = id_generator()
		imgFromUrl = urllib.urlopen('https://imgur.com/'+id+'.jpg')
		file = open('/home/pi/TwitPiBot/img.jpg', 'r+')
		file.write(imgFromUrl.read())
		file.close()
		Image.open(dir+'img.jpg').convert('RGB').save(dir+'img.jpg')
		img = Image.open(dir+'img.jpg')
		wpercent = (W/float(img.size[0]))
		hsize = int((float(img.size[1])*float(wpercent)))
		img = img.resize((W,hsize), PIL.Image.ANTIALIAS)
		img.save(dir+'img.jpg')
		if (filecmp.cmp(dir+'img.jpg', dir+'imgold.jpg') == False) and (filecmp.cmp(dir+'img.jpg', dir+'nla1.jpg') == False) and (filecmp.cmp(dir+'img.jpg', dir+'nla2.jpg') == False):
			break
	
	str = ''
	data = app.tag_urls(['https://imgur.com/'+id+'.jpg'])
	i=0
	for i in range(5):
		str = str+'#'+data['outputs'][0]['data']['concepts'][i]['name'].replace(" ", "")+" "	 		
	tweetimg = open(dir+'img.jpg')
	twitter.update_status_with_media(status = str, media = tweetimg)
	print('https://imgur.com/'+id+'.jpg '+str)
	
	search_results = twitter.search(q="#TwitterShitter", count=5)
	try:
		for tweet in search_results["statuses"]:
			twitter.retweet(id = tweet["id_str"])
	except TwythonError as e:
		print e
	
	time.sleep (60*30)

if __name__ == '__main__':
	while True:
		#try:
			main()
			
		#except:
			#pass