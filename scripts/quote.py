#!/usr/bin/env python3
'''A script to randomly print a quote'''
from collections import defaultdict
from dataclasses import dataclass
import argparse
import os
import random
import re
import textwrap

# pylint: disable=import-error
# pylint: disable=too-few-public-methods
from colorama import Fore, Style

from genutils import check_if_file_exists

QUOTE_FILENAME = 'config/Quotes.md'

@dataclass( frozen=True )
class Quote:
    '''A class to represet a quote'''
    text : str
    tags : dict

    def __str__( self ):
        return self.text

class QuoteDB:
    '''The class to represent the quote database'''
    def __init__( self, filename ):
        script_path = os.path.realpath( os.path.dirname( __file__ ) )
        filename = os.path.join( script_path, filename )
        check_if_file_exists( filename )
        self.filename = filename
        self.data = []
        self.tags_dict = defaultdict( list )

    def add_tag( self, quote, tags ):
        '''Add quote to the tag dictionary for future lookup by tag

        args:
            qoute (Quote) : the Qoute object to add
            tags : the list of tags to associate with this Quote object
        '''
        if not tags:
            return
        for tag in tags:
            self.tags_dict[ tag ].append( quote )

    def add_quote( self, quote ):
        '''Add a quote to the database

        args:
            quote (str) : the quote to add
        '''
        def sanitize_text( txt, width=100 ):
            num_line = txt.count( '\n' )
            return textwrap.fill( txt, width=width ) if num_line < 2 else txt

        tags = None
        lines = quote.split( '\n' )
        if '[//]: #' in lines[ 0 ]:
            # Process the Markdown comment [//]: # (comment here)
            obj = re.match( r'^\[\/{2}\]: # \((.*)\)$', lines[ 0 ].rstrip() )
            assert obj, f'Unable to parse the comment\n{lines[ 0 ]}'
            tags = obj.group( 1 )
            tags = tags.split( ',' )
            tags = [ t.strip() for t in tags ]
            quote = '\n'.join( lines[ 1: ] )

        new_quotes = []
        if 'span style' in quote:
            lines = quote.split( '\n' )
            quote = '\n'.join( lines[ 1:-1 ] )
            new_quotes.append( quote )
        else:
            new_quotes.append( quote )

        for text in new_quotes:
            quote = Quote( sanitize_text( text ), tags )
            self.data.append( quote )
            self.add_tag( quote, tags )

    def run( self ):
        '''Load the quotes from the quote files'''
        with open( self.filename, "r", encoding="utf8" ) as quote_file:
            msg = ''
            for line in quote_file:
                if '# Quotes' in line:
                    # Skip the first line which is the filename.
                    # This is the requirement of MWeb Pro that I use to
                    # write the Markdown notes
                    pass
                elif line == '\n':
                    if msg != '':
                        # A blank new line means the end of the current quote.
                        self.add_quote( msg.rstrip() )
                        msg = ''
                elif line == "```\n":
                    # Ignore ``` which is a tag for the beginning or ending
                    # of a quoted text in markdown.
                    pass
                else:
                    msg += line
            if msg != '':
                # Handle the last quote in the file
                self.add_quote( msg.rstrip() )

    def print_quotes( self, all_quotes=False, tag=None ):
        '''Print quotes

        args:
            all (bool) : print all quotes if true; otherwise, randomly print
                one quote
            tag (str) : print only the quote with this tag
        '''
        if tag and tag in self.tags_dict:
            data = self.tags_dict[ tag ]
        else:
            data = self.data

        if all_quotes:
            color = Fore.YELLOW
            for text in data:
                print( f'{color}{text}' )
                color = Fore.GREEN if color == Fore.YELLOW else Fore.YELLOW
                print()
            print( Style.RESET_ALL )
        else:
            index = random.randint( 0, len( data ) - 1 )
            print( f'{Fore.YELLOW}{data[ index ]}{Style.RESET_ALL}' )

def parse_arguments():
    '''Parse the command line argument

    return:
        a parsed argparse namespace
    '''
    parser = argparse.ArgumentParser(description="Quote")
    parser.add_argument( "-t", "--tag", action="store",
                         help="Print only quotes with this tag" )
    parser.add_argument( "-a", "--all", action="store_true",
                         help="Print all quotes" )
    return parser.parse_args()

def main():
    '''The main function'''
    args = parse_arguments()
    quote_db = QuoteDB( QUOTE_FILENAME )
    quote_db.run()
    quote_db.print_quotes( all_quotes=args.all, tag=args.tag )

if __name__ == '__main__':
    main()
