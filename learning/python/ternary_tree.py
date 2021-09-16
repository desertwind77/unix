#!/usr/bin/env python3
# My mistakes
# 1) Not checking if self.left, self.right and self.center are None before performing
#     operation on them
# 2) Not considering all cases (in if-else statements)
# 3) Not checking if string is None before doing concatenation
# 4) Assume that it will be easy and jump into the conclusion to quickly. I should
#     think carefully. For example, I assume autocomplete will be a piece of cake
#     once I finish prefixSearch
class TernaryTree:
   def __init__( self ):
      self.data = None
      self.isEndOfWord = False
      self.left = self.center = self.right = None

   def insert( self, word ):
      if self.data:
         if self.data == word[ 0 ]:
            assert( self.center )
            if len( word ) > 1:
               self.center.insert( word[ 1: ] )
            else:
               self.center.isEndOfWord = True
         elif self.data > word[ 0 ]:
            if not self.left:
               self.left = TernaryTree()
            self.left.insert( word )
         else:
            if not self.right:
               self.right = TernaryTree()
            self.right.insert( word )
      else:
         self.data = word[ 0 ]
         self.center = TernaryTree()
         if len( word ) > 1:
            self.center.insert( word[ 1: ] )
         else:
            self.center.isEndOfWord = True

   def prefixSearch( self, word ):
      if not word:
         return None
      if self.data == word[ 0 ]:
         if len( word ) == 1:
            return self
         else:
            return self.center.prefixSearch( word[ 1: ] )
      elif self.data > word[ 0 ]:
         if self.left:
            return self.left.prefixSearch( word )
      else:
         if self.right:
            return self.right.prefixSearch( word )
      return None

   def search( self, word ):
      result = self.prefixSearch( word )
      if result:
         return self.center.isEndOfWord
      return False

   def display( self, prefix='' ):
      result = []
      if self.isEndOfWord:
         result.append( prefix )
      if not self.data:
         return result
      if self.left:
         result += self.left.display( prefix=prefix )
      if self.center:
         nextPrefix = prefix + self.data if prefix else self.data
         result += self.center.display( prefix=nextPrefix )
      if self.right:
         result += self.right.display( prefix=prefix )
      return result

   def autoComplete( self, prefix='' ):
      result = []
      if prefix:
         node = self.prefixSearch( prefix )
         if node and node.center:
            result = node.center.display( prefix )
      else:
         result = self.display()
      return result

   def delete( self, word ):
      if not self.data:
         return
      elif self.data == word[ 0 ]:
         assert( self.center )
         if len( word ) == 1:
            if self.center.data:
               self.center.isEndOfWord = False
            else:
               self.center = None
               if not any( [ self.left, self.center, self.right ] ):
                  self.data = None
         else:
            self.center.delete( word[ 1: ] )
      elif self.data > word[ 0 ]:
         if self.left:
            self.left.delete( word )
            if not self.left.data:
               self.left = None
      else:
         if self.right:
            self.right.delete( word )
            if not self.right.data:
               self.right = None

def main():
   presentList = [ 'c', 'cat', 'cabbage', 'caution', 'capture', 'there', 'baby',
                   'babybloomer', 'therefore' ]
   notPresentList = [ 'hello', 'world', 'a', 'z' ]

   tree = TernaryTree()
   for i in presentList:
      tree.insert( i )
   for i in presentList:
       if not tree.search( i ):
          print( '%s is not found' % i )
          assert( False )
   for i in notPresentList:
      assert( not tree.search( i ) )

   print( tree.display() )
   print( tree.autoComplete() )
   for i in [ 'c', 'ca', 'ba' ]:
      print( "--- Autocomplete '%s' ---" % i )
      print( tree.autoComplete( prefix=i ) )

   for i in notPresentList:
      tree.delete( i )
   for i in presentList:
      print( "--- Deleting '%s' ---" % i )
      tree.delete( i )
      print( tree.display() )

if __name__ == "__main__":
   main()

