#!/usr/bin/env python3

from collections import defaultdict
import os
import random
import textwrap

# pylint: disable=import-error
from colorama import Fore, Style

from genutils import check_if_file_exists

QUOTE_FILENAME = 'config/quotes.txt'

def get_quote():
    '''Get a quote from the quote file'''
    script_path = os.path.realpath( os.path.dirname( __file__ ) )
    filename = os.path.join( script_path, QUOTE_FILENAME )
    check_if_file_exists( filename )

    quote_db = []
    tag_db = defaultdict( list )
    with open( filename, "r", encoding="utf8") as quote_file:
        msg = ''
        tags = []
        for line in quote_file:
            if line[ 0 ] == '@':
                if msg:
                    tags = [ t.strip() for t in tag_str.split( ',' ) ]
                    for tag in tags:
                        tag_db[ tag ].append( msg )
                    quote_db.append( msg.rstrip() )
                if '<' in line and '>' in line:
                    lpos = line.find( '<' )
                    rpos = line.find( '>' )
                    tag_str = line[ lpos + 1 : rpos ]
                    msg = line[ rpos + 1 : ]
                else:
                    msg = line[ 1: ]
                    tags = []
            elif line != '\n':
                msg += line
        tags = [ t.strip() for t in tag_str.split( ',' ) ]
        for tag in tags:
            tag_db[ tag ].append( msg )
        quote_db.append( msg.rstrip() )

    size = len( quote_db )
    index = random.randint( 0, size - 1 )
    return quote_db[ index ]

# TODO:
# command line argument for tags, color

def main():
    '''The main function'''
    text = get_quote()
    text = textwrap.fill( get_quote(), width=85 )
    print( Fore.GREEN + text )
    print(Style.RESET_ALL)

if __name__ == '__main__':
    main()
