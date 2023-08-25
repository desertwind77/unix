#!/usr/bin/env python3
# https://pymotw.com/3/string/index.html
# - capwords
# - templates
# - advanced templates
# - formatter
# - constants
import string

'''
capwords : capitalize all of the words in a string.
'''
s = 'The quick brown fox jumped over the lazy dog.'
assert( string.capwords( s ) == 'The Quick Brown Fox Jumped Over The Lazy Dog.' )

'''
Template : an alternative to the built-in interpolation syntax in which variables
are identified by prefixing the name with $ e.g. $var or ${var}.

Unlike interpolation and formatting, template doesn't care about the type of
argument. The values are always converted to string. No way to format the output

The downside of the built-in interpolation is that we need to specify the type. For
example, if we forget 's' in '%(var)siable', python will crash.
e.g. no control over the nubmer of digits to represent a floating-point value.
'''
values = { 'var' : 'foo' }

t = string.Template("""
Variable        : $var
Escape          : $$
Variable in text: ${var}iable
""")
template_str = '''
Variable        : foo
Escape          : $
Variable in text: fooiable
'''
assert( t.substitute( values ) == template_str )

s = """
Variable        : %(var)s
Escape          : %%
Variable in text: %(var)siable
"""
interpolate_str = '''
Variable        : foo
Escape          : %
Variable in text: fooiable
'''
assert( s % values == interpolate_str )

s = """
Variable        : {var}
Escape          : {{}}
Variable in text: {var}iable
"""
format_str = '''
Variable        : foo
Escape          : {}
Variable in text: fooiable
'''
assert( s.format( **values ) == format_str )

'''
substitute() will raise exception if any values needed by the Template are missing.
But safe_substitue() will silently ignore it.
'''
values = { 'var': 'foo' }
t = string.Template( "$var is here but $missing is not provided" )
try:
   print('substitute()     :', t.substitute(values))
except KeyError as err:
   print('ERROR:', str(err))
assert( t.safe_substitute(values) == 'foo is here but $missing is not provided' )

'''
advanced Template : change the default syntax by adjusting the regular expression
patterns for finding the variable names in the Template body.
'''
class MyTemplate(string.Template):
   # Change the delimiter from $ to %
   delimiter = '%'
   # Require the variable name to have '_'
   idpattern = '[a-z]+_[a-z]+'


template_text = '''
Delimiter : %%
Replaced  : %with_underscore
Ignored   : %notunderscored
'''

replaced_text = '''
Delimiter : %
Replaced  : replaced
Ignored   : %notunderscored
'''

d = {
   'with_underscore' : 'replaced',
   'notunderscored' : 'not replaced',
}

t = MyTemplate(template_text)
assert( t.safe_substitute(d) == replaced_text )

'''
the built-in str.format() is more convenient than the Formatter class. But the
Formatter class may be useful for customizations by subclassing it.
'''

'''
Useful string constants esp when working with ASCII
ascii_letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_lowercase='abcdefghijklmnopqrstuvwxyz'
ascii_uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits='0123456789'
hexdigits='0123456789abcdefABCDEF'
octdigits='01234567'
printable='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
whitespace=' \t\n\r\x0b\x0c
'''
import inspect

def is_str(value):
   return isinstance(value, str)

for name, value in inspect.getmembers(string, is_str):
   if name.startswith('_'):
      continue
   print('%s=%r' % (name, value))
