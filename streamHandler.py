from tweepy import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
import re

import fullSentStrings

CONSUMER_KEY = "nAl92YiAW3oRgxaoD8kY3KRqR"
CONSUMER_SECRET_KEY = "c80v1jASHmnjqBIOLTf2gUWuKDBaoc14WOhXXkVkbxk6IQRdX9"
ACCESS_TOKEN = "761422321001172992-jq1DFQE9iAfWH73MXbssEQcoy4pDrBV"
ACCESS_SECRET_TOKEN = "2bI4HyPTFNRl41dVXBYFhzXqAgPqnbqdLUnaIltQ8DtHe"

class Listener(StreamListener):

    def __init__(self, numOfTweets = 0):
        self.numOfTweets = numOfTweets
    

    def on_data(self, data):
        self.numOfTweets += 1
        startIndex = data.index("text")
        possibleEndIndex1 = 99999999
        if ",\"display_text_range" in data:
            possibleEndIndex1 = data.index(",\"display_text_range")

        possibleEndIndex2 = data.index(",\"source\"")

        if possibleEndIndex1 < possibleEndIndex2:
            endIndex = possibleEndIndex1
        else:
            endIndex = possibleEndIndex2
        
        tweet = data[startIndex:endIndex]
        new = tweet.replace("\\u2026", "...")
        new = new.replace("\/", "/")
        new = new.replace("\\n", "")
        new = new.replace("\\\"", "\"")
        new = new.replace("\\u2019", "'")
        new = new.replace("\\u2018", "'")
        
        file = open('savedTweets.txt', 'w+')
        file.writelines(new)
        file.close()

        print(new)
        
        if self.numOfTweets >= 25:
            self.numOfTweets = 0
            return False

    def on_error(self, status):
        print(status)
    







def main():
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

    tweetStreamListener = Listener()
    tweetStream = Stream(auth, tweetStreamListener)


    print(fullSentStrings.INTRODUCTION)
    print(fullSentStrings.USAGE)

    while(1):
        keyword = input(">> ")

        if keyword == "end":
            break
        if keyword == "\'end\'":
            keyword = "end"

        tweetStream.filter(languages=["en"], track = [keyword])
        print()

main()