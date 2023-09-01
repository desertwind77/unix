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
import re

# pylint: disable=import-error
from colorama import Fore, Style
import yaml

from genutils import check_if_file_exists

CONFIG_FILENAME = 'config/vocabulary.yaml'

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
        Pattern( '\\"', '"' ),
        Pattern( '{', '' ),
        Pattern( '}', '' ),
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
        print( f'Dictionary size = { len( words ) } words' )
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
                if '\{' in example and '\}' in example:
                    example = example.replace( '\{', '{' )
                    example = example.replace( '\}', '}' )
                begin_index = example.find( '{' )
                end_index = example.find( '}' )
                if begin_index == -1 or end_index == -1:
                    print( Fore.CYAN + f'{tab}{tab}{sanitize_text( example ) }' )
                else:
                    begin = sanitize_text( example[ 0 : begin_index ] )
                    middle = sanitize_text( example[ begin_index : end_index + 1 ] )
                    end = sanitize_text( example[ end_index + 1 : ] )
                    print( f'{tab}{tab}', end='' )
                    print( Fore.CYAN + f'{begin}', end='' )
                    print( Fore.YELLOW + f'{middle}', end='' )
                    print( Fore.CYAN + f'{end}' )
    print( Style.RESET_ALL )

def game_fill_in_word( vocab ):
    '''Game to fill a word in the blank'''
    def get_word( vocab ):
        word, word_info  = random.choice( list( vocab.items() ) )
        # FIXME: development
        word = 'aquit'
        word_info = vocab[ word ]
        meaning = random.choice( list( word_info.keys() ) )
        example = random.choice( word_info[ meaning ] )
        return word, meaning, example

    def get_multiple_choices( vocab, word ):
        # Select three multiple choices
        cindices = list( random.sample( range( 0, len( vocab ) - 1 ), 4 ) )
        choices = [ sorted( vocab.keys() )[ i ] for i in cindices ]
        if word not in choices:
            choices.append( word )
        random.shuffle( choices )
        return choices

    word, meaning, example = get_word( vocab )
    choices = get_multiple_choices( vocab, word )

    obj = re.search( r'.*({.*}).*', example )
    if not obj:
        assert False, example
    pattern = obj.group( 1 )
    blank = '_' * len( pattern )
    print( f'Question : {example.replace( pattern, blank )}\n' )
    print( f'Meaning  : {meaning}\n' )
    print(  'Answer   :' )
    for choice in choices:
        print( f'* {choice}' )

def process_arguments():
    '''Process the command line arguments'''
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers( dest='command' )
    subparser.required = True

    show_parser = subparser.add_parser( 'show',
            help='Print a word from the dictionary' )
    show_parser.add_argument( '-a', '--all', action='store_true',
            help='Print all words in the dictionary' )

    fill_parser = subparser.add_parser( 'fill',
            help='Play the game to fill in the blank' )

    return parser.parse_args()

def main():
    '''The main function'''
    args = process_arguments()
    vocab = load_vocabuary( CONFIG_FILENAME )

    if args.command == 'show':
        print_word( vocab, all_words=args.all )
    elif args.command == 'fill':
        game_fill_in_word( vocab )

if __name__ == '__main__':
    main()
