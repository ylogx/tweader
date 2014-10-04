#!/usr/bin/env python2

import random
import sys
import time
import tweepy

import markov
# Global
api = None
SHORT_URL = 'goo.gl/DnwHCy'
MESSAGES = [
            'Check out',
            'Go see',
            'Found this',
            'This looks nice',
            'This is amazing',
            'This changed me',
            'I love this',
            ]
MESSAGES = [out+' '+SHORT_URL for out in MESSAGES]
MAX_ITEMS = 60     # No. of items from past to check

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
    #for page in tweepy.Cursor(api.user_timeline, id=screen_name).pages(3):
        #for status in page:
            #statuses.append(status.text)
    print len(statuses), 'statues as algorithm input.'

    machine = markov.Machine(statuses)

    return machine.generate(size=random.randint(4,20))
    #final = []
    #for _ in range(20):
        #final.append(machine.generate(size=random.randint(4, 20)))
    #return final


def send_replies(query=None):
    '''
    Send replies to random netizens and get banned consequently
    '''
    count = 0
    if query == None:
        query = 'Music'
    api = init_api('KEYS')
    from httplib import IncompleteRead
    try:
        searched_tweets = api.search(query)
    except IncompleteRead:
        send_replies()
    except:
        print 'EXCEPTION: ', sys.exc_info()[1]
        raise
    print 'Found ', len(searched_tweets), ' results for query: ', query
    print 'Processing now ...'
    for tweet in searched_tweets:
        screen_name = tweet.user.screen_name
        in_reply_to_status_id = tweet.id
        try:
            reply_name = '@' + screen_name + ' '
            print '%d. Training new AI Machine to Learn for user'%(count+1),
            print screen_name, 'with',

            interesting_line = get_interesting(screen_name)

            check_out_msg = ' ' + MESSAGES[random.randint(0, len(MESSAGES)-1)]
            mystatus = reply_name + interesting_line + check_out_msg
            #TODO: Better splitting
            while len(mystatus) > 140-8:    # 7 for http:// which is implicit
                interesting_line = interesting_line[:-1*(len(mystatus)-(140-8-1))]
                mystatus = reply_name + interesting_line + check_out_msg

            print 'Updating: ', mystatus
            api.update_status(mystatus, in_reply_to_status_id)
            print 'Following: ', screen_name
            api.create_friendship(screen_name)
            count += 1
        except KeyboardInterrupt:
            raise
        except tweepy.error.TweepError:
            try:
                print 'Yo',sys.exc_info()[1][0][0]['code']
                if sys.exc_info()[1][0][0]['code'] == 88:   #Twitter Limit reached
                    return count
                elif sys.exc_info()[1][0][0]['code'] == 186:   #Twitter Limit reached
                    print 'Status Long: ', sys.exc_info()[1]
                else:
                    print sys.exc_info()
            except TypeError:
                print sys.exc_info()
                continue
        except:
            print 'EXCEPTION: ', sys.exc_info()[0], sys.exc_info()[1]
    return count

def main(argv):
    ''' main '''
    api = init_api('KEYS')
    return send_replies()

if __name__ == '__main__':
    main(sys.argv)
