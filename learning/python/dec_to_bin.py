#!/usr/bin/env python3

def decToBin( number, fill=0 ):
    output = None
    if fill != 0:
        output = "{0:{filler}{fill}b}".format( 10, filler='0', fill=fill )
    else:
        output = "{0:b}".format( 10 )
    return output

print( decToBin( 10 ) )
print( decToBin( 10, fill=8 ) )
input = [ 22, 25, 28, 29, 30, 31, 44, 45 ]
for i in input:
    print( i, decToBin( i, fill=7 ) )
