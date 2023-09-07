# Python

## Miscellaneous
To run python script iteratively, `python -i script.py`

**Print function name**
```python
import inspect

def get_function_name():
    # get the frame object of the function
    frame = inspect.currentframe()
    return frame.f_code.co_name

print( "The name of function is : " + get_function_name() )
```

**all and any**
```python
myData = [ 2, 6, 4, 5, 8 ]
# isAllEven = False
isAllEven = all( i % 2 == 0 for i in myData )
# isEven = True
isEven = any( i % 2 == 0 for i in myData )

x, y, z = 0, 1, 0
passed = any( ( x, y, z ) )
```
**Combining two dictionaries**
```python
x = { 'a' : 1, 'b' : 2 }
y = { 'b' : 3, 'c' : 4 }
# Python 2.x
z = dict( x, **y )
# Python 3.5+
z = { **x, **y }
```
**Unpacking function arguments**
```python
def myfunc( x, y, z ):
    print( x, y, z )

tuple_vec = ( 1, 0, 1 )
dict_vec = { 'x': 1, 'y': 0, 'z': 1 }
myfunc( *tuple_vec )
myfunc( **dict_vec )
```
**Sorting a dictionary by value**
```python
x = { 'a' : 4, 'b' : 3, 'c' : 2, 'd' : 1 }
sorted( x.items(), key=lambda x: x[1] )

import operator
sorted( x.items(), key=operator.itemgetter( 1 ) )
```
**Converting binary to/from decimal**
```python
# Converting binary to decimal
binary = '1110'
decimal = int( binary, 2 )

# Converting decimal to binary
binary = '{0:b}'.format( decimal )      # without leading 0
binary = '{0:06b}'.format( decimal )    # with leading 0
    
def decToBin( number, fill=0 ):
    output = None
    if fill != 0:
        output = "{0:{filler}{fill}b}".format( 10, filler='0', fill=fill )
    else:
        output = "{0:b}".format( 10 )
    return output

print( decToBin( 10 ) )             # 1010
print( decToBin( 10, fill=8 ) )     # 00001010
```
**Print leading zero**
```python
def print_leading_zero():
    # Displaying numbers with leading zeros
    print( "{:06d}".format( 99 ) )      # 000099
    print( f"{67 :07d}" )               # 0000067
    str( 73 ).rjust( 7, '0' )           # 0000073
    '37'.zfill( 6 )                     # 000037
```
**enumerate**
```python
def enumerate_example():
    # https://realpython.com/python-enumerate/
    values = [ 'a', 'b', 'c', 'd', 'e' ]
    for count, value in enumerate( values ):
        print( count, value )
````
**deque**
Deque is preferred over list in the cases where we need quicker append and pop operations from both the ends of container, as deque provides an O(1) time complexity for append and pop operations as compared to list which provides O(n) timecomplexity.
```python
from collections import deque

print( deque() )                        # deque([])
print( deque( [ 'a', 'b', 'c' ] ) )     # deque(['a', 'b', 'c'])
print( deque( 'abc' ) )                 # deque(['a', 'b', 'c'])
print( deque( [ { 'data' : 'a' }, { 'data' : 'b' } ] ) )    
# deque([{'data': 'a'}, {'data': 'b'}])

llist = deque( 'abcde' )
print( llist )              # deque(['a', 'b', 'c', 'd', 'e'])
llist.append( 'f' )
print( llist )              # deque(['a', 'b', 'c', 'd', 'e', 'f'])
llist.pop()
print( llist )              # deque(['a', 'b', 'c', 'd', 'e'])
llist.appendleft( 'z' )
print( llist )              # deque(['z', 'a', 'b', 'c', 'd', 'e'])
llist.popleft()
print( llist )              # deque(['a', 'b', 'c', 'd', 'e'])

queue = deque()
queue.append( "Mary" )
queue.append( "John" )
queue.append( "Susan" )
print( queue )              # deque(['Mary', 'John', 'Susan'])
print( queue.popleft() )    # Mary
print( queue.popleft() )    # John
print( queue.popleft() )    # Susan
```
**namedtuple**
Like tuples, namedtuples are immutable
```python
from collections import namedtuple

Car = namedtuple( 'Car', 'color mileage' )
my_car = Car( 'red', 3812.4 )
print( my_car )
print( my_car.color )
print( my_car.mileage )
```
**heapq**
```python
import heapq

li = [ 5, 7, 9, 1, 3 ]
heapq.heapify( li )
print( "The created heap is : ", li )
heapq.heappush( li, 4 )
print( "The modified heap after push is : ", li )
print( "The smallest element is : ", heapq.heappop( li ) )

li1 = [5, 7, 9, 4, 3]
li2 = li1[:]
heapq.heapify( li1 )
heapq.heapify( li2 )
print()
print( "original      : ", li1 )
# push 2 and then pop the smallest
heapq.heappushpop( li1, 2 )
print( "heappushpop 2 : ", li1 )
# replace the smallest with 2
heapq.heapreplace( li2, 2 )
print( "heapreplace 2 : ", li2 )

