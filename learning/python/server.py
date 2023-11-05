#!/usr/bin/env python3

import argparse
import socket
import sys

def process_argument() -> argparse.Namespace:
    '''Process command line arguments

    return:
        a parsed argparse namespace
    '''
    parser = argparse.ArgumentParser(description="server")
    parser.add_argument( "-p", "--port", default=1234, type=int )
    return parser.parse_args()

def start_server( port : int ) -> None:
    '''Start a UDP server that prints the incoming messages

    args:
        port (int) : listening port number
    '''
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.bind( ( 'localhost', port ) )
    sock.listen( 5 )

    try:
        while True:
            conn, _ = sock.accept()
            data = conn.recv( 1024 )
            while data:
                print( data.decode( 'utf-8' ) )
                data = conn.recv( 1024 )
    except KeyboardInterrupt:
        sock.close()

def main():
    '''Main function'''
    args = process_argument()
    start_server( args.port )

if __name__ == '__main__':
    main()
