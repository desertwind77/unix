# debuglib.py : utilities for debugging
import os
import pprint 
import shutil

debugLevel = 0

def setDebugLevel( level ):
    '''Set global debug level'''
    global debugLevel
    debugLevel = level

def trace( level, *args ):
    '''
    Print the message if current debug level is greater than 
    the debug level of the message
    '''
    if debugLevel >= level:
        for i in args:
            print i,
        print

def t0( *args ):
    '''Trace level 0'''
    trace( 0, *args )

def t1( *args ):
    '''Trace level 1'''
    trace( 1, *args ) 

def t2( *args ):
    '''Trace level 2'''
    trace( 2, *args ) 

def pprint_trace(level,  arg ):
    '''pprint guarded by debug level'''
    if debugLevel >= level:
        pprint.pprint( arg )

def pprint0( arg ):
    '''pprint_trace level 0'''
    pprint_trace( 0, arg );

def pprint1( arg ):
    '''pprint_trace level 1'''
    pprint_trace( 1, arg );
