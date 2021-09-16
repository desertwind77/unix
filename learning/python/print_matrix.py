#!/usr/bin/env python3
ROW = COL = 10

def initMatrix():
   matrix = []
   for i in range( 0, ROW ):
      row = []
      for j in range( 0, COL ):
         row.append( i * COL + j )
      matrix.append( row )
   return matrix

def printMatrix( matrix ):
   for i in range( 0, ROW ):
      for j in range( 0, COL ):
         r = i
         c = j
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def printDiagonal1( matrix ):
   # 0   0-0
   # 1   1-0 0-1
   # 2   2-0 1-1 0-2
   # 3   3-0 2-1 1-2 0-3
   # 4   4-0 3-1 2-2 1-3 0-4
   # 5   5-0 4-1 3-2 2-3 1-4 0-5
   # ...
   for i in range( 0, ROW ):
      for j in range( 0, i + 1 ):
         r = i - j
         c = j
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def printDiagonal2( matrix ):
   # 0   9-0 8-1 7-2 6-3 5-4 4-5 3-6 2-7 1-8 0-9
   # 1   8-0 7-1 6-2 5-3 4-4 3-5 2-6 1-7 0-8
   # 2   7-0 6-1 5-2 4-3 3-4 2-5 1-6 0-7
   # 3   6-0 5-1 4-2 3-3 2-4 1-5 0-6
   # 4   5-0 4-1 3-2 2-3 1-4 0-5
   # ...
   for i in range( 0, ROW ):
      index = ROW - 1 - i
      for j in range( 0, index + 1 ):
         r = index - j
         c = j
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def printDiagonal3( matrix ):
   # 0   9-0 8-1 7-2 6-3 5-4 4-5 3-6 2-7 1-8 0-9
   # 1   9-1 8-2 7-3 6-4 5-5 4-6 3-7 8-2 1-9
   # 2   9-2 8-3 7-4 6-5 5-6 4-7 3-8 2-9
   # 3   9-3 8-4 7-5 6-6 5-7 4-8 3-9
   # 4   9-4 8-5 7-6 6-7 5-8 4-9
   # ...
   for i in range( 0, ROW ):
      index = ROW - 1 - i
      for j in range( 0, index + 1 ):
         r = ROW - 1 - j
         c = j + i
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def printDiagonal4( matrix ):
   # 0   9-9
   # 1   9-8 8-9
   # 2   9-7 8-8 7-9
   # 3   9-6 8-7 7-8 6-9
   # 4   9-5 8-6 7-7 6-8 5-9
   # 5   9-4 8-5 7-6 6-7 5-8 4-9
   # ...
   for i in range( 0, ROW ):
      # i is running from 0 - 9
      # index is running from 9 - 0
      index = ROW - 1 - i
      for j in range( 0, i + 1 ):
         r = ROW - 1 - j
         c = index + j
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def printDiagonal5( matrix ):
   # 0   0-0
   # 1   1-0 1-1
   # 2   2-0 2-1 2-2
   # 3   3-0 3-1 3-2 3-3
   # 4   4-0 4-1 4-2 4-3 4-4
   # ..
   for i in range( 0, ROW ):
      for j in range( 0, i + 1 ):
         r = i
         c = j
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def printDiagonal6( matrix ):
   # 0   0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9
   # 1   1-0 2-1 3-2 4-3 5-4 6-5 7-6 8-7 9-8
   # 2   2-0 3-1 4-2 5-3 6-4 7-5 8-6 9-7
   # 3   3-0 4-1 5-2 6-3 7-4 8-5 9-6
   # 4   4-0 5-1 6-2 7-3 8-4 9-5
   # ..
   for i in range( 0, ROW ):
      index = ROW - 1 - i
      for j in range( 0, index + 1 ):
         r = i
         c = j
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def printDiagonal7( matrix ):
   # 0   0-0 1-1 2-2 3-3 4-4 5-5 6-6 7-7 8-8 9-9
   # 1   0-1 1-2 2-3 3-4 4-5 5-6 6-7 7-8 8-9
   # 2   0-2 1-3 2-4 3-5 4-6 5-7 6-8 7-9
   # 3   0-3 1-4 2-5 3-6 4-7 5-8 6-9
   # 4   0-4 1-5 2-6 3-7 4-8 5-9
   # ..
   for i in range( 0, ROW ):
      index = ROW - 1 - i
      for j in range( 0, index + 1 ):
         r = j
         c = i + j
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def printDiagonal8( matrix ):
   # 0   0-9
   # 1   0-8 1-9
   # 2   0-7 1-8 2-9
   # 3   0-6 1-7 2-8 3-9
   # 4   0-5 1-6 2-7 3-8 4-9
   # 5   0-4 1-5 2-6 3-7 4-8 5-9
   # ..
   for i in range( 0, ROW ):
      index = ROW - 1 - i
      for j in range( 0, i + 1 ):
         r = j
         c = index - i
         print( "%02d" % matrix[ r ][ c ], end=" " )
      print()

def main():
   matrix = initMatrix()
   printMatrix( matrix )
   print()
   printDiagonal1( matrix )
   printDiagonal2( matrix )
   print()
   printDiagonal3( matrix )
   printDiagonal4( matrix )
   print()
   printDiagonal5( matrix )
   printDiagonal6( matrix )
   print()
   printDiagonal7( matrix )
   printDiagonal8( matrix )

if __name__ == '__main__':
   main()
