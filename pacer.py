#!/usr/bin/env python2

import os
import platform
import sys
from tweader import send_replies

MINUTES = 2     # minutes to sleep if no status updated last time
def pacer(query=None, keyfile=None, keynumber=None):
    '''
    Pace the machine according to the allowed limits
    '''
    import time
    count = 0
    print '--------------------------'
    while 1:
        out = send_replies(query=query, keyfile=keyfile, keynumber=keynumber)
        print 'Sent ', out, ' replies in last call.'
        print '--------------------------'
        if out == 0:
            print 'I\'m too tired. Going to sleep for ', MINUTES, ' minutes.'
            time.sleep(60*MINUTES)

    return count

def main():
    ''' main '''
    # Parse command line arguments
    from optparse import OptionParser
    parser = OptionParser(version="%prog 1.0")
    parser.add_option("-f", "--file", type='str', dest="keyfile",
                        help="Use the specified file for keys")
    parser.add_option("-k", "--key-file", type='str', dest="keyfile",
                        help="Same as --file to specify file containing keys")
    parser.add_option("-n", "--key-number", type='int', dest="keynumber",
                        help='Use the keys palaced at this number in keyfile')
    parser.add_option("-t", "--timeout", type='int', dest="timeout",
                        help='Number of minutes to timeout if multiple '
                                'requests fails')
    (options, args) = parser.parse_args()
    argc = len(args)

    query = None
    if argc > 0:
        query = ' '.join(args)
    if options.timeout:
        global MINUTES
        MINUTES = options.timeout
    # By default None: options.keyfile, options.keynumber
    return pacer(
            query=query,
            keyfile=options.keyfile,
            keynumber=options.keynumber
            )

if __name__ == '__main__':
    try:
        main()
        if os.name == 'nt' or platform.system() == 'Windows':
            raw_input('Press Enter or Close the window to exit !')
    except KeyboardInterrupt:
        print '\nClosing garacefully :)', sys.exc_info()[1]
    except SystemExit:
        pass
    except:
        print 'Unexpected Error:', sys.exc_info()[0]
        print 'Details:', sys.exc_info()[1]
        raise
