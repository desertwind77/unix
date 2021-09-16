#!/usr/bin/env python
import random

# Waht is the longest random walk you can take so that
# on average you end up 4 blocks for fewer from home?

def random_walk( n ):
    """Return coordinates after 'n' block random walk."""
    x = 0
    y = 0
    for i in range( n ):
        step = random.choice( [ 'N', 'S', 'E', 'W' ] )
        if step == 'N':
            y += 1
        elif step == 'S':
            y -= 1
        elif step == 'E':
            x += 1
        else:
            x -= 1
    return ( x, y )

for i in range( 25 ):
    walk = random_walk( 10 )
    text = str( walk )
    text += ' Distance from home = '
    text += str( abs( walk[ 0 ] ) + abs( walk[ 1 ] ) )
    print( text )
