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



def get_tweets(topic:str, num_of_tweets,api = auth()):
    # Get the 100 most recent tweets made to the handle
    tweets = api.search_tweets(q=topic, tweet_mode='extended',count=num_of_tweets)

    # Create an empty DataFrame to store the tweets
    tweets_df = pd.DataFrame(columns=[ "text"])

    # Clean tweet and print the text of each tweet
    for tweet in tweets:

        # Ensure full text is returned
        try:
            tweet = tweet.retweeted_status.full_text 
        except AttributeError:  # So this is not a Retweet
            tweet = tweet.full_text

        # Remove hashtags, user mentions, and URLs
        tweet = re.sub(r'#\w+', '', tweet)
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

        tweet_df = pd.DataFrame({ "text": [tweet]})

        tweets_df = tweets_df.append(tweet_df, ignore_index=True)
        
    tweets_df.to_csv('tweets_df.csv',index=False)
    return 

get_tweets('inec',10)




