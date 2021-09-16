#!/usr/bin/python3

import time
import threading

class MyThread( threading.Thread ):
    def __init__( self, *args, **kwargs ):
        super( MyThread, self ).__init__( *args, **kwargs )
        self.stopFlag = threading.Event()

    def stop( self ):
        self.stopFlag.set()

    def stopped( self ):
        return self.stopFlag.isSet()

    def run( self ):
        while True:
            if self.stopped():
                return
            print( 'Hello, world!' )
            time.sleep( 1 )

t1 = MyThread()
t1.start()
time.sleep( 5 )
t1.stop()
t1.join()
