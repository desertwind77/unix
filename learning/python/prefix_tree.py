#!/usr/bin/env python3

class PrefixTree:
   def __init__( self ):
      self.children = {}
      self.isEndOfWord = False

   def insert( self, word ):
      if not word:
         return

      firstChar = word[ 0 ]
      if firstChar not in self.children:
         self.children[ firstChar ] = PrefixTree()

      if len( word ) > 1:
         self.children[ firstChar ].insert( word[ 1: ] )
      else:
         self.children[ firstChar ].isEndOfWord = True

   def delete( self, word ):
      if not word:
         return False

      firstChar = word[ 0 ]
      if firstChar not in self.children:
         # This string is not in the prefix tree
         return False
      node = self.children[ firstChar ]

      if len( word ) == 1:
         if not node.isEndOfWord:
            # This string is not in the prefix tree
            return False
         node.isEndOfWord = False
         if len( node.children ) == 0:
            del self.children[ firstChar ]
            return True
         return False
      else:
         if node.delete( word[ 1: ] ):
            if len( node.children ) == 0:
               del self.children[ firstChar ]
               return True
         return False

   def prefixSearch( self, word='' ):
      if not word:
         return None

      firstChar = word[ 0 ]
      if firstChar not in self.children:
         return None
      else:
         if len( word ) == 1:
            return self.children[ firstChar ]
         else:
            return self.children[ firstChar ].prefixSearch( word[ 1: ] )
      return None

   def search( self, word ):
      node = self.prefixSearch( word )
      if node and node.isEndOfWord:
         return True
      return False

   def display( self, prefix='' ):
      # This is equivalent to sorting array of string
      result = []
      if self.isEndOfWord:
         result.append( prefix )
      for key in sorted( self.children.keys() ):
         result += self.children[ key ].display( prefix=prefix+key )
      return result

   def autoComplete( self, prefix='' ):
      result = []
      node = self.prefixSearch( prefix )
      if node:
         result = node.display( prefix=prefix )
      else:
         result = self.display()
      return result

def main():
   presentList = [ 'the', 'a', 'there', 'answer', 'any', 'by', 'bye', 'their' ]
   notPresentList = [ 'hello', 'world', 'b', 'c' ]

   tree = PrefixTree()
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

   for i in [ 'a', 'b', 'th' ]:
      print( "--- Autocomplete '%s' ---" % i )
      print( tree.autoComplete( prefix=i ) )

   for i in notPresentList:
       tree.delete( i )
   for i in presentList:
      print( "--- Deleteing '%s' ---" % i )
      tree.delete( i )
      print( tree.display() )

if __name__ == '__main__':
   main()
