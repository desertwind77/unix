#!/usr/bin/env python
import random

# Waht is the longest random walk you can take so that
# on average you end up 4 blocks for fewer from home?

def random_walk_2( n ):
    """Return coordinates after 'n' block random walk."""
    x, y = 0, 0
    for i in range( n ):
        ( dx, dy ) = random.choice( [ ( 0, 1 ), ( 0, -1 ), ( 1, 0 ), ( -1, 0 ) ] )
        x += dx
        y += dy
    return ( x, y )

number_of_walks = 10000

for walk_length in range( 1, 31 ):
    no_transport = 0    # Number of walks 4 or fewer blocks from home
    for i in range( number_of_walks ):
        ( x, y ) = random_walk_2( walk_length )
        distance = abs( x ) + abs( y )
        if distance <= 4:
            no_transport += 1
    no_transport_percentage = float( no_transport ) / number_of_walks
    text = 'Walk size = '
    text += str( walk_length )
    text += ' / % of no transport = '
    text += str( 100 * no_transport_percentage )
    print( text )
