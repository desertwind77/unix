#!/usr/bin/env python3

def toDecimal( num, base ):
   '''2 <= base <= 10'''
   result = 0
   multiplier = 1

   while num > 0:
      result += ( num % 10 ) * multiplier
      multiplier *= base
      num = int( num / 10 )
   return result

def fromDecimal( num, base ):
   '''2 <= base <= 10'''
   result = 0
   multiplier = 1

   while num > 0:
      result += ( num % base ) * multiplier
      multiplier *= 10 
      num = int( num / base )
   return result

def fromDecimal2( num, base ):
   '''2 <= base <= 20'''
   chars = '0123456789ABCDEFGHIJ'
   result = ''

   while num > 0:
      result = chars[ num % base ] + result
      num = int( num / base )
   return result

if __name__ == '__main__':
   assert toDecimal( 101011, 2 ) == 43
   assert fromDecimal( 43, 2 ) == 101011
   assert fromDecimal2( 1435, 16 ) == '59B' 
