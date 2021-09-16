#!/usr/bin/env python3

boolList = [ True, True ]
all( boolList )

myData = [ 2, 6, 4, 5, 8 ]
isAllEven = all( i % 2 == 0 for i in myData )
isEven = any( i % 2 == 0 for i in myData )
print( isAllEven )
print( isEven )
