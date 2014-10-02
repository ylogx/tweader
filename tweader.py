#!/usr/bin/env python2

import random
import sys
import tweepy
# Global
api = None
SHORT_URL = 'http://goo.gl/DnwHCy'
MESSAGES = [
            'Check out ',
            'Go see ',
            'Found this ',
            'This looks nice ',
            'This is amazing ',
            'This changed me ',
            ]
MESSAGES = [out+SHORT_URL for out in MESSAGES]
print MESSAGES
MAX_ITEMS = 100     # No. of items from past to check

def get_keys(filename):
    '''
    @return [
                KEY_LAZY_MUSIC,
                SECRET_LAZY_MUSIC,
                ACCESS_TOKEN,
                ACCESS_TOKEN_SECRET
            ]
    '''
    fhan = open(filename, 'rU')
    #Read top 4 lines which should contain keys in the order shown above
    list_keys = [x.strip() for x in fhan.readlines()[:4]]
    return list_keys


def init_api(filename):
    '''
    Initialize the api using keys stored in filename
    '''
    global api
    if api != None:
        return api
    (key_lazy_music, secret_lazy_music,
            access_token, access_token_secret) = get_keys(filename)

    auth = tweepy.OAuthHandler(key_lazy_music, secret_lazy_music)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api


def get_tweet_with(query):
    ''' Get a tweet with particular query '''
    api = init_api('KEYS')
    searched_tweets = api.search(query)
    for tweet in searched_tweets:
        print tweet.user.screen_name, ': ', tweet.text
        #print get_interesting(tweet.screen_name)[1]

def get_interesting(screen_name):
    '''
    Get Interesting Statuses for user 'screen_name'
    '''
    #screen_name = str(screen_name)

    api = init_api('KEYS')
    #for page in tweepy.Cursor(timeline, count=200).pages(16):
    statuses = []
    for status in tweepy.Cursor(api.user_timeline,
            id=screen_name).items(MAX_ITEMS):
        statuses.append(status.text)

    print len(statuses), 'statues found.'

    import markov
    machine = markov.Machine(statuses)

    return machine.generate(size=random.randint(4,20))
    #final = []
    #for _ in range(20):
        #final.append(machine.generate(size=random.randint(4, 20)))
    #return final


def send_replies():
    count = 0
    query = 'Music'
    api = init_api('KEYS')
    searched_tweets = api.search(query)
    print 'Found ', len(searched_tweets), ' results'
    print 'Processing now ...'
    for tweet in searched_tweets:
        screen_name = tweet.user.screen_name
        in_reply_to_status_id = tweet.id
        try:
            mystatus = '@' + screen_name + ' '
            print 'Creating Markov Machine for ', screen_name
            interesting_line = get_interesting(screen_name)
            mystatus += interesting_line[:120]   #TODO: split properly
            mystatus += ' ' + MESSAGES[random.randint(0,len(MESSAGES)-1)]

            print 'Updating: ', mystatus
            api.update_status(mystatus, in_reply_to_status_id)
            print 'Following: ', screen_name
            api.create_friendship(screen_name)
            count += 1
        except KeyboardInterrupt:
            raise
        except:
            print 'Exception: ', sys.exc_info()[0]
            print sys.exc_info()[1]
    return count

def pacer():
    count = 0
    count += send_replies()

def main(argv):
    ''' main '''
    api = init_api('KEYS')
    send_replies()
    return
    query_list = ['Music']
    if len(argv) > 1:
        query_list = argv[1:]
    for query in query_list:
        get_tweet_with(query)
    return

if __name__ == '__main__':
    main(sys.argv)
