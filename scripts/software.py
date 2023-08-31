#!/usr/bin/env python3
'''
Install packages on different OSs
'''

import argparse

from genutils import load_config

CONFIG_FILENAME='config/software.json'

def process_arguments():
    return None

def main():
    '''The main function'''
    config = load_config( CONFIG_FILENAME )
    args = process_arguments
    platform = 'MacOS'
    platform_config = config[ 'Platforms' ][ platform ]
    command = platform_config[ 'command' ]
    packages = platform_config[ 'packages' ]
    packages = ' '.join( packages )
    print( command, packages )

if __name__ == '__main__':
    main()
