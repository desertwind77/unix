#!/usr/bin/env python3

from functools import cache, lru_cache

@cache
def fib1( n ):
   if n <= 1:
      return n
   return fib1( n - 1 ) + fib1( n - 2 )

@lru_cache( maxsize = 5 )
def fib2( n ):
   if n <= 1:
      return n
   return fib2( n - 1 ) + fib2( n - 2 )

def main():
   for i in range( 400 ):
      #print( i, fib1( i ) )
      print( i, fib2( i ) )
   print( "done" )

main()
