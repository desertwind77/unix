#!/usr/bin/env python3
'''
Deque is preferred over list in the cases where we need quicker append and pop
operations from both the ends of container, as deque provides an O(1) time complexity
for append and pop operations as compared to list which provides O(n) time
complexity.
'''
from collections import deque
print( deque() )
print( deque( [ 'a', 'b', 'c' ] ) )
print( deque( 'abc' ) )
print( deque( [ { 'data' : 'a' }, { 'data' : 'b' } ] ) )

llist = deque( 'abcde' )
print( llist )
llist.append( 'f' )
print( llist )
llist.pop()
print( llist )
llist.appendleft( 'z' )
print( llist )
llist.popleft()
print( llist )

queue = deque()
queue.append( "Mary" )
queue.append( "John" )
queue.append( "Susan" )
print( queue )
print( queue.popleft() )
print( queue.popleft() )
print( queue.popleft() )
