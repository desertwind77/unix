#!/usr/bin/env python
import heapq

li = [ 5, 7, 9, 1, 3 ]
heapq.heapify( li )
print( "The created heap is : ", li )
heapq.heappush( li, 4 )
print( "The modified heap after push is : ", li )
print( "The smallest element is : ", heapq.heappop( li ) )

li1 = [5, 7, 9, 4, 3]
li2 = li1[:]
heapq.heapify( li1 )
heapq.heapify( li2 )
print()
print( "original      : ", li1 )
# push 2 and then pop the smallest
heapq.heappushpop( li1, 2 )
print( "heappushpop 2 : ", li1 )
# replace the smallest with 2
heapq.heapreplace( li2, 2 )
print( "heapreplace 2 : ", li2 )

li3 = [6, 7, 9, 4, 3, 5, 8, 10, 1]
heapq.heapify( li3 )
print()
print( "Original                   : ", li3 )
print( "The 3 largest numbers are  : ", heapq.nlargest( 3, li3 ) )
print( "The 3 smallest numbers are : ", heapq.nsmallest( 3, li3 ) )
