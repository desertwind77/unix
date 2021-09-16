#!/usr/bin/python3

################### First-class function : consider function as an object #######################

def decorator_func1( msg ):
    def wrapper_func():
        print( msg )
    return wrapper_func

hi_func = decorator_func1( 'Hi' )
bye_func = decorator_func1( 'Bye' )

hi_func()
bye_func()

############################### Syntax 1 ####################################################

def decorator_func2( original_func ):
    def wrapper_func( *args, **kwargs ):
        print( 'wrapper executed this before {}'.format( original_func.__name__ ) )
        return original_func( *args, **kwargs )
    return wrapper_func

def display1():
    print( 'display function ran' )

decorated_display = decorator_func2( display1 )
decorated_display()

############################### Syntax 2 ####################################################

@decorator_func2
def display2():
    print( 'display function ran' )

display2()

########################### Passing arguments ##########################################

@decorator_func2
def display_info1( name, age ):
    print( 'display_info ran with arguments ( {}, {} )'.format( name, age ) )

display_info1( 'John', 25 )

############################# Class decorator ########################################

class decorator_class( object ):
    def __init__( self, original_func ):
        self.original_func = original_func

    def __call__( self, *args, **kwargs ):
        print( 'call method executed this before {}'.format( self.original_func.__name__ ) )
        return self.original_func( *args, **kwargs )

@decorator_class
def display_info2( name, age ):
    print( 'display_info ran with arguments ( {}, {} )'.format( name, age ) )

display_info2( 'John', 25 )

########################## Real use case and chained decorators #########################
from functools import wraps

def my_logger( orig_func ):
    import logging 

    logging.basicConfig( filename='{}.log'.format( orig_func.__name__ ), level=logging.INFO )

    @wraps( orig_func ) 
    def wrapper( *args, **kwargs ):
        logging.info( 'Ran with args: {}, and kwargs: {}'.format( args, kwargs ) )
        return orig_func( *args, **kwargs )

    return wrapper

def my_timer( orig_func ):
    import time

    @wraps( orig_func ) 
    def wrapper( *args, **kwargs ):
        t1 = time.time()
        result = orig_func( *args, **kwargs )
        t2 = time.time() - t1
        print( '{} ran in: {} sec'.format( orig_func.__name__, t2 ) )

    return wrapper

@my_logger
@my_timer
def display_info3( name, age ):
    import time
    time.sleep( 1 ) 
    print( 'display_info3 ran with arguments ( {}, {} )'.format( name, age ) )

display_info3( 'Hank', 30 )
