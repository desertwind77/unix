#!/usr/bin/env python3
import math

def sieve2( n ):
   primes = [ True ] * ( n + 1 )
   primes[ 0 ] = primes[ 1 ] = False

   for i in range( 2, n + 1 ):
      multiplier = 2
      while i * multiplier <= n:
         primes[ i * multiplier ] = False
         multiplier += 1

   answer = [ i for i in range( 2, n + 1 ) if primes[ i ] ]
   return answer

def sieve( n ):
   primes = [ True ] * ( n + 1 )
   primes[ 0 ] = primes[ 1 ] = False
   m = int( math.sqrt( n ) )

   for i in range( 2, m + 1 ):
      if primes[ i ]:
         k = i * i
         while k <= n:
            primes[ k ] = False
            k += i

   answer = [ i for i in range( 2, n + 1 ) if primes[ i ] ]
   return answer

if __name__ == '__main__':
   answer = sieve( 20 )
   print( answer )
