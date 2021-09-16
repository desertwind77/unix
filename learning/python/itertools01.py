#!/usr/bin/env python3

import itertools

target = 10
# counter = 0
# while True:
#    counter += 1
#    print( counter )
#    if counter == target:
#       break
#
# Problem with this is that target cannot change in the loop
# for counter in range( 0, target ):
#    print( counter )
#
# This is better because we don't have to worry about start, step and increment
for counter in itertools.count( start=0, step=1 ):
   if counter > target:
      break
   print( counter )

#---------------------------------------------------------
ex_list = [ 'a', 'b', 'c' ]
loop_round = 3

# Nested loop
# for i in range( loop_round ):
#    for j in range( len( ex_list ) ):
#       print( ex_list[ j ] )
#
# Hard to read
# for i in range( loop_round * len( ex_list ) ):
#    print( ex_list[ i % len( ex_list ) ] )

counter = 0
for ex_char in itertools.cycle( ex_list ):
   if counter == loop_round * len( ex_list ):
      break
   print( ex_char )
   counter += 1

#---------------------------------------------------------

word = 'stackpython'
# for i in range( loop_round ):
#    print( word )

for word in itertools.repeat( word, times=loop_round ):
   print( word )

#---------------------------------------------------------
list_a = [ 1, 2, 3 ]
list_b = [ 4, 5, 6 ]
list_c = [ 7, 8, 9 ]
# Waste memeory and CPU esp when lists are large
# for item in list_a + list_b + list_c:
#    print( item )

looper = itertools.chain( list_a, list_b, list_c )
for item in looper:
   print( item )

#---------------------------------------------------------
name = [ 'Thomas', 'John', 'Sam' ]
attendance = [ False, True, True ]
# attended = [ name[ i ] if attendance[ i ] else '' for i in range( len( name ) ) ]
# attended = [ curName for curName in attended if curName != '' ]
looper = itertools.compress( name, attendance )
attended = [ name for name in looper ]
print( 'Name of attendance are ' + ', '.join( attended ) )

#---------------------------------------------------------
compressed_words = [ 0, 0, 0, 0, 1, 1, 1, 0, 1 ]
is_ended = False
drop_condition = 0
word_count = 0
# Skip all the leading 0
# for word in compressed_words:
#    if is_ended is False and word != drop_condition:
#       is_ended = True
#    if is_ended:
#       print( compressed_words[ word_count ] )
#    word_count += 1
for word in itertools.dropwhile( lambda x : x == 0, compressed_words ):
   print( word )
