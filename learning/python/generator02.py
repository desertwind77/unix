#!/usr/bin/env python
#import mem_profile
import resource
import random
import time

names = [ 'John', 'Corey', 'Adam', 'Steve', 'Rick', 'Thomas' ]
majors = [ 'Math', 'Engineering', 'CompSci', 'Arts', 'Business' ]

def people_list( num_people ):
    result = []
    for i in range( num_people ):
        person = {
                    'id' : i,
                    'name' : random.choice( names ),
                    'major' : random.choice( majors )
                 }
        result.append( person )
    return result

def people_generator( num_people ):
    for i in xrange( num_people ):
        person = {
                    'id' : i,
                    'name' : random.choice( names ),
                    'major' : random.choice( majors )
                 }
        yield person

mem1 = resource.getrusage( resource.RUSAGE_SELF ).ru_maxrss
t1 = time.process_time()
people = people_list( 1000000 )
t2 = time.process_time()
mem2 = resource.getrusage( resource.RUSAGE_SELF ).ru_maxrss
print( 'List' )
print( 'Memory : {} Mb'.format( mem2 - mem1 ) )
print( 'Time   : {} Seconds'.format( round( t2 - t1, 2 ) ) )
print()

mem1 = resource.getrusage( resource.RUSAGE_SELF ).ru_maxrss
t1 = time.process_time()
people = people_generator( 1000000 )
t2 = time.process_time()
mem2 = resource.getrusage( resource.RUSAGE_SELF ).ru_maxrss
print( 'Generator' )
print( 'Memory : {} Mb'.format( mem2 - mem1 ) )
print( 'Time   : {} Seconds'.format( round( t2 - t1, 2 ) ) )
