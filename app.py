from dotenv import load_dotenv
import os
import tweepy
import time

load_dotenv()

TWITTER_CONSUMER_KEY= os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET= os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN= os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET= os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

client = tweepy.Client(consumer_key=TWITTER_CONSUMER_KEY,
                    consumer_secret=TWITTER_CONSUMER_SECRET,
                    access_token=TWITTER_ACCESS_TOKEN,
                    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)

query = '#kaavish -is:retweet'
kaavish_id = '74840248'
hashtag_file = 'last_hashtag.txt'
mentioned_file = 'last_mentioned.txt'

def read_sinceid():
    file_read = open(hashtag_file, 'r')
    since_id = int(file_read.read().strip())
    file_read.close()
    return since_id

def store_untilid(since_id):
    file_write = open(hashtag_file, 'w')
    file_write.write(str(since_id))
    file_write.close()
    return

def read_mentionedId():
    file_read = open(mentioned_file, 'r')
    since_id = int(file_read.read().strip())
    file_read.close()
    return since_id

def store_mentionedId(since_id):
    file_write = open(mentioned_file, 'w')
    file_write.write(str(since_id))
    file_write.close()
    return

def split_date(id):
    id = str(id)
    datestr = "".join(list(id)[:14])
    return int(datestr)

def like_retweet_hashags():
    since = read_sinceid()
    tweets = client.search_recent_tweets(query=query, since_id=since, max_results=10, user_auth=True)
    if tweets.data != None:
        for tweet in tweets.data:
            client.like(tweet_id=tweet.id)
            client.retweet(tweet_id=tweet.id)
            if tweet.id > since:
                store_untilid(tweet.id)
    else:
        print("Found nothing to like and retweet in hashtags")

def like_mentions():
    since = read_mentionedId()
    tweets = client.get_users_mentions(id=kaavish_id, since_id=since, max_results=10, user_auth=True)
    if tweets.data != None:
        for tweet in tweets.data:
            client.like(tweet_id=tweet.id)
            print(tweet.id)
            if tweet.id > since:
                store_mentionedId(tweet.id)
    else:
        print("Found nothing to like in mentioned tweets")



while True:
    print("Liking and retweeting hashtags")
    like_retweet_hashags()
    print("Liking mentions")
    like_mentions()
    print("Now Sleeping")
    time.sleep(900)