li3 = [6, 7, 9, 4, 3, 5, 8, 10, 1]
heapq.heapify( li3 )
print()
print( "Original                   : ", li3 )
print( "The 3 largest numbers are  : ", heapq.nlargest( 3, li3 ) )
print( "The 3 smallest numbers are : ", heapq.nsmallest( 3, li3 ) )
```
Ouput:
```
The created heap is :  [1, 3, 9, 7, 5]
The modified heap after push is :  [1, 3, 4, 7, 5, 9]
The smallest element is :  1

original      :  [3, 4, 9, 5, 7]
heappushpop 2 :  [3, 4, 9, 5, 7]
heapreplace 2 :  [2, 4, 9, 5, 7]

Original                   :  [1, 3, 5, 4, 6, 9, 8, 10, 7]
The 3 largest numbers are  :  [10, 9, 8]
The 3 smallest numbers are :  [1, 3, 4]
```
**Measuring time**
```python
import timeit
time = timeit.timeit( '"-".join( str( n ) for n in range( 100 ) )', number=10000 )
print( time )
```
## Regular Expression

This is how to match a string with multiple lines.
```python
import re

texts = [
'''
06/07 06/07 743953650SRS94F2T
-           06/07
-           06/07
07/08/23
         1 BR T
         2 BR T
         3 XX X
         4 XX XEVA AIR     6952453854489 BANGKOK  TH
TH BAHT
       2300.00  X    0.02880869
EVAAIRPNAME
SAN FRANCISCO        TAIPEI
TAIPEI               BANGKOK
BANGKOK              UNKNOWN LOCATION
UNKNOWN LOCATION     UNKNOWN LOCATION66.26
'''
]

rx1 = re.compile( r'^(\d{2}\/\d{2}) \d{2}\/\d{2} \w{17}.*\n.*\n.*\n.*\n.*\n.*\n.*\n.{15}(.*)\n.*\n.*\n.*\n.*\n.*\n.*\n.{37}([0-9.,]+)$',
                  re.MULTILINE )

for txt in texts:
    for match in rx1.finditer( txt ):
        print( match.group( 1 ), match.group( 2 ), match.group( 3 ) )
```
Output is as follows.
```
06/07 EVA AIR     6952453854489 BANGKOK  TH 66.26
```

## Generate a document using Sphinx
Install sphinx and a theme. More themes are available at https://www.writethedocs.org/guide/tools/sphinx-themes/
```
pip install sphinx sphinx_rtd_theme
```
Assuming that the root folder contains the source folder called `scripts`. We will create a document folder called `docs`.
```
$ mkdir docs
$ ls -l
drwxr-xr-x     - athichart  2 Sep 23:36 docs
lrwxr-xr-x    20 athichart 21 Oct  2022 scripts
```
Run the `sphinx-quickstart` script and answer the questions. For the question `Separate the source and build directories`, select Yes for the better organization.
```
sphinx-quickstart docs
```
Edit `docs/source/conf.py`
```python
import os
import sys
sys.path.insert(0, os.path.abspath('../../scripts'))
...
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'       # To recognize Google and NumPy Docstrings
]
...
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
...
html_theme = 'sphinx_rtd_theme'
```
Add the source code using `sphinx-apidoc`.
```
sphinx-apidoc -o docs/source/ scripts/
```
Include the generated `modules.rst` file in `docs/source/index.rst`.
```
.. My S documentation master file, created by
   sphinx-quickstart on Sat Sep  2 23:36:35 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to My S's documentation!
================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```
Fire the build.
```
cd docs
make html
```
To update the generated html after the source code is modified.
```
make clean html
make html
```
To see popular docstring formats [[1](https://betterprogramming.pub/3-different-docstring-formats-for-python-d27be81e0d68)]

## dataclass
dataclass module is introduced in Python 3.7 as a utility tool to make structured classes specially for storing data. These classes hold certain properties and functions to deal specifically with the data and its representation

For exmaple, use the Comment class instead of implementing all method in the ManualCommont class.
```python
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
```
## Logging
```python
import logging

# Customize the log message using basicConfig().
# This function can only be called once. The default filemode is append.
msg_format = '%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig( level=logging.DEBUG, filename='app.log',
                     datefmt='%d-%b-%y %H:%M:%S',
                     filemode='w', format=msg_format )

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

try:
    c = 5 / 0
except Exception as e:
    # exc_info = True is to log the exception information
    # logging.error( "Exception occurred", exc_info=True )
    logging.exception( "Exception occurred" )
```
The output:
```
02-Sep-23 00:28:09 - 61363 - root - DEBUG - This is a debug message
02-Sep-23 00:28:09 - 61363 - root - INFO - This is an info message
02-Sep-23 00:28:09 - 61363 - root - WARNING - This is a warning message
02-Sep-23 00:28:09 - 61363 - root - ERROR - This is an error message
02-Sep-23 00:28:09 - 61363 - root - CRITICAL - This is a critical message
02-Sep-23 00:28:09 - 61363 - root - ERROR - Exception occurred
Traceback (most recent call last):
  File "/Users/athichart/Workspace/github/unix/learning/python/./logging01.py", line 18, in <module>
    c = 5 / 0
        ~~^~~
