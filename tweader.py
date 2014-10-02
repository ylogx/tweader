#!/usr/bin/env python2

import random
import sys
import tweepy
# Global
api = None

def get_keys(filename):
    ''' KEY_LAZY_MUSIC, SECRET_LAZY_MUSIC, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    '''
    fhan = open(filename, 'rU')
    list_keys = [x.strip() for x in fhan.readlines()]
    return list_keys

def get_tweet_with(query):
    ''' Get a tweet with particular query '''
    searched_tweets = api.search(query)
    for tweet in searched_tweets:
        print '* ', tweet.text

def get_interesting(screen_name):
    '''
    Get Interesting Statuses for user 'screen_name'
    '''
    screen_name = str(screen_name)

    #for page in tweepy.Cursor(timeline, count=200).pages(16):
    statuses = []
    for status in tweepy.Cursor(api.user_timeline, id=screen_name).items(200):
        statuses.append(status.text)

    print len(statuses), 'statues found.'

    import markov
    machine = markov.Machine(statuses)

    final = []

    for _ in range(20):
        final.append(machine.generate(size=random.randint(4, 20)))

    print final
    return final



def init_api(filename):
    (key_lazy_music, secret_lazy_music,
            access_token, access_token_secret) = get_keys(filename)

    auth = tweepy.OAuthHandler(key_lazy_music, secret_lazy_music)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)



def main(argv):
    ''' main '''
    init_api('KEYS')
    query_list = ['Music']
    if len(argv) > 1:
        query_list = argv[1:]
    for query in query_list:
        get_tweet_with(query)
    return

if __name__ == '__main__':
    main(sys.argv)
