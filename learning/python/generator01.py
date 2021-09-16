#!/usr/bin/env python
# Storing a huge list takes a lot of memory.
# Generator creates an item on demand.
#
# Difference between range and xrange:
# - range returns a list.
# - xrange returns a generator.

nums = [ 1, 2, 3, 4, 5 ]
def square_num( nums ):
    for n in nums:
        yield ( n * n )

square1 = square_num( nums )
print( square1 )
for _ in nums:
    print( next( square1 ) )

square2 = ( i * i for i in nums )
print( square2 )
for i in square2:
    print( i )

nums2 = list( square2 )
print( nums2 )

square3 = square_num( nums )
nums3 = list( square3 )
print( nums3 )