ZeroDivisionError: division by zero
```
Using the customer logger and handler
```python
#!/usr/bin/env python3

import logging

# Logger: This is the class whose objects will be used in the application code
# directly to call the functions.
#
# LogRecord: Loggers automatically create LogRecord objects that have all the
# information related to the event being logged, like the name of the logger,
# the function, the line number, the message, and more.
#
# Haqdler: Handlers send the LogRecord to the required output destination, like
# the console or a file. Handler is a base for subclasses like StreamHandler,
# FileHandler, SMTPHandler, HTTPHandler, and more. These subclasses send the
# logging outputs to corresponding destinations, like sys.stdout or a disk
# file.
#
# Formatter: This is where you specify the format of the output by specifying a
# string format that lists out the attributes that the output should contain.

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.warning('This is a warning')
logger.error('This is an error')
```
Output to the console
```
__main__ - WARNING - This is a warning
__main__ - ERROR - This is an error
```
Output to the file
```
2023-09-02 00:23:39,758 - __main__ - ERROR - This is an error
2023-09-02 00:29:22,081 - __main__ - ERROR - This is an error
```
The configuration can be stored in a file and loaded by the Python script.
```python
#!/usr/bin/env python3
import logging
import logging.config

logging.config.fileConfig(fname='file.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

logger.debug('This is a debug message')
```
The config file
```
[loggers]
keys=root,sampleLogger

[handlers]
keys=consoleHandler

[formatters]
keys=sampleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_sampleLogger]
level=DEBUG
handlers=consoleHandler
qualname=sampleLogger
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=sampleFormatter
args=(sys.stdout,)

