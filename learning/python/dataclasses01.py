#!/usr/bin/env python3
'''
dataclass module is introduced in Python 3.7 as a utility tool to make structured
classes specially for storing data. These classes hold certain properties and
functions to deal specifically with the data and its representation

For exmaple, use Comment instead of implementing all method in ManualCommont.
'''

import dataclasses
import inspect
from dataclasses import dataclass, field
from pprint import pprint

class ManualCommont:
   def __init__( self, id: int, text: str ):
      self.__id : int = id
      self.__text : str = text

   # This is readable but not writable
   @property
   def id( self ):
      return self.__id

   # This is readable but not writable
   @property
   def text( self ):
      return self.__text

   def __repr__( self ):
      return "{}(id={}, text={})".format( self.__class__.__name__,
                                          self.id, self.text )

   def __eq__( self, other ):
      if other.__class__ is self.__class__:
         return ( self.id, self.text ) == ( other.id, other.text )
      else:
         return NotImplemented

   def __ne__( self, other ):
      result = self.__eq__( other )
      if result is NotImplemented:
         return NotImplemented
      else:
         return not result

   def __hash__( self ):
      return hash( ( self.__class__, self.id, self.text ) )

   def __lt__( self, other ):
      if other.__class__ is self.__class__:
         return ( self.id, self.text ) < ( other.id, other.text )
      else:
         return NotImplemented

   def __le__( self, other ):
      if other.__class__ is self.__class__:
         return ( self.id, self.text ) <= ( other.id, other.text )
      else:
         return NotImplemented

   def __gt__( self, other ):
      if other.__class__ is self.__class__:
         return ( self.id, self.text ) > ( other.id, other.text )
      else:
         return NotImplemented

   def __ge__( self, other ):
      if other.__class__ is self.__class__:
         return ( self.id, self.text ) >= ( other.id, other.text )
      else:
         return NotImplemented

@dataclass( frozen=True, order=True )
class Comment:
   """A class for holding data"""
   # Attributes Declaration
   # using Type Hints
   id : int = field()
   text : str = field( default="" )
   # replies : list[ int ] = []
   # We don't want all instances of Comment to share the defaul list
   # if it is not passed it.
   # repr = False    We don't want this field to show when printed
   # compare = False We don't want to use this field in comparison
   replies : list[ int ] = field( default_factory=list, repr=False, compare=False )

def main():
   # Create a Comment object
   comment = Comment( 1, "I just subscribed!" )
   # id is immutable
   # comment.id = 3
   print( comment )
   print( dataclasses.astuple( comment ) )
   print( dataclasses.asdict( comment ) )
   copy = dataclasses.replace( comment, id = 3 )
   print( copy )

   pprint( inspect.getmembers( Comment, inspect.isfunction ) )

if __name__ == '__main__':
   main()
