#!/usr/bin/env python

from collections import defaultdict
import random
import re

class Machine(object):
    '''
    Generates a tweet, storing words in memory, using Markov bigrams.
    '''
    def __init__(self, statuses):
        self.words = self.get_words(statuses) # get a list of clean words
        self.num_words = len(self.words)
        self.tokens = defaultdict(list) # maps (w2, w2 -> [w3, w4]) for every pair w1, w2
        self.triples()

    def get_words(self, statuses):
        '''
        Returns words in given statuses without any @ mentions, or hashtags.
        '''
        words = []
        ignore_pattern = re.compile(r'http|[@#][_A-Za-z0-9]+|RT|MT')
        for status in statuses: # for each status
            for word in status.split(): # for each word
                if not bool(ignore_pattern.search(word)):
                    words.append(word.lower())
        return words

    def triples(self):
        '''
        Builds the tokens dictionary. For each (w1, w2, w3), maps
        (w1, w2) -> w3.
        '''
        if self.num_words < 3: return
        for i in xrange(self.num_words - 2):
            key = (self.words[i], self.words[i + 1])
            next_word = self.words[i + 2]
            self.tokens[key].append(next_word)

    def generate(self, size=6):
        '''
        Generate a tweet of given word size.
        '''
        seed_num = random.randint(0, self.num_words - 3) # this will be w1
        w1, w2 = self.words[seed_num], self.words[seed_num + 1]
        gen_words = []

        for i in xrange(size):
            gen_words.append(w1) # add w1
            if self.tokens[(w1, w2)] == []:
                break
            w1, w2 = w2, random.choice(self.tokens[(w1, w2)]) # get a random w3 from list mapped to by (w1, w2)
        gen_words.append(w2)
        return ' '.join(gen_words)


def main(screen_name):
    '''
    Get Interesting Statuses for user 'screen_name'
    '''

    from tweader import get_keys
    #(app_key, app_secret, _, _) = get_keys('KEYS')
    screen_name = str(screen_name)
    import tweepy
    (key_lazy_music, secret_lazy_music,
            access_token, access_token_secret) = get_keys('KEYS')

    auth = tweepy.OAuthHandler(key_lazy_music, secret_lazy_music)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    #statuses = [status.parse() for status in timeline]

    #for page in tweepy.Cursor(timeline, count=200).pages(16):
    statuses = []
    for status in tweepy.Cursor(api.user_timeline, id=screen_name).items(200):
        # Process the status here
        statuses.append(status.text)

    print len(statuses), 'statues found.'

    machine = Machine(statuses)

    final = []

    for _ in range(20):
        final.append(machine.generate(size=random.randint(4, 20)))

    print final
    return final

if __name__ == '__main__':
    main('ChaudharySimply')
