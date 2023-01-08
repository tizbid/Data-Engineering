import tweepy
import configparser
import re
from nltk.corpus import stopwords
import pandas as pd


def auth(config = configparser.ConfigParser()):
    #Read configuration
    config.read('config.ini')

    # Authenticate to the Twitter API using the keys and tokens
    auth = tweepy.OAuth1UserHandler(
        consumer_key = config['consumer_key_secret']['key'],
        consumer_secret = config['consumer_key_secret']['secret'],
        access_token = config['access_token_secret']['token'],
        access_token_secret = config['access_token_secret']['secret']
        )

    # Create an API client
    api = tweepy.API(auth)
    return api


api = auth()




# Replace "handle" with the actual handle you want to get tweets for
handle = "inec"

# Get the 100 most recent tweets made to the handle
tweets = api.search_tweets(q=handle, tweet_mode='extended',count=5)

# Print the text of each tweet
for tweet in tweets:
    
    #print(tweet.text)
    
    # Remove hashtags, user mentions, and URLs
    tweet = re.sub(r'#\w+', '', tweet.full_text)
    tweet = re.sub(r'@\w+', '', tweet)
    tweet = re.sub(r'https?:\/\/\S+', '', tweet)
        
    # Remove punctuation and convert to lowercase
    #tweet = re.sub(r'[^\w\s]', '', tweet)
    tweet = tweet.lower()
        
    # Remove stopwords
        
    stopwords_list = stopwords.words('english')
    tweet_words = tweet.split()
    tweet_without_stopwords = [word for word in tweet_words if word not in stopwords_list]
        
    # Rejoin tweet
    tweet = ' '.join(tweet_without_stopwords)
     
    
    print(tweet)

