#!/usr/bin/python3

import multiprocessing
import threading
import time

def func( number ):
    for i in range( 1, 10 ):
        time.sleep( 0.01 )
        #print( 'Thread ' + str( number ) + ': prints ' + str( number * i ) )
        print( 'Processing ' + str( number ) + ': prints ' + str( number * i ) )

all_processes = []

for i in range( 0, 3 ):
    #thread = threading.Thread( target=func, args=( i, ) )
    #thread.start()
    process = multiprocessing.Process( target=func, args=( i, ) )
    process.start()
    all_processes.append( process )

time.sleep( 0.03 )
for process in all_processes:
    process.terminate()
