#!/usr/bin/env python3
'''
A script to randomly print a word from custom dictionary

TODO:
1) games : fill in the gaps, match words and its meaning
2) Python GUI
3) Mobile App
4) Native Mac App
'''
from collections import namedtuple
import argparse
import os
import random

# pylint: disable=import-error
from colorama import Fore, Style
import yaml

from genutils import check_if_file_exists

CONFIG_FILENAME = 'config/vocabuary.yaml'

Pattern = namedtuple( 'Pattern', [ 'src', 'dst' ] )

def load_vocabuary( filename ):
    '''Load the vocabuary from a file'''
    script_path = os.path.realpath( os.path.dirname( __file__ ) )
    filename = os.path.join( script_path, filename )
    check_if_file_exists( filename )

    output = None
    with open( filename, 'r', encoding='utf-8' ) as yaml_file:
        output = yaml.safe_load( yaml_file )
    return output

def sanitize_text( txt ):
    '''Clean up text'''
    replacement = [
        Pattern( '\(', '(' ),
        Pattern( '\)', ')' ),
        Pattern( '\\"', '"' ),
    ]
    for pattern in replacement:
        txt = txt.replace( pattern.src, pattern.dst )
    return txt

def print_word( vocab, all_words=False ):
    '''Print a word'''
    tab = '   '
    keys = sorted( vocab.keys() )
    if all_words:
        words = keys
    else:
        index = random.randint( 0, len( keys ) - 1 )
        words = [ keys[ index ] ]

    for word in words:
        print( Fore.RED + f'{sanitize_text( word )}:' )
        for meaning, examples in vocab[ word ].items():
            print( Fore.GREEN + f'{tab}{sanitize_text( meaning ) }:' )
            if not examples:
                continue
            for example in examples:
                print( Fore.CYAN + f'{tab}{tab}{sanitize_text( example ) }' )
    print( Style.RESET_ALL )

def process_arguments():
    '''Process the command line arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument( '-a', '--all', action='store_true',
                         help='Print all words in the dictionary' )
    return parser.parse_args()

def main():
    '''The main function'''
    args = process_arguments()
    vocab = load_vocabuary( CONFIG_FILENAME )
    print_word( vocab, all_words=args.all )

if __name__ == '__main__':
    main()
