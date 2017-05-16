from twython import Twython, TwythonError
import authorization

def retweet():	#retweet tweets with a set hashtag
	search_results = authorization.twitter.search(q="#TwitterShitter", count=5)
	try:
		for tweet in search_results["statuses"]:
			authorization.twitter.retweet(id = tweet["id_str"])
			log_str = "retweeted "+tweet["id_str"]
			log_file=open('log_file.txt', 'a')
			log_file.write(log_str)
			log_file.close()
			print log_str,
	except TwythonError as e:
		print e
		
	return