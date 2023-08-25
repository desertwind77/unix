#!/usr/bin/env python3
# https://pymotw.com/3/textwrap/index.html

import textwrap

sample_text = '''
    The textwrap module can be used to format text for output in
    situations where pretty-printing is desired.  It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text editors.
    '''

# Print 50 chars per lines
print( textwrap.fill( sample_text, width=50 ) )

# Remove the common whitespace prefix from all of the lines
#
# Since “dedent” is the opposite of “indent,” the result is a block
# of text with the common initial whitespace from each line removed.
# If one line is already indented more than another, some of the whitespace will not be removed.
#
# Input like:
#␣Line one.
#␣␣␣Line two.
#␣Line three.
#
# becomes:
#Line one.
#␣␣Line two.
#Line three.
dedented_text = textwrap.dedent( sample_text ).strip()
print( dedented_text )

# Combining Dedent and Fill
for width in [45, 60]:
    print( '{} Columns:\n'.format( width ) )
    print( textwrap.fill( dedented_text, width=width ) )
    print()

# Indenting blocks
# Use the indent() function to add consistent prefix text to all of the lines in a string.
wrapped = textwrap.fill( dedented_text, width=50 )
wrapped += '\n\nSecond paragraph after a blank line.'
wrapped = textwrap.indent( wrapped, '> ' )
print('Quoted block:\n')
print( wrapped )

# To control which lines receive the new prefix,
# pass a callable as the predicate argument to indent().
def should_indent( line ):
    return len(line.strip()) % 2 == 0

wrapped = textwrap.fill( dedented_text, width=50 )
final = textwrap.indent( wrapped, 'EVEN ', predicate=should_indent )
print( '\nQuoted block:\n' )
print( final )
print()

# Hanging Indents: In the same way that it is possible to set the
# width of the output, the indent of the first line can be
# controlled independently of subsequent lines.
dedented_text = textwrap.dedent( sample_text ).strip()
print( textwrap.fill( dedented_text, initial_indent='',
                      subsequent_indent=' ' * 4, width=50,) )

# To truncate text to create a summary or preview, use shorten()
dedented_text = textwrap.dedent(sample_text)
original = textwrap.fill(dedented_text, width=50)

print('Original:\n')
print(original)

shortened = textwrap.shorten(original, 100)
shortened_wrapped = textwrap.fill(shortened, width=50)

print('\nShortened:\n')
print(shortened_wrapped)
