from twython import Twython, TwythonError
import authorization
import re

def deleteTweet(): #Deletes a tweet with the given ID
	search_results = authorization.twitter.search(q="#DeleteID", count=5, result_type='recent')
	try:
		for tweet in search_results["statuses"]:
			id_to_delete = int(re.sub("\D", "", tweet["text"]))
			authorization.twitter.destroy_status(id=id_to_delete)
			authorization.twitter.update_status(status="Tweet "+str(id_to_delete)+" deleted!", in_reply_to_status_id = tweet["id_str"])
			
			log_str = "Deleted tweet with ID "+str(id_to_delete)+"\n"
			log_file=open('log_file.txt', 'a')
			log_file.write(log_str)
			log_file.close()
			print log_str,
	except TwythonError as e:
		print e
		
	return
	