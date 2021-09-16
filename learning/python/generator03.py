#!/usr/bin/env python3

fib = None 

def calculate_fibonnaci( num ):
    global fib
    fib = {}
    i = 0
    while i <= num:
        if i == 0:
            fib[ i ] = 0
        elif i == 1:
            fib[ i ] = 1
        else:
            fib[ i ] = fib[ i - 1 ] + fib[ i - 2 ]
        i += 1

def fibonacci( num ):
    '''
    Generate Fibonacci series up to n
    '''
    global fib
    if not fib:
        calculate_fibonnaci( num )
    for i in range( num + 1 ):
        yield fib[ i ]

series = fibonacci( 10 )
print( list( series ) )
