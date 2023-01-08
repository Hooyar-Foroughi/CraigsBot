import tweepy

# Authentication Tokens
APIkey = 'API key here'
APIsecret = 'API secret here'
accessToken = 'access token here'
accessTokenSecret = 'access token secret here'
# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
   APIkey, APIsecret, accessToken, accessTokenSecret
)
# Create API object
twitter = tweepy.API(auth)
# Verify credentials
try:
    twitter.verify_credentials()
except:
    print("Error during tweepy authentication")
