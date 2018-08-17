import tweepy
import csv
import re
import string
from random import randint

# access_token = "854033995839000579-Zbf4IzWa6yHa5Yo3FbUgQvPJqSbZN7j"
# access_token_secret = "poiXCOwDPwmjNjMc8nCNYvGzuyiXucxC6kP1KHbbiXT6H"
# consumer_key = "YPDiEqkRSgGGcUv9UOUdFOz6V"
# consumer_secret = "toy4Do1aolGmgkqXDniLcooUNJxZhf3vYZYzsiF5qQTAKn635G"

def get_tweets(profile_name):
	#Handle getting the tweets using tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
   
	api = tweepy.API(auth)
    #Array that holds all of a person tweets(Eg. Blake Shelton)
	blake_tweets = []
    #Change 'count to more or less depending on how much words you want
	get_recent_tweets = api.user_timeline(screen_name = profile_name, count = 5)

	#Adds the tweets into the array
	blake_tweets.extend(get_recent_tweets)

	#Updates the index to get the next tweet
	update_id = get_recent_tweets[-1].id - 1

	#Number of iterations of 'count' + 1, since the first iteration above tweets wanted
	num_tweets_needed = 6;
	iteration = 0

	#Keep getting tweets until 
	while iteration < num_tweets_needed:
		print "Getting %s's tweets..." % (profile_name)
		#Change 'count to more or less depending on how much words you want
		get_recent_tweets = api.user_timeline(screen_name = profile_name, count = 5, max_id = update_id)
		#Adds the tweets into the array
		blake_tweets.extend(get_recent_tweets)
		#Updates the index 
		update_id = get_recent_tweets[-1].id - 1

		iteration += 1


	print "%s tweets downloaded sucessfully." % (len(blake_tweets))
	#Formats the tweets into utf-8
	
	formatedTweets = [[tweet.text.encode("utf-8")] for tweet in blake_tweets]
	#Output tweets to a csv that we will gather from later
	
	ostream = open('%s_tweets.csv' % profile_name, 'w')
	
	writer = csv.writer(ostream)
	writer.writerows(formatedTweets)
	
	pass

	
#Clean the tweets up and gets rid of the unnecessary characters
def clean_tweets(profile_name):
	istream = open("%s_tweets.csv" % profile_name)
	ostream = open("%s_cleaned_tweets.csv" % profile_name, 'w')

	#CSV reader to read the file we created
	csv_f = csv.reader(istream)
	#CSV writer to output a new CSV later
	writer = csv.writer(ostream)
	
	#Cleans each tweet row by row
	for line in csv_f:
		line = str(line)
		
		with_emojis = get_rid_of_symbols(get_rid_of_links(line))
		
		writer.writerow(with_emojis.split(','))

#Get rid of the URL's
def get_rid_of_links(text):
    link_reg = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_reg, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    
    return text

#Get rid of the '@', "#", etc
def get_rid_of_symbols(text):
    rand_symbols = ['@','#','!','?','\'']

    words = []
    for word in text.split():
        if word[0] not in rand_symbols:
            words.append(word)
    return ' '.join(words)

#Generate a random sentence using the cleaned CSV file
def get_random_sentence(profile_name):
	
	stream = csv.reader(open('%s_cleaned_tweets.csv' % (profile_name)), delimiter=';', quotechar='|')
	sentenceArray = []
	theSentence = ""
	finalSentence = " "

	#Add sentence to an array
	for row in stream:
		sentenceArray.append(', '.join(row))
		
	#Select random words from the array
	for i in sentenceArray:
		try:
			i.rsplit(' ', 1)[randint(2,5)]
		except IndexError:
			try:
				i.rsplit(' ', 1)[1]
			except IndexError:
				pass

		theSentence += i
	

	wordList = re.sub("[^\w]", " ",  theSentence).split()

	#Extra clean up on some random emoji chars and some single letter strings
	for word in wordList:
		if len(word) == 3:
			word = re.sub("x" + "[\w]" + "[\w]", " ", word)
		if len(word) < 2:
			word = re.sub("[\w]", " ", word)
		#Get rid of apostophes, since for some reason the code above doesn't
		word = re.sub("x99" + "[\w]", " ", word)
                print word
		finalSentence += word + " "



	#Output final result into a text file
	text_file = open("Output.txt", "w")
	text_file.write(finalSentence)
	text_file.close()

if __name__ == '__main__':
	#Runs the program
  	#"blakeshelton" can be replaced with any twitter account name
	get_tweets("blakeshelton")
	clean_tweets("blakeshelton")
	get_random_sentence("blakeshelton")