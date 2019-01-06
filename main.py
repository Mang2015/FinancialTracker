import json, sys, tweepy
from bs4 import BeautifulSoup as bs
import urllib2
from tweepy.streaming import StreamListener
from IPython.display import clear_output
from tweepy import OAuthHandler
from tweepy import Stream
import re

class appProperties:
    def __init__(self, consumerKey, consumerSecret, accessKey, accessSecret):
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.accessKey = accessKey
        self.accessSecret = accessSecret


class JSONListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def __init__(self, ticker, max_tweets = 50):
        self.counter = 0
        self.ticker = ticker
        self.output  = open('./outputs/' + ticker + '.json', 'w')
        self.max_tweets = max_tweets

    def on_data(self, data):
        if self.counter < self.max_tweets:
            self.output.write(data)
            self.counter += 1

            clear_output()
            print 'Tweets collected so far: {}'.format(self.counter)
            # Print the information
            # Comment these lines of code when you are crawling data for assignment 3!!!
            #'''
        #    status = json.loads(data)
        #    print 'Tweet No. {} at [Time = {}]'.format(self.counter, status['created_at'])
        #    print status['text']
            #'''
            return True
        else:
            print 'Totally {} tweets collected'.format(self.max_tweets)
            self.output.close()
            return False


    def on_error(self, status):
        print 'Error: ' + str(status)


def main():
    auth = OAuthHandler(appConfig.consumerKey, appConfig.consumerSecret)
    auth.set_access_token(appConfig.accessKey, appConfig.accessSecret)
    api = tweepy.API(auth)
    # listen = JSONListener("TSLA")
    # stream = Stream(auth, listen)
    # stream.filter(track=['Tesla'])
    #
    # stream.disconnect()
    name_ticker = {'Tesla': 'TSLA', 'Microsoft': 'MSFT', 'Majesco': 'MJCO', 'Netflix': 'NFLX'}
    for key in name_ticker:
        print key
        twitterSentiment(api, key)

        html = urllib2.urlopen("https://www.marketwatch.com/investing/stock/" + name_ticker[key])
        soup = bs(html, 'html.parser')
        elems = soup.find_all(class_ =["kv__value kv__primary ", "kv__value kv__primary is-na"])

        print "P/E Ratio: " + elems[8].text + '\n'
        out = open("test.txt", 'w')

        out.write(str(soup))
        out.close()

def twitterSentiment(api, key):
    posLexicon = []
    negLexicon = []
    text = []
    pos_words = []
    pos_count = 0
    neg_count = 0
    neg_words = []
    tot_words = 0

    fp = open("poswords.txt")
    for line in fp:
        posLexicon.append(line.rstrip())

    fp.close()

    fp = open("negwords.txt")
    for line in fp:
        negLexicon.append(line.rstrip())

    fp.close()

    for i in range(5):
        tweets = api.search(key)
        tweet_text = []
        for tweet in tweets:
            tweet_text.append(re.sub(r'\W+', ' ', tweet.text.encode('utf-8').strip()))
    # fp = open("./outputs/" + ticker + ".json")
    # for line in fp:
    #     text.append(re.sub(r'\W+', ' ', json.loads(line)['text'].encode('utf-8').strip()))

        for line in tweet_text:
            for word in line.split():
                if word in pos_words:
                    pos_count += 1
                    tot_words += 1
                elif word in posLexicon:
                    pos_words.append(word)
                    pos_count += 1
                    tot_words += 1
                elif word in neg_words:
                    neg_count += 1
                    tot_words += 1
                elif word in negLexicon:
                    neg_words.append(word)
                    neg_count += 1
                    tot_words += 1
                else:
                    continue

    print "pos percentage: " + str(float(pos_count/float(tot_words)))
    print "neg percentage: " + str(float(neg_count/float(tot_words)))



if __name__ == "__main__":
    appConfig = appProperties("tRizS6fqnvCkV5BIs16lFBPkH", "uze9ADJ4mtWbNpZqBs5qgBTjZSAmOHXG5GTW5YbI0vWam0wWDu", "919344396306468865-4v7TABdLhzQuWrnmNB3wDcDWX1mv9QR", "Tx7ZBfv9DxRj3sdjjdqukufVgAz61CcQsKOmyGyeWCvjX")
    main()