[formatter_sampleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```
The output
```
2023-09-02 00:32:22,830 - __main__ - DEBUG - This is a debug message
```
Load the config stored in the YAML format.
```python
import logging
import logging.config
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

logger.debug('This is a debug message')
```
The same config in the YAML format
```
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
loggers:
  sampleLogger:
    level: DEBUG
    handlers: [console]
    propagate: no
root:
  level: DEBUG
  handlers: [console]
```

## dateutil module
```python
from datetime import date, datetime
from dateutil.relativedelta import *
import calendar
def dateutil_example():
    # dateutil package
    #   https://dev.to/ejbarba/python-dateutil-module-4m03
    #   install: pip3 install python-dateutil
    #
    #   use cases
    #   - Computing of relative deltas (next Monday, next week, last week of
    #     the previous month, next five years, etc).
    #   - Computing of relative deltas between two given dates and/or datetime
    #     objects.
    now = datetime.now()
    today = date.today()
    last_week = today + relativedelta( weeks=-1 )
    next_week = today + relativedelta( weeks=+1 )
    last_month = today + relativedelta( months=-1 )
    next_month = today + relativedelta( months=+1 )
    next_month_plus_one_week = today + relativedelta( months=+1, weeks=+1 )
    added_time = today + relativedelta( months=+1, weeks=+1, hour=13 )
    one_month_before_one_year = today + relativedelta( years=+1, months=-1 )

    # Adding one month will never cross the month boundary:
    print(date(2020, 1, 27) + relativedelta(months=+1))
    # 2020-02-27
    print(date(2020, 1, 31) + relativedelta(months=+1))
    # 2020-02-29 (2020 is a leap year!)
    print(date(2020, 1, 31) + relativedelta(months=+2))
    # 2020-03-31
    # This logic also applies for years, even on leap years
    print(date(2020, 2, 28) + relativedelta(years=+1))
    # 2021-02-28
    print(date(2020, 2, 29) + relativedelta(years=+1))
    # 2021-02-28
    # Subtracting 1 year from Feb 29 2020 will print Feb 28 2019
    print(date(2020, 2, 29) + relativedelta(years=-1))
    # 2019-02-28

    # Assumming today is a Monday
    coming_friday = today + relativedelta( weekday=FR )
    next_tueday = today + relativedelta( weeks=+1, weekday=TU )
    # Making use of the calendar import
    next_tueday_calendar = today + relativedelta( weeks=+1, weekday=calendar.TUESDAY )

    # Get the 237th day of 2020
    print( date( 2020, 1, 1 ) + relativedelta( yearday=237 ) )
    # 2020-08-24

    # Getting the difference of two dates
    nasa_birthday = datetime( 1958, 7, 29, 0, 0 )
    age_of_nasa = relativedelta( today, nasa_birthday )
    print( age_of_nasa )
    print( 'It has been {} years, {} months and {} days since the birth of NASA.'
```
## Arguments to a function
`*args` means optional arguments and `**kwargs` means keyword arguments

```python
def foo( required, *args, **kwargs ):
    print( required )
    if args:
        print( args )
    if kwargs:
        print( kwargs )

def foo2( x, *args, **kwargs ):
    kwargs[ 'name' ] = 'Alice'
    # args is a tuple which is immutable
    new_args = args + ( 'extra', )
    foo( x, *new_args, **kwargs )

foo( 'hello' )
foo( 'hello', 1, 2, 3 )
foo( 'hello', 1, 2, 3, key1="value", key2=999 )
foo2( 'world', 4, 5, 6, key1='value1', key2='value2' )
```
The output of the last print is as follows
```
world
(4, 5, 6, 'extra')
{'key1': 'value1', 'key2': 'value2', 'name': 'Alice'}
```
Using it in the object-oriented programming.
```python
class Car:
    def __init__( self, color, mileage ):
        self.color = color
        self.mileage = mileage

class AlwaysBlueCar( Car ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.color = 'blue'
```

## Command line argument parsing
sys.argv can achieve simple tasks. It can be accessed like a normal Python list.

```python
import sys

for i in range(len(sys.argv)):
    print(f"sys.argv[ { i } ] = { sys.argv[ i ] }")
```
Here is the output.

```
sys.argv[ 0 ] = /Users/athichart/Workspace/tmp/parsing.py
sys.argv[ 1 ] = arg1
sys.argv[ 2 ] = arg2
```

For more complicated tasks, argparse is the best. (optparse is deprecated and getopt is too basic.) It has a built-in help.

```python
import argparse

parser = argparse.ArgumentParser(description="Demo")

# 1) Optional arguments
# argparse determines the number of arguments based on the action specified.
# By default, argparse will look for a single argument. The store_true action 
# takes no argument.

# Specify a default value and the variable type. The default variable type is string.
parser.add_argument("-l", "--limit", default=5, type=int)
# This flag is required.
parser.add_argument("-r", "--required", required=True)
# The default action is to assign the variable specified. But there are a couple
# of other actions that can be specified e.g. store_true, store_false, count, append
parser.add_argument("-v", "--verbose", action="store_true", help="verbose flag")
parser.add_argument("-d", "--debug", action="count", help="Set debug level")
parser.add_argument("-L", "--list", action="append")

# 2) Positional arguments
parser.add_argument("action", choices=["print", "count"])
# built-in filetypes for the ease of openning# files
parser.add_argument("filename", type=argparse.FileType("r"))
# Number of parameters
#   nargs='2'   needs 2 arguments
#   nargs='*'   needs any number of arguments
#   nargs='+'   needs one or more arguments
#   nargs='?'   may or may not have arguments
parser.add_argument("numbers", nargs="*")
# optional arguments require 0 or nargs arguments
parser.add_argument("--latitude", nargs=2)
parser.add_argument("--longtitude", nargs=2)

args = parser.parse_args()

if args.verbose:
    print(f"Limit       : {args.limit}")
    print(f"Debug level : {args.debug}")
    print(f"List        : {args.list}")
    print(f"Latitude    : {args.latitude}")
    print(f"Longtitude  : {args.longtitude}")
    print(f"Action      : {args.action}")
    print(f"Filename    : {args.filename.name}")
    print(f"Numbers     : {args.numbers}")

if args.action == "print":
    count = 0
    for line in args.filename:
        print(line.strip())

        count += 1
        if count == args.limit:
            break
elif args.action == "count":
    count = 0
    for line in args.filename:
        count += 1
    print(f"Line count  : {count}")
```

Here is the output.
```
./parsing.py -v -r 3 -d -d -d -L opt1 -L opt2 --latitude 2 3 count ./parsing.py 1 2                                                                                       
Limit       : 5
Debug level : 3
List        : ['opt1', 'opt2']
Latitude    : ['2', '3']
Longtitude  : None
Action      : count
Filename    : ./parsing.py
Numbers     : ['1', '2']
Line count  : 62
```
The argparse module assumes that flags like `-f` and `--bar` indicate optional arguments, which can always be omitted at the command line. A far more elegant solution would be to create another group for “required named arguments”.
```python
parser = argparse.ArgumentParser( description='Foo' )
parser.add_argument( '-o', '--output', default='stdout',
                     help='Output file name' )
requiredNamed = parser.add_argument_group( 'required named arguments' )
requiredNamed.add_argument( '-i', '--input', required=True,
                            help='Input file name' )
parser.parse_args( ['-h'] )
```
Here is the output.
```
usage: [-h] [-o OUTPUT] -i INPUT

Foo

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name

required named arguments:
  -i INPUT, --input INPUT
                        Input file name
```
Here is how to use `const`, `default` and `nargs`.
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument( '--head', dest='size', type=int,
                     const=80, default=10, nargs='?',
                     action="store",
                     help='Only print the head of the output')
# No --head argument is supplied. size should be the const value (80).
args = parser.parse_args( ''.split() )
print( args )
# --head is supplied without any value. size should be the default value (10).
args = parser.parse_args('--head'.split())
print( args )
# --head is supplied along with a value 15. size should be 15.
args = parser.parse_args('--head 15'.split())
print( args )
```
Here is the output.
```
Namespace(size=10)
Namespace(size=80)
Namespace(size=15)
```
Required argument 'y' if 'x' is present
```python
non_int.add_argument('--prox', action='store_true', help='Flag to turn on proxy')
non_int.add_argument('--lport', type=int, help='Listen Port.')
non_int.add_argument('--rport', type=int, help='Proxy port.')
if args.prox and (args.lport is None or args.rport is None):
    parser.error("--prox requires --lport and --rport.")
```

## Executing an external command

subprocess is simple and powerful. `check=True` tells subprocess to raise an exception on the face of execution failure. This is better than manually checks the returncode.

```python
import subprocess

cmd = [ 'ls', '-l' ]
subprocess.run( cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL )
```

If we want to redirect the input from our python script to the external command, we can use the `input` parameter.

```python
import subprocess

result = subprocess.run(
    ["wc"], stdout=subprocess.PIPE, text=True, input="Hello from the other side"
)
print(result.stdout)
```

* `stdout=subprocess.PIPE` tells Python to redirect the output of the command to an object so it can be manually read later.
* `text=True` returns stdout and stderr as strings. The default return type is bytes.
* `input="Hello from the other side"` tells Python to redirect the string as input to the cat command.

**Basic example of using pipe. May need to revisit this.**

```python
import subprocess

result = subprocess.Popen(
    ["cat"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)
# sending input to the external program
output, errors = result.communicate(input="Hello from the other side!")
# wait for the external program to finish
result.wait()
print(output)
print(errors)
```

||os.system|subprocess.run|subprocess.Popen|
|-|---------|--------------|----------------|
|Requires parsed arguments|no|yes|yes|
|Waits for the command|yes	|yes|no|
|Communicates with stdin and stdout|no|yes|yes|
|Returns|return value|object|object|

## Print a table
* Formatted
```python
d = {
    1: ["Python", 33.2, 'UP'],
    2: ["Java", 23.54, 'DOWN'],
    3: ["Ruby", 17.22, 'UP'],
    10: ["Lua", 10.55, 'DOWN'],
    5: ["Groovy", 9.22, 'DOWN'],
    6: ["C", 1.55, 'UP']
} 

print("{:<8} {:<15} {:<10} {:<10}".format("Pos", "Lang", "Percent", "Change"))
for k, v in d.items():
    lang, perc, change = v
    print("{:<8} {:<15} {:<10} {:<10}".format(k, lang, perc, change))
```
```
Pos      Lang            Percent    Change    
1        Python          33.2       UP        
2        Java            23.54      DOWN      
3        Ruby            17.22      UP        
10       Lua             10.55      DOWN      
5        Groovy          9.22       DOWN      
6        C               1.55       UP
```
* Using format() function to print dict and lists
```python
dota_teams = ["Liquid", "Virtus.pro", "PSG.LGD", "Team Secret"]
data = [[1, 2, 1, "x"], ["x", 1, 1, "x"], [1, "x", 0, 1], [2, 0, 2, 1]]
format_row = "{:>12}" * (len(dota_teams) + 1)
print(format_row.format("", *dota_teams))
for team, row in zip(dota_teams, data):
    print(format_row.format(team, *row))
```
```
                  Liquid  Virtus.pro     PSG.LGD Team Secret
      Liquid           1           2           1           x
  Virtus.pro           x           1           1           x
     PSG.LGD           1           x           0           1
 Team Secret           2           0           2           1
```
* Using tabulate() function to print dict and lists
```python
from tabulate import tabulate

data = [
    [1, "Liquid", 24, 12],
    [2, "Virtus.pro", 19, 14],
    [3, "PSG.LGD", 15, 19],
    [4, "Team Secret", 10, 20],
]
print(tabulate(data, headers=["Pos", "Team", "Win", "Lose"]))
```
```
  Pos  Team           Win    Lose
-----  -----------  -----  ------
    1  Liquid          24      12
    2  Virtus.pro      19      14
    3  PSG.LGD         15      19
    4  Team Secret     10      20
```
* Using pandas
```python
import pandas

data = [
    [1, "Liquid", 24, 12],
    [2, "Virtus.pro", 19, 14],
    [3, "PSG.LGD", 15, 19],
    [4, "Team Secret", 10, 20],
]
headers = ["Pos", "Team", "Win", "Lose"]
print(pandas.DataFrame(data, headers, headers))
```
```
      Pos         Team  Win  Lose
Pos     1       Liquid   24    12
Team    2   Virtus.pro   19    14
Win     3      PSG.LGD   15    19
Lose    4  Team Secret   10    20
```
* Others options: texttable, beautifultable, PrettyTable

## Returning multiple values from a function
1. Using a list (not good)
2. Using a tuple
3. Using a dictionary
4. Using a class
5. Using a dataclass (3.7+)
```
@dataclass
class Returnvalue:
    y0: int
    y1: float
    y3: int

def total_cost(x):
    y0 = x + 1
    y1 = x * 3
    y2 = y0 ** y3
    return ReturnValue(y0, y1, y2)
```

## Python GUI with tkinter
tkinter is a wrapper for Tck/Tk. It is used to develop cross-platform GUI applications in Python. Although its widgets are more basic than those of wxPython, it is a part of the Python standard library. So it is more portable.

### Even Types
|Event|Modifier|Type|Qualifier|Action|
|-----|--------|----|---------|------|
|\<Button-1\>||Button|1|Left mouse button click.|
|\<Button-2\>||Button|2|Middle mouse button click.|
|\<Destroy\>||Destroy||Window is being destroyed.|
|\<Double-Button-1\>|Double|Button|1|Double-click first mouse button 1.|
|\<Enter\>|Enter|||Cursor enters window.|
|\<Expose\>||Expose||Window fully or partially exposed.|
|\<KeyPress-a\>||KeyPress|a|Any key has been pressed.|
|\<KeyRelease\>||KeyRelease||Any key has been released.|
|\<Leave\>||Leave||Cursor leaves window.|
|\<Print\>|||Print|PRINT key has been pressed.|
|\<FocusIn\>||FocusIn||Widget gains focus.|
|\<FocusOut\>||FocusOut||widget loses focus.|

### Basic Examples
```python
from tkinter import *
import threading

class SimpleAppTk:
    def __init__(self):
        # Create a top-level window
        self.window = Tk()
        self.initialize()

    def initialize(self):
        """
        Create all the GUI elements e.g. button, text fields, etc
        """
        # Create three Label widgets
        self.label1 = Label(self.window, text="First number: ", font=("Helvetica", 14))
        self.label2 = Label(self.window, text="Second number: ", font=("Helvetica", 14))
        self.label3 = Label(
            self.window, text="Result: ", fg="red", font=("Helvetica", 14)
        )

        # Create three Textfield widgets
        # bd = border size
        self.text1 = Entry(self.window)
        self.text2 = Entry(self.window)
        self.text3 = Entry(self.window, bd=3)

        # Create a Button widget
        # Properties are text, bg, fg, font, image, command, etc.
        # For button1, we use the command parameter to bind the event handler
        # to the default event of the widget. Note that each widget has its
        # own default event. Left click is the default event of the button
        # widget.
        # For button2, we use the bind method to bind the event handler. In
        # this approach, we need to supply the event type.
        self.button1 = Button(self.window, text="Add", command=self.thread_add)
        self.button2 = Button(self.window, text="Subtrack")
        self.button2.bind("<Button-1>", self.thread_subtract)

        # Place all the widgets on the parent window
        self.label1.place(x=20, y=50)
        self.text1.place(x=150, y=50)
        self.label2.place(x=20, y=100)
        self.text2.place(x=150, y=100)
        self.button1.place(x=20, y=150)
        self.button2.place(x=150, y=150)
        self.label3.place(x=20, y=200)
        self.text3.place(x=150, y=200)

        self.window.title("My Demo Tkinter Application")
        # Define "widthxheight+XPOS+YPOS"
        self.window.geometry("400x300+10+10")

    def thread_add(self):
        # Threading should be used in long-running event handlers because
        # the GUI will be irresponsive while the event handler is being
        # executed. Thread synchronization should be used, as well.
        th = threading.Thread(target=self.add)
        th.start()

    def thread_subtract(self):
        th = threading.Thread(target=self.subtract)
        th.start()

    def add(self):
        # delete takes two parameters: firstIndex and lastIndex
        # It will delete the string from the firstIndex until the lastIndex
        self.text3.delete(0, "end")
        num1 = int(self.text1.get())
        num2 = int(self.text2.get())
        result = num1 + num2
        # insert requires the position the string to insert
        self.text3.insert(END, str(result))

    def subtract(self, event):
        self.text3.delete(0, "end")
        num1 = int(self.text1.get())
        num2 = int(self.text2.get())
        result = num1 - num2
        self.text3.insert(END, str(result))

    def run(self):
        # Waiting for events
        self.window.mainloop()

if __name__ == "__main__":
    app = SimpleAppTk()
    app.run()
```
Reference : [1](https://realpython.com/python-gui-tkinter/)

## Data Model
\_\_method\_\_ is called data model method in Python. A top-level function or syntax has a corresponding data model method. For example:
* `x + y` is corresponding to `__add__`
* class initialization is corresponding to `__init__`
* `repr(x)` is corresponding to `__repr__`
* `x()` is corresponding to `__call__`

[reference](https://www.youtube.com/watch?v=cKPlPJyQrt4&t=2s)

```python
class Polynomial:
    def __init__(self, *coeffs):
        self.coeffs = coeffs

    def __repr__(self):
        return f"Polynomail(*{self.coeffs})"

    def __add__(self, other):
        return Polynomial(*(x + y for x, y in zip(self.coeffs, other.coeffs)))

    def __len__(self):
        # The size of a polynomial is its degree.
        return len(self.coeffs)


p1 = Polynomial(1, 2, 3)
p2 = Polynomial(3, 4, 3)
print(p1 + p2)
```

## Decorator
Decorator is an easy way to modify the behavior of Python functions without rewriting the whole functions. Both `timer()` and `ntimes()` are decorators. `ntimes()` is called high-order decorator because it has more than one level.

```python
from time import time

def timer(func):
    def f(*args, **kwargs):
        before = time()
        rv = func(*args, **kwargs)
        after = time()
        print("elapsed", after - before)
        return rv
    return f

def ntimes(n):
    def inner(f):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                print(f"runing {f.__name__}")
                rv = f(*args, **kwargs)
            return rv
        return wrapper

@timer
@ntimes(3)
def add(x, y=10):
    return x + y

@timer
@ntimes(2)
def sub(x, y=10):
    return x - y

add(3)
sub(20)
```
Result
```
uning add
runing add
runing add
elapsed 2.5033950805664062e-05
runing sub
runing sub
elapsed 4.76837158203125e-06
```

## Generator
Instead of eagerly computing and returning all the results, just compute the value one at a time when it is asked for. Generator consumes less memory and less CPU cycles than eagerly computing all the results and returning a list of results. The following code does the work but the syntax is hard to remember.

```python
import time

class Compute:
    def __iter__(self):
        self.last = 0
        return self

    def __next__(self):
        rv = self.last
        self.last += 1
        if self.last > 10:
            raise StopIteration
        time.sleep(0.5)
        return rv

for i in Compute():
    print(i)
```

Instead, use the following syntax.

```python
import time
def compute():
    for i in range(10):
        time.sleep(0.5)
        yield (i)

for i in compute():
    print(i)
```

Another core concept of generator is coroutine nad interleaving. The library code and the user code are interleaving. Namely, running the library code, which is the generater, return to the user code so it can consume the value yielded by the generator, and so on. One application of this is to enforce sequencing. Here we want to implement an API where `first()`, `second()` and `last()` have to be called in this order. The following code has no way to enforce this ordering.

```python
class Api:
    def run_this_first(self):
        first()
    def run_this_second(self):
        second()
    def run_this_last(self):
        last()
```

The API implemented as follows does enforce the ordering.

```python
def api():
    first()
    yield
    second()
    yield
    last()
```

## Context Manager
The concept of context manager is to set up and tear down the resources. For example, the following code needs to create the table at the beginning and drop it at the end of the execution. But this is not fail-safe. If any exception occurs, the table will not be dropped. As a result, the next execution of the script will fail due to the existence of `test.db`.

```python
from sqlite3 import connect

with connect("test.db") as conn:
    cur = conn.cursor()
    cur.execute("create table points(x int, y int)")
    cur.execute("insert into points (x, y) values(1, 1)")
    cur.execute("insert into points (x, y) values(1, 2)")
    cur.execute("insert into points (x, y) values(2, 1)")
    for row in cur.execute("select x, y from points"):
        print(row)
    for row in cur.execute("select sum(x * y ) from points"):
        print(row)
    cur.execute("drop table points")
```

Following is a better version. The builtin method `__enter__` and `__exit__` are used to force the order. However, this code is still not fail safe as the previous one.

```python
from sqlite3 import connect

class TempTable:
    def __init__(self, cur):
        self.cur = cur

    def __enter__(self):
        self.cur.execute("create table points(x int, y int)")

    def __exit__(self, *args):
        self.cur.execute("drop table points")

with connect("test.db") as conn:
    cur = conn.cursor()
    with TempTable(cur):
        cur.execute("insert into points (x, y) values(1, 1)")
        cur.execute("insert into points (x, y) values(1, 2)")
        cur.execute("insert into points (x, y) values(2, 1)")
        for row in cur.execute("select x, y from points"):
            print(row)
        for row in cur.execute("select sum(x * y ) from points"):
            print(row)
```

The following code is little better version because it enforces the sequece of creating and deleting the table by using the generator.

```python
def temptable(cur):
    cur.execute("create table points(x int, y int)")
    yield
    cur.execute("drop table points")

class TempTable:
    def __init__(self, cur):
        self.cur = cur

    def __enter__(self):
        self.gen = temptable(self.cur)
        next(self.gen)

    def __exit__(self, *args):
        next(self.gen, None)
```

However the code above is not generic enough and cannot be reused anywhere else because the generator `temptable` is hard-coded inside `TempTable`. The following code passes `temptable` as a parameter to the class `ContextManager`.

```python
class ContextManager:
    def __init__(self, gen):
        self.gen = gen

    def __call__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        return self

    def __enter__(self):
        self.gen_inst = self.gen(*self.args, **self.kwargs)
        next(self.gen_inst)

    def __exit__(self, *args):
        next(self.gen_inst, None)
        
def temptable(cur):
    cur.execute("create table points(x int, y int)")
    yield
    cur.execute("drop table points")

with connect("test.db") as conn:
    cur = conn.cursor()
    with ContextManager(temptable)(cur):
        cur.execute("insert into points (x, y) values(1, 1)")
        cur.execute("insert into points (x, y) values(1, 2)")
        cur.execute("insert into points (x, y) values(2, 1)")
        for row in cur.execute("select x, y from points"):
            print(row)
        for row in cur.execute("select sum(x * y ) from points"):
            print(row)
```

The cumbersome syntax `with ContextManager(temptable)(cur):` in line 23 can be replaced by the more fashionable code.

```python
def temptable(cur):
    cur.execute("create table points(x int, y int)")
    yield
    cur.execute("drop table points")
temptable = ContextManager(temptable)

with connect("test.db") as conn:
    cur = conn.cursor()
    with temptable(cur):
        ...
```

Howver, line 18-22 above can be replaced by the decorator syntax.

```python
@ContextManager
def temptable(cur):
    cur.execute("create table points(x int, y int)")
    yield
    cur.execute("drop table points")
```

Fortunately, we don't have to re-implement the class `ContextManager`. Python already provides this functionality via `contextlib.contextmanager`. Following is the final version of the code which is also fail-safe.

```python
from sqlite3 import connect
from contextlib import contextmanager

@contextmanager
def temptable(cur):
    cur.execute("create table points(x int, y int)")
    try:
        yield
    finally:
        cur.execute("drop table points")

with connect("test.db") as conn:
    cur = conn.cursor()
    with temptable(cur):
        cur.execute("insert into points (x, y) values(1, 1)")
        cur.execute("insert into points (x, y) values(1, 2)")
        cur.execute("insert into points (x, y) values(2, 1)")
        for row in cur.execute("select x, y from points"):
            print(row)
        for row in cur.execute("select sum(x * y ) from points"):
            print(row)
```

## Metaclasses
Metaclasses is a way to hook into the class creation at run time. Assuming `library.py` and `user.py` have two different ownerships. The owner of one file can neither access nor modify the other. Usually, `user.py` imports `library.py`.

```python
# library.py
class Base(type):
    def foo_parent(self):
        return "foo_parent"

    def bar_parent(self):
        return self.bar_child()

# user.py
# Check if foo_parent exists in the parent class or not. If not, fail early.
assert hasattr(Base, "foo_parent"), "You broke it, you fool!"

class Derived(Base):
    def foo_child(self):
        return self.foo_parent()

    def bar_child(self):
        return "bar"

child = Derived()
```

The code above has two problems
- `foo_child()` may fail if foo_parent() has been renamed or removed from Base, for example, when the library is updated. So in the context of Derived, we want to check the required behavior of the parent class and fail early if something is missing. This can be done by adding the assert code at line 11.
- bar_parent() may fail if its derived classes don't implement bar_child(). The solution above is not possible because the base class doesn't know the name of its child classes. A solution is to use Metaclasses.
    - Overriding the builtin function `__build_class__` doesn't work ing Python3.
    - I cannot get `__init_subclass__` to work.

```python
# library.py
class BaseMeta(type):
    def __new__(cls, name, bases, body):
        if not "bar_child" in body:
            raise TypeError("bad derived class")
        return super().__new__(cls, name, bases, body)

    def foo_parent(self):
        return "foo_parent"

    def bar_parent(self):
        return self.bar_child()

# user.py
class Derived(metaclass=BaseMeta):
    def foo_child(self):
        return self.foo_parent()

    def bar_child(self):
        return "bar"

child = Derived()
```

## asyncio

## FastAPI

Adding a background task to a FastAPI server
```python
import asyncio

from fastapi import FastAPI

app = FastAPI()
x = [ 1 ]           # a global variable x

@app.get( "/" )
async def root():
    '''URL handler for /'''
    return {"message": "Hello World"}

async def periodic():
    '''This function will be called every 3 second'''
    while True:
        x[ 0 ] += 1
        print( f'x is now {x}' )
        # sleep for 3 seconds after running above code
        await asyncio.sleep( 3 )

@app.on_event( "startup" )
async def schedule_periodic():
    '''This function will be called on the startup'''
    loop = asyncio.get_event_loop()
    loop.create_task( periodic() )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run( app )
```

## sqlite3

```sql
create table project (
    name        text primary key,
    description text,
    deadline    date
);

-- Tasks are steps that can be taken to complete a project
create table task (
    id           integer primary key autoincrement not null,
    priority     integer default 1,
    details      text,
    status       text,
    deadline     date,
    completed_on date,
    project      text not null references project(name)
);
```

## Disassembler
This is how to use disassemler.
```python
def _():
    class Base2:
        pass


from dis import dis

dis(_)
```
Result

```python
./python3 disassembler.py                                                                                                                                                    
  3           0 LOAD_BUILD_CLASS
              2 LOAD_CONST               1 (<code object Base2 at 0x10497da50, file "/Users/athichart/Workspace/tmp/disassembler.py", line 3>)
              4 LOAD_CONST               2 ('Base2')
              6 MAKE_FUNCTION            0
              8 LOAD_CONST               2 ('Base2')
             10 CALL_FUNCTION            2
             12 STORE_FAST               0 (Base2)
             14 LOAD_CONST               0 (None)
             16 RETURN_VALUE

Disassembly of <code object Base2 at 0x10497da50, file "/Users/athichart/Workspace/tmp/disassembler.py", line 3>:
  3           0 LOAD_NAME                0 (__name__)
              2 STORE_NAME               1 (__module__)
              4 LOAD_CONST               0 ('_.<locals>.Base2')
              6 STORE_NAME               2 (__qualname__)

  4           8 LOAD_CONST               1 (None)
             10 RETURN_VALUE
```

## Python modules for Visual Studio Code
|Modules|Function|
|-------|--------|
|black|Python code formatting|
|mypy|Type hinting|

