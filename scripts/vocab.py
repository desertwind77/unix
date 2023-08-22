#!/usr/bin/env python3
'''A script to randomly print a word from custom dictionary'''
import os
import random

# pylint: disable=import-error
from colorama import Fore, Style
import yaml

from genutils import check_if_file_exists

CONFIG_FILENAME = 'config/vocabuary.yaml'

def load_vocabuary( filename ):
    '''Load the vocabuary from a file'''
    script_path = os.path.realpath( os.path.dirname( __file__ ) )
    filename = os.path.join( script_path, filename )
    check_if_file_exists( filename )

    output = None
    with open( filename, 'r', encoding='utf-8' ) as yaml_file:
        output = yaml.safe_load( yaml_file )
    return output

def print_word( vocab, all_words=False ):
    '''Print a word'''
    keys = sorted( vocab.keys() )
    if all_words:
        words = keys
    else:
        index = random.randint( 0, len( keys ) - 1 )
        words = [ keys[ index ] ]

    for word in words:
        print( Fore.RED + f'{keys[ index ]}:' )
        for meaning, examples in vocab[ word ].items():
            print( Fore.GREEN + f'   {meaning}:' )
            if not examples:
                continue
            for example in examples:
                print( Fore.CYAN + f'      {example}' )
    print( Style.RESET_ALL )

#TODO: options to pring all words, games, python gui, mobile app, mac app

def main():
    '''The main function'''
    vocab = load_vocabuary( CONFIG_FILENAME )
    print_word( vocab )

if __name__ == '__main__':
    main()
