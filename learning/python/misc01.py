#!/usr/bin/env python3

def namedtuple_example():
    from collections import namedtuple

    Car = namedtuple( 'Car', 'color mileage' )
    my_car = Car( 'red', 3812.4 )
    print( my_car )
    print( my_car.color )
    print( my_car.mileage )

    # Like tuples, namedtuples are immutable
    #my_car.color = 'blue'

def combining_two_dict():
    x = { 'a' : 1, 'b' : 2 }
    y = { 'b' : 3, 'c' : 4 }
    # Python 3.5+
    z = { **x, **y }
    # Python 2.x
    #z = dict( x, **y )
    print( z )

def any_example():
    x, y, z = 0, 1, 0

    if x == 1 or y == 1 or z == 1:
        print( 'passed' )
    if 1 in ( x, y, z ):
        print( 'passed' )
    if x or y or z:
        print( 'passed' )
    if any( ( x, y, z ) ):
        print( 'passed' )

def sort_dict_by_value():
    x = { 'a' : 4, 'b' : 3, 'c' : 2, 'd' : 1 }
    sorted( x.items(), key=lambda x: x[1] )
    import operator
    sorted( x.items(), key=operator.itemgetter( 1 ) )

def function_argument_unpack():
    def myfunc( x, y, z ):
        print( x, y, z )

    tuple_vec = ( 1, 0, 1 )
    dict_vec = { 'x': 1, 'y': 0, 'z': 1 }
    myfunc( *tuple_vec )
    myfunc( **dict_vec )

def measure_time():
   import timeit
   time = timeit.timeit( '"-".join( str( n ) for n in range( 100 ) )', number=10000 )
   print( time )

def print_binary():
   for i in range( 64 ):
      print( "Decimal: %2s" % i, "Binary: {0:06b}".format( i ) )

namedtuple_example()
combining_two_dict()
any_example()
sort_dict_by_value()
function_argument_unpack()
measure_time()
print_binary()
