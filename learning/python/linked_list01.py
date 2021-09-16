#!/usr/bin/env python3

class Node:
   def __init__( self, data ):
      self.data = data
      self.next = None
      self.prev = None

   def __repr__( self ):
      return self.data

class LinkedList:
   def __init__( self, nodes=None ):
      self.head = None
      if nodes is not None:
         node = Node( data=nodes.pop( 0 ) )
         self.head = node
         for elem in nodes:
            node.next = Node( data=elem )
            node = node.next

   def __repr__( self ):
      node = self.head
      nodes = []
      while node is not None:
         nodes.append( node.data )
         node = node.next
      nodes.append( "None" )
      return "->".join( nodes )

   def __iter__( self ):
      node = self.head
      while node is not None:
         yield node
         node = node.next

   def add_first( self, node ):
      node.next = self.head
      self.head = node

   def add_last( self, node ):
      if self.head is None:
         self.head = node
         return

      # cur = self.head
      # while cur.next is not None:
      #    cur  = cur.next
      # cur.next = node
      for cur in self:
         pass
      cur.next = node

   def add_after( self, data, newNode ):
      if self.head is None:
         raise Exception( 'List is empty' )

      for node in self:
         if node.data == data:
            newNode.next = node.next
            node.next = newNode
            return

      raise Exception( "Node with data '%s' not found" % data )

   def add_before( self, data, newNode ):
      if self.head is None:
         raise Exception( 'List is empty' )

      if self.head.data == data:
         newNode = self.head.next
         self.head.next = newNode

      prev = self.head
      for node in self:
         if node.data == data:
            prev.next = newNode
            newNode.next = node
            return
         prev = node

      raise Exception( "Node with data '%s' not found" % data )

   def remove( self, data ):
      if self.head is None:
         return
      elif self.head.data == data:
         self.head = self.head.next
         return
      prev = self.head
      for node in self:
         if node.data == data:
            prev.next = node.next
            return
         prev = node

      raise Exception( "Node with data '%s' not found" % data )


class CircularLinkedList:
   def __init__( self ):
      self.head = None

   def traverse( self, startingPoint = None ):
      if startingPoint is None:
         startingPoint = self.head

      node = startingPoint
      while node is not None and ( node.next != startingPoint ):
         yield node
         node = node.next
      yield node

   def print_list( self, startingPoint=None ):
      nodes = []
      for node in self.traverse( startingPoint ):
         nodes.append( str( node ) )
      print( '->'.join( nodes ) )

def main():
   llist = LinkedList( [ 'a', 'b', 'c', 'd', 'e' ] )
   print( llist )
   for node in llist:
      print( node )

   llist.add_first( Node( 'z' ) )
   llist.add_first( Node( 'y' ) )
   llist.add_last( Node( 'f' ) )
   llist.add_last( Node( 'g' ) )
   print( llist )

   llist.add_after( 'c', Node( 'cc' ) )
   print( llist )
   llist.add_after( 'b', Node( 'aa' ) )
   print( llist )

   for i in [ 'a', 'b', 'c', 'd', 'e', 'f', 'g' ]:
      llist.remove( i )
   print( llist )

   a = Node( 'a' )
   b = Node( 'b' )
   c = Node( 'c' )
   d = Node( 'd' )
   a.next = b
   b.next = c
   c.next = d
   d.next = a
   clist = CircularLinkedList()
   clist.head = a
   clist.print_list()
   clist.print_list( b )
   clist.print_list( d )

main()

