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
from check import *
from retweet import *

import authorization

import PIL
from PIL import Image, ImageDraw, ImageFont

from clarifai import rest
from clarifai.rest import ClarifaiApp

dir = str(os.getcwd())+'/'
os.chdir(dir)

def main():
	W = 440
	shutil.copyfile(dir+'img.jpg', dir+'imgold.jpg')
	while True:
		id = authorization.id_generator()

		imgFromUrl = urllib.urlopen('https://imgur.com/'+id+'.jpg')
		file = open(str(os.getcwd())+'/img.jpg', 'r+')
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

	tweet_text = ''
	data = authorization.app.tag_urls(['https://imgur.com/'+id+'.jpg'])
	i=0
	for i in range(5):
		tweet_text = tweet_text+'#'+data['outputs'][0]['data']['concepts'][i]['name'].replace(" ", "")+" "	 		
	tweetimg = open(dir+'img.jpg')
	authorization.twitter.update_status_with_media(status = tweet_text, media = tweetimg)
	
	log_str = "https://imgur.com/"+id+".jpg "+tweet_text+"\n"
	log_file=open('log_file.txt', 'a')
	log_file.write(log_str)
	log_file.close()
	print log_str,
	
	retweet()
  
	time.sleep (60*30)