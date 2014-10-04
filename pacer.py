#!/usr/bin/env python2

import sys
from tweader import send_replies

MINUTES = 2     # minutes to sleep if no status updated last time
def pacer(query=None):
    '''
    Pace the machine according to the allowed limits
    '''
    import time
    count = 0
    print '--------------------------'
    while 1:
        out = send_replies(query)
        print 'Sent ', out, ' replies in last call.'
        print '--------------------------'
        if out == 0:
            print 'I\'m too tired. Going to sleep for ', MINUTES, ' minutes.'
            time.sleep(60*MINUTES)

    return count

def main(argv):
    ''' main '''
    query = None
    if len(argv) > 1:
        query = ' '.join(argv[1:])
    return pacer(query)

if __name__ == '__main__':
    main(sys.argv)
