#!/usr/bin/python3

def foo( required, *args, **kwargs ):
    print( required )
    if args:
        print( args )
    if kwargs:
        print( kwargs )

foo( 'hello' )
print()
foo( 'hello', 1, 2, 3 )
print()
foo( 'hello', 1, 2, 3, key1="value", key2=999 )
print()

def foo2( x, *args, **kwargs ):
    kwargs[ 'name' ] = 'Alice'
    # args is a tuple which is immutable
    new_args = args + ( 'extra', )
    foo( x, *new_args, **kwargs )

foo2( 'world', 4, 5, 6, key1='value1', key2='value2' )

class Car:
    def __init__( self, color, mileage ):
        self.color = color
        self.mileage = mileage

class AlwaysBlueCar( Car ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.color = 'blue'
