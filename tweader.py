#!/usr/bin/env python2

import sys

def get_keys(filename):
    ''' KEY_LAZY_MUSIC, SECRET_LAZY_MUSIC, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    '''
    fhan = open(filename, 'rU')
    list_keys = [x.strip() for x in fhan.readlines()]
    return list_keys

def get_tweet_with(query):
    ''' Get a tweet with particular query '''
    import tweepy
    (key_lazy_music, secret_lazy_music,
            access_token, access_token_secret) = get_keys('KEYS')

    auth = tweepy.OAuthHandler(key_lazy_music, secret_lazy_music)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    searched_tweets = api.search(query)
    for tweet in searched_tweets:
        print '* ', tweet.text


def main(argv):
    ''' main '''
    query_list = ['Music']
    if len(argv) > 1:
        query_list = argv[1:]
    for query in query_list:
        get_tweet_with(query)
    return

if __name__ == '__main__':
    main(sys.argv)